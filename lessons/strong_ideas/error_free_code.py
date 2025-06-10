# 1
"""Есть метод во вью, который подписывает документ, предварительно проверяя наличие signature_request.
Можно перед подписанием через фабрику создать объект сервисного класса для одного состояния документа из:
- неподписанный документ
- подписанный одной стороной
- подписанный обеими стронами (активный документ)
и вызывать метод, например, .perform_next_sign_step(), который в разных состояних будет делать разные операции
"""


# текущий код
@action(detail=True, methods=["put"])
def sign(self, request, *args, **kwargs):
    document = self.get_object()
    user = self.request.user
    signer_is_counterpart = user.selected_membership.company_id == document.counterpart_id
    signer_is_gc = user.selected_membership.company_id == document.created_by_company_id

    ...

    signature_request = sign_service.get_or_create_signature_request()

    sign_url = sign_service.get_user_signature_url(signature_request)
    if sign_url:
        DocumentProjectConfirmationLog.create_confirmation_log(self.request, document)
        return Response({"url": sign_url})
    return Response(
        {"message": "Signature request already signed"},
        status=status.HTTP_400_BAD_REQUEST,
    )


# возможный код
class DocumentStateFabric:
    """на основе данных из БД определяем текущее состояние документа"""

    def __init__(self, document):
        if document.status == "sent":
            return NotSignedDocumentState(document)
        if document.status == "signed":
            return SignedDocumentState(document)
        if document.status == "active":
            return ActiveDocumentState(document)


class NotSignedDocumentState:
    def __init__(self, document):
        self.document = document

    def perform_next_sign_step(self):
        """создаем signature_request и получаем подпись контрагента"""
        signature_request = self.document.sign_service.create_signature_request()
        return self.document.sign_service.get_other_user_signature_url(signature_request)

    def get_signature_request(self):
        return None


class SignedDocumentState:
    def __init__(self, document):
        self.document = document

    def perform_next_sign_step(self):
        """получаем созданный signature_request и получаем подпись стороны - владельца контракта"""
        signature_request = self.document.sign_service.get_signature_request()
        return self.document.sign_service.get_current_user_signature_url(signature_request)

    def get_signature_request(self):
        return self.document.signature_request


class ActiveDocumentState:
    def __init__(self, document):
        self.document = document

    def perform_next_sign_step(self):
        return None

    def get_signature_request(self):
        return self.document.signature_request


"""тогда во вью мы можем просто создать то или иное состояние документа и взвать соответствующий метод.
Если вдруг кто-то попробует обратиться на этот ендпойнт с активным документом - вернется ошибка в лог о невозможности
подписать уже подписанный документ"""


@action(detail=True, methods=["put"])
def sign(self, request, *args, **kwargs):
    document = self.get_object()
    document_state = DocumentStateFabric(document)

    ...

    sign_url = document_state.perform_next_sign_step()
    if sign_url:
        DocumentProjectConfirmationLog.create_confirmation_log(self.request, document)
        return Response({"url": sign_url})
    return Response(
        {"message": "Signature request already signed"},
        status=status.HTTP_400_BAD_REQUEST,
    )


# 2
"""Этот же документ до подписания проходит через ряд статусов, в каждом из которых он доступен или нет для правок с
той или иной стороны. Этот функционал тоже можно было бы оформить в виде состояний."""


class IDocumentState(ABC):
    def send(self):
        raise NotImplementedError

    def edit_by_self(self):
        raise NotImplementedError

    def edit_by_counterpart(self):
        raise NotImplementedError

    def approve_wokflow_step(self):
        raise NotImplementedError

    def set_next_status(self, status):
        raise NotImplementedError

    ...


class DraftDocumentState(IDocumentState):
    AVAILABLE_NEXT_STATUSES = [
        "sent",
        "rejected",
    ]

    def edit_by_self(self): ...

    def approve_wokflow_step(self):
        ...
        if approve:
            self.send_document()
        else:
            self.set_next_status("rejected")
        ...

    def set_next_status(self, status):
        self.status = status
        # плюс логика проверок готовности документа и сохранения его в БД

    def send_document(self):
        """метод, доступный только для документа в статусе draft"""
        ...
        self.set_next_status("sent")


class SentDocumentStatus(IDocumentState):
    AVAILABLE_NEXT_STATUSES = [
        "edited",
        "signed",
    ]

    def edit_by_counterpart(self):
        ...
        self.set_next_status("edited")

    def set_next_status(self, status):
        self.status = status

    def sign_document(self):
        ...
        self.set_next_status("signed")

    ...


"""в целом, думая над подобным подходом, вижу, что многих if...else блоков и мелких сервисных функций можно было бы
избежать, изолировав логику работ с каждым статусом в своем классе."""

# 3
"""Есть модель, описыывающая набор статусов компании-сабконтрактора. По сути - это уже состояние этой компании, 
хранимое в БД. Можно было бы подумать о том, чтоб сразу хранить их в разных таблицах, но не уверен, что это удобное
решение. Пока можно просто на стороне сервисного слоя собрать из полей этой модели состояние компании"""


class SubcontractorStageStatus(CoreModelMixin):
    ONBOARDING = "onboarding"
    UNDERWRITING = "underwriting"
    READY = "ready"
    STAGE_CHOICES = [
        (ONBOARDING, ONBOARDING),
        (UNDERWRITING, UNDERWRITING),
        (READY, READY),
    ]

    ONBOARD_IN_PROCESS = "in_process"
    ONBOARD_COMPLETED = "completed"
    ONBOARD_STOPED = "stopped"
    UNDERWRITE_IN_QUEUE = "in_queue"
    UNDERWRITE_UNDER_REVIEW = "in_review"
    UNDERWRITE_APPROVED = "approved"
    UNDERWRITE_REJECTED = "rejected"
    READY_OK = "ok"
    READY_DELINQUENT = "delinquent"
    READY_DEFAULTED = "defaulted"
    STATUS_CHOICES = [
        (ONBOARD_IN_PROCESS, ONBOARD_IN_PROCESS),
        (ONBOARD_COMPLETED, ONBOARD_COMPLETED),
        (ONBOARD_STOPED, ONBOARD_STOPED),
        (UNDERWRITE_IN_QUEUE, UNDERWRITE_IN_QUEUE),
        (UNDERWRITE_UNDER_REVIEW, UNDERWRITE_UNDER_REVIEW),
        (UNDERWRITE_APPROVED, UNDERWRITE_APPROVED),
        (UNDERWRITE_REJECTED, UNDERWRITE_REJECTED),
        (READY_OK, READY_OK),
        (READY_DELINQUENT, READY_DELINQUENT),
        (READY_DEFAULTED, READY_DEFAULTED),
    ]

    STAGE_STATUSES_CORRESPONDANCE = {
        ONBOARDING: [ONBOARD_IN_PROCESS, ONBOARD_COMPLETED, ONBOARD_STOPED],
        UNDERWRITING: [UNDERWRITE_IN_QUEUE, UNDERWRITE_UNDER_REVIEW, UNDERWRITE_APPROVED, UNDERWRITE_REJECTED],
        READY: [READY_OK, READY_DELINQUENT, READY_DEFAULTED],
    }

    subcontractor = models.ForeignKey("epp.SubContractor", related_name="stage_status", on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=12, choices=STAGE_CHOICES, default=ONBOARDING)
    stage_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ONBOARD_IN_PROCESS)
    reason_note = models.TextField(blank=True, null=True)


"""Для разных состояний будут применимы разные действия над изменением статусов и запросами документов. Можно во вью
также реализовать фабрику по сборке объекта состояния и в дальнейшем вызывать методы, присущие тем или иным 
состояниям"""


class SubcontractorStageState:
    def __init__(self): ...


class IStageState(ABC):
    def set_next_stage(self):
        """установка аттрибутов, характиризующих следующее состояние"""
        raise NotImplementedError

    def request_documents(self):
        raise NotImplementedError

    def is_ready_to_fund(self):
        raise NotImplementedError


class OnbordingState(IStageState):
    REQUIRED_DOCUMENTS = [
        ...  # список категорий документов, по которому можно проверить наличие загруженных документов
    ]

    def request_documents(self): ...

    def set_next_stage(self): ...

    def is_ready_to_fund(self):
        return False


class UnderwritingState(IStageState):
    REQUIRED_DOCUMENTS = [
        ...  # список категорий документов, по которому можно проверить наличие загруженных документов
    ]

    def request_documents(self): ...

    def set_next_stage(self): ...

    def is_ready_to_fund(self):
        return False


class ReadyState(IStageState):
    def request_documents(self):
        raise NotImplementedError

    def set_next_stage(self):
        raise NotImplementedError

    def is_ready_to_fund(self):
        return True

    def get_provided_documents(self): ...
