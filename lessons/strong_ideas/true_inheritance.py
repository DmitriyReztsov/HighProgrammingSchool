# flake8: noqa

from abc import ABC, abstractmethod
from typing import Any


# Текущая иерархия классов
class Company:
    def is_contractor(self) -> bool:
        return hasattr(self, "contractor")


class Contractor(Company):
    def is_contractor(self) -> bool:
        return True


class Broker(Company):
    def is_contractor(self) -> bool:
        return False


# После применения Посетителя
class CompanyABC(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor") -> Any: ...


class Company:
    def accept(self, visitor: "Visitor") -> bool:
        raise NotImplementedError

    def is_contractor(self) -> bool:
        return hasattr(self, "contractor")

    def is_broker(self) -> bool:
        return hasattr(self, "broker")


class Contractor(Company):
    contractor = 1

    def accept(self, visitor: "Visitor") -> bool:
        return visitor.visit_contractor(self)

    def i_am_contractor(self):
        return True


class Broker(Company):
    broker = 1

    def accept(self, visitor: "Visitor") -> bool:
        return visitor.visit_broker(self)

    def i_am_broker(self):
        return True


class Visitor(ABC):
    @abstractmethod
    def visit_contractor(self, element: Contractor) -> bool: ...

    @abstractmethod
    def visit_broker(self, element: Broker) -> bool: ...


class ContractorVisitor(Visitor):
    def visit_contractor(self, element: Contractor) -> bool:
        return element.i_am_contractor()

    def visit_broker(self, element: Broker) -> bool:
        return element.is_contractor()


class BrokerVisitor(Visitor):
    def visit_contractor(self, element: Contractor) -> bool:
        return element.is_broker()

    def visit_broker(self, element: Broker) -> bool:
        return element.i_am_broker()


contractor = Contractor()
broker = Broker()

visitor_contractor = ContractorVisitor()
visitor_broker = BrokerVisitor()

print(contractor.accept(visitor_contractor))
print(broker.accept(visitor_contractor))

print(contractor.accept(visitor_broker))
print(broker.accept(visitor_broker))

"""Пример, возможно, не слишком удачный. В рабочем коде практически нет моделей, которые были бы не джанговскими Model
и редко используется наследование в моделях. Для простой проверки типа объекта этот паттерн - лишнее усложнение.
Но подумав над его применением, если бы там была какая-нибудь логика посложнее, то применение такого подхода было бы
более оправдано и позволило бы легче добавлять новых наследников и новых Посетителей. Во всяком случае, выглдит это
аккуратнее и читаемее цепочки if-elif"""
