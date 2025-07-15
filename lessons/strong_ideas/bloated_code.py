# 1.
# есть такая связка методов для обработки отправляемых писем. Получается, что мы не знаем, какой тип данных
# мы обрабатываем.
@staticmethod
def split_mailing_list_by_type(mailing_list: list[str | Membership]) -> tuple[list[str], list[Membership]]:
    emails: list[str] = []
    memberships: list[Membership] = []

    for recipient in mailing_list:
        if isinstance(recipient, str):
            emails.append(recipient)
        elif isinstance(recipient, Membership):
            memberships.append(recipient)

    prefetch_related_objects(memberships, "user")
    return emails, memberships


@staticmethod
def get_clean_mailing_lists(message_dispatcher, to, cc, ignore_user_settings, membership_company):
    stop_list_emails = set(message_dispatcher.memberships_stop_list.values_list("user__email", flat=True))
    to_emails, to_memberships = MailService.split_mailing_list_by_type(to)
    cc_emails, cc_memberships = MailService.split_mailing_list_by_type(cc)

    cc_send = set(cc_emails) | set(membership.user.email for membership in cc_memberships)
    cc_send -= stop_list_emails
    to_send = set()

    if not to or not message_dispatcher.membership_category_id or ignore_user_settings:
        to_send |= set(to_emails) | set(membership.user.email for membership in to_memberships)
        to_send -= stop_list_emails
        return list(to_send), list(cc_send)
    ...


@staticmethod
def send_email_wrapper(
    template_identifier: str,
    to: Membership | QuerySet[Membership] | str | list | tuple | set,
    trial_mode_on: bool,
    stop_all_notifications: bool,
    email_type: str = None,
    dataset: dict | None = None,
    subject: str = None,
    ignore_user_settings: bool = False,
    cc: Membership | QuerySet[Membership] | str | list | tuple | set | None = None,
    attachment=None,
    reminder=False,
    branding_company=None,
    merge_metadata=None,
    **kwargs,
) -> None:
    ...
    to_list, cc_list = MailService.get_clean_mailing_lists(
        message_dispatcher, to, cc, ignore_user_settings=ignore_user_settings, membership_company=membership_company
    )


# в рамках борьбы с раздутостью кода, возможно, имеет смысл ужесточить требования к передаваемым атрибутам to и cc и
# принимать только списки, а обработку и преобразование из других объектов производить как метод класса модели или
# отдельного сервисного метода.
@staticmethod
def send_email_wrapper(
    template_identifier: str,
    to: list,  # <-----
    trial_mode_on: bool,
    stop_all_notifications: bool,
    email_type: str = None,
    dataset: dict | None = None,
    subject: str = None,
    ignore_user_settings: bool = False,
    cc: list | None = None,  # <----
    attachment=None,
    reminder=False,
    branding_company=None,
    merge_metadata=None,
    **kwargs,
) -> None: ...


# и в менеджере модели, например
class MembershipQuerySet(QuerySet):
    def get_emails_list(self):
        return self.values_list("email", flat=True)


# а в коде достаточно вызывать обертку со значением [membership.email]


# 2.
# продолжая рассматривать код отправки писем можно заметить множество флагов, например trial_mode_on или
# stop_all_notifications или branding_company
@staticmethod
def send_email_wrapper(
    template_identifier: str,
    to: list,
    trial_mode_on: bool,  # <-----
    stop_all_notifications: bool,  # <-----
    email_type: str = None,
    dataset: dict | None = None,
    subject: str = None,
    ignore_user_settings: bool = False,  # <-----
    cc: list | None = None,  # <----
    attachment=None,
    reminder=False,
    branding_company=None,  # <-----
    merge_metadata=None,
    **kwargs,
) -> None: ...
# по сути это - скрытые фичи. Одну из я сам даже писал в начале работы. Жаль, что тогда не прочитал еще это занятие.
# Если подумать о сервисе отправки писем как о некотором связанном классе, который зависит от настроек конкретного
# аккаунта, то имел бы смысл переделать вообще сервис, сделав его не статичным, а, например, связанным с аккаунтом и
# эти флаги брать из атрибутов связанного объекта
class CommonEmailService:
    def send_email_wrapper(
        self,
        template_identifier: str,
        to: list,
        # trial_mode_on: bool,  # <----- убираем, берем из self
        # stop_all_notifications: bool,  # <----- убираем, берем из self
        email_type: str = None,
        dataset: dict | None = None,
        subject: str = None,
        ignore_user_settings: bool = False,
        cc: list | None = None,  # <----
        attachment=None,
        reminder=False,
        # branding_company=None,  # <----- убираем, берем из self
        merge_metadata=None,
        **kwargs,
    ) -> None: ...
    
class AccountEmailService(CommonEmailService):
     _instance = None

    def __new__(cls, *args, **kwargs):
        # организовать синглтон
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, account_settings):
        # при инициализации затянуть сюда настройки аккаунта из базы
        ...

# и далее в коде инициализируем и посылаем письмо с помощью связанного объекта
email_service = AccountEmailService(account.settings)
email_service.send_email_wrapper(...)


# 3.
# имеется сервис, который должен обрабатывать два класса. Один класс, представленный типом HeronFinancialDocument
# заменяет другой класс FinancialDocument. Заменяет постепенно, не сразу у всех аккаунтов, через фича-флагинг
class HeronUploaderService:
    def run(self, documents_queryset: Iterable[FinancialDocument | HeronFinancialDocument]) -> None:
        """
        Run the Heron upload process for the given FinancialDocument queryset.
        It is assumed the queryset is already filtered by allowed document types.
        Groups documents by subcontractor and processes each group.
        """
        grouped_documents = defaultdict(list)
        for document in documents_queryset:
            grouped_documents[document.subcontractor].append(document)
        for subcontractor, documents in grouped_documents.items():
            logger.info("Starting Heron upload run", subcontractor_id=subcontractor.id)
            self.get_or_create_heron_account(subcontractor)
            if documents:
                heron_data = subcontractor.constrafor_company.heron_data
                # в методах осуществляется проверка на тип элементов
                self._upload_financial_documents_async(documents, heron_data)
                self._upload_financial_documents_async_new(documents, heron_data)
            logger.info("Completed Heron upload run", subcontractor_id=subcontractor.id)

# Возможно, стоит разделить этот сервис для двух классов, поскольку поддержка старого класса прекращается, а логика
# работы нового класса будет изменять код. Плюс в текущей реализации в качестве documents_queryset передаются разные
# типы коллекций: кверисет или список.
class HeronUploaderServiceDeprecated:
    def run(self, documents_queryset: QuesrySet[FinancialDocument]) -> None:
        ...

class HeronUploaderService:
    def run(self, documents_queryset: list[HeronFinancialDocument]) -> None:
        ...

# сейчас это будет копи-пастой, но через какое-то время все равно придется удалять устаревший код, и тогда удобнее
# будет удалить явно устаревший код, а не вычищать куски кода из работающего сервиса