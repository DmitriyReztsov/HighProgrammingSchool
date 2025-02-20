#1. написал такую функцию в небольшом проекте, где от легаси тянется проверка входных данных подобным образом.
# конечно же это надо переносить на уровень выше - в сериализатор, где описание полей можно считать за типы данных со своими валидаторами, которые на этапе запроса уже не допустят входа неправильных данных
# Было
def validate_uploaded_document_bytes(data: dict) -> None:
    match data:
        case {
            "document_uuid": document_uuid,
            "host": api_host,
            "file_type": extension,
            "original_document_bytes": original_document_bytes,
            **reminder,
        } if (
            not reminder
            and isinstance(document_uuid, str)
            and isinstance(api_host, str)
            and isinstance(extension, str)
            and isinstance(original_document_bytes, str)
        ):
            return
        case _:
            raise ValidationError("Wrong uploaded data")

# Стало
class CreateDocumentFromBytes(serializers.Serializer):
    document_uuid = serializers.UUIDField(format='hex_verbose')
    host = serializers.URLField(max_length=200, min_length=None, allow_blank=False)
    file_type = serailizers.CharField(max_length=3)
    original_document_bytes = Base64FileField()  # from drf-extra-fields
# в общем, по проекту есть несколько таких однотипных мест, которые надо переписать на нормальные сериалайзеры


#2. функция формировала словарь с определенным набором полей
def get_variables_mapping_from_ledger(ledger: Ledger) -> dict:
    net_funding_amount = ledger.net_funding_amount / 100 if ledger.net_funding_amount else 0
    advance_rate = ledger.advance_rate if ledger.advance_rate else 0
    payment_term = ledger.payment_term if ledger.payment_term else 0
    supplier = ledger.epp_request.supplier.name if ledger.epp_request.supplier else ""
    return {
        "net_funding_amount": net_funding_amount,
        "advance_rate": advance_rate,
        "payment_term": payment_term,
        "supplier": supplier,
    }

# ввел датакласс, который бы проверял сам значения + сделал функцию по пересчету центов в доллары, которая возвращала бы 0, если бы в нее заходил None
@dataclass(kw_only=True)
class LedgerToSummaryVariables:
    net_funding_amount: int
    advance_rate: float
    payment_term: int
    supplier: str = ""


def get_variables_mapping_from_ledger(ledger: Ledger) -> LedgerToSummaryVariables:
    return LedgerToSummaryVariables(
        net_funding_amount=get_dollar_amount_from_cents(ledger.net_funding_amount),
        advance_rate=ledger.advance_rate,
        payment_term=ledger.payment_term,
        supplier=ledger.epp_request.supplier.name if ledger.epp_request.supplier else None,
    )


#3. похожую задачу решает Pydantic, когда проверяет типы поступивших значений. Например, если бы было так:
class TexturaScrapper:
    ...
    def _validate_data(self, data: dict) -> None:
        validated_data = None

        if not isinstance(data.get("deactivated"), bool):
            raise ValidationError(...)
        if not isinstance(data.get(editUserUrl), (str, None)):
            raise ValidationError(...)
        ...

# то можно было бы делегировать проверку типов модели Pydentic
class TexturaProjectParticipant(BaseModel):
    deactivated: bool
    editUserUrl: str | None
    email: str
    fullName: str
    jobTitle: str
    orgUrl: str
    organizationName: str
    organizationRoles: list[int]
    phone: str | None


class TexturaScrapper:
    def _validate_data(self, data: dict, model: TexturaProjectParticipant) -> TexturaProjectParticipant | None:
        validated_data = None

        try:
            validated_data = model(**data)
        except ValidationError as ex:
            extra = dict(
                contractor_id=self.contractor.id,
                error_message=ex,
            )
            logger.error(
                "An error occurred during the validate parsed data from Textura",
                extra=extra,
                exc_info=True,
                stack_info=True,
            )
            raise ex
        return validated_data
# во всех этих случаях требования к состоянию данных, которые передаются, могут быть получены клиентом из того же сваггера, который формирует документацию на основе моделей пайдентика или сериалайзера джанги.

#4. При создании записи необходимо убеждаться, что контракт пришел с нужной категорией.
class OfferSummaryContractViewSet(...):
    ...
    def perform_create(self, serializer):
        with transaction.atomic():
            current_user = self.request.user
            epp_contract = serializer.validated_data.get("epp_contract")
            if epp_contract.category.name != self.EPP_CONTRACT_CATEGORY:
                raise ValueError("epp_contract should be DocumentProject instance with EPP Contract category")
            ...  # ряд вызовов функций, нужных для обработки контакта
        return os_contract
    
# перенес проверку и весь функционал в сервис
class AppendixServiceAbstract(ABC):
    EPP_CONTRACT_CATEGORY = EPP_CONTRACT_CATEGORY_NAME
    APPENDIX_REGEX = APPENDIX_REGEX

    # to be defined in concrete classes
    PDF_FILE_NAME_PREFIX = ""
    RELATED_NAME = ""

    def __init__(self, epp_contract: DocumentProject):
        if epp_contract.category.name != self.EPP_CONTRACT_CATEGORY:
            raise ValueError("epp_contract should be DocumentProject instance with EPP Contract category")
        self.epp_contract = epp_contract
        self.template_variables = self._set_template_variables()
        self.template = self._set_template(epp_contract)
        self.document = Document()


class OfferSummaryContractViewSet(...):
    def perform_create(self, serializer):
        with transaction.atomic():
            current_user = self.request.user
            epp_contract = serializer.validated_data.get("epp_contract")
            os_service = OfferSummaryService(epp_contract)
            os_template: DocumentTemplate = os_service.get_template()
            os_contract: OfferSummaryContract = serializer.save(
                created_by=current_user, updated_by=current_user, template=os_template
            )
            os_service.create_pdf_file_from_template(os_contract)
        return os_contract
# Питон не обращает внимание на типы в рантайме, но при проверке mypy несоответствие (если где-то будет попытка передать иной тип документа) будет подсвечено + сама проверка перемещена в тип данных сервиса


#5. Так же в сервис перемещане проверка контракта для выбора шаблона приложения
class OfferSummaryContractViewSet(...):
    ...
    def perform_create(self, serializer):
        with transaction.atomic():
            ...
            active_templates = DocumentTemplate.objects.filter(google_file_deleted=False)
            match epp_contract:
                case DocumentProject(epp=EPPRequest(supplier=supplier)) if supplier is not None:
                    return active_templates.filter(category__name=OFFER_SUMMARY_SUPPLIER).first()
                case DocumentProject(
                    epp=EPPRequest(ledger=Ledger(cross_collateralization=cross_collateralization))
                ) if cross_collateralization:
                    return active_templates.filter(category__name=OFFER_SUMMARY_ROLLOVER).first()
                case DocumentProject():
                    return active_templates.filter(category__name=OFFER_SUMMARY_GENERIC).first()
                case _:
                    raise ValueError("epp_contract should be DocumentProject instance.")
        return os_contract
    
# стало
class OfferSummaryService(AppendixServiceAbstract):
    PDF_FILE_NAME_PREFIX = OFFER_SUMMARY_PREFIX_FILE_NAME
    RELATED_NAME = OFFER_SUMMARY_RELATED_NAME

    def _set_template(self, epp_contract: DocumentProject) -> DocumentTemplate:
        active_templates = DocumentTemplate.objects.filter(google_file_deleted=False)
        match epp_contract:
            case DocumentProject(epp=EPPRequest(supplier=supplier)) if supplier is not None:
                return active_templates.filter(category__name=OFFER_SUMMARY_SUPPLIER).first()
            case DocumentProject(
                epp=EPPRequest(ledger=Ledger(cross_collateralization=cross_collateralization))
            ) if cross_collateralization:
                return active_templates.filter(category__name=OFFER_SUMMARY_ROLLOVER).first()
            case DocumentProject():
                return active_templates.filter(category__name=OFFER_SUMMARY_GENERIC).first()
            case _:
                raise ValueError("epp_contract should be DocumentProject instance.")
