"""Миксин добавляет новое поле и поведение при сохранении сущности в нужную модель.
От конкретного типа объекта не зависит, поскольку в Джанге можно создавать абстрактные
классы от моделей Model, они не создаю собственных таблиц и сущностей, но добавляют поля,
как в моем случае, и поведение в классы, которые их наследуют.
"""


class TrackingFieldsChangesGFKMixin(models.Model):
    fields_last_changes = GenericRelation(FieldsLastChanges)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        with transaction.atomic():
            pre_changed_attrs = None
            if not self._state.adding:
                stored_instance = self.__class__.objects.get(id=self.id)
                pre_changed_attrs = deepcopy(stored_instance.__dict__)
            super().save(*args, **kwargs)
            create_or_update_last_changes_data(self._meta.model, self, pre_changed_attrs)


class Company(TrackingFieldsChangesGFKMixin):
    pass


class EarlyPayProject(TrackingFieldsChangesGFKMixin):
    pass


class FinancialDocument(TrackingFieldsChangesGFKMixin):
    pass


"""В этом примере миксин используется в более клссическом понимании, без наследования от
какого-либо базового класса. Миксин добаляет несколько проперти в классы, которые могут
поддержать работу миксина наличием соответствующих аттрибутов у объектов.
"""


class WorkflowCommonModelPropertiesMixin:
    @property
    def has_unfinished_workflow(self):
        return bool(self.workflow) and not self.workflow.is_finished

    @property
    def has_unfinished_workflow_edition(self):
        return bool(self.workflow_edition) and not self.workflow_edition.is_finished

    @property
    def active_workflow(self):
        if self.has_unfinished_workflow:
            return self.workflow
        elif self.has_unfinished_workflow_edition:
            return self.workflow_edition
        return None


class DocumentProject(Document, WorkflowCommonModelPropertiesMixin): ...


class ScheduleOfValues(TimeStampMixin, WorkflowCommonModelPropertiesMixin): ...
