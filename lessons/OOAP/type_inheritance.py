class Document:
    IS_GOVERNMENT: bool
    IS_PRIVATE: bool
    IS_INTERNAL: bool

    @abstractmethod
    def sign_process(self):
        # в таком случае нам придется либо в родительском, либо в дочерних классах
        # перебирать какие-то флаги и в зависимости от тех или иных требований к подписанию документа реализовывать
        # то или ное поведение
        pass


class Contract(Document): ...


class Invoice(Document): ...


class DocumentProcess:
    @abstractmethod
    def sign_process(self):
        pass


class GovernmentDocumentProcess(DocumentProcess):
    def sign_process(self):
        pass


class PrivateDocumentProcess(DocumentProcess):
    def sign_process(self):
        pass


class InternalDocumentProcess(DocumentProcess):
    def sign_process(self):
        pass


"""Смысл в том, что есть класс документов, который может рассматриваться с точки зрения как конкретного вида документа:
контракт, счет и пр. со своими методами обработки документа, так и с точки зрения направленности документа:
госконтракт, частный контракт, внутренний документ. Тогда мы можем, например, определив главным критерием вид, добавить
в него полиморфное поле, через которое будем вызывать общие методы для работы с тем или иным потребителем контракта."""


class Contract(Document):
    process_dispatcher: DocumentProcess
