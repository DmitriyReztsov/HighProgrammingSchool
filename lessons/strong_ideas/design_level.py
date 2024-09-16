"""Задача - добавить ноые пермишены юзерам на некоторых ендпойнтах.

Вначале делал по пункту 1. Т.е. написал тесты, которые ожидаемо падали в тех местах, где юзеру
не хватало пермишенов.

Как пример:
"""


def test_list_epp_requests_with_permissions(self):
    url = "/epp/epp-requests/"

    self.force_authenticate_with_membership(self.subcontractor1_admin1)
    response = self.client.get(url)
    self.assertEqual(403, response.status_code)
    self.client.handler._force_user.selected_membership.flush_perm_cache()

    # epp_user_group
    self.sub1_admin1_mbr.groups.add(self.epp_user_group)
    response = self.client.get(url)

    self.assertIn(self.epp_user_group, self.sub1_admin1_mbr.groups.all())
    self.assertEqual(200, response.status_code)
    self.assertEqual(
        set(epp_request["id"] for epp_request in response.data["results"]),
        set(epp_request.id for epp_request in self.sub1_epp_requests_list),
    )
    self.sub1_admin1_mbr.groups.remove(self.epp_user_group)

    # epp_manager_group
    self.sub1_admin1_mbr.groups.add(self.epp_manager_group)
    response = self.client.get(url)

    self.assertIn(self.epp_manager_group, self.sub1_admin1_mbr.groups.all())
    self.assertEqual(200, response.status_code)
    self.assertEqual(
        set(epp_request["id"] for epp_request in response.data["results"]),
        set(epp_request.id for epp_request in self.sub1_epp_requests_list),
    )
    self.sub1_admin1_mbr.groups.remove(self.epp_manager_group)

    # epp_superuser_group
    self.sub1_admin1_mbr.groups.add(self.epp_super_user_group)
    response = self.client.get(url)

    self.assertIn(self.epp_super_user_group, self.sub1_admin1_mbr.groups.all())
    self.assertEqual(200, response.status_code)
    self.assertEqual(
        set(epp_request["id"] for epp_request in response.data["results"]),
        set(epp_request.id for epp_request in self.sub1_epp_requests_list),
    )
    self.sub1_admin1_mbr.groups.remove(self.epp_super_user_group)


"""На одном из тестов столкнулся с тем, что реализация проверки пермишена
была написана таким образом, что формировала тот или иной кверисет. Т.е. ответ на запрос retrieve
оказывался не с 403 статусом, а с 404. Поправил тест
"""


def test_retrieve_epp_contracts_with_permissions(self, mock_cget_download_document_link_as_pdf):
    rnd_contract = fake.random_elements(elements=self.epp_contracts_list, length=1)[0]
    contract_url = f"/constrafor/document_projects/{rnd_contract.id}/"

    self.force_authenticate_with_membership(self.subcontractor1_admin1)
    response = self.client.get(contract_url)

    self.assertEqual(404, response.status_code)


"""т.е. на уровне работы кода все правильно, казалось бы - пользователю без пермишена объект
не возвращается.

Но после изучения материалов из п. 2 стало понятно, что в таком простом примере содержится
та ошибка, о котором п. 2 говорит - я в тестах последовал за особенностью реализации. При том,
что особо никакой спецификации тут не было, то надо было как-то для себя этот момент определить.
Я определил, что ответ на запрос объекта без пермишена должен содержать 403 код, чтоб логически
была сразу понятна причина отсутствия объекта в ответе пользователю. Это определило не только значение,
которое надо проверять, но и то, как это значение должно быть записано в коде.

Число 403 не читается однозначно, поэтому я заменил его на полный статус.
Итого я поправил тест:
"""


def test_retrieve_epp_contracts_with_permissions(self, mock_cget_download_document_link_as_pdf):
    rnd_contract = fake.random_elements(elements=self.epp_contracts_list, length=1)[0]
    contract_url = f"/constrafor/document_projects/{rnd_contract.id}/"

    self.force_authenticate_with_membership(self.subcontractor1_admin1)
    response = self.client.get(contract_url)

    self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


"""при этом необходимо стало поправить реализацию - я перенес проверку пермишена из метода
get_queryset в метод check_object_permissions
"""


def check_object_permissions(self, request, obj):
    ...
    match self.action:
        case "retrieve":
            if not user_can_retrieve_document_project(user, obj) or not user_can_retrieve_epp_contract(user, obj):
                raise PermissionDenied


"""
В целом получилось на простом примере разделить уровни поведения программы:
на уровне исполнения не допущены возвраты объектов, которые нельзя возвращать,
на уровне кода - реализации - описано как именно мы осуществляем проверку пермишенов,
на уровне логики - описано что именно должен возвращать сервер на запрос пользователя без пермишена.
Далее за этой логикой следуют и реализация (место, в котором мы проверяем и исключение, которое поднимаем)
и тесты, проверяя, что именно этот код ответа возвращается.
Так же на уровне реализации и тестов определено вслед за логикой, что именно кроется за цифрой 403.
"""
