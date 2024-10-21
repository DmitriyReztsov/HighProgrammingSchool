# 1
class Ledger(SoftDeleteObject, models.Model):
    """Объект модели Ledger создается после выполнения процесса сбора документов в рамках ЕПП
    (статус объекта модели EPPRequest переводится в значение EXECUTED)
    при условии, что счет, прикрепленный к ЕПП, переводится в статус APPROVED (объект модели Invoice).
    Модель используется для отслеживания статуса запроса ЕПП и платежей, сделанных в рамках обеспечения счета.

    Параметры Ledger определяемые Credit Teams (командой кредитного отдела) - обязательные:
    - invoice_amount
    - advance_rate
    - weekly_discount_rate
    - payment_term (days)

    остальные параметры, такие как overdue_fee_ratio и grace_period и другие поля для отслеживания - опционально.
    Поля, не заполняемые напрямую - рассчитываются на основе этих параметров и сумм, выплаченных по инвойсу.
    Часть полей (см. метод save()) рассчитывается при каждом обновлении объекта, часть - единожды при создании.

    """

    invoice_number = models.CharField(max_length=50)
    invoice_amount = models.BigIntegerField()
    invoice_approval_date = models.DateField(blank=True, null=True)
    invoice_purchase_date = models.DateField(blank=True, null=True)
    is_invoice_paid = models.BooleanField(default=False)

    advance_rate = models.FloatField()
    estimated_repayment_period = models.PositiveIntegerField(blank=True, null=True)
    weekly_discount_rate = models.FloatField(blank=True, null=True)

    ...
    grace_period = models.SmallIntegerField(default=5)
    overdue_fee_ratio = models.FloatField(default=1.5)
    grace_period_fee_ratio = models.FloatField(default=1.0)

    ...
    # temporary fields, calculated on every updates
    balance_amount = models.BigIntegerField(blank=True, null=True)
    collected_amount = models.BigIntegerField(blank=True, null=True)
    rebate_amount = models.BigIntegerField(blank=True, null=True)
    recent_payment_date = models.DateField(blank=True, null=True)
    overdue_fee = models.BigIntegerField(blank=True, null=True)

    advance_amount = models.FloatField(blank=True, null=True)
    payment_term = models.IntegerField(blank=True, null=True)
    days_overdue = models.IntegerField(blank=True, null=True)
    discount_percentage = models.FloatField(blank=True, null=True)
    discount_amount = models.BigIntegerField(blank=True, null=True)
    purchase_price = models.BigIntegerField(blank=True, null=True)
    ...
    ...

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        prv_status = self.status
        prv_fund = self.spv_fund
        prv_is_insured = self.is_insured

        if self.write_off and self.status == LedgerStatusChoices.COMPLETED:
            logger.info(
                f"Ledger {self.id} has status {LedgerStatusChoices.COMPLETED} and write_off set to True, skipping..."
            )
            raise Exception("Cannot write off a completed EPP")
        if self.write_off:
            self.status = self.get_status()
        if self.status == LedgerStatusChoices.COMPLETED and not self.can_update_completed_ledger:
            logger.info(
                f"Ledger {self.id} has status {self.status} and cannot be updated without the "
                f"can_update_completed_ledger flag being set to True, skipping..."
            )
            self.calculate(update_overdue_fee=False)
        else:
            self.calculate()
        self.check_and_set_completed_date(prv_status, self.status)

        kwargs["force_insert"] = force_insert
        kwargs["force_update"] = force_update
        self._previous_status = prv_status
        super().save(*args, **kwargs)
        # Applied Insurance and related fields can be recalculated, see self.should_calculate_insurance for details
        if self.gencontractor and self.should_calculate_insurance(prv_status, prv_fund, prv_is_insured):
            from epp.models import GenContractor

            # One-time calculation of constrafor score (from pending to open)
            if not self.constrafor_score:
                from epp.tasks import update_constrafor_score

                try:
                    logger.info("Attempting to sync Constrafor score")
                    update_constrafor_score()
                    logger.info("Finished syncing Constrafor score, continuing on Ledger save...")
                except Exception as e:
                    logger.warning("Failed to sync Constrafor score", exc_info=e)

                if self.gencontractor.constrafor_score and self.subcontractor.constrafor_score:
                    self.constrafor_gc_score = self.gencontractor.constrafor_score
                    self.constrafor_sub_score = self.subcontractor.constrafor_score
                    self.constrafor_score = round(
                        (CONSTRAFOR_SCORE_GC_WEIGHT * self.gencontractor.constrafor_score)
                        + (CONSTRAFOR_SCORE_SUB_WEIGHT * self.subcontractor.constrafor_score),
                        2,
                    )
                    self.save(update_fields=["constrafor_score", "constrafor_gc_score", "constrafor_sub_score"])
                    logger.info(
                        "Updated Ledger Constrafor score",
                        score=self.constrafor_score,
                        gc=self.gencontractor,
                        sub=self.subcontractor,
                    )
                elif self.gencontractor.constrafor_score or self.subcontractor.constrafor_score:
                    # Base case: both gc and sub have a score
                    # This branch should only happen when there is only one score
                    gc_has_score = bool(self.gencontractor.constrafor_score)
                    contractor_score = (
                        self.gencontractor.constrafor_score if gc_has_score else self.subcontractor.constrafor_score
                    )
                    logger.warning(
                        "Ledger only has a score for the" + "GC"
                        if gc_has_score
                        else "Sub" + ", calculating Constrafor score based on that"
                    )
                    self.constrafor_gc_score = contractor_score if gc_has_score else None
                    self.constrafor_sub_score = contractor_score if not gc_has_score else None
                    self.constrafor_score = contractor_score
                    self.save(update_fields=["constrafor_score", "constrafor_gc_score", "constrafor_sub_score"])
                else:
                    logger.warning(
                        "Not updating Ledger Constrafor score because of missing gc or sub score",
                        gc=self.gencontractor,
                        sub=self.subcontractor,
                    )

            prv_cov, prv_applied, prv_avail = (
                self.insurance_coverage if self.insurance_coverage else 0,
                self.applied_insurance if self.applied_insurance else 0,
                self.available_insurance if self.available_insurance else 0,
            )

            gc_ledgers = GenContractor.objects.get(id=self.gencontractor.id).ledgers.values()
            total_outstanding_ledgers = [
                (
                    x.get("total_outstanding")
                    if x.get("total_outstanding")
                    and not x.get("write_off")
                    and not x.get("pending")
                    and (
                        x.get("spv_fund") in [LedgerFundChoices.PLATINUM, LedgerFundChoices.IRIDIUM]
                        or (x.get("spv_fund" == LedgerFundChoices.GOLD) and x.get("is_insured"))  # noqa
                    )
                    and x.get("total_outstanding") > 0
                    else 0
                )
                for x in gc_ledgers
            ]
            self.applied_insurance = sum(total_outstanding_ledgers) - (
                self.total_outstanding if self.total_outstanding and not self._is_uninsured_gold_ledger() else 0
            )
            # There are edge cases where the applied insurance can be negative
            # This can be related to the reserve return payment, where the ledger has a negative total outstanding
            self.applied_insurance = max(self.applied_insurance, 0)
            self.insurance_coverage = (
                self.gencontractor.insurance_max if self.gencontractor and self.gencontractor.insurance_max else 0
            )
            self.available_insurance = self.insurance_coverage - self.applied_insurance
            # Added as a safeguard to ensure that the available insurance never exceeds the insurance coverage
            self.available_insurance = min(self.available_insurance, self.insurance_coverage)
            super().save(*args, **kwargs)
            self.save(update_fields=["applied_insurance", "insurance_coverage", "available_insurance"])

            with bound_contextvars(
                insurance_coverage=self.insurance_coverage,
                applied_insurance=self.applied_insurance,
                available_insurance=self.available_insurance,
            ):
                if any([prv_cov, prv_applied, prv_avail]):
                    logger.info(
                        "Ledger has updated insurance information, recalculating based on outstanding ledgers...",
                        num_outstanding=len(total_outstanding_ledgers),
                        prv_insurance_coverage=prv_cov,
                        prv_applied_insurance=prv_applied,
                        prv_available_insurance=prv_avail,
                    )
                else:
                    logger.info("First time calculating insurance information for Ledger")

        # Upsert a transaction for the reserve return fee
        self._upsert_reserve_return_fee()

    ...

# 2
class DocumentProject(Document, WorkflowCommonModelPropertiesMixin):
    """
    Модель описывает контракты, привязанные к проектам. Является дочерней по отношению к базовой
    модели документов (Document). Возможные вариации, описанные в модели:
    - документы, созданные генподрядчиком для субподрядчика (базовый случай)
    - документы, созданные субподрядчиком для генподрядчика (поле counterpart = gencontractor)
    - документы, созданные займодателем (подтип генподрядчика) для субподрядчика (поле epp != None)

    При создании контракта создается объект модели DocumentProjectMembership, связывающий
    пользователей субподрядчика с контрактом. Таким образом можно контролировать и получать пользователей,
    получивших доступ к контаркту со стороны субподрядчика. Есть ограничения на доступ к контракту ЕПП:
    пользователи должны иметь соответствующие пермишены или быть с ролью ADMIN.

    Смена статуса контракта происходит:
    - при отправке его на подписание - если внутреннего согласования (workflow) нет или в статусе COMPLETED,
    - при запросе правок - нет ограничений,
    - при запросе утверждения правок - если внутреннего соглания (workflow_edition) нет или в статусе COMPLETED,
    - при подписании субподрядчиком - если правки утверждены запроса на правки нет,
    - при подписании генподрядчиком - если документ подписан субподрядчиком.

    """
    SUBCONTRACTOR = "subcontractor"
    PROJECT_OWNER = "project_owner"
    GENCONTRACTOR = "gencontractor"  # for contracts created by sub
    COUNTERPART_TYPE_CHOICES = [
        (SUBCONTRACTOR, "Subcontractor"),
        (PROJECT_OWNER, "Owner"),
        (GENCONTRACTOR, "General_contractor"),
    ]

    number = models.CharField(max_length=64, blank=True, db_index=True, default="")

    project = models.ForeignKey(
        "constrafor.Project",
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True,
    )
    counterpart = models.ForeignKey(
        "constrafor.Company",
        on_delete=models.CASCADE,
        related_name="shared_documents",
        validators=[validate_counterpart],
        null=True,
        blank=True,
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=64, default=DocumentProjectStatus.DRAFT)
    counterpart_type = models.CharField(max_length=13, choices=COUNTERPART_TYPE_CHOICES, default=SUBCONTRACTOR)
    signing_user_gc = models.ForeignKey(
        "user.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="contracts",
    )

    workflow = models.OneToOneField(
        "constrafor.ContractWorkflow",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contract",
    )

    workflow_edition = models.OneToOneField(
        "constrafor.ContractWorkflow",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contract_edition",
    )

    epp = models.ForeignKey(
        "epp.EPPRequest",
        on_delete=models.CASCADE,
        related_name="epp_contracts",
        null=True,
        blank=True,
    )
...

    # for ability to create a contract by sub
    gc_counterpart = models.ForeignKey(
        "constrafor.GencontractorList",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sub_document_project",
    )

    __previous_project_id = None
    __previous_counterpart_id = None

 ...

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        is_new = self._state.adding
        project_changed = not is_new and self.project_id != self.__previous_project_id
        counterpart_changed = not is_new and self.counterpart_id != self.__previous_counterpart_id

        if is_new and self.epp:
            self.epp.status = EPPRequest.APPROVED
            self.epp.save(update_fields=["status"])

        super().save(force_insert, force_update, *args, **kwargs)
        if self.counterpart:
            if (
                self.project
                and (is_new or project_changed or counterpart_changed)
                and self.counterpart.is_contractor
                and not self.category.internal
            ):
                ProjectSubcontractor.objects.update_or_create(
                    project_id=self.project_id,
                    subcontractor_id=self.counterpart_id,
                    defaults={"is_currently_active": True},
                )
            elif (is_new or counterpart_changed) and not self.category.internal:
                if (
                    self.created_by_company.is_contractor
                    and self.counterpart_type == self.SUBCONTRACTOR
                    and self.counterpart.is_contractor
                ):
                    self.created_by_company.contractor.subcontractors.add(self.counterpart.contractor)
                self.created_by_company.contacts.add(self.counterpart)

        self.__previous_project_id = self.project_id
        self.__previous_counterpart_id = self.counterpart_id
    ...

#3
class HubspotContact(AbstractHubspotLifeCycleStageField, HubspotIntegrationCommon):
    """
    Класс предназначен для связывания сущностей пользователей из различных компаний (связь с компаниями и юзерами через
    поле membership) и записей стороннего сервиса Hubspot. Значения полей, содержащих данные о пользователе, содержатся
    в виде словаря в поле properties, данные о дате изменения в полях и флаг возможности синхронизации данных - в поле 
    properties_meta_data. Данные, измененные на стороне Hubspot должны быть исключены из дальнейшей синхронизации.

    """
    membership = models.OneToOneField(
        "user.Membership",
        on_delete=models.CASCADE,
        related_name="hubspot_contact",
    )
    score = models.IntegerField(null=True, blank=True, help_text="Hubspot Score")
    sales_rep = models.ForeignKey(
        "hubspot_integration.HubspotOwner",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Hubspot Contact Owner",
    )
    sales_rep_assigned_date = models.DateTimeField(null=True, blank=True, help_text="Hubspot Owner Assigned Date")
    last_contacted_date = models.DateTimeField(null=True, blank=True, help_text="Hubspot Last Contacted")
    number_of_sessions = models.IntegerField(null=True, blank=True, help_text="Hubspot Number of Sessions")
    number_of_page_views = models.IntegerField(null=True, blank=True, help_text="Hubspot Number of Page Views")

    # hubspot contact properties
    hubspot_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    properties = models.JSONField(default=dict, null=True, blank=True)
    properties_meta_data = models.JSONField(default=dict, null=True, blank=True)
