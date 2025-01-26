# 1. все три правила:
# - избавляться от точек генерации исключений - был словарь в качестве сеттингов, проверка содержимого
# осуществлялась внутри класса. Введением отдельного класса мы передаем эту проверку на уровень генерации
# такого объекта.
# - отказаться от дефолтных конструкторов без параметров и передавать конструктору обязательные аргументы;
# - избегать увлечения примитивными типами данных. Словарь преобразован в объект настроек.
# Было
class TextToPdf(PageSettingsGeneral, ObjToPdf):
    def __init__(self, text_blocks: list[str], text_settings: dict | None = None) -> None:
        self.trimmed_text_blocks: list[str] = []
        self._trim_text_blocks(text_blocks)
        if text_settings:
            for attr_name, attr_value in text_settings.items():
                setattr(self, attr_name, attr_value)
        else:
            self._set_text_settings()


# Можно улучшить, применив датакласс с приемом только именованных аргументов
@dataclass(kw_only=True)
class PageSettings:
    DEFAULT_FONT: str = "Times-Roman"
    DEFAULT_FONT_SIZE: int = 9
    DEFAULT_BOTTOM_MARGIN: float = 1 * inch
    DEFAULT_LEFT_MARGIN: float = 0.75 * inch
    DEFAULT_RIGHT_MARGIN: float = 0.5 * inch
    PARAGRAPH_VERT_SPACE: float = 0.1 * inch
    DEFAULT_FIRST_LINE_INDENT: float = 0.2 * inch
    DEFAULT_PAGE_SIZE: tuple[float, float] = A4
    DEFAULT_TOP_MARGIN: float = 0.5 * inch


DEFAULT_PAGE_SETTINGS = PageSettings()


class TextToPdf(PageSettingsGeneral, ObjToPdf):
    def __init__(self, text_blocks: list[str], text_settings: PageSettings = DEFAULT_PAGE_SETTINGS) -> None:
        self.trimmed_text_blocks: list[str] = []
        self._trim_text_blocks(text_blocks)
        self._set_text_settings(text_settings)


# 2. Первое правило. Есть модель Workflow, описывающая процесс согласования документа. Внутри нее есть
# шаги (модель Step), которая описывает конктретного юзера, ответственного за согласование на данном шаге.
# Вместо того, чтобы явно вызывать метод конкретного шага и следить за порядком вызовов это все делегировано
# классу, который внутри себя хранит порядок юзеров и последовательно вызывает шаги после завершения текущего
class Workflow(models.Model):
    ...

    def start(self):
        first_step = self.steps.first()
        first_step.request_action()
        self.progress = self.Progress.IN_PROGRESS
        self.save(update_fields=["progress"])

    def finish(self, *args, **kwargs):
        self.progress = self.Progress.FINISHED
        self.save(update_fields=["progress"])

    def reset(self):
        for step in self.steps.all():
            step.status = WorkflowStep.StepStatus.ASSIGNED
            step.save(update_fields=["status"])


class WorkflowStep(models.Model):
    ...

    def request_action(self):
        """Request approval for assignee, change status from ASSIGNED to PENDING"""
        ...

    def skip(self, user):
        ...
        self.to_next_step(user)

    def reject(self, user):
        ...
        self.workflow.finish(
            user,
            status=status_correspondence.get(type(self.workflow)),
            after_edition=(self.subtype == self.StepType.REVIEW_EDITION),
        )

    def complete(self, user):
        ...
        self.to_next_step(user)

    def to_next_step(self, user):
        try:
            next_step = self.get_next_in_order()
            next_step.request_action()
        except WorkflowStep.DoesNotExist:
            self.workflow.finish(user, after_edition=(self.subtype == self.StepType.REVIEW_EDITION))


# 3. Второе правило - явное указание параметров в конструкторе. Тут я отказался от дефолтных значений, таким образом
# заставляя в будущем явно прописывать те или иные настройки, чтобы не забыть. При этом в модуле есть дефолтные
# настройки страницы. Нужно только их указать.
class ToPDFService(PageSettingsGeneral):
    def __init__(
        self,
        to_pdf_obj: ObjToPdf,
        file_name: str,
        created_by: User,
        doc_settings: PageSettings,
    ) -> None:
        self.to_pdf_obj = to_pdf_obj
        self.file_name = file_name
        self.created_by = created_by
        self._set_doc_settings(doc_settings)


# 4. Правило третье - избегать примитивных типов данных. Еще один класс я написал под впечатлением от этого правила для
# маппинга переменных, которые надо прописать в файле на обозначенные места. Плюс второе правило - без этого маппинга
# класс не инициализируется.
@dataclass(kw_only=True)
class LedgerToSummaryVariables:
    net_funding_amount: int
    advance_rate: float
    payment_term: int


class TextRenderService:
    """Inserted variables should be surrounded by double square quotes and be a single word with underscore in place of
    spaces

    "Text before variable [[net_funding_amount]] text after variable"
    """

    def __init__(self, initial_text: str, variables_mapping: LedgerToSummaryVariables) -> None:
        self.template_text: str = initial_text
        self.rendered_text: str = initial_text
        self.variables_mapping = asdict(variables_mapping)


# 5. Что-то похожее на правило три, про оборачивание примитивных типов данных, можно наблюдать в полях моделей Джанго.
# Например, тут примитив int дополняется валидатором и становится типом данных, характеризаующимся минимальным (0) и
# максимальным значением. Таким образом в поле amount уже не получится занести просто какое-то произвольное число
class DocumentProject(Document, WorkflowCommonModelPropertiesMixin):
    ...
    amount = models.PositiveBigIntegerField(
        null=True, blank=True, help_text="Contract amount in cents", validators=[MaxValueValidator(50000000000)]
    )


# 6. Певое правило - исключать точки генерации исключений на уровне интерфейсов. Теоретически мы можем брать стороны
# договора из самого договора, но надежнее явно прописывать их при инициализации объекта класса. Это может быть связано,
# например, с ограничениями в правах и доступах, или с внутренними регламентами компании
class Contract:
    def __init__(self, contract_params: dict, signer_1: User, signer_2: User):
        pass
