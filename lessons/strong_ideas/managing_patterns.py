# 1
# поскольку Django Rest Framework в сериалайзерах игнорирует коды при вызове стандартного исключения ValidationError,
# подставляя всегда 400 статус, то, чтобы не вызывать каждый раз APIException проще сделать собственное исключение
class MySerializer(serializers.ModelSerializer):
    ...

    def validate(self, data):
        ...
        raise APIException("Error", 408)


# создем классы ошибок и вызываем уже их
class ValidationErrorConflict(rest_exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict occurred."
    default_code = "conflict"


class MySerializer(serializers.ModelSerializer):
    ...

    def validate(self, data):
        ...
        raise ValidationErrorConflict()


# 2
# преобразование конструкции try-except-finally в контекстный менеджер, как у Раймонда
def run_sync(self, subscriber: RyvitSubscriber):
    try:
        subscriber.run_start()
        self._sync_object_cache(subscriber)
        self._sync_actions(subscriber)
        last_error = None
    except Exception:
        logger.warning("Exception while syncing with Ryvit", exc_info=True)
        last_error = traceback.format_exc()
    finally:
        subscriber.run_end(last_error)


# adaptor
class SubscriberError(Exception):
    pass


class SubscriberContextManager:
    def __init__(self, subscriber: RyvitSubscriber):
        self.subscriber = subscriber

    def run_sync(self):
        try:
            self.subscriber.run_start()
            self._sync_object_cache(self.subscriber)
            self._sync_actions(self.subscriber)
        except Exception:
            raise SubscriberError

    def __enter__(self):
        return self

    def __exit__(self, exctype, excinst, exctb):
        last_error = None
        if exctype == SubscriberError:
            logger.warning("Exception while syncing with Ryvit", exc_info=True)
            last_error = traceback.format_exc()
        self.subscriber.run_end(last_error)


# и тогда метод можно переписать
def run_sync(self, subscriber: RyvitSubscriber):
    with SubscriberContextManager(subscriber) as subcm:
        subcm.run_sync()


# 3
# есть метод, который связывает две сущности (взаимосвязанные) с какой-то логикой
def link_epp_request_to(ledger):
    """Create or update EPP Request for a given Ledger."""
    epp_request = EPPRequest.objects.filter(ledger_id=ledger.id).first()

    # If EPP Request already exists, update it
    if epp_request:
        logger.info("Found existing EPP Request for Ledger")
        if general_contractor_name and not epp_request.epp_project.project.general_contractor_name:
            epp_request.epp_project.project.general_contractor_name = general_contractor_name
            logger.info("GC Name on EPP Request - EPP Project - Project was not set, updating...")
        prv_status = epp_request.status
        status = get_epp_request_status(ledger)
        if status != prv_status:
            epp_request.status = get_epp_request_status(ledger)
            logger.info("Updating EPP Request status", new_status=status, prv_status=prv_status)
        link_files(ledger, epp_request)
        sync_supplier(ledger, epp_request)
        epp_request.save()
        return

    # If EPP Request does not exist, create it
    prepare_epp_request_data()

    # Now we can handle the EPP Request
    # First, update the Ledger with the related SR & AM fields
    if ledger.subcontractor:
        logger.info("Ledger has subcontractor, updating related SR & AM fields...")
        update = False
        if ledger.subcontractor.sales_rep and ledger.sales_rep is None:
            ledger.sales_rep = ledger.subcontractor.sales_rep
            logger.info(
                f"Updating Ledger [{ledger.id}] with empty sales rep field to [{ledger.sales_rep}] "
                f"based on the assigned sales rep for subcontractor [{ledger.subcontractor.name}]"
            )
            update = True
        if ledger.subcontractor.account_manager and ledger.account_manager is None:
            ledger.account_manager = ledger.subcontractor.account_manager
            logger.info(
                f"Updating Ledger [{ledger.id}] with empty account manager field to [{ledger.account_manager}] "
                f"based on the assigned account manager for subcontractor [{ledger.subcontractor.name}]"
            )
            update = True
        if ledger.subcontractor.account_manager_manager and ledger.account_manager_manager is None:
            ledger.account_manager_manager = ledger.subcontractor.account_manager_manager
            logger.info(
                f"Updating Ledger [{ledger.id}] with empty account manager manager field to "
                f"[{ledger.account_manager_manager}] "
                f"based on the assigned account manager manager for subcontractor [{ledger.subcontractor.name}]"
            )
            update = True
        if update:
            ledger.save()
    else:
        logger.warning("Ledger has no EPP Sub -- THIS SHOULD NEVER HAPPEN!!!")

    # Finally, we create the EPP Request
    epp_request = EPPRequest(ledger=ledger, epp_project=epp_project)
    epp_request.save()


# можно также оформит в контекстный менеджер, поскольку тут есть захват ресурса (EPP Request) и его обновление в конце
class EPPRequestContext:
    def __init__(self, ledger: Ledger):
        self.ledger = ledger
        self.epp_request = EPPRequest.objects.filter(ledger_id=ledger.id).first()

    def link_with_ledger(self):
        ...
        # логика создания связи

    def __enter__(self):
        return self

    def __exit__(self, exctype, excinst, exctb):
        self.epp_request.save()


# и тогда в сервисной функции можно обойтись коротким вызовом контекста
def link_epp_request_to(ledger):
    with EPPRequestContext(ledger) as epp_request_cm:
        epp_request_cm.link_with_ledger()
