from collections.abc import Callable


class Company:
    def get_name(self):
        pass


class Contractor(Company):
    def get_contract(self):
        pass


class Broker(Company):
    def get_deal(self):
        pass


class StockBroker(Broker):
    def get_deal(self):
        pass


class InsuranceBrocker(Broker):
    def get_insurance(self):
        pass


company = Company()
contractor = Contractor()
broker = Broker()
stock_brocker = StockBroker()
insurance_broker = InsuranceBrocker()

# ковариантная типизиция
company_list: list[Company] = [
    company,
    contractor,
    broker,
    stock_brocker,
    insurance_broker,
]


# контравариативность
def make_action_by_broker(action: Callable[[Broker], None], broker: Broker) -> None:
    action(broker)


def make_deal(broker: Broker):
    broker.get_deal()


def set_name(company: Company):
    company.get_name()


def make_insurance(broker: InsuranceBrocker):
    broker.get_insurance()


make_action_by_broker(make_deal, broker)  # it's ok broker реализует свой метод
make_action_by_broker(set_name, broker)  # it'ok broker реализует метод родительского класса

# it's NOT ok broker (как объект родительского по отношению к insurance_broker) пытается рeализовать специфичный
# для потомка метод
# Argument 1 to "make_action_by_broker" has incompatible type "Callable[[InsuranceBrocker], Any]";
# expected "Callable[[Broker], None]"
make_action_by_broker(make_insurance, broker)
