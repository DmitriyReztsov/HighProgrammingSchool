# 2.1. большой класс, изначально (в рамках концепции тонкой модели) предназначенный для работы с базой данных
# затем разросся до монстра, в которого впихнули кучу сервисных методов.
class DocumentProject(models.Model):
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
    status_updated_at = models.DateTimeField(auto_now_add=True, null=True)
    ...  # другие поля модели

    @classmethod
    def from_db(cls, db, field_names, values): ...

    def save(self, force_insert=False, force_update=False, *args, **kwargs): ...

    def execute_contract(self, user): ...

    def send_contract(self, init_log_data: None | dict = None, send_notification: bool = True) -> None: ...

    def set_status(self, status): ...

    def get_view_document_url(self, company_id): ...

    def create_authenticated_code_url(self, user, company): ...

    @staticmethod
    def get_related_roles_by_sub_side(): ...

    @staticmethod
    def get_related_roles_by_gc_side(): ...

    def get_uploaded_files(self): ...

    def get_subfolder_path(self): ...

    def send_reminder(self, automatic_reminder: bool = False) -> None: ...

    @cached_property
    def subcontractor_has_approved_coi(self): ...

    @cached_property
    def subcontractor_has_uploaded_coi(self): ...

    def get_counterpart_name(self): ...

    @cached_property
    def created_by_sub(self): ...


# в текущем проекте мы не создаем при обработке каждого конкретного запроса больше одного инстанса той модели,
# на которую направлен запрос. Но если мы получим какой-то список для инициализации какого-то класса и создадим много
# инстансов для последующей обработки - то это может негативно сказаться на памяти, поскольку все эти объекты будут
# храниться одновременно. В условиях Питона - неоптимизированно. С т.з. ясного кода эти все объекты, скорее всего,
# получат имена с индексами или будут храниться и обрабатываться в коллекциях через циклы и условные операторы,
# что не способствует уменьшению цикломатической сложности кода.


# 2.2. класс слишком маленький - например, класс, которую инкапсулирует какую-то функцию, которую можно было бы
# использовать отдельно, без класса. Получается бесполезный класс.
class Calculation:
    @classmethod
    def calculate_smth(cls, value1, value2):
        pass


# 2.3. как-то встречалось что-то типа такого, когда в метода одного класса содержалась логика обрабоки объекта другого
# класса и все, для чего нужен был этот метод - это связать один объект с другим.
class Document:
    def attach_serfificate(self, sertif):
        if sertif.has_bank_account:
            sertif.prepare_some_stuff()
        if sertif.is_new:
            sertif.do_smth_else()
        self.sertif = sertif


# логичнее было бы обработать сертификат в своем классе и связать с документом либо там, либо в сервисе


# 2.4. Класс хранит данные, которые загоняются в него в множестве разных мест в программе. Возможно - это ситуация,
# когда объект класса создается в каком-то одном месте, а дальше передается по цепочке вызовов, дополняется в последующих
# функциях какими-то данными и где-то в конце такой цепочки сохраняется. Или, если все объекты хранятся в памяти в
# рантайме, то это ситуация вызова объектов в разных местах программы для дополнения их какими-то данными.


# 2.5. Печать документа. Зависит от реализации класса ToPdf. Если нам потребуется преобразовать в пдф не текст,
# а html, то придется переписывать реализацию.
class Document:
    def as_pdf(self):
        return TpPdf.make_pdf(self.text)


class ToPdf:
    def make_pdf(self, text): ...


# 2.6. Приведение типов вниз по иерархии
class Document: ...


class Invoice(Document):
    def specific_method(self): ...


def proceed_document(doc: Document):
    if isinstance(doc, Invoice):
        doc.specific_method()
    ...


# 2.7. При созданнии наследника - надо создавать наследников для других классов. Я с такими случаями еще не встречался,
# но полагаю, что это следствие зависимости от реализации, а не от абстракции. Наверное что-то типа такого
class Document:
    printer: ToPdfPrinter


class ToPdfPrinter:
    # какая-то сложная логика по предобразованию и подготовке документа к печати
    # и метод печати
    def print(self): ...


class Invoice(Document):
    printer: ToPaperPrinter


class ToPaperPrinter(ToPdfPrinter):
    # хотим сохранить логику подготовки документа
    # но переопределить метод печати
    def print(self): ...


# 2.8. Дочерниекласс не используют методы и аттрибуты родительских классов или переопределяют их
class Contract:
    STATUS_CHOICES = (
        "DRAFT",
        "NEED_EDIT",
        "APPROVED_EDIT",
        "SIGNED",
        "EXECUTED",
    )

    def sign_contract(self):
        # логика подписания контракта двумя сторонами
        ...


class ContractInvoice(Contract):
    STATUS_CHOICES = (
        "DRAFT",
        "REJECTED",
        "SIGNED",
    )

    def sign_contract(self):
        # логика подписания контракта одной стороной
        ...


# 3
# 3.1. Одна модификация требует внесения изменений в несколько классов. Была такая ситуация, когда за информацию о дате
# последнего изменения объекта модели отвечали два разных поля. В одних моделях - created_on / updated_on, в других -
# created_at / updatedf_at. При выносе поля created_at / updated_at в миксин пришлось вносить изменения (миграции схемы,
# миграции данных) в модели с первым типов таких полей.
# Еще была ситуация, когда некая константа проверялась не по имени константы, а по значению. Что-то типа такого:
class Document(models.Model):
    STATUS = "active"
    status = models.CharField()


class Contract(Document):
    def some_check(self):
        if self.status == "active":
            ...


# и в какой-то момент потребовалось переопределить значение этой константы и приходилось руками отлавливать все такие
# литералы и менять их на имя константы.


# 3.2. Использование сложных паттернов проектирования. В текущем проекте, например, есть две модели
class Document: ...


class DocumentProject(Document): ...


# Document больше нигде не используется в качестве родительского класса и сам по себе тоже не используется. Скорее всего
# это было сделано на будущее, но будущее в том виде, как оно виделось 4 года назад, не наступило.

# еще ка пример - в Джанге есть сигналы. Что-то похожее на паттерн Наблюдателя. Чаще всего удобнее не использовать их,
# а просто добавить какой-то вызов после сохранения объекта, поскольку чаще всего это сохранение локализовано в одном
# месте конкретной вью.
