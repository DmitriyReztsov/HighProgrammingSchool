# 1. Метод, который отрисовывает и заполняет нижний колонтитул в ПДФ-документе
def _set_page_footer(
    self,
    canvas: Canvas,
    footer_text_lines: dict[int, str],
    page_num: int,
    total_pages: int,
    page: dict[Any, Any],
):
    # Add page
    canvas.setPageSize((page.BBox[2], page.BBox[3]))
    canvas.doForm(makerl(canvas, page))

    # Draw footer
    canvas.saveState()
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setLineWidth(0.5)
    start_position_horiz = self.left_margin
    end_position_horiz = page.BBox[2] - self.right_margin
    start_position_vert = self.bottom_margin
    end_position_vert = self.bottom_margin
    canvas.line(start_position_horiz, start_position_vert, end_position_horiz, end_position_vert)
    canvas.setFont(self.font, self.font_size)

    # Fill footer
    for line_num, line_text in footer_text_lines.items():
        if line_num == 0:
            line_text = line_text.format(page_num, total_pages)
        start_position_horiz = self.left_margin
        start_position_vert = self.bottom_margin - 0.25 * inch - line_num * self.font_size
        canvas.drawString(
            start_position_horiz,
            start_position_vert,
            line_text,
        )

    # Save document
    canvas.restoreState()
    canvas.showPage()

# 2. Метод, берущий контент шаблона и создающий из него пдф-документ с добавлением необходимых колонтитулов
def create_pdf_file_from_template(self, appendix_contract: AppendixContractBase) -> None:
    # create document from template
    template_doc_content = self._get_doc_content(self.template.uuid)
    self.document = Document(template_doc_content)

    self._render_document()
    buffer = BytesIO()
    self.document.save(buffer)
    buffer.seek(0)

    document_storage_interface.create_document_storage_entry_from_bytes(
        str(appendix_contract.uuid), "docx", buffer, appendix_contract.created_by_id
    )

    latest_file_info = get_latest_file_url(appendix_contract.uuid)
    if latest_file_info.get("error"):
        logger.error(
            "Error occurred during getting latest file info",
            prefix="[AppendixService.create_pdf_file_from_template]",
            noa_contract=appendix_contract,
        )
        return

    # make pdf from the document
    noa_contract_name = f"NOA for {appendix_contract.epp_contract.name}"
    pdf_url = convert_document(
        noa_contract_name,
        latest_file_info.get("file_key"),
        latest_file_info.get("file_url"),
        "pdf",
        latest_file_info.get("file_type"),
    )

    pdf_content: bytes = document_storage_interface.get_bytes_content(pdf_url)
    bytes_to_pdf_obj = BytesToPdf(pdf_content)
    to_pdf_service = ToPDFService(
        bytes_to_pdf_obj,
        f"Notice of Assignment from {appendix_contract.created_at.strftime('%y-%m-%d at %H:%M:%S')}",
        appendix_contract.created_by,
    )
    pdf_file = to_pdf_service.get_pdf_file_with_footer(to_set_page_number=True)
    appendix_contract.pdf_file = to_pdf_service.create_file_instance(pdf_file)
    appendix_contract.save()

# 3. Функция отправки уведомлений. Собрает информацию по событию, добавляет технические детали для определения
# ыремени отправки и запускает асинхронную таску для отправки сообщения
def send_epp_event_notification(event_object: Collection | Ledger, **kwargs) -> None:
    bind_contextvars(event_object=event_object, got_kwargs=kwargs)
    if is_notification_disabled(event_object):
        logger.info("EPP notifications are disabled for this event object")
        return None

    notification_data = None

    # get initial notification data
    if isinstance(event_object, Ledger):
        notification_data = process_email_for_ledger(event_object, **kwargs)
    elif isinstance(event_object, Collection):
        notification_data = process_email_for_collection(event_object, **kwargs)

    if not notification_data:
        logger.info("Received empty notification data, skipping sending email")
        return

    notification_data.update(
        {
            "from_sender_name": ACCOUNTS_RECEIVABLE_SENDER_NAME,
            "from_sender_email": ACCOUNTS_RECEIVABLE_FROM_EMAIL,
            "cc": MailService.EPP_EVENT_NOTIFICATIONS_EMAILS,
        }
    )
    if settings.BUILD_ENV in ["production"]:
        notification_data.update({"cc": notification_data["cc"] + [ACCOUNTS_RECEIVABLE_FROM_EMAIL]})

    # add notifiaction settings
    max_calls_number = notification_data.pop("max_calls_number", 0)
    task_result_unique_str = notification_data.pop(TASK_KEY, "")
    periodic_task_name = f"send_epp_notification_{task_result_unique_str}"
    bind_contextvars(notification_data=notification_data, task_key=task_result_unique_str, task_name=periodic_task_name)

    logger.info("Finished processing EPP event notification, determining when to send...")

    # determine time frames for sending
    sub_geo_point = get_geography_point(event_object)
    estimated_time = get_estimated_time_or_none(
        company_geo_point=sub_geo_point,
        reserve_return=notification_data.pop("reserve_return", False),
        epp_funded=notification_data.pop("epp_funded", False),
    )

    # do sending notification
    if estimated_time:
        logger.info("Scheduling EPP notification task for the future", estimated_time=estimated_time)
        create_and_schedule_distant_future_task(
            "notifier.tasks.send_email_message",
            periodic_task_name,
            estimated_time,
            task_args=[notification_data],
            task_kwargs={
                "max_calls_number": max_calls_number,
                TASK_KEY: task_result_unique_str,
                PERIODIC_TASK_KEY: periodic_task_name,
            },
        )
    else:
        logger.info("Sending EPP notification to celery for immediate processing")
        send_email_message.apply_async(
            args=[notification_data],
            kwargs={
                "max_calls_number": max_calls_number,
                TASK_KEY: task_result_unique_str,
                PERIODIC_TASK_KEY: periodic_task_name,
            },
        )

# 4. функция для проверки, что входящие документы покрывают промежутки между существующими и не создают
# новых промежутков. Сначала собираем документы, периоды которых надо проверить, за тем собираем периоды, которые
# содержатся во входных данных и добавляем к ним периоды из документов и третьим этапом обрабатываем эти периоды.
# На полноценные функции эти этапы не тянут, поскольку нужны только для этих специфичных обработок.
def validate_documents_set_on_gaps(
    documents: QuerySet[FinancialDocumentsCoreABC], data_to_validate: dict
) -> tuple[bool, dict]:
    subcontractor = data_to_validate.get("subcontractor")
    dates_to_validate: list[dict] = data_to_validate.get("dates_to_validate")

    # collect documents
    closest_document_subquery = (
        documents.filter(subcontractor=subcontractor, end_date__lte=dates_to_validate[0]["start_date"])
        .order_by("-end_date")
        .values("end_date")[:1]
    )
    existing_documents = (
        documents.filter(subcontractor=subcontractor)
        .annotate(closest_end_date=Subquery(closest_document_subquery))
        .annotate(uuid=F("file__uuid"))
    )

    existing_documents_data = existing_documents.filter(end_date__gte=F("closest_end_date")).values(
        "uuid", "period_type", "start_date", "end_date"
    )

    # collect dates
    dates_to_validate.sort(
        key=lambda elem: (date_to_timestamp(elem["end_date"]), date_to_timestamp(elem["start_date"]))
    )
    all_dates = copy(dates_to_validate)  # intentionally used copy() to keep pointers to dicts in dates_to_validate
    all_dates += existing_documents_data

    all_dates.sort(
        key=lambda elem: (-date_to_timestamp(elem["end_date"]), date_to_timestamp(elem["start_date"]))
    )  # from most recent to older
    is_valid = True

    # process dates
    prev_doc = {}
    for cursor_ind, document in enumerate(all_dates):
        document["errors"] = []
        if cursor_ind == 0:
            if date.today() - document["end_date"] > timedelta(days=30):
                is_valid = False
                document["errors"].append(RECENT_DOCUMENT_ERROR)
            prev_doc = document
            continue
        if prev_doc["start_date"] - document["end_date"] > timedelta(days=1):
            is_valid = False
            document["errors"].append(
                (DISCONTINUITY_ERROR[0], DISCONTINUITY_ERROR[1].format(to_date=prev_doc["start_date"]))
            )
            prev_doc["errors"].append(
                (DISCONTINUITY_ERROR[0], DISCONTINUITY_ERROR[1].format(to_date=document["end_date"]))
            )

        if (
            document["period_type"] == prev_doc["period_type"]
            and document["start_date"] == prev_doc["start_date"]
            and document["end_date"] == prev_doc["end_date"]
        ):
            is_valid = False
            document["errors"].append(DUPLICATE_PERIOD_ERROR)
            prev_doc["errors"].append(DUPLICATE_PERIOD_ERROR)
        prev_doc = document

    return is_valid, data_to_validate


# 5. метод обновления документа. Хорошо бы его разбить и унести в сервисный слой, но сейчас он вызывается в сериалайзере
# и состоит из нескольких этапов: обновление статуса документа, запуска и прохождения процессо согласования (если надо),
# обновление прикрепленных документов
def update(self, instance, validated_data):
    request = self.context["request"]
    user = request.user

    old_status = instance.status
    old_status_updated_at = instance.status_updated_at or instance.updated_at or instance.created_at

    new_status = validated_data.get("status")
    counterpart_type = validated_data.get("counterpart_type", instance.counterpart_type)
    start_workflow = validated_data.pop("for_internal_approval", False)
    exhibit_files = validated_data.pop("exhibit_files", None)

    can_update_contract = False
    can_save_counterpart_type_field = False
    can_update_contract_require_coi = False

    # status update
    if old_status == DocumentProjectStatus.DRAFT.value:
        can_update_contract = True
        can_save_counterpart_type_field = True

    if old_status in [
        DocumentProjectStatus.SENT.value,
        DocumentProjectStatus.EDITED.value,
        DocumentProjectStatus.INTERNAL.value,
        DocumentProjectStatus.PENDING_APPROVAL.value,
        DocumentProjectStatus.REVIEWED.value,
        DocumentProjectStatus.PENDING_COUNTERPART_REVIEW.value,
    ]:
        can_update_contract_require_coi = True

    wf_service: None | ContractWorkflowService = None

    status_changed = new_status and old_status != new_status

    if status_changed:
        new_status_updated_at = timezone.now()
        validated_data["status_updated_at"] = new_status_updated_at
        posthog_capture_event.apply_async(
            kwargs={
                "event_name": PosthogCustomEvent.CONTRACT_STATUS_UPDATE,
                "user_id": self.context["request"].user.id,
                "properties": {
                    "new_status": new_status,
                    "old_status": old_status,
                    "event_timestamp": new_status_updated_at,
                    "stayed_in_status": (new_status_updated_at - old_status_updated_at).total_seconds(),
                },
            }
        )

    # Start roadmap process
    if can_update_contract:
        updated_instance = self.update_instance_with_workflow(
            instance=instance, validated_data=validated_data, start_workflow=start_workflow
        )

        updated_instance = super().update(updated_instance, validated_data)

        if start_workflow and updated_instance.workflow and not getattr(updated_instance, "is_subless_sov", False):
            wf_service = ContractWorkflowService(workflow=updated_instance.workflow, start=True)
            wf_service.step_service.postpone_email = True
            wf_service.start_()

        prev_workflow = instance.workflow
        self.workflow_clear_process_handler(updated_instance.workflow, prev_workflow)

        prev_workflow_edition = instance.workflow_edition
        self.workflow_clear_process_handler(updated_instance.workflow_edition, prev_workflow_edition)
    elif can_update_contract_require_coi:
        updated_instance = super().update(instance, validated_data)
    else:
        raise ValueError("Contract can not be updated")

    if start_workflow:
        contract_log_data: dict = {
            "document": updated_instance,
            "user_id": user.id,
            "company_id": user.selected_membership.company_id,
        }
        if isinstance(wf_service, ContractWorkflowService) and isinstance(
            wf_service.step_service.intermediate_email_data_to_send, list
        ):
            for email_data in wf_service.step_service.intermediate_email_data_to_send:
                contract_log_data["email_data"] = email_data
                create_log_and_send_notification(**contract_log_data)

        else:
            handle_document_status_change(**contract_log_data)

    if can_save_counterpart_type_field:
        updated_instance.counterpart_type = counterpart_type
        updated_instance.save()

    # Update exhibit files process
    if exhibit_files is not None:
        updated_instance.exhibit_files.set(exhibit_files)

    return updated_instance