# 1
# В этом методе мы разделяем пути получения notification_data хотя по сути это словарь со схожими полями
def send_epp_event_notification(event_object: Collection | Ledger, **kwargs) -> None:
    notification_data = None

    if isinstance(event_object, Ledger):
        notification_data = process_email_for_ledger(event_object, **kwargs)
    elif isinstance(event_object, Collection):
        notification_data = process_email_for_collection(event_object, **kwargs)
    # дальнейшая обработка notification_data
    ...
    sub_geo_point = get_geography_point(event_object)
    estimated_time = get_estimated_time_or_none(
        company_geo_point=sub_geo_point,
        reserve_return=notification_data.pop("reserve_return", False),
        epp_funded=notification_data.pop("epp_funded", False),
    )
    ...

# в рамках повышения полиморфности можно ввести интерфейс или протокол, который бы описал методы передаваемого объекта и поля notification_data
@dataclass
class NotificationData:
    from_sender_name: str
    from_sender_email: str
    cc: str
    trial_mode_on: bool
    stop_all_notifications: bool
    max_calls_number: int
    TASK_KEY: str
    is_epp_funded: bool
    template_identifier: str
    email_type: str
    to: list[str]
    dataset: dict
    subject: str


class EventObject(Protocol):
    def process_email(self) -> NotificationData: ...
    def get_geography_point(self) -> Point: ...


# и тогда в самом методе можно не делать проверку на тип входящего объекта, а инициировать объект EventObject где-то ближе к собственно событию, вызывающему отправку нотификаций
def send_epp_event_notification(event_object: EventObject, **kwargs) -> None:
    notification_data = event_object.process_email()
    # дальнейшая обработка notification_data
    ...
    sub_geo_point = event_object.get_geography_point()
    estimated_time = get_estimated_time_or_none(
        company_geo_point=sub_geo_point,
        reserve_return=notification_data.pop("reserve_return", False),
        epp_funded=notification_data.pop("epp_funded", False),
    )
    ...


#2
# в методе сохранения документов у компании есть несколько похожих по смыслу действий - мы сохраняем отдельно из данных инвойс и финансовые документы
class EppReadyUploadDocsStepView(viewsets.ViewSet):
    def post(self, request, *args, **kwargs):
        user_company = request.user.selected_membership.company

        with transaction.atomic():
            invoice_serializer = EppReadyFlowInvoiceSubmitSerializer(
                data=request.data, context={"user_company": user_company, "request": request}
            )
            invoice_serializer.is_valid(raise_exception=True)
            invoice_data = invoice_serializer.data

            company_profile_serializer = EPPReadyFlowCompanyProfileFileSubmitSerializer(
                data=request.data, context={"user_company": user_company, "request": request}
            )
            company_profile_serializer.is_valid(raise_exception=True)
            company_profile_data = company_profile_serializer.data

            company_prequal_section_serializer = EppReadyFlowCompanyPrequalSectionSubmitSerializer(
                data=request.data, context={"user_company": user_company, "request": request}
            )
            company_prequal_section_serializer.is_valid(raise_exception=True)
            company_prequal_section_data = company_prequal_section_serializer.data

            financial_documents_serializer = EppReadyFlowFinancialDocumentsSubmitSerializer(
                data=request.data, context={"user_company": user_company, "request": request}
            )
            financial_documents_serializer.is_valid(raise_exception=True)
            financial_documents_data = financial_documents_serializer.data

            project_serializer = EPPReadyFlowProjectUpdateSerializer(data=request.data)
            project_serializer.is_valid(raise_exception=True)
            project_data = project_serializer.data

            update_or_create_invoice_for_epp(request, invoice_data)  # <---

            update_company_profile(user_company, company_profile_data, request)
            update_company_prequal_section(user_company, company_prequal_section_data)
            update_financial_documents(user_company, financial_documents_data, request)  # <---
            ...
    

# для повышения полиморфности можно создать ряд сервисных классов на основе интерфейса 
class DocumentService(ABC):
    @abstractmethod
    def update_or_create(self, request, raw_data: dict, partial_update: bool = False):
        pass


class InvoiceService(DocumentService): ...

class FinancialDocumentService(DocumentService): ...

# и в методе post создавать сервисы, в которых потом в цикле вызывать этот метод
...
invoice_service = InvoiceService(invoice_serializer.data)
financial_documents_service = FinancialDocumentService(financial_documents_serializer.data)

for service in (invoice_service, financial_documents_service):
    service.update_or_create()


# таким образом мы сможем расширить применение этого метода, если понадобится добавлять другие виды документов


# 3
# сервис по получению доанных из документов содержит метод, в котором через if...else проверяется тип входящего документа.
class Textractor:
    ...
    def process_file(self, file_type=None):
        if file_type == self.CHECK:
            response = self._analyze_check_document()
            output = self._parse_questions_response(response)
            all_output = response
        elif file_type == self.CERTIFICATE_OF_INSURANCE:
            response = self._analyze_coi_document()
            output = self._parse_coi_output(response)
            all_output = response
        elif file_type == self.AIA_INVOICE:
            response = self._analyze_aia_output()
            output = self._parse_aia_output(response)
            all_output = response
        else:
            all_output = self._analyze_coi_document()
            output = all_output
        return output, all_output
    

# можно опять же выделить для каждого типа сой обработчик, сделать мэппинг по типу файла и просто вызывать нужный метод
class DocumentProcessor(ABC):
    @abstractmethod
    def analyze(self, textractor: Textractor):
        pass

    @abstractmethod
    def parse(self, response):
        pass

class CheckProcessor(DocumentProcessor):
    def analyze(self, textractor: Textractor):
        return textractor._analyze_check_document()

    def parse(self, response):
        return textractor._parse_questions_response(response)

class COIProcessor(DocumentProcessor):
    def analyze(self, textractor: Textractor):
        return textractor._analyze_coi_document()

    def parse(self, response):
        return textractor._parse_coi_output(response)

class AIAInvoiceProcessor(DocumentProcessor):
    def analyze(self, textractor: Textractor):
        return textractor._analyze_aia_output()

    def parse(self, response):
        return textractor._parse_aia_output(response)
    

PROCESSOR_MAP = {
    Textractor.CHECK: CheckProcessor(),
    Textractor.CERTIFICATE_OF_INSURANCE: COIProcessor(),
    Textractor.AIA_INVOICE: AIAInvoiceProcessor(),
}


def process_file(self, file_type=None):
    processor = PROCESSOR_MAP.get(file_type, COIProcessor())
    response = processor.analyze(self)
    output = processor.parse(response)
    return output, response

# это должно позволить добавлять новые обработчики просто добавляя нужный метод и расширяя мэппинг, а в process_file становится понятнее, что происходит


# 4
# похожая проблема - выбор типа и содержания письма в зависимости от того, отправляется ли письмо в рамках процесса страхования или просто в рамках реализации проекта
def send_notification_invitation_to_contractor(
    contractor,
    subcontractor,
    email,
    project=None,
    is_coi=False,
    is_new_user=False,
    url=None,
    reminder=False,
):
    email_data = {
        "contractor_name": contractor.name,
        "subcontractor_name": subcontractor.name,
    }

    if project is None:
        subject = f"{contractor.name} has invited you to Constrafor"
        email_data["project_name"] = "Constrafor"
    else:
        subject = f"{contractor.name} has invited you to {project.name} at Constrafor"
        email_data["project_name"] = f"project {project.name} at Constrafor"

    if reminder:
        subject = "Reminder: " + subject

    if is_coi:
        template = MailService.COI_SUB_PROJECT_INVITATION_EXISTING
    else:
        template = MailService.SUB_PROJECT_INVITATION_EXISTING

    if url:
        email_data["activation_link"] = url
    elif is_new_user:
        email_data["activation_link"] = subcontractor.created_by.create_invitation_url(
            invited_by_user_id=contractor.get_admin("id")
        )
        email = subcontractor.created_by.email
    elif is_coi:
        email_data["activation_link"] = build_frontend_url(SUBCONTRACTOR_INSURANCE)

    if email:
        user_metadata = {email: {"first_name": User.objects.get(email=email).first_name}}
        MailService.send_email_wrapper(
            template_identifier=template,
            to=email,
            dataset=email_data,
            subject=subject,
            trial_mode_on=contractor.trial_mode_on,
            stop_all_notifications=subcontractor.stop_all_notifications,
            branding_company=contractor,
            merge_metadata=user_metadata,
        )
    else:
        logger.warning(f"Could not send email to {subcontractor} because contact email is not set")
    return None

# можно разделить этот метод на два сервиса, которые будут формировать свои письма независимо. Также это облегчит расширение метода
class InvitationABC(ABC):
    @abstractmethod
    def send(self, contractor, subcontractor, email, project=None, url=None):
        pass


class COIInvitationService(InvitationABC):
    def send(self, contractor, subcontractor, email, project=None, url=None):
        subject = f"{contractor.name} has invited you to Constrafor"
        template = MailService.COI_SUB_PROJECT_INVITATION_EXISTING
        activation_link = url or build_frontend_url(SUBCONTRACTOR_INSURANCE)
        # ... формируем email_data ...
        MailService.send_email_wrapper(
            template_identifier=template,
            to=email,
            dataset={"activation_link": activation_link, ...},
            subject=subject,
            trial_mode_on=contractor.trial_mode_on,
            stop_all_notifications=subcontractor.stop_all_notifications,
            branding_company=contractor,
        )

class SubProjectInvitationService(InvitationABC):
    def send(self, contractor, subcontractor, email, project=None, url=None):
        subject = f"{contractor.name} has invited you to {project.name} at Constrafor" if project else f"{contractor.name} has invited you to Constrafor"
        template = MailService.SUB_PROJECT_INVITATION_EXISTING
        activation_link = url or build_frontend_url(SUBCONTRACTOR_INSURANCE)
        # ... формируем email_data ...
        MailService.send_email_wrapper(
            template_identifier=template,
            to=email,
            dataset={"activation_link": activation_link, ...},
            subject=subject,
            trial_mode_on=contractor.trial_mode_on,
            stop_all_notifications=subcontractor.stop_all_notifications,
            branding_company=contractor,
        )

INVITATION_STRATEGY_MAP = {
    "coi": COIInvitationService(),
    "sub_project": SubProjectInvitationService(),
    # можно добавить другие сценарии
}


def send_notification_invitation_to_contractor(
    contractor,
    subcontractor,
    email,
    project=None,
    scenario="sub_project",
    url=None,
):
    strategy = INVITATION_STRATEGY_MAP.get(scenario, SubProjectInvitationService())
    strategy.send(contractor, subcontractor, email, project, url)


# 5
# более широким охватом можно посмотреть на функцию, которая отправляет письма с разными параметрами
def send_contract_notification(
    contract_id,
    template_identifier,
    to,
    dataset,
    trial_mode_on,
    stop_all_notifications,
    email_type=None,
    subject=None,
    reminder=False,
    merge_metadata=None,
    internal=False,
    init_log_data: None | dict = None,
    automatic_reminder: bool = False,
):
    from constrafor import tasks

    match to:
        case QuerySet() | [Membership()]:
            to_memberships_ids = [membership.id for membership in to]
            to = None
        case Membership():
            to_memberships_ids = [to.id]
            to = None
        case _:
            to_memberships_ids = None

    kwargs: dict = {
        "contract_id": contract_id,
        "template_identifier": template_identifier,
        "email_type": email_type,
        "to": to,
        "to_memberships_ids": to_memberships_ids,
        "dataset": dataset,
        "trial_mode_on": trial_mode_on,
        "stop_all_notifications": stop_all_notifications,
        "subject": subject,
        "reminder": reminder,
        "merge_metadata": merge_metadata,
        "internal": internal,
    }
    task_countdown: int = 3

    if init_log_data:
        raw_log_entry_data: None | tuple = contract_log.handle_document_status_change(**init_log_data)
        if isinstance(raw_log_entry_data, tuple):
            log_entry_data, task_countdown = raw_log_entry_data
            kwargs["entry_data"] = log_entry_data
            kwargs["document_uuid"] = init_log_data["document"].uuid
            kwargs["automatic_reminder"] = automatic_reminder

    tasks.contract_notify.apply_async(
        countdown=task_countdown,
        kwargs=kwargs,
    )


# проблема в том, что по всему коду разбросаны вызовы, которые можно разделить на несколько сценариев - либо отправка нотификации о подписании контракта, либо о его отправке.
def send_sign_notification(
    document: DocumentProject,
    signer_user,
    recipient_company=None,
    reminder=False,
    init_log_data: None | dict = None,
    automatic_reminder: bool = False,
) -> None:
    ...

    send_contract_notification(
        contract_id=document.id,
        template_identifier=MailService.CONTR_SUB_SIGNED,
        to=recipients,
        dataset=data,
        trial_mode_on=from_company.trial_mode_on,
        stop_all_notifications=recipient_company.stop_all_notifications,
        reminder=reminder,
        merge_metadata=users_metadata,
        internal=document.category.internal,
        init_log_data=init_log_data,
        automatic_reminder=automatic_reminder,
    )

def send_sent_document_notification(
    document: DocumentProject,
    reminder=False,
    exclude_membership_ids=None,
    init_log_data: None | dict = None,
    automatic_reminder: bool = False,
) -> None:
    ...

    if document.epp and recipients:
        # For EPPs generate a code for each user and send a separate email with authenticated code for user
        for recipient in recipients:
            user = recipient.user
            data["contract_link"] = document.create_authenticated_code_url(user, document.counterpart)
            send_contract_notification(
                contract_id=document.id,
                template_identifier=MailService.CONTR_SUB_SENT_EXISTING,
                to=recipient,
                dataset=data,
                trial_mode_on=document.created_by_company.trial_mode_on,
                stop_all_notifications=document.counterpart.stop_all_notifications,
                subject=subject,
                reminder=reminder,
                merge_metadata=users_metadata,
                internal=document.category.internal,
                automatic_reminder=automatic_reminder,
            )

    send_contract_notification(
        contract_id=document.id,
        template_identifier=MailService.CONTR_SUB_SENT_EXISTING,
        to=recipients,
        dataset=data,
        trial_mode_on=document.created_by_company.trial_mode_on,
        stop_all_notifications=document.counterpart.stop_all_notifications,
        subject=subject,
        reminder=reminder,
        merge_metadata=users_metadata,
        internal=document.category.internal,
        init_log_data=init_log_data,
    )


# можно поискать общие черты и сделать интерфейс в виде абстрактного класса
class ContractNotificationStrategy(ABC):
    @abstractmethod
    def build_kwargs(self, document, **context) -> dict:
        pass

    @abstractmethod
    def send(self, document, **context):
        pass

# и далее под каждый сценарий использования создавать отдельный класс
class SignNotificationStrategy(ContractNotificationStrategy):
    def build_kwargs(self, document, signer_user, recipient_company, **context):
        # формируем kwargs для send_contract_notification
        # ...
        return kwargs

    def send(self, document, signer_user, recipient_company, **context):
        kwargs = self.build_kwargs(document, signer_user, recipient_company, **context)
        send_contract_notification(**kwargs)

class SentNotificationStrategy(ContractNotificationStrategy):
    def build_kwargs(self, document, **context):
        # формируем kwargs для send_contract_notification
        # ...
        return kwargs

    def send(self, document, **context):
        kwargs = self.build_kwargs(document, **context)
        send_contract_notification(**kwargs)

# Тогда вызов в коде отправки нотификации сведется к выбору сценария
NOTIFICATION_STRATEGY_MAP = {
    "sign": SignNotificationStrategy(),
    "sent": SentNotificationStrategy(),
    # можно добавить другие сценарии
}

def notify_contract(document, scenario="sign", **context):
    strategy = NOTIFICATION_STRATEGY_MAP.get(scenario, SignNotificationStrategy())
    strategy.send(document, **context)
