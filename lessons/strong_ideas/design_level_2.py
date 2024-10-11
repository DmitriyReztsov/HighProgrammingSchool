"""
Задача: синхронизация данных между записями о компаниях на сервере и в стороннем
сервисе HubSpot

Дизайн:
Имеется таблица Компаний, таблица с данными записей ХабсПота. Между таблицами 
установлена связь один-к-одному. Возможны ситуации:
- компания не имеет соответствующей записи в таблице данных Хабспота (новая,
еще ни разу не интегрированная);
- компания имеет запись в таблице данных Хабспота, но не имеет идентификатора 
Хабспота (запись создана, но по каким-то причинам данные с Хабспота не получены);
- компания имеет запись в таблице данных Хабспота и имеет идентификатор

1. разбить компании по категориям: для создания записей в таблице Хабспота,
для создания записей в существующих записях Хабспота (есть запись, но нет данных),
для обновления существующих записей.

1.1. для этого в запросе из базы необходимо аннотировать данные признаком
наличия для Компании записи Хабспота

2. для каждого типа компаний применить свой метод обработки
2.1. Если у Компании нет записи в таблице Хабспота:
2.1.1. получить со стороннего сервиса Хабспот список 1 записей, связанных с айди
Компаний (через АПИ)
2.1.2. найти компании, которые не представлены в списке 1 стороннего сервиса
2.1.3. создать записи в стороннем сервисе Хабспота (через АПИ)
2.1.4. дополнить список 1 созданными с стороннем сервисе компаниями
2.1.5. собрать данные по каждой компании - айди записи стороннего сервиса и
аттрибуты, которые надо сохранить у себя
2.1.6. сохранить эти данные

2.2. Если у Компании есть запись в таблице Хабспота, но нет данных о айди записи стороннего
сервиса (пустая запись или только аттрибуты)
2.2.1. получить со стороннего сервиса Хабспот список 2 записей, связанных с айди
Компаний (через АПИ)
2.2.2. получить список аттрибутов по каждой компании - айди записи стороннего сервиса и
аттрибуты, которые надо сохранить у себя
2.2.3. обновить записи таблицы Хабспота

2.3. Если у Компании есть запись в таблицу Хабспота и есть запись айди
2.3.1. для каждой компании получить инпут: проверить хранящийся аттрибут в таблице Хабспота с 
актуальным аттрибутом компании
2.3.2. обновить данные в стороннем сервисе Хабспота (через АПИ)
2.3.3. обновить данные в таблице Хабспота

"""


# initial function
def sync_companies(queryset, batch_size=HUBSPOT_DEFAULT_BATCH_SIZE):
    companiess_paginator = Paginator(queryset, batch_size)
    for page in range(1, companiess_paginator.num_pages + 1):
        batch_of_companiess = companiess_paginator.page(page).object_list
        companies_action = action_on_companies(batch_of_companiess)
        if companies_action["to_create_hubspot_company"]:
            create_hubspot_company_from_company(companies_action["to_create_hubspot_company"])
        if companies_action["to_update_hubspot_company_with_empty_properties"]:
            update_hubspot_company_from_hubspot(companies_action["to_update_hubspot_company_with_empty_properties"])
        if companies_action["to_sync_hubspot_company"]:
            sync_hubspot_companies_by_companies(companies_action["to_sync_hubspot_company"])


# 2.1. create Hubspot Company entity
def create_hubspot_company_from_company(companies: list[Company]) -> None:
    hubspot_companies_map = get_hubspot_companies_map(companies)

    companies_new_for_hubspot = [
        company for company in companies if str(company.id) not in hubspot_companies_map.keys()
    ]

    created_companies_from_hubspot = create_companies(companies_new_for_hubspot)
    hubspot_created_contacts_map = {
        company_from_hubspot.properties["constrafor_company_id"]: company_from_hubspot
        for company_from_hubspot in created_companies_from_hubspot
    }
    hubspot_companies_map.update(hubspot_created_contacts_map)

    companies_properties_map = get_companies_properties_map(hubspot_companies_map, companies)
    create_platform_hubspot_company(companies_properties_map)


# 2.1.1.
def get_hubspot_companies_map(companies: list[Company]) -> dict:
    companies_ids = [company.id for company in companies]
    existing_companies_from_hubspot = hubspot_company.hubspot_search_multiple_companies(companies_ids)

    hubspot_companies_map = {
        company_from_hubspot.properties["constrafor_company_id"]: company_from_hubspot
        for company_from_hubspot in existing_companies_from_hubspot
    }
    return hubspot_companies_map


# 2.1.3.
def create_companies(companies: list[Company]) -> list:
    result = hubspot_company.hubspot_batch_create_companies([{"company": company} for company in companies]).results
    return result


# 2.1.5.
def get_companies_properties_map(hubspot_companies_map: dict, companies: list[Company]) -> dict:
    companies_properties_map = {}
    for company in companies:
        company_from_hubspot_data = hubspot_companies_map.get(str(company.id))
        if not company_from_hubspot_data:
            continue

        companies_properties_map[company] = {
            "hubspot_id": company_from_hubspot_data.id,
            "properties": company_from_hubspot_data.properties,
        }
    return companies_properties_map


# 2.1.6
def create_platform_hubspot_company(companies_properties_map: dict) -> None:
    bulk_create_list = []
    for company, company_from_hubspot_data in companies_properties_map.items():
        properties = company_from_hubspot_data["properties"]
        hubspot_lifecycle_stage = hubspot_general_funcs.get_platform_lifecycle_stage_from_hubspot_lifecycle_stage(
            properties["lifecyclestage"]
        )

        bulk_create_list.append(
            HubspotCompany(
                company=company,
                lifecycle_stage=hubspot_lifecycle_stage,
                hubspot_id=company_from_hubspot_data["hubspot_id"],
                properties=properties,
                properties_meta_data=hubspot_general_funcs.create_properties_meta_data(properties),
            )
        )

    HubspotCompany.objects.bulk_create(bulk_create_list)


"""
Рефлексия по первой части.

Код в целом следует за дизайном. Дизайн описывает порядок действий, необходимый для создания записи в БД,
синхронизированной по данным с записью в стороннем сервисе. Если описать его проще, своими словами, то нужно
получить компании из БД, сверить их с записями в стороннем сервисе, дополнить сторонний сервис разницей и сохранить
данные в связанной модели в БД.

Что можно было бы изменить. В целом код выглядит следующим за дизайном, каких-то повторяющихся действий нет.
Можно переписать его в декларативной манере, спрятав список и операции над ним в сервисный класс и вызывая методы
класса для обработки.

"""


class HubspotSyncService:
    def __init__(self, entities_list: list) -> None:
        self.entities_list = entities_list
        self.hubspot_companies_map = self._get_hubspot_companies_map(self.companies)

    def _get_hubspot_companies_map(self):
        companies_ids = [company.id for company in self.entities_list]
        existing_companies_from_hubspot = hubspot_company.hubspot_search_multiple_companies(companies_ids)

        hubspot_companies_map = {
            company_from_hubspot.properties["constrafor_company_id"]: company_from_hubspot
            for company_from_hubspot in existing_companies_from_hubspot
        }
        return hubspot_companies_map

    def update_hubspot_entries(self):
        companies_new_for_hubspot = [
            company for company in self.companies if str(company.id) not in self.hubspot_companies_map.keys()
        ]

        created_companies_from_hubspot = create_companies(companies_new_for_hubspot)
        hubspot_created_contacts_map = {
            company_from_hubspot.properties["constrafor_company_id"]: company_from_hubspot
            for company_from_hubspot in created_companies_from_hubspot
        }
        self.hubspot_companies_map.update(hubspot_created_contacts_map)

    def update_platform_entries(self):
        companies_properties_map = get_companies_properties_map(self.hubspot_companies_map, self.entities_list)
        create_or_update_platform_hubspot_company(companies_properties_map)


# initial function
def sync_companies(queryset, batch_size=HUBSPOT_DEFAULT_BATCH_SIZE):
    companiess_paginator = Paginator(queryset, batch_size)
    for page in range(1, companiess_paginator.num_pages + 1):
        batch_of_companiess = companiess_paginator.page(page).object_list
        companies_action = action_on_companies(batch_of_companiess)
        if companies_action["to_create_hubspot_company"]:
            create_hubspot_company_from_company(companies_action["to_create_hubspot_company"])
        if companies_action["to_update_hubspot_company_with_empty_properties"]:
            update_hubspot_company_from_hubspot(companies_action["to_update_hubspot_company_with_empty_properties"])
        if companies_action["to_sync_hubspot_company"]:
            sync_hubspot_companies_by_companies(companies_action["to_sync_hubspot_company"])


# 2.1. create Hubspot Company entity
def create_hubspot_company_from_company(companies: list[Company]) -> None:
    """
    Если по-новому взглянуть на этом уровне, то можно перефразировать, что нам надо взять компании
    и обновить данные стороннего сервиса и данные на платформе. Убрать детали реализации в сервис и
    тогда можно обобщить операции для остальных категорий компаний.

    """

    sync_service = HubspotSyncService(companies)
    sync_service.update_hubspot_entries()
    sync_service.update_platform_entries()


"""
Когда у нас ситуация, при которой компании в базе уже есть, достаточно будет вызвать только обновление их данных

"""


def update_hubspot_company_from_hubspot(companies: list[Company]) -> None:
    sync_service = HubspotSyncService(companies)
    sync_service.update_platform_entries()


"""
Есть еще сущность контактов (помимо компаний), которые надо также обновлять. Действия там были бы все те же самые,
разница только в том, какие именно аттрибуты контакта надо обновлять и отслеживать.
Сервисный класс тогда мог бы выглядеть как-то так:

"""


class HubspotSyncServiceBase:
    def __init__(self, entities_list: list) -> None:
        self.entities_list: list = entities_list
        self.hubspot_entities_map: dict = self._get_hubspot_entities_map(self.entities_list)
        self.lookup_field_name = self._get_lookup_field_name()

    def _get_hubspot_entities_map(self, entities_list) -> dict:
        raise NotImplemented

    def _get_entities_properties_map(self) -> dict:
        raise NotImplemented

    def _create_entity(self) -> dict:
        raise NotImplemented

    def _get_lookup_field_name(self) -> str:
        raise NotImplemented

    def _create_or_update_platform_hubspot_entity(self, properties_map) -> None:
        raise NotImplemented

    def update_hubspot_entries(self):
        entites_new_for_hubspot = [
            entity for entity in self.entities_list if str(entity.id) not in self.hubspot_entities_map.keys()
        ]

        created_entities_from_hubspot = self._create_entity(entites_new_for_hubspot)
        hubspot_created_entites_map = {
            entity_from_hubspot.properties[self.lookup_field_name]: entity_from_hubspot
            for entity_from_hubspot in created_entities_from_hubspot
        }
        self.hubspot_entities_map.update(hubspot_created_entites_map)

    def update_platform_entries(self):
        entities_properties_map = self._get_entities_properties_map()
        self._create_or_update_platform_hubspot_entity(entities_properties_map)


class HubspotSyncServiceCompany(HubspotSyncServiceBase):
    """
    Сервис для синхронизации компаний

    """

    def _get_hubspot_entities_map(self, companies) -> dict:
        companies_ids = [company.id for company in companies]
        existing_companies_from_hubspot = hubspot_company.hubspot_search_multiple_companies(companies_ids)

        hubspot_companies_map = {
            company_from_hubspot.properties["constrafor_company_id"]: company_from_hubspot
            for company_from_hubspot in existing_companies_from_hubspot
        }
        return hubspot_companies_map

    def _get_entities_properties_map(self) -> dict:
        companies_properties_map = {}
        for company in self.entities_list:
            company_from_hubspot_data = self.hubspot_entities_map.get(str(company.id))
            if not company_from_hubspot_data:
                continue

            companies_properties_map[company] = {
                "hubspot_id": company_from_hubspot_data.id,
                "properties": company_from_hubspot_data.properties,
            }
        return companies_properties_map

    def _create_entity(self) -> dict:
        result = []
        result = hubspot_company.hubspot_batch_create_companies(
            [{"company": company} for company in self.entities_list]
        ).results
        return result

    def _get_lookup_field_name(self) -> str:
        return "constrafor_company_id"

    def _create_or_update_platform_hubspot_entity(
        self, create_properties_map: dict = None, update_propertirs_name: dict = None
    ) -> None:
        if create_properties_map is None:
            create_properties_map = {}
        if update_propertirs_name is None:
            update_propertirs_name = {}

        bulk_create_list = []
        for company, company_from_hubspot_data in create_properties_map.items():
            properties = company_from_hubspot_data["properties"]
            hubspot_lifecycle_stage = hubspot_general_funcs.get_platform_lifecycle_stage_from_hubspot_lifecycle_stage(
                properties["lifecyclestage"]
            )

            bulk_create_list.append(
                HubspotCompany(
                    company=company,
                    lifecycle_stage=hubspot_lifecycle_stage,
                    hubspot_id=company_from_hubspot_data["hubspot_id"],
                    properties=properties,
                    properties_meta_data=hubspot_general_funcs.create_properties_meta_data(properties),
                )
            )

        HubspotCompany.objects.bulk_create(bulk_create_list)

        bulk_update_list = []
        for company, company_from_hubspot_data in update_propertirs_name.items():
            company_from_hubspot_value_mapping = hubspot_company.get_company_from_hubspot_mapping_for_platform_fields(
                company_from_hubspot_data["properties"]
            )

            company_hubspot_company = company.hubspot_company
            for attr, value in company_from_hubspot_value_mapping.items():
                setattr(company_hubspot_company, attr, value)

            company_hubspot_company.hubspot_id = company_from_hubspot_data["hubspot_id"]
            company_hubspot_company.properties = company_from_hubspot_data["properties"]
            company_hubspot_company.properties_meta_data = hubspot_general_funcs.create_properties_meta_data(
                company_from_hubspot_data["properties"]
            )
            bulk_update_list.append(company_hubspot_company)

        fields_list = [field.name for field in HubspotCompany._meta.get_fields() if field.name != "id"]
        HubspotCompany.objects.bulk_update(bulk_update_list, fields_list)


class HubspotSyncServiceContacts(HubspotSyncServiceBase):
    """ "
    Сервис для синхронизации контактов

    """

    def _get_hubspot_entities_map(self, memberships) -> dict:
        emails = [membership.user.email.lower() for membership in memberships]
        existing_hubspot_contacts = hubspot_contact.hubspot_search_multiple_contacts(emails)
        hubspot_contacts_map = {
            hubspot_contact.properties["email"]: {
                "hubspot_contact": hubspot_contact,
            }
            for hubspot_contact in existing_hubspot_contacts
        }
        return hubspot_contacts_map

    def _get_entities_properties_map(self) -> dict:
        membership_properties_map = {}
        for membership in self.entities_list:
            hubspot_contact_data = self.hubspot_entities_map.get(membership.user.email.lower())
            if not hubspot_contact_data:
                continue

            hubspot_contact = hubspot_contact_data["hubspot_contact"]
            membership_properties_map[membership] = {
                "hubspot_id": hubspot_contact.id,
                "properties": hubspot_contact.properties,
            }
        return membership_properties_map

    def _create_entity(self) -> dict:
        result = []
        result = hubspot_company.hubspot_batch_create_contact(
            [{"membership": membership} for membership in self.entities_list]
        ).results
        return result

    def _get_lookup_field_name(self) -> str:
        return "email"

    def _create_or_update_platform_hubspot_entity(
        self, create_properties_map: dict = None, update_properties_name: dict = None
    ) -> None:
        if create_properties_map is None:
            create_properties_map = {}
        if update_properties_name is None:
            update_propertirs_name = {}

        bulk_create_list = []
        for membership, hubspot_user_data in create_properties_map.items():
            properties = hubspot_user_data["properties"]
            hubspot_lifecycle_stage = hubspot_contact.get_platform_lifecycle_stage_from_hubspot_lifecycle_stage(
                properties["lifecyclestage"]
            )
            sales_rep_assigned_date = hubspot_contact.get_hubspot_contact_date_value(
                properties, "hubspot_owner_assigneddate"
            )
            last_contacted_date = hubspot_contact.get_hubspot_contact_date_value(properties, "notes_last_contacted")

            bulk_create_list.append(
                HubspotContact(
                    membership=membership,
                    lifecycle_stage=hubspot_lifecycle_stage,
                    score=properties.get("hubspotscore"),
                    sales_rep_assigned_date=sales_rep_assigned_date,
                    last_contacted_date=last_contacted_date,
                    hubspot_id=hubspot_user_data["hubspot_id"],
                    number_of_sessions=properties.get("hs_analytics_num_visits"),
                    number_of_page_views=properties.get("hs_analytics_num_page_views"),
                    properties=properties,
                    properties_meta_data=hubspot_general_funcs.create_properties_meta_data(properties),
                )
            )

        HubspotContact.objects.bulk_create(bulk_create_list)

        bulk_update_list = []
        for membership, hubspot_user_data in update_properties_name.items():
            hubspot_contact_value_mapping = hubspot_contact.get_hubspot_contact_mapping_for_platform_fields(
                hubspot_user_data["properties"]
            )
            membership_hubspot_contact = membership.hubspot_contact
            for attr, value in hubspot_contact_value_mapping.items():
                setattr(membership_hubspot_contact, attr, value)

            membership_hubspot_contact.hubspot_id = hubspot_user_data["hubspot_id"]
            membership_hubspot_contact.properties = hubspot_user_data["properties"]
            membership_hubspot_contact.properties_meta_data = hubspot_general_funcs.create_properties_meta_data(
                hubspot_user_data["properties"]
            )
            bulk_update_list.append(membership_hubspot_contact)

        fields_list = [field.name for field in HubspotContact._meta.get_fields() if field.name != "id"]
        HubspotContact.objects.bulk_update(bulk_update_list, fields_list)


"""
В итоге я избавился по коду от повторяющихся вызовов одних и тех же функций для разных случаев синхронизации,
код на уровне модуля синхронизации стал чище и понятнее, реализация ушла в сервисные классы.

"""
