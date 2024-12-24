# 4. functional variation inheritance. Например, при реализации какого-то документа, где не подразумевается
# вторая сторона (уведомление, извещение или односторонний договор), метод полученияподписей в дочернем классе
# переопределяется. Сигнатура при этом не меняется.
class Document:
    def get_signature(self, one_sign, another_sign):
        self.one_sign = one_sign
        self.another_sign = another_sign


class OneSideDocument(Document):
    def get_signature(self, one_sign, another_sign):
        self.one_sign = one_sign
        self.another_sign = None


# 5. reification inheritance.
class IDocument:
    @final
    def notify_about_contract(self):
        """реализованный метод, который должен быть унаследован в обязательном порядке"""
        send_email()
        send_to_slack()

    @abstractmethod
    def get_signature(self, one_side, another_side): ...


class Document(IDocument):
    def get_signature(self, one_sign, another_sign):
        self.one_sign = one_sign
        self.another_sign = another_sign


# 6. structure inheritance.
class Archive:
    def archive(self):
        # логика для архивирования любого документа
        ...


class Document(IDocument, Archive): ...


class Invoice(IDocument, Archive): ...


class Memo(IDocument, Archive): ...
