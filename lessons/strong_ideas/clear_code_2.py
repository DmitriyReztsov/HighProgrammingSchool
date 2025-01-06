# 1. Методы, который используются только в тестах.
# В рабочем проекте таких примеров не нашел. Возможная ситуация - методы, создающие набор объектов для тестирования
# и заполнения базы данных.
class Document(Model):
    ...

    def fill_data_base(self): ...


# возможное решение - создать базовый тестовый класс с методом-фабрикой, который будет создавать объекты той модели,
# которую в него передадим.
class BaseTest(TestCase):
    def create_objects(self, for_model, *args, **kwargs):
        for_model.objects.create(args, kwargs)


# 2. Цепочки методов. Первая итерация метода post() была написана так, что цепочкой методов формировала ответ.
class EppReadyUploadDocsStepView(viewsets.ViewSet):
    ...
    def post(self, request, *args, **kwargs):
        user_company = request.user.selected_membership.company
        with transaction.atomic():
            response_data = combine_upload_documents_response(user_company, request.data)
        return Response(data=response_data, status=status.HTTP_201_CREATED)


# и далее в сервисах передавались излишние данные
def combine_upload_documents_response(user_company: "Company", request_data: dict) -> dict:
    response_dict = {}
    invoice = update_or_create_invoice_for_epp(request_data)
    response = add_invoice_to_response(invoice, user_company, request_data, response_dict)
    return response


def add_invoice_to_response(invoice, user_company, request_data, response_dict):
    if invoice:
        invoice_data = {
            "project": invoice.project_id,
            "invoice_uuid": str(invoice.id),
            "invoice_amount": invoice.amount,
            "invoice_number": invoice.number,
            "invoice_file": invoice.summary_file.uuid if invoice.summary_file else None,
            "billing_from": invoice.billing_from,
            "billing_to": invoice.billing_to,
        }
        response_dict.update(invoice_data)
    response = add_company_profile_to_response(user_company, request_data, response_dict)
    return response


def add_company_profile_to_response(user_company, request_data, response_dict):
    company_profile_data = {
        "w9_form": [w9_form.uuid for w9_form in user_company.w9_form.all()],
    }
    response_dict.update(company_profile_data)
    ...
    return response
...


def update_or_create_invoice_for_epp(request_data: dict) -> Optional["Invoice"]:
    ...
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


def clean_dict_from_none(data: dict) -> dict:
    cleaned_data = {}
    for key, value in data.items():
        if value is not None:
            cleaned_data[key] = value
    return cleaned_data


# на этапе отладки функционал был переписан в более декларативной манере, управляя изменениями и созданием записей
# непосредственно из начального метода, что повысило читаемость и понимание, что происходит, из одного места
class EppReadyUploadDocsStepView(viewsets.ViewSet):
    ...
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

            modified_request_data = set_previous_and_current_year_in_bank_statements_by_current_date(request.data)
            financial_documents_serializer = EppReadyFlowFinancialDocumentsSubmitSerializer(
                data=modified_request_data, context={"user_company": user_company, "request": request}
            )
            financial_documents_serializer.is_valid(raise_exception=True)
            financial_documents_data = financial_documents_serializer.data

            project_serializer = EPPReadyFlowProjectUpdateSerializer(data=request.data)
            project_serializer.is_valid(raise_exception=True)
            project_data = project_serializer.data

            invoice = update_or_create_invoice_for_epp(request, invoice_data)

            update_company_profile(user_company, company_profile_data, request)
            update_company_prequal_section(user_company, company_prequal_section_data)
            update_financial_documents(user_company, financial_documents_data, request)

            attrs_for_epp_ready_flow = {"current_step": EppReadyFlow.EppReadyFlowStep.CONNECT_BANK_ACCOUNT}
            if invoice:
                attrs_for_epp_ready_flow.update({"invoice": invoice})
            if project_id := project_data.get("project"):
                attrs_for_epp_ready_flow.update({"project_id": project_id})
            set_attrs_in_epp_ready_flow(user_company, attrs_for_epp_ready_flow)

            add_epp_manager_group_for_membership(request.user.selected_membership)

            response_data = combine_upload_documents_response(user_company, invoice, project_data)
        return Response(data=response_data, status=status.HTTP_201_CREATED)


# 3. У метода слишком большой список параметров
class MailService:
    @staticmethod
    def send_email_wrapper(
        template_identifier: str,
        to: Membership | QuerySet[Membership] | str | list | tuple | set,
        trial_mode_on: bool,
        stop_all_notifications: bool,
        email_type: str = None,
        dataset: dict | None = None,
        subject: str = None,
        ignore_user_settings: bool = False,
        cc: Membership | QuerySet[Membership] | str | list | tuple | set | None = None,
        attachment=None,
        reminder=False,
        branding_company=None,
        merge_metadata=None,
        **kwargs,
    ) -> None: ...


# можно было бы свести все настройки либо в объект дата-класса, либо в словарь. И передавать в двух переменных
# предварительно преобразовав объект датакласса в словарь и дальше уже распаковывать и работать с переменными.
@dataclass
class MailingSettings:
    trial_mode_on: bool
    stop_all_notifications: bool
    ignore_user_settings: bool = False
    reminder: bool = False
    branding_company: bool = False


@dataclass
class LetterAttributes:
    template_identifier: str
    to: Membership | QuerySet[Membership] | str | list | tuple | set
    email_type: str = None
    dataset: dict | None = None
    subject: str = None
    cc: Membership | QuerySet[Membership] | str | list | tuple | set | None = None
    attachment: File = None
    merge_metadata: dict = None


class MailService:
    @staticmethod
    def send_email_wrapper(
        letter_attributes: dict,
        mailing_settings: dict,
        **kwargs,
    ) -> None: ...


# 4. Странные решения.
# есть ряд функций, работающих с пдф-файлами, объединяющими их в один файл. Дополнительно потребовался целый сервис
# для работы с пдф-файлами: создание пдф из текста, html, добавление коллонтитулов к существующим пдф. Хоть это и не
# совсем одно и тоже на уровне реализации, но логично было бы дополнить сервис методами работы с объединением пдф и 
# заменить код отдельных функций
def merge_to_pdf(files: List, created_by: User, merged_name: str) -> Optional[File]:
    buffer = BytesIO()
    merger = PdfMerger()
    merged_filename = f"{merged_name}.pdf"
    try:
        for file in files:
            try:
                merger.append(determine_handler(file)(file))
            except (PyPdfError, ValueError):
                return None
        try:
            merger.write(buffer)
        except (PyPdfError, ValueError):
            return None
    finally:
        merger.close()
    buffer.seek(0)
    merged_file = File.objects.create(
        file=DjangoFile(buffer, merged_filename),
        name=merged_filename,
        created_by=created_by,
    )
    return merged_file


def merge_to_zip(files: List, created_by: User, merged_name: str) -> Optional[File]:
    merged_filename = f"{merged_name}.zip"
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zip:
        if settings.BUILD_ENV == "local":
            for file in files:
                zip.write(file, os.path.basename(file))
        else:
            for file in files:
                pdf_content, ok = get_request(file)
                if not ok:
                    return None
                pdf_buffer = BytesIO(pdf_content)
                file_name = get_filename_from_url(file)
                zip.writestr(file_name, pdf_buffer.getvalue())
    merged_file = File.objects.create(
        file=DjangoFile(buffer, merged_filename),
        name=merged_filename,
        created_by=created_by,
    )
    return merged_file


class ToPdfService:
    ...
    def merge_to_pdf(self, ...): ...
    def merge_to_zip(self, ...): ...


def get_merged_or_zip_(document: DocumentProject) -> File:
    ...
    files, to_zip = gather_files_list(files_list)
    ...
    if not to_zip:
        # to_return = merge_to_pdf(files, document.created_by, merged_name)  БЫЛО
        to_return = ToPdfService.merge_to_pdf(...)

    if to_return is None:
        # to_return = merge_to_zip(files, document.created_by, merged_name)  БЫЛО
        to_return = ToPdfService.merge_to_zip(...)

    return to_return


# 5. Чрезмерный результат.
# В тестовых классах используется метод create_account(), который возвращает аккаунт (юзера) и мембершип (связь юзера с
# конкретной компанией, поскольку юзер может работать в нескольких компаниях). В тестах обычно, если не нужен был мембершип,
# то его сливали в переменную _
class ConstraforTestCase(APITestCase, MockedHelpersMixin):
    ...
    @classmethod
    def create_account(cls, email=None, **kwargs):
        account, membership = cls._create_account(email, **kwargs)
        return account, membership
    

user, _ = self.create_account()


# логичное решение разделить методы
class ConstraforTestCase(APITestCase, MockedHelpersMixin):
    ...
    @classmethod
    def create_account(cls, email=None, **kwargs):
        account, _ = cls._create_account(email, **kwargs)
        return account

    @classmethod
    def create_account_with_membership(cls, email=None, **kwargs):
        account, membership = cls._create_account(email, **kwargs)
        return account, membership
