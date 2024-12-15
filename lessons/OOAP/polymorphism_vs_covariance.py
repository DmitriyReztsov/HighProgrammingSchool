from typing import TypeVar


T = TypeVar("T", bound="BaseDocument")


class BaseDocument:
    def is_approved(self) -> bool:
        return True

    @classmethod
    def return_type(cls, object: list[T]) -> list[T]:
        return object


class Contract(BaseDocument):
    WE_SIGNED_STATUS = 0
    OTHER_SIGNED_STATUS = 1

    def __init__(self):
        self._we_signed = self.WE_SIGNED_STATUS
        self._other_signed = self.OTHER_SIGNED_STATUS

    def is_approved(self) -> bool:
        return bool(self._we_signed) and bool(self._other_signed)


class Invoice(BaseDocument):
    IS_APPROVED_STATUS = 0

    def __init__(self):
        self._is_approved = self.IS_APPROVED_STATUS

    def is_approved(self):
        return bool(self._is_approved)


class Brochure(BaseDocument):
    APPROVED_TO_PRINT_STATUS = 0

    def __init__(self):
        self._approved_to_print = self.APPROVED_TO_PRINT_STATUS

    def is_approved(self, typography: str) -> bool:
        # mypy: error: Signature of "is_approved" incompatible with supertype "BaseDocument"  [override]
        return bool(typography) and bool(self._approved_to_print)


"""Полиморфизм в Питоне реализуется через реализацию одинакового интерфейса в классах или
как в примере - через наследование от общего родителя и переопределение родительского метода.
Перегрузка в случае такого полиморфного вызова приведет к ошибке, если будут добавлены обязательные
аргументы в вызов.
Реализация полиморфизма:
"""
contract1 = Contract()
contract2 = Contract()
invoice1 = Invoice()
invoice2 = Invoice()
brochure1 = Brochure()

documents_to_check: list[BaseDocument] = [contract1, contract2, invoice1, invoice2]
for doc in documents_to_check:
    print(doc.is_approved())
    # OK

"""documents_to_check: list[BaseDocument] = [contract1, contract2, invoice1, invoice2, brochure1]
for doc in documents_to_check:
    print(doc.is_approved())
    # TypeError: Brochure.is_approved() missing 1 required positional argument: 'typography'"""

"""Ковариантность в Питоне может быть использована только в контексте аннтотации типов. В рантайме ни на что она 
не влияет.
До типов есть дело только тайп-чекеру."""
print(Brochure.return_type(documents_to_check))  # ошибок mypy не выдает

some_doc: BaseDocument = BaseDocument()
base_doc_list: list[BaseDocument] = [some_doc, contract1, invoice1]
contract_list: list[Contract] = [contract1, contract2]

contract_list = base_doc_list
# error: Incompatible types in assignment (expression has type "list[BaseDocument]", variable has type "list[Contract]")
print(contract_list)
