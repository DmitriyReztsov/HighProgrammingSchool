class Document:
    """Родительский класс для документов. Предусмотрены методы для архивирования, подписани и установки статуса
    документа.
    """

    def archive(self):
        raise NotImplementedError

    def set_sign(self, signer):
        raise NotImplementedError

    def set_status(self, status):
        self.status = status


class Invoice(Document):
    """Наследник класса Document не требует метода archive(), поэтому его не реализует - специализация у наследника.
    Метод set_status() расширяется дополнительной логикой. Класс расширяется специализированным методом оплаты инвойса.
    """

    APPROVED = False

    def set_sign(self, signer):
        self.signer = signer

    def set_status(self, status):
        super().set_sign(status)
        if self.status == self.APPROVED:
            self.to_pay = True

    def pay_invoice(self):
        if self.to_pay:
            ...


class Memo(Document):
    """Наследник класса Document для служебных записок (Memo) не требует метода подписания - специализация, использует
    как есть метод установки статуса документа и реализует метод архивирования.
    """

    STATUS_SENT = False

    def archive(self):
        self.is_archived = True
