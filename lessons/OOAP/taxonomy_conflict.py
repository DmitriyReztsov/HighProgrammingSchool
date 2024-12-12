class Document:
    def __init__(self):
        self.document_type = None
        self.signature = None

    def get_signature(self):
        """Могло быть что-то типа:
        if self.document_type == "contract:
            self.signature = get_counterparts_signatures()
        elif self.document_type == "invoice":
            self.signature = get_approver_signature()
        """
        raise NotImplementedError


class Contract(Document):
    def __init__(self):
        self.document_type = "contract"
        self.signature = self.get_signature()

    def get_signature(self):
        """Получение объекта подписей двух сторон контракта"""
        pass


class Invoice(Document):
    def __init__(self):
        self.document_type = "invoice"
        self.signature = self.get_signature()

    def get_signature(self):
        """Получение объекта подписи стороны, утверждающей счет"""
        pass
