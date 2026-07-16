""" 1
Удобный паттерн в Джанге - ставить контроллер между ОРМ и логикой, который будет вызывать какие-то задачи, которые должны выполняться до или после сохранения инстанса. Обычные сигналы в Джанге имеют свои особенности, поэтому такой подход позволяет более точечно управлять обработкой событий, в т.ч. учитывая сохранение и изменения в отдельных полях
"""

class ModelsController:
    def delete_model(self, instance, context: None | dict = None):
        before_model_hard_deleted_events.send(instance, context=context)
        instance.delete()
        after_model_hard_deleted_events.send(instance, context=context)

    def update_model(
        self,
        instance,
        field_values: dict,
        context: None | dict = None,
        save_to_db=True,
        force_events=False,
        force_fields: set[str] | None = None,
    ):
        from core.model_event_dispatch import dispatch_model_event

        changed_fields = dict()
        for k, v in field_values.items():
            prev_val = getattr(instance, k)
            if prev_val != v or force_events or (force_fields and k in force_fields):
                changed_fields[k] = prev_val
            setattr(instance, k, v)

        if not changed_fields:
            return

        # иначе запрос на сохранение неизменного поля в базу отсылается каждый раз, даже без изменений
        if save_to_db:
            update_fields_list = list(changed_fields.keys())
            if isinstance(instance, MyTimeStampedModel):
                update_fields_list.append("updated_at")
            instance.save(update_fields=update_fields_list)

        logger.debug("Найдены изменённые поля", changed_fields=changed_fields, instance=instance)
        dispatch_model_event(
            "update",
            instance=instance,
            context=context,
            changed_fields=changed_fields,
            new_values=field_values,
            save_to_db=save_to_db,
        )

    def create_model(self, klass, fields, context: None | dict = None):
        from core.model_event_dispatch import dispatch_model_event

        instance = klass(**fields)
        logger.info("Создание нового экземпляра", instance=instance, klass=klass, fields=fields)

        before_model_created_events.send(instance, context=context)
        instance.save()
        dispatch_model_event("create", instance=instance, context=context)

        return instance
    

"""далее по коду регистрируем через декоратор таски в before_model_created_events и dispatch_model_event и в них выполняем эти таски

"""
class SingleModelEventSignal:
    def __init__(self):
        self.registry = {}

    def register(self, klass, order=1, **kwargs):
        def decorator(fn):
            klass_str = f"{klass.__module__}.{klass.__name__}"
            self.registry.setdefault(klass_str, [])
            filters = kwargs.get("filters", [])
            if not isinstance(filters, list):
                filters = [filters]

            bisect.insort(self.registry[klass_str], ModelHandlerItem(fn, filters, order))
            return fn

        return decorator

    def send(self, sender, **kwargs):
        key = f"{sender.__class__.__module__}.{sender.__class__.__name__}"
        handler_items: list[ModelHandlerItem] = self.registry.get(key, [])
        for handler_item in handler_items:
            try:
                flag = True
                for d in handler_item.filters:
                    if not d(sender, **kwargs):
                        flag = False
                        break

                if flag:
                    handler_item.handler(sender, **kwargs)
            except Exception:
                logger.exception("Ошибка в обработчике сигнала", handler=handler_item.handler.__qualname__, sender=key)


before_model_created_events = SingleModelEventSignal()


"""2
Что касается абстракций, то мы используем базовый класс для каналов общения с прописанными методами создания и отправки сообщений и далее реализации для разных конкретных каналов (ТГ, ВК, Вайбер...). Далее в коде просто обращаемся в тот или иной канал.

"""
class BaseChannelAPI(metaclass=ABCMeta):
    ...
    @abstractmethod
    def get_channel(self, channel_id: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def send_message(self, user_id: Union[str, int], data: dict, channel_id: str):
        raise NotImplementedError

    @abstractmethod
    def process_message(self, channel, message, session):
        raise NotImplementedError


class TelegramAPI(BaseChannelAPI):
    ...  # релизация


class VKontakteAPI(BaseChannelAPI):
    ...  # релизация
