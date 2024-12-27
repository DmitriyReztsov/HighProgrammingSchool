# 7. implementation inheritance. Метод get_signature() наследуюется в неизменном виде, но структура объекта
# GovernmentContract расширяется дополнительными атрибутами
class Contract:
    def __init__(self, one_side, another_side, amount):
        self.one_side = one_side
        self.another_side = another_side
        self.amount = amount

    def get_signature(self, one_sign, another_sign):
        self.one_sign = one_sign
        self.another_sign = another_sign


class GovernmentContract(Contract):
    def __init__(self, one_side, another_side, amount, is_verified=False, is_tender_required=False):
        super().__init__(one_side, another_side, amount)
        self.is_verified = is_verified
        self.is_tender_required = is_tender_required


# 8. facility inheritance.
class PageSettingsGeneral:
    DEFAULT_FONT: str = "Times-Roman"
    DEFAULT_FONT_SIZE: int = 9
    DEFAULT_BOTTOM_MARGIN: float = 1 * inch
    DEFAULT_LEFT_MARGIN: float = 0.75 * inch
    DEFAULT_RIGHT_MARGIN: float = 0.5 * inch
    PARAGRAPH_VERT_SPACE: float = 0.1 * inch
    DEFAULT_FIRST_LINE_INDENT: float = 0.2 * inch
    DEFAULT_PAGE_SIZE: tuple[float, float] = A4
    DEFAULT_TOP_MARGIN: float = 0.5 * inch


class TextToPdf(PageSettingsGeneral, ...): ...


class HtmlToPdf(PageSettingsGeneral, ...): ...


class PdfToPdf(PageSettingsGeneral, ...): ...
