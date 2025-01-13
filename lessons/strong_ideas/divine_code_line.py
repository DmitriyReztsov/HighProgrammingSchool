# тут в одной строчке происходит вызов функции, которая отвечает за возврат коллекции объектов и тут же вызывается фильтрация результата
document_projects = self.get_queryset().filter(id__in=document_projects_ids)

# исправление
queeryset = self.get_queryset()
document_projects = queryset.filter(id__in=document_projects_ids)

# тут происходит 1) получение текущего шага активного процесса согласования; 2) инциализация этим шагом сервисного класса; 3)вызов метода 
# отправки писем из сервиса
ContractWorkflowStepService(active_workflow.get_current_step()).send_request_action_email(
    reminder=True, initiator=self.request.user, contract_log_data=entry_data
)

# исправление
current_step = active_workflow.get_current_step()
workflow_step_service = ContractWorkflowStepService(current_step)
workflow_step_service.send_request_action_email(
    reminder=True, initiator=self.request.user, contract_log_data=entry_data
)

# тут одновременно и добаляется в список новый элемент, и инициализируется объект класса, и создается значение properties_meta_data
bulk_create_list.append(
    HubspotContact(
        membership=membership,
        lifecycle_stage=hubspot_lifecycle_stage,
        score=properties.get("hubspotscore"),
        sales_rep=hubspot_owner,
        sales_rep_assigned_date=sales_rep_assigned_date,
        last_contacted_date=last_contacted_date,
        hubspot_id=hubspot_user_data["hubspot_id"],
        number_of_sessions=properties.get("hs_analytics_num_visits"),
        number_of_page_views=properties.get("hs_analytics_num_page_views"),
        properties=properties,
        properties_meta_data=hubspot_general_funcs.create_properties_meta_data(properties),
    )
)

# исправление
properties_meta_data=hubspot_general_funcs.create_properties_meta_data(properties)
hs_contact = HubspotContact(
    membership=membership,
    lifecycle_stage=hubspot_lifecycle_stage,
    score=properties.get("hubspotscore"),
    sales_rep=hubspot_owner,
    sales_rep_assigned_date=sales_rep_assigned_date,
    last_contacted_date=last_contacted_date,
    hubspot_id=hubspot_user_data["hubspot_id"],
    number_of_sessions=properties.get("hs_analytics_num_visits"),
    number_of_page_views=properties.get("hs_analytics_num_page_views"),
    properties=properties,
    properties_meta_data=properties_meta_data,
)
bulk_create_list.append(hs_contact)

# одновременное формирование списка, вызов метода для получения полей и проверка условий. Может быть, в данном случае это не сильно усложняет восприятие кода, но однозначно 
# стоит избегать более сложных логических проверок
fields_list = [field.name for field in HubspotContact._meta.get_fields() if field.name != "id"]

# исправление
fields_list = []
hs_contact_fields = HubspotContact._meta.get_fields()
for field in hs_contact_fields:
    if field.name != "id":
        fields_list.append(field,name)

# хоть это и распространенная практика на проекте, но тут происходит 1) фильтрация и 2) обработка отфильтрованного кверисета и формирование 
# ответа в виде списка
user_email_list = (
    MembershipNoticeCategorySetting.objects.filter(*args, **kwargs)
    .filter(category_id=message_dispatcher.membership_category_id)
    .values_list("membership__user__email", flat=True)
)

# исправление
filtered_queryset = (
    MembershipNoticeCategorySetting.objects.filter(*args, **kwargs)
    .filter(category_id=message_dispatcher.membership_category_id)
)
user_email_list = filtered_queryset.values_list("membership__user__email", flat=True)

# внутри функции, отвечающей за фильтрацию получателей писем происходит вызов функции, отвечающей за формирование выражения для фильтрации
exclude_emails = get_filtered_emails(
    get_iexact_in_filter_expr("membership__user__email", to_emails),
    **company_filter,
)

# исправление
email_filters = get_iexact_in_filter_expr("membership__user__email", to_emails)
exclude_emails = get_filtered_emails(
    email_filters,
    **company_filter,
)

# в одном выражении обновление списка и получение объекта для обновления
to_send.update(
    get_filtered_emails(
        email=True,
        membership__in=to_memberships,
    )
)

# исправление
filtered_emails = get_filtered_emails(
    email=True,
    membership__in=to_memberships,
)
to_send.update(filtered_emails)
