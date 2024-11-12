# наследование. Здесь мы наследуем от родительского класса часть методов, модифицируем метод add()
# добавляем конструктор и специфичные для потомка методы.
class HashTableABC(ABC):
    NEXT_SLOT_STEP = 1
    NOT_IN_TABLE_IND = -1
    ADD_NIL: int = 0
    ADD_OK: int = 1
    ADD_ERR: int = 2
    REMOVE_NIL: int = 0
    REMOVE_OK: int = 1
    REMOVE_ERR: int = 2
    IN_TABLE_NIL = 0
    IN_TABLE_OK = 1
    IN_TABLE_ERR = 2

    # команды
    def add(self, node: Node) -> None: ...
    def remove(self, node: Node) -> None: ...

    # запросы
    def is_in_table(self, node: Node) -> bool: ...
    def get_add_status(self) -> int: ...
    def get_remove_status(self) -> int: ...
    def size(self) -> int: ...


class PowerSetABC(HashTableABC):
    ALREADY_EXISTS = -1
    INTERSEC_NIL = 0
    INTERSEC_OK = 1
    INTERSEC_ERR = 2
    UNION_NIL = 0
    UNION_OK = 1
    UNION_ERR = 2
    DIFF_NIL = 0
    DIFF_OK = 1
    DIFF_ERR = 2
    ISSUB_NIL = 0
    ISSUB_OK = 1
    ISSUB_ERR = 2
    EQUAL_NIL = 0
    EQUAL_OK = 1
    EQUAL_ERR = 2

    # конструктор
    def PowerSet(self, set_size: int) -> Self: ...

    # команды
    def add(self, node: Node) -> None: ...

    # запросы
    def intersection(self, power_set: Self) -> Self: ...
    def get_intersec_status(self) -> int: ...
    def union(self, power_set: Self) -> Self: ...
    def get_union_status(self) -> int: ...
    def difference(self, power_set: Self) -> Self: ...
    def get_diff_status(self) -> int: ...
    def issubset(self, power_set: Self) -> bool: ...
    def get_issub_status(self) -> int: ...
    def equals(self, power_set: Self) -> bool: ...
    def get_equal_status(self) -> int: ...


# композиция. Вариант из обучения. Тут объект очереди будет содержать в поле _queue объект встроенного типа list
class Queue(QueueABC):
    def Queue(self) -> Self:
        self._clear()
        return self

    def _clear(self):
        self._head = self.HEAD_POS
        self._tail = self.TAIL_POS

        self._queue = []
        self._count = self.COUNT

        self._dequeue_status = self.DEQUEUE_NIL


# композиция из рабочего кода Джанги. например, любое поле сериалайзера - объект сериалайзера будет сдержать
# объект поля
class EppReadyFlowFinancialDocumentSerializer(serializers.ModelSerializer):
    file = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=File.objects.all(),
        required=True,
    )
    subcontractor = serializers.PrimaryKeyRelatedField(queryset=SubContractor.objects.all(), required=True)


# полиморфизм. Тут в примере из рабочего проекта у нас есть документ (который может быть контрактом или инвойсом),
# у которого есть поле со ссылкой на workflow, который может быть либо Workflow, либо InvoiceWorkflow.
# Соответствующий воркфлоу реализует немного разную логику завершения в зависимости от того, какому именно классу
# принадлежит тот или иной воркфлоу из того или иного документа
class Workflow(models.Model):
    ...

    def finish(self, *args, **kwargs):
        self.progress = self.Progress.FINISHED
        self.save(update_fields=["progress"])


class InvoiceWorkflow(Workflow):
    ...

    def finish(self, finished_by, status=None, **kwargs):
        super().finish(finished_by)
        if not status:
            status = Invoice.APPROVED
        self.invoice.status = status
        self.invoice.save()


class Document(models.Model):
    workflow = models.ForeignKey("app.Workflow")


class Invoice(Document):
    workflow = models.ForeignKey("app.InvoiceWorkflow")
    ...
