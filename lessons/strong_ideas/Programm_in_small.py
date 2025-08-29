# 1
def process_email_for_ledger(
    ledger: Ledger, previous_status: LedgerStatusChoices, new_status: LedgerStatusChoices
) -> dict[str, Any] | None:

    if should_skip_ledger_event_notification(ledger, previous_status, new_status):
        return None

    notification_data = collect_ledger_data(ledger)
    if not notification_data:
        return None

    days_remaining = notification_data.get("days_remaining", 0)
    days_overdue = notification_data.get("dpd", 0)

    remain_template_id = get_days_remaining_template_mapping(days_remaining)
    dpd_template_id = f"dpd_{days_overdue}"
    template_id = get_task_key_and_template_id(new_status, remain_template_id, dpd_template_id)
    task_key = get_task_key_and_template_id(new_status, days_remaining, days_overdue, ledger.id)

    bind_contextvars(notification_data=notification_data, template_id=template_id, task_key=task_key)

    notification_template = TASK_KEY_TO_TEMPLATE_MAP.get(template_id)
    if not notification_template:
        return None

    data_to_send = prepare_notification_to_send(notification_data, notification_template)
    data_to_send.update(
        {
            "trial_mode_on": False,
            "stop_all_notifications": ledger.subcontractor.constrafor_company.stop_all_notifications,
            "max_calls_number": 1,
            TASK_KEY: task_key,
            "epp_funded": notification_template == PENDING_OPEN,
        }
    )
    return data_to_send


"""
1. Когда выход будет пуст? - когда настройки будут препятствовать отправке; когда шаблон не будет найден; когда собранные данные окажутся пустыми. Если вынести проверку этих параметров за скобки этой функции и принять, что мы формируем словарь из определенных ключей и значений, то выход будет пуст, когда мы доберемся до конца списка ключей.
2. Если выход не пуст, то какова его голова? - Ключ-значение, где ключ - первое значение аттрибута из списка аттрибутов, необходимых для формирования словаря, а значение - значение аттрибута в объекте той модели, которую мы парсим.
3. Из каких данных рекурсивно строится хвост выхода? - из данных объекта, переданного в функцию.

"""

class NotificationService:
    """Для простоты реализации, чтобы не раздувать классы Ledger и Collection вводим
    сервис, в котором определим все методы, возвращающие конкретные значения
    """

    def get_template_identifier_for_Ledger(self, ...) -> str:
        ...

    def process_email(self, obj: Ledger | Collection, **kwargs) -> dict[str, Any]:

        def recursively_collect_data(attr_list, obj, **kwargs):
            if not attr_list:
                return {}
            value = getattr(self, f"get_{attr_list[0]}_for_{obj.__class__.__name__}")(obj, kwargs)
            return {attr_list[0]: value}.update(recursively_collect_data(attr_list[1:], obj, kwargs))

        attr_list = [
            "template_identifier",
            "email_type",
            "to",
            "dataset",
            "subject",
            "trial_mode_on",
            "stop_all_notifications",
            "max_calls_number",
            "epp_funded",
        ]

        return recursively_collect_data(attr_list, obj, kwargs)

# 2
def build_frontend_url(url: str, membership_company_id: str = None) -> str:
    base_url = urljoin(settings.FRONTEND_URL, f"./{url}")
    parsed_url = urlparse(base_url)
    query_params = parse_qs(parsed_url.query)

    if membership_company_id:
        query_params["membership_company"] = [membership_company_id]

    new_query_string = urlencode(query_params, doseq=True)
    new_url = parsed_url._replace(query=new_query_string)

    return urlunparse(new_url)

"""
1. Когда выход будет пуст? - в данном случае выход пуст не будет, поскольку будет в любом случае использован урл из настроек, но базовый случай как раз - значение урла из настроек
2. Если выход не пуст, то какова его голова? - урл из настроек
3. Из каких данных рекурсивно строится хвост выхода? - из частей урла, переданных в функцию и квери-паратметров

"""

def build_frontend_url(url: str, membership_company_id: str = None) -> str:
    """Определяем функции, которые будут формировать части составного урла"""
    def get_scheme(*args, **kwargs):
        return settings.BASE_SCHEME
    
    def get_netloc(*args, **kwargs):
        return settings.BASE_URL
    
    def get_path(url: ParseResult, *args, **kwargs):
        return url.path
    
    def get_params(url: ParseResult, *args, **kwargs):
        return url.params
    
    def get_query(url: ParseResult, membership_company_id, *args, **kwargs):
        query_params = parse_qs(url.query)
        if membership_company_id:
            query_params["membership_company"] = [membership_company_id]
        return urlencode(query_params, doseq=True)
    
    def get_fragment(url: ParseResult, *args, **kwargs):
        return url.fragment

    url_parts = [
        get_scheme,
        get_netloc,
        get_path,
        get_params,
        get_query,
        get_fragment,
    ]

    def rec_collect_url(url_struct: list, url_parts_remain: list) -> str:
        """Рекурсивно проходимся, собирая конкретные значения в список, который будет передан в
        конструктор и распарсен в строку. Передаем в функции-парсеры полный набор входящих аргументов,
        функция самостоятельно вычленяет часть, за котороую отвечает.
        """

        if not url_parts_remain:
            return urlunparse(ParseResult(*url_struct))
        
        url_struct.append(url_parts_remain[0](urlparse(url), membership_company_id))
        return rec_collect_url(url_struct, url_parts_remain[1:])
    
    return rec_collect_url([], url_parts)


# 3
"""Есть некий парсер документов, который по заданной структуре сканирует и распознает документ и
сохраняет коды заполннных полей. Метод update_suplier_categories собирает информацию в список, по которому
фильтрует из базы объекты категорий, которые привязывает к компании. Можно переписать в рекурсивном стиле
"""
class SensibleParser:
    ...
    def extract_value(self, field_name):
        field = self.parsed_document[field_name]
        value = None
        if field:
            value = field["value"]
        else:
            self.none_fields.append(field_name)

        return value
    
    def update_supplier_categories(self):
        core_competency_demo = self.extract_value("core_competency_demo")  # 02
        core_competency_concrete_masonry = self.extract_value("core_competency_concrete_masonry")  # 03
        core_competency_architectural_woodwork = self.extract_value("core_competency_architectural_woodwork")  # 06
        core_competency_structural_steel = self.extract_value("core_competency_structural_steel")  # 05
        core_competency_hollow_metal = self.extract_value("core_competency_hollow_metal")  # 05
        core_competency_metal_glass = self.extract_value("core_competency_metal_glass")  # 05 08
        core_competency_window_treatments = self.extract_value("core_competency_window_treatments")  # 08
        core_competency_drywall_carpentry = self.extract_value("core_competency_drywall_carpentry")  # 09
        core_competency_ceramic_tile_stone = self.extract_value("core_competency_ceramic_tile_stone")  # 09
        core_competency_carpet_vct = self.extract_value("core_competency_carpet_vct")  # 09
        core_competency_paint_wallcovering = self.extract_value("core_competency_paint_wallcovering")  # 09
        core_competency_equipment = self.extract_value("core_competency_equipment")  # 11
        core_competency_sprinklers = self.extract_value("core_competency_sprinklers")  # 21
        core_competency_plumbing = self.extract_value("core_competency_plumbing")  # 22
        core_competency_hvac = self.extract_value("core_competency_hvac")  # 23
        core_competency_electrical = self.extract_value("core_competency_electrical")  # 26
        core_competency_other = self.extract_value("core_competency_other")  # 0

        supplier_category_codes = []
        if core_competency_demo:
            supplier_category_codes.append("02")
        if core_competency_concrete_masonry:
            supplier_category_codes.append("03")
        if core_competency_architectural_woodwork:
            supplier_category_codes.append("06")
        if core_competency_structural_steel or core_competency_hollow_metal or core_competency_metal_glass:
            supplier_category_codes.append("05")
        if core_competency_metal_glass or core_competency_window_treatments:
            supplier_category_codes.append("08")
        if (
            core_competency_drywall_carpentry
            or core_competency_ceramic_tile_stone
            or core_competency_carpet_vct
            or core_competency_paint_wallcovering
        ):
            supplier_category_codes.append("09")
        if core_competency_equipment:
            supplier_category_codes.append("11")
        if core_competency_sprinklers:
            supplier_category_codes.append("21")
        if core_competency_plumbing:
            supplier_category_codes.append("22")
        if core_competency_hvac:
            supplier_category_codes.append("23")
        if core_competency_electrical:
            supplier_category_codes.append("26")
        if core_competency_other:
            supplier_category_codes.append("0")

        supplier_categories = SupplierCategory.objects.filter(code__in=supplier_category_codes)

        self.company.contractor.supplier_categories.set(supplier_categories)
        self.company.contractor.save()

"""
1. Когда выход будет пуст? - если ни одно из заданных структурой списка полей не будет заполнено значениями
2. Если выход не пуст, то какова его голова? - код заполненного поля
3. Из каких данных рекурсивно строится хвост выхода? - из кодов оставшихся заполненных полей

NB: также можно немного улучшить метод, проверяющий заполненность поля
"""

class SensibleParser:
    Field = namedtuple("Field", ["name", "code"])
    ...
    def extract_value_code(self, field: Field) -> tuple[str | None, str | None]:
        doc_field = self.parsed_document[field.name]
        if doc_field:
            return doc_field["value"], field.code
        
        self.none_fields.append(field.name)
        return None, None

    
    def update_supplier_categories(self):
        """здесь или в ините определим поля для этого метода, которые сформируют структуру выходного списка"""

        code_list_structure = [
            Field("core_competency_demo", "02"),
            Field("core_competency_architectural_woodwork", "03"),
            Field("core_competency_architectural_woodwork", "06"),
            Field("core_competency_structural_steel", "05"),
            ...

        ]

        """Для целей этого метода нам не нужен список кодов, нам нужен сет, поскольку нет смысла в повторяющихся
        кодах
        """

        def rec_collect_set(active_codes: set, remain_codes: list) -> set:
            if not remain_codes:
                return active_codes
            
            _, code = self.extract_value_code(remain_codes[0])
            if code:
                return rec_collect_set(active_codes.add(code), remain_codes[1:])
            return rec_collect_set(active_codes, remain_codes[1:])

        supplier_categories = SupplierCategory.objects.filter(code__in=rec_collect_set({}, code_list_structure))

        self.company.contractor.supplier_categories.set(supplier_categories)
        self.company.contractor.save()
