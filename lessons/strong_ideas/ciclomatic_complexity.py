# === 1 ===
# исходная функция, цикломатическая сложность, замеренная через radon = 9
def collect_epp_related_users(ledger: Ledger, epp_request: EPPRequest = None) -> list[User] | None:
    all_sub_epps = EPPRequest.objects.filter(ledger__subcontractor=ledger.subcontractor)
    all_epp_contracts = DocumentProject.objects.filter(epp__in=all_sub_epps).order_by("id")
    sub_memberships_all = []
    if all_epp_contracts.filter(epp=epp_request).exists():
        for epp_contract in all_epp_contracts.filter(epp=epp_request):
            sub_doc_proj_memberships = epp_contract.document_project_membership_rel.select_related("membership__user")
            sub_memberships_all.extend(
                doc_proj_membership.membership for doc_proj_membership in sub_doc_proj_memberships
            )
    elif all_epp_contracts.exists():
        sub_doc_proj_memberships = all_epp_contracts.last().document_project_membership_rel.select_related(
            "membership__user"
        )
        sub_memberships_all.extend(doc_proj_membership.membership for doc_proj_membership in sub_doc_proj_memberships)
    else:
        ledger_subcontractor = ledger.subcontractor
        if not ledger_subcontractor:
            return None

        subcontractor = ledger_subcontractor.constrafor_company
        if not subcontractor:
            return None

        sub_memberships_all = subcontractor.memberships.select_related("user")

    return list(membership.user for membership in set(sub_memberships_all))


# через вынос циклов и list-comprehension в отдельные методы, устранения else снизил сложность до 3
def collect_from_epp_request(all_contracts_from_epp_request):
    sub_memberships_all = []
    for epp_contract in all_contracts_from_epp_request:
        sub_doc_proj_memberships = epp_contract.document_project_membership_rel.select_related("membership__user")
        sub_memberships_all.extend(doc_proj_membership.membership for doc_proj_membership in sub_doc_proj_memberships)
    return sub_memberships_all


def collect_from_single_contract(epp_contract):
    sub_memberships_all = []
    sub_doc_proj_memberships = epp_contract.document_project_membership_rel.select_related("membership__user")
    sub_memberships_all.extend(doc_proj_membership.membership for doc_proj_membership in sub_doc_proj_memberships)
    return sub_memberships_all


def collect_from_subcontractor(ledger_subcontractor):
    if not ledger_subcontractor:
        return None

    subcontractor = ledger_subcontractor.constrafor_company
    if not subcontractor:
        return None

    return subcontractor.memberships.select_related("user")


def get_users_list_from_memberships(sub_memberships_all):
    return list(membership.user for membership in set(sub_memberships_all))


def collect_epp_related_users(ledger: Ledger, epp_request: EPPRequest = None) -> list[User] | None:
    all_sub_epps = EPPRequest.objects.filter(ledger__subcontractor=ledger.subcontractor)
    all_epp_contracts = DocumentProject.objects.filter(epp__in=all_sub_epps).order_by("id")

    if all_epp_contracts.filter(epp=epp_request).exists():
        sub_memberships_all = collect_from_epp_request(all_epp_contracts.filter(epp=epp_request))
        return get_users_list_from_memberships(sub_memberships_all)
    
    if all_epp_contracts.exists():
        sub_memberships_all = collect_from_single_contract(all_epp_contracts.last())
        return get_users_list_from_memberships(sub_memberships_all)

    sub_memberships_all = collect_from_subcontractor(ledger.subcontractor)
    return get_users_list_from_memberships(sub_memberships_all)


# === 2 ===
# исходный метод, сложность 20
def save(self, force_insert=False, force_update=False, *args, **kwargs):
    is_new = self._state.adding
    is_active_changed = not is_new and self.is_active != self.__previous_is_active
    current_owner_id = self.owner.id if self.owner else None
    owner_changed = self.__previous_owner_id != current_owner_id
    super().save(force_insert, force_update, *args, **kwargs)

    if is_new and self.contractor:
    if self.get_is_new_with_contractor():
    if not self.owner_subcontractor:
        memberships = self.contractor.memberships.exclude(role__in=FIELD_ROLES)
        users = [membership.user for membership in memberships]
        for user in users:
            assign_perm(Project.PERM_ACCESS_PROJECT, user, self)

    update_fields = ["general_contractor_name"]
    self.general_contractor_name = self.contractor.name or ""

    if self.contractor.participates_in_epp:
        self.epp_approved = True
        update_fields.append("epp_approved")

    super().save(update_fields=update_fields)

    if owner_changed:
        if self.__previous_owner_id:
            previous_owner = ProjectOwner.objects.get(pk=self.__previous_owner_id)
            users = [membership.user for membership in previous_owner.memberships.all()]
            for user in users:
                perms = get_user_perms(user, self)
                if Project.PERM_ACCESS_PROJECT_NAME in perms:
                    remove_perm(Project.PERM_ACCESS_PROJECT, user, self)

        if self.owner:
            users = [membership.user for membership in self.owner.memberships.all()]
            for user in users:
                perms = get_user_perms(user, self)
                if Project.PERM_ACCESS_PROJECT_NAME not in perms:
                    assign_perm(Project.PERM_ACCESS_PROJECT, user, self)

    if is_active_changed:
        self.projectsubcontractor_set.update(is_currently_active=self.is_active)
    self.__previous_owner_id = current_owner_id
    self.__previous_is_active = self.is_active

# применил диспетчеризацию, вынос циклов и булевых операторов в отдельные методы. Сложность стала 3
def process_with_contractor(self):
    if not self.owner_subcontractor:
        memberships = self.contractor.memberships.exclude(role__in=FIELD_ROLES)
        users = [membership.user for membership in memberships]
        for user in users:
            assign_perm(Project.PERM_ACCESS_PROJECT, user, self)

    self.general_contractor_name = self.contractor.name or ""

    if self.contractor.participates_in_epp:
        self.epp_approved = True

def process_with_owner(self):
    if not self.owner:
        return

    users = [membership.user for membership in self.owner.memberships.all()]
    for user in users:
        perms = get_user_perms(user, self)
        if Project.PERM_ACCESS_PROJECT_NAME not in perms:
            assign_perm(Project.PERM_ACCESS_PROJECT, user, self)

def process_with_previous_owner(self):
    if not self.__previous_owner_id:
        return

    previous_owner = ProjectOwner.objects.get(pk=self.__previous_owner_id)
    users = [membership.user for membership in previous_owner.memberships.all()]
    for user in users:
        perms = get_user_perms(user, self)
        if Project.PERM_ACCESS_PROJECT_NAME in perms:
            remove_perm(Project.PERM_ACCESS_PROJECT, user, self)

def process_active_change(self):
    if self.is_active != self.__previous_is_active:
        self.projectsubcontractor_set.update(is_currently_active=self.is_active)

def save(self, force_insert=False, force_update=False, *args, **kwargs):
    is_new = self._state.adding
    current_owner_id = self.owner.id if self.owner else None
    super().save(force_insert, force_update, *args, **kwargs)

    dispatcher = {
        (is_new is True): (
            self.process_with_contractor,
            self.process_with_owner,
        ),
        (is_new is False): (self.process_with_previous_owner, self.process_with_owner, self.process_active_change),
    }
    for method in dispatcher[is_new]:
        method()

    self.__previous_owner_id = current_owner_id
    self.__previous_is_active = self.is_active


# === 3 ===
# начальная версия, сложность 15
def confirm(self, request, *args, **kwargs):
    document: DocumentProject = self.get_object()
    signature_id = request.data.get("signature_id", None)
    editor_permissions = request.data.get("editor_permissions")

    try:
        signature_request = SignatureRequestDocument.objects.get(document=document)
    except exceptions.ObjectDoesNotExist:
        return Response(
            {"message": "Signature request not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    signature_request = DropboxSignService.get_signature_request(signature_request.signature_request_id)
    user_signature_map = {sig.signature_id: sig for sig in signature_request.signatures}
    signature = user_signature_map[signature_id]

    if not signature.signed_at:
        return Response(
            {"message": "Signature request is not signed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        signer_user = Signature.objects.get(signature_id=signature_id).user
        document.updated_by = signer_user
        if document.status != DocumentProjectStatus.SIGNED and document.status != DocumentProjectStatus.EXECUTED:
            document.status = DocumentProjectStatus.SIGNED
            logger.info(f"Contract {document.name}:{document.id} status change to SIGNED")
        if (
            document.epp
            and document.counterpart
            and document.counterpart.memberships.filter(user=signer_user).exists()
        ):
            trigger_slack_epp_contract_signed_workflow(document, signer_user)

        if document.require_coi_approval:
            coi = (
                InsuranceRequest.objects.filter(
                    subcontractor_id=document.counterpart_id, project_id=document.project_id
                )
                .prefetch_related("insurance_policies")
                .first()
            )
            policies = coi.insurance_policies.all()
            should_send_notification = policies.exists() and not any(
                policy.status not in [PolicyStatus.ACTIVE, PolicyStatus.WAIVED] for policy in policies
            )
        else:
            should_send_notification = True

    if all(sig.signed_at for sig in user_signature_map.values()):
        document.status = DocumentProjectStatus.EXECUTED
        logger.info(f"Contract {document.name}:{document.id} status change to EXECUTED")
    # Do this because of Django default behavior for update_fields
    # See here: https://code.djangoproject.com/ticket/22981
    document.updated_at = datetime.now()
    document.save(update_fields=["status", "updated_by", "updated_at"])

    init_log_data: dict[str, Any] = {
        "document": document,
        "user_id": self.request.user.id,
        "editor_permissions": editor_permissions,
        "company_id": self.request.user.selected_membership.company_id,
        "run_task": False,
    }
    if should_send_notification:
        send_sign_notification(document, signer_user, init_log_data=init_log_data)

    serializer = self.get_serializer(document)
    return Response(serializer.data)

# убрал лишний else, вынес проверки и цепочки булевых операций в соответствующие модели 
# (в т.ч. в дочернюю модель, в родительской опрелелен абстрактный метод, для реализации на других дочерних моделях), 
# переписал в условии list comprehension на map
# сложность стала 9
class Document():
    ...
    @abstractmethod
    def should_send_notifications():
        ...

class DocumentProject(Document):
    ...
    def should_send_notifications(self):
        if self.require_coi_approval:
            coi = (
                InsuranceRequest.objects.filter(subcontractor_id=self.counterpart_id, project_id=self.project_id)
                .prefetch_related("insurance_policies")
                .first()
            )
            policies = coi.insurance_policies.all()
            return policies.exists() and not any(
                policy.status not in [PolicyStatus.ACTIVE, PolicyStatus.WAIVED] for policy in policies
            )
        return True

class SignatureRequestDocument():
    ...
    def get_signature_map(self):
        return {sig.signature_id: sig for sig in self.signatures}

class DocumentProjectViewSet(DocumentViewSet):
    ...
    @action(detail=True, methods=["put"])
    def confirm(self, request, *args, **kwargs):
        document: DocumentProject = self.get_object()
        signature_id = request.data.get("signature_id", None)
        editor_permissions = request.data.get("editor_permissions")

        try:
            signature_request = SignatureRequestDocument.objects.get(document=document)
        except exceptions.ObjectDoesNotExist:
            return Response(
                {"message": "Signature request not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        signature_request = DropboxSignService.get_signature_request(signature_request.signature_request_id)
        user_signature_map = signature_request.get_signature_map()
        signature = user_signature_map[signature_id]

        if not signature.signed_at:
            return Response(
                {"message": "Signature request is not signed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        signer_user = Signature.objects.get(signature_id=signature_id).user
        document.updated_by = signer_user
        if document.status not in [DocumentProjectStatus.SIGNED, DocumentProjectStatus.EXECUTED]:
            document.status = DocumentProjectStatus.SIGNED
            logger.info(f"Contract {document.name}:{document.id} status change to SIGNED")
        if document.epp and document.counterpart and document.counterpart.memberships.filter(user=signer_user).exists():
            trigger_slack_epp_contract_signed_workflow(document, signer_user)

        if all(map(lambda sig: sig.signed_at, user_signature_map.values())):
            document.status = DocumentProjectStatus.EXECUTED
            logger.info(f"Contract {document.name}:{document.id} status change to EXECUTED")
        # Do this because of Django default behavior for update_fields
        # See here: https://code.djangoproject.com/ticket/22981
        document.updated_at = datetime.now()
        document.save(update_fields=["status", "updated_by", "updated_at"])

        init_log_data: dict[str, Any] = {
            "document": document,
            "user_id": self.request.user.id,
            "editor_permissions": editor_permissions,
            "company_id": self.request.user.selected_membership.company_id,
            "run_task": False,
        }
        if document.should_send_notification:
            send_sign_notification(document, signer_user, init_log_data=init_log_data)

        serializer = self.get_serializer(document)
        return Response(serializer.data)
    

    # === 4 ===
    # сложность 39
    def update(self, instance, validated_data):
        request = self.context.get("request")
        # prequal_data = copy.deepcopy(validated_data)
        prequal_sync = PrequalCompanyProfileSync(instance)

        if "address" in validated_data:
            address_data = validated_data.pop("address")
            if instance.address:
                address_data["updated_by"] = request.user
                for attr, value in address_data.items():
                    setattr(instance.address, attr, value)
                instance.address.save()
            else:
                instance.address = Address.objects.create(created_by=request.user, **address_data)
            prequal_sync.sync_address(instance.address)

        if "companysuppliercategory_set" in validated_data:
            subcontractor_works_data = validated_data.pop("companysuppliercategory_set", [])
            updated_list = []
            for work in subcontractor_works_data:
                obj, created = CompanySupplierCategory.objects.update_or_create(
                    company_id=instance.id,
                    supplier_category=work["supplier_category_id"],
                    defaults={"amount": work["amount"]},
                )
                updated_list.append(obj.id)
            CompanySupplierCategory.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

        if "gross_receipts" in validated_data:
            gross_receipts = validated_data.pop("gross_receipts", [])
            updated_list = []
            for receipt in gross_receipts:
                obj, created = GrossReceipt.objects.update_or_create(
                    company_id=instance.id,
                    year=receipt["year"],
                    defaults={"amount": receipt["amount"]},
                )
                updated_list.append(obj.id)
            GrossReceipt.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

        if "creditreports" in validated_data:
            credit_reports = validated_data.pop("creditreports", [])
            updated_list = []
            try:
                with transaction.atomic():
                    for credit_report in credit_reports:
                        obj, created = CompanyCreditReport.objects.update_or_create(
                            company_id=instance.id,
                            year=credit_report["year"],
                            file=credit_report["file_uuid"],
                            defaults={"description": credit_report.get("description", "")},
                        )
                        updated_list.append(obj.id)
            except IntegrityError:
                raise serializers.ValidationError("Company can have only one credit report file for each year")
            CompanyCreditReport.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

        if "financialstatements" in validated_data:
            financial_statements = validated_data.pop("financialstatements", [])
            updated_list = []
            try:
                with transaction.atomic():
                    for statement in financial_statements:
                        obj, created = CompanyFinancialStatement.objects.update_or_create(
                            company_id=instance.id,
                            year=statement["year"],
                            file=statement["file_uuid"],
                            defaults={"description": statement.get("description", "")},
                        )
                        updated_list.append(obj.id)
            except IntegrityError:
                raise serializers.ValidationError("Company can have only one financial statement file for each year")
            CompanyFinancialStatement.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()
            prequal_sync.sync_financial_statements(instance.financialstatements.all())

        if "monthlybankstatements" in validated_data:
            monthly_bank_statements = validated_data.pop("monthlybankstatements", [])
            updated_list = []
            try:
                with transaction.atomic():
                    for monthly_bank_statement in monthly_bank_statements:
                        obj, created = CompanyMonthlyBankStatement.objects.update_or_create(
                            company_id=instance.id,
                            year=monthly_bank_statement["year"],
                            month=monthly_bank_statement["month"],
                            file=monthly_bank_statement["file_uuid"],
                            defaults={"description": monthly_bank_statement.get("description", "")},
                        )
                        updated_list.append(obj.id)
            except IntegrityError:
                raise serializers.ValidationError(
                    "Company can have only one monthly bank statement file for each year and month"
                )
            CompanyMonthlyBankStatement.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()
            prequal_sync.sync_bank_statements(instance.monthlybankstatements.all())

        if "taxfilings" in validated_data:
            tax_filings = validated_data.pop("taxfilings", [])
            updated_list = []
            try:
                with transaction.atomic():
                    for filing in tax_filings:
                        obj, created = CompanyTaxFiling.objects.update_or_create(
                            company_id=instance.id,
                            year=filing["year"],
                            file=filing["file_uuid"],
                            defaults={"description": filing.get("description", "")},
                        )
                        updated_list.append(obj.id)
            except IntegrityError:
                raise serializers.ValidationError("Company can have only one tax filing file for each year")
            CompanyTaxFiling.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()
            prequal_sync.sync_taxfilings(instance.taxfilings.all())

        if "bondinglimits" in validated_data:
            bonding_limits = validated_data.pop("bondinglimits")
            if bonding_limits is None:
                CompanyBondingLimits.objects.filter(company_id=instance.id).delete()
            else:
                _files = bonding_limits.pop("files", [])
                try:
                    obj = CompanyBondingLimits.objects.get(company_id=instance.id)
                    for key, value in bonding_limits.items():
                        setattr(obj, key, value)
                    obj.save()
                except CompanyBondingLimits.DoesNotExist:
                    bonding_limits.update({"company_id": instance.id})
                    obj = CompanyBondingLimits.objects.create(**bonding_limits)
                obj.files.set(_files)
            if hasattr(instance, "bondinglimits"):
                prequal_sync.sync_bonding_limits(instance.bondinglimits)

        if "license" in validated_data:
            license = validated_data.pop("license")
            if license is None:
                if instance.license:
                    instance.license.delete()
                    instance.license = None
            else:
                _files = license.pop("files", [])
                try:
                    obj = CompanyLicense.objects.get(company__id=instance.id)
                    for key, value in license.items():
                        setattr(obj, key, value)
                    obj.save()
                except CompanyLicense.DoesNotExist:
                    obj = CompanyLicense.objects.create(**license)
                    instance.license = obj

                obj.files.set(_files)

        if "prequal_section" in validated_data:
            prequal_section = validated_data.pop("prequal_section")

            if prequal_section is None and hasattr(instance, "prequal_section"):
                instance.prequal_section.delete()
            elif prequal_section is not None and hasattr(instance, "prequal_section"):
                prequal_section.update({"company": instance})
                prequal_section_serializer = CompanyPrequalSectionSerializer(data=prequal_section)
                prequal_section_serializer.is_valid()
                prequal_section_serializer.update(instance=instance.prequal_section, validated_data=prequal_section)
            elif prequal_section is not None and not hasattr(instance, "prequal_section"):
                prequal_section.update({"company": instance})
                prequal_section_serializer = CompanyPrequalSectionSerializer(data=prequal_section)
                prequal_section_serializer.is_valid()
                prequal_section_serializer.create(validated_data=prequal_section, user=request.user)

        if "epp_pre_approval_status" in validated_data:
            epp_pre_approval_status = validated_data.get("epp_pre_approval_status")
            if epp_pre_approval_status == EppPreApprovalStatus.processing:
                email_data = {
                    "company_name": instance.name,
                    "company_id": instance.id,
                    "django_admin_url": f"{settings.BASE_API_URL}{get_admin_url(instance)}",
                }
                MailService.notify_epp_pre_approval_team(
                    template=MailService.EPP_PRE_APPROVE_REQUESTED,
                    **email_data,
                )
            else:
                raise serializers.ValidationError(
                    f"Epp pre-approval status can be changed only to {EppPreApprovalStatus.processing}"
                )

        result = super().update(instance, validated_data)
        prequal_sync.sync_object_to(validated_data)

        return result
    
# за счет диспетчеризации устранено множество проверок. Сложность = 3, сложности дополнительных методов не превышают 3
def process_address(self, instance, validated_data):
    request = self.context.get("request")
    prequal_sync = PrequalCompanyProfileSync(instance)
    address_data = validated_data.pop("address")
    if instance.address:
        address_data["updated_by"] = request.user
        for attr, value in address_data.items():
            setattr(instance.address, attr, value)
        instance.address.save()
    else:
        instance.address = Address.objects.create(created_by=request.user, **address_data)
    prequal_sync.sync_address(instance.address)

def process_companysuppliercategory_set(self, instance, validated_data):
    subcontractor_works_data = validated_data.pop("companysuppliercategory_set", [])
    updated_list = []
    for work in subcontractor_works_data:
        obj, created = CompanySupplierCategory.objects.update_or_create(
            company_id=instance.id,
            supplier_category=work["supplier_category_id"],
            defaults={"amount": work["amount"]},
        )
        updated_list.append(obj.id)
    CompanySupplierCategory.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

def process_gross_receipts(self, instance, validated_data):
    gross_receipts = validated_data.pop("gross_receipts", [])
    updated_list = []
    for receipt in gross_receipts:
        obj, created = GrossReceipt.objects.update_or_create(
            company_id=instance.id,
            year=receipt["year"],
            defaults={"amount": receipt["amount"]},
        )
        updated_list.append(obj.id)
    GrossReceipt.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

def process_creditreports(self, instance, validated_data):
    credit_reports = validated_data.pop("creditreports", [])
    updated_list = []
    try:
        with transaction.atomic():
            for credit_report in credit_reports:
                obj, created = CompanyCreditReport.objects.update_or_create(
                    company_id=instance.id,
                    year=credit_report["year"],
                    file=credit_report["file_uuid"],
                    defaults={"description": credit_report.get("description", "")},
                )
                updated_list.append(obj.id)
    except IntegrityError:
        raise serializers.ValidationError("Company can have only one credit report file for each year")
    CompanyCreditReport.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

def process_financialstatements(self, instance, validated_data):
    financial_statements = validated_data.pop("financialstatements", [])
    updated_list = []
    try:
        with transaction.atomic():
            for statement in financial_statements:
                obj, created = CompanyFinancialStatement.objects.update_or_create(
                    company_id=instance.id,
                    year=statement["year"],
                    file=statement["file_uuid"],
                    defaults={"description": statement.get("description", "")},
                )
                updated_list.append(obj.id)
    except IntegrityError:
        raise serializers.ValidationError("Company can have only one financial statement file for each year")
    CompanyFinancialStatement.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

    prequal_sync = PrequalCompanyProfileSync(instance)
    prequal_sync.sync_financial_statements(instance.financialstatements.all())

def process_monthlybankstatements(self, instance, validated_data):
    monthly_bank_statements = validated_data.pop("monthlybankstatements", [])
    updated_list = []
    try:
        with transaction.atomic():
            for monthly_bank_statement in monthly_bank_statements:
                obj, created = CompanyMonthlyBankStatement.objects.update_or_create(
                    company_id=instance.id,
                    year=monthly_bank_statement["year"],
                    month=monthly_bank_statement["month"],
                    file=monthly_bank_statement["file_uuid"],
                    defaults={"description": monthly_bank_statement.get("description", "")},
                )
                updated_list.append(obj.id)
    except IntegrityError:
        raise serializers.ValidationError(
            "Company can have only one monthly bank statement file for each year and month"
        )
    CompanyMonthlyBankStatement.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

    prequal_sync = PrequalCompanyProfileSync(instance)
    prequal_sync.sync_bank_statements(instance.monthlybankstatements.all())

def process_taxfilings(self, instance, validated_data):
    tax_filings = validated_data.pop("taxfilings", [])
    updated_list = []
    try:
        with transaction.atomic():
            for filing in tax_filings:
                obj, created = CompanyTaxFiling.objects.update_or_create(
                    company_id=instance.id,
                    year=filing["year"],
                    file=filing["file_uuid"],
                    defaults={"description": filing.get("description", "")},
                )
                updated_list.append(obj.id)
    except IntegrityError:
        raise serializers.ValidationError("Company can have only one tax filing file for each year")
    CompanyTaxFiling.objects.filter(company_id=instance.id).exclude(id__in=updated_list).delete()

    prequal_sync = PrequalCompanyProfileSync(instance)
    prequal_sync.sync_taxfilings(instance.taxfilings.all())

def process_bondinglimits(self, instance, validated_data):
    bonding_limits = validated_data.pop("bondinglimits")
    if bonding_limits is None:
        CompanyBondingLimits.objects.filter(company_id=instance.id).delete()
    else:
        _files = bonding_limits.pop("files", [])
        try:
            obj = CompanyBondingLimits.objects.get(company_id=instance.id)
            for key, value in bonding_limits.items():
                setattr(obj, key, value)
            obj.save()
        except CompanyBondingLimits.DoesNotExist:
            bonding_limits.update({"company_id": instance.id})
            obj = CompanyBondingLimits.objects.create(**bonding_limits)
        obj.files.set(_files)
    if hasattr(instance, "bondinglimits"):
        prequal_sync = PrequalCompanyProfileSync(instance)
        prequal_sync.sync_bonding_limits(instance.bondinglimits)

def process_license(self, instance, validated_data):
    license = validated_data.pop("license")
    if license is None:
        if instance.license:
            instance.license.delete()
            instance.license = None
    else:
        _files = license.pop("files", [])
        try:
            obj = CompanyLicense.objects.get(company__id=instance.id)
            for key, value in license.items():
                setattr(obj, key, value)
            obj.save()
        except CompanyLicense.DoesNotExist:
            obj = CompanyLicense.objects.create(**license)
            instance.license = obj

        obj.files.set(_files)

def process_prequal_section(self, instance, validated_data):
    prequal_section = validated_data.pop("prequal_section")

    if prequal_section is None and hasattr(instance, "prequal_section"):
        instance.prequal_section.delete()
    elif prequal_section is not None and hasattr(instance, "prequal_section"):
        prequal_section.update({"company": instance})
        prequal_section_serializer = CompanyPrequalSectionSerializer(data=prequal_section)
        prequal_section_serializer.is_valid()
        prequal_section_serializer.update(instance=instance.prequal_section, validated_data=prequal_section)
    elif prequal_section is not None and not hasattr(instance, "prequal_section"):
        prequal_section.update({"company": instance})
        prequal_section_serializer = CompanyPrequalSectionSerializer(data=prequal_section)
        prequal_section_serializer.is_valid()
        prequal_section_serializer.create(validated_data=prequal_section, user=request.user)

    if "epp_pre_approval_status"(self, instance, validated_data):
        epp_pre_approval_status = validated_data.get("epp_pre_approval_status")
        if epp_pre_approval_status == EppPreApprovalStatus.processing:
            email_data = {
                "company_name": instance.name,
                "company_id": instance.id,
                "django_admin_url": f"{settings.BASE_API_URL}{get_admin_url(instance)}",
            }
            MailService.notify_epp_pre_approval_team(
                template=MailService.EPP_PRE_APPROVE_REQUESTED,
                **email_data,
            )
        else:
            raise serializers.ValidationError(
                f"Epp pre-approval status can be changed only to {EppPreApprovalStatus.processing}"
            )

def update(self, instance, validated_data):
    dispatcher = {
        "address": self.process_address,
        "companysuppliercategory_set": self.process_companysuppliercategory_set,
        "gross_receipts": self.process_gross_receipts,
        "creditreports": self.process_creditreports,
        "financialstatements": self.process_financialstatements,
        "monthlybankstatements": self.process_monthlybankstatements,
        "taxfilings": self.process_taxfilings,
        "bondinglimits": self.process_bondinglimits,
        "license": self.process_license,
        "prequal_section": self.process_prequal_section,
    }
    for key in validated_data:
        if process_method := dispatcher.get(key):
            process_method(instance, validated_data)

    return super().update(instance, validated_data)
