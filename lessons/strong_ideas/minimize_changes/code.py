# view.py
class EppReadyUploadDocsStepView(views.APIView):
    ...

    def patch(self, request, *args, **kwargs):
        user = request.user
        if (
            not user
            or not hasattr(user, "selected_membership")
            or not user.selected_membership
            or not user.selected_membership.company
        ):
            return Response(
                "Method PATCH is not allowed without user.selected_membership.company attribute of request.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_company = user.selected_membership.company

        with transaction.atomic():
            data = set_previous_and_current_year_in_bank_statements_by_current_date(request.data)
            epp_ready_upload_docs_serializer = EppReadyFlowUploadDocsUpdateSerializer(
                data=data, partial=True, context={"request": request, "action": "patch"}
            )
            epp_ready_upload_docs_serializer.is_valid(raise_exception=True)

            company_profile_epp_ready_flow_serializer = EppReadyFlowUploadDocsCompanyProfileUpdateSerializer(
                data=data, partial=True
            )
            company_profile_epp_ready_flow_serializer.is_valid(raise_exception=True)

            invoice = update_or_create_invoice_for_epp_ready_flow(
                request, epp_ready_upload_docs_serializer.data, partial_update=True
            )
            if invoice:
                set_invoice_in_epp_ready_flow(user_company, invoice)
            update_company_profile(user_company, company_profile_epp_ready_flow_serializer.data, request)
            update_company_prequal_section(user_company, epp_ready_upload_docs_serializer.data, partial_update=True)
            update_financial_documents(user_company, epp_ready_upload_docs_serializer.data, request)
            set_epp_ready_step(user_company, step=EppReadyFlow.EppReadyFlowStep.CONNECT_BANK_ACCOUNT)

            response_data = combine_update_response(user_company)
        return Response(data=response_data, status=status.HTTP_200_OK)


# service.py
def update_or_create_invoice_for_epp_ready_flow(request, raw_data: dict, partial_update: bool = False) -> "Invoice":
    from payments.models import Invoice
    from payments.serializers import InvoiceSerializer

    invoice_uuid = raw_data.get("invoice_uuid")
    if partial_update and not invoice_uuid:
        return Invoice.objects.none().first()

    invoice_data = {
        "number": raw_data.get("invoice_number"),
        "billing_from": raw_data.get("billing_from"),
        "billing_to": raw_data.get("billing_to"),
        "amount": raw_data.get("invoice_amount"),
        "summary_file": raw_data.get("invoice_file"),
        "project": raw_data.get("project"),
        "subcontractor": request.user.selected_membership.company_id,
        "status": Invoice.APPROVED,
    }

    initial_invoice = Invoice.objects.filter(id=invoice_uuid).first()

    if initial_invoice:
        clean_data = clean_dict_from_none(invoice_data)

        invoice_serializer = InvoiceSerializer(
            initial_invoice,
            data=clean_data,
            context={"request": request, "is_invoice_for_epp": True},
            partial=True,
        )
    else:
        invoice_serializer = InvoiceSerializer(
            data=invoice_data,
            context={"request": request, "is_invoice_for_epp": True},
        )

    invoice_serializer.is_valid(raise_exception=True)
    invoice = invoice_serializer.save()

    return invoice


def set_invoice_in_epp_ready_flow(company: "Company", invoice: "Invoice") -> None:
    EppReadyFlow.objects.update_or_create(
        company=company,
        defaults={"invoice": invoice},
    )


def update_company_profile(company: "Company", company_profile_data: dict, request: Request) -> None:
    profile_serializer = company.company_profile_serializer(
        company.contractor,
        data=company_profile_data,
        context={"request": request},
        partial=True,
    )
    profile_serializer.is_valid(raise_exception=True)
    profile_serializer.save()


def update_company_prequal_section(company: "Company", raw_data: dict, partial_update: bool = False) -> None:
    from constrafor.serializers.company.company_prequal_section import CompanyPrequalSectionSerializer

    prequal_data = {
        "work_in_progress": raw_data.get("work_in_progress"),
        "company": company.id,
    }
    prequal_section, _ = CompanyPrequalSection.objects.get_or_create(company=company)

    if partial_update:
        prequal_data = clean_dict_from_none(prequal_data)
    company_prequal_section_serializer = CompanyPrequalSectionSerializer(
        prequal_section,
        data=prequal_data,
        partial=True,
    )
    company_prequal_section_serializer.is_valid(raise_exception=True)
    company_prequal_section_serializer.save()


def update_financial_documents(user_company: "Company", raw_data: dict, request: Request) -> None:
    from epp.serializers.epp_ready_flow import FinancialDocumentUpdateSerializer

    epp_subcontractor = SubContractor.objects.filter(constrafor_company=user_company).first()
    if not epp_subcontractor:
        raise ValueError("There is no EPP Subcontractor for the current user company.")

    company_fin_docs = FinancialDocument.objects.filter(subcontractor=epp_subcontractor)
    for doc_data in raw_data.get("financial_documents"):
        # validate incoming data
        cleaned_data = clean_dict_from_none(doc_data)
        financial_documents_serializer = FinancialDocumentUpdateSerializer(
            data=cleaned_data,
            context={"request": request, "epp_subcontractor": epp_subcontractor},
        )
        financial_documents_serializer.is_valid(raise_exception=True)
        valid_doc_data = financial_documents_serializer.validated_data

        # try to find existing finance data by file
        financial_doc_instance = company_fin_docs.filter(file=valid_doc_data["file"]).first()

        if financial_doc_instance:
            # change smth in existing financial document and we have no constraints for that
            # otherwise serialiser Validation Error would be raised
            for attr, value in valid_doc_data.items():
                setattr(financial_doc_instance, attr, value)
            financial_doc_instance.save()
            continue

        # either to change the file in existing entity or create a new entity
        # find the same constraint and change file
        existing_fin_doc = company_fin_docs.filter(
            document_type=valid_doc_data["document_type"],
            financial_year=valid_doc_data["financial_year"],
            financial_month=valid_doc_data["financial_month"],
            financial_quarter=valid_doc_data["financial_quarter"],
        ).first()

        if existing_fin_doc:
            # 1 if there is an entity without the file, but with the same constraint - update file
            existing_fin_doc.file = valid_doc_data["file"]
            existing_fin_doc.save()
        else:
            # 2 if the set of fields is unique - create a new entity
            FinancialDocument.objects.create(**valid_doc_data)


def set_epp_ready_step(
    company: "Company",
    step: EppReadyFlow.EppReadyFlowStep,
) -> EppReadyFlow:
    epp_ready_flow, _ = EppReadyFlow.objects.update_or_create(
        company=company,
        defaults={
            "current_step": step,
        },
    )
    return epp_ready_flow


def combine_update_response(user_company: "Company") -> dict:
    epp_subcontractor = SubContractor.objects.filter(constrafor_company=user_company).first()

    epp_ready_flow_obj = EppReadyFlow.objects.filter(company=user_company).first()
    epp_ready_flow_data = {}

    invoice = epp_ready_flow_obj.invoice
    invoice_data = {
        "project": invoice.project_id,
        "invoice_uuid": invoice.id,
        "invoice_amount": invoice.amount,
        "invoice_number": invoice.number,
        "invoice_file": invoice.summary_file.uuid,
        "billing_from": invoice.billing_from,
        "billing_to": invoice.billing_to,
    }

    company_profile_data = {
        "w9_form": [w9_form.uuid for w9_form in user_company.w9_form.all()],
    }

    company_prequal_section = user_company.prequal_section
    company_prequal_section_data = {
        "work_in_progress": [wip.uuid for wip in company_prequal_section.work_in_progress.all()],
    }

    financial_documents = epp_subcontractor.financial_documents.exclude(
        Q(financial_year__lt=FinancialDocument.UNDEFINED_PERIOD)
        | Q(financial_quarter__lt=FinancialDocument.UNDEFINED_PERIOD)
        | Q(financial_month__lt=FinancialDocument.UNDEFINED_PERIOD)
    )

    financial_documents_data = {
        "financial_documents": [
            {
                "financial_year": fin_doc.financial_year,
                "financial_month": fin_doc.financial_month,
                "financial_quarter": fin_doc.financial_quarter,
                "document_type": fin_doc.document_type,
                "file": fin_doc.file.uuid,
                "subcontractor": fin_doc.subcontractor.id,
            }
            for fin_doc in financial_documents
        ]
    }
    epp_ready_flow_data.update(invoice_data)
    epp_ready_flow_data.update(company_profile_data)
    epp_ready_flow_data.update(company_prequal_section_data)
    epp_ready_flow_data.update(financial_documents_data)

    return epp_ready_flow_data
