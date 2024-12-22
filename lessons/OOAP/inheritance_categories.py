# 1. subtype inheritance. В части реализации интерфейса (абстрактного класса) происходит
# расделение общего класса ObjToPdf на подтипы со своими независимыми реализациями
# общего метода get_pdf_file()
class ObjToPdf(ABC):
    @abstractmethod
    def get_pdf_file(self, file_name: str, created_by: User, settings: dict | None) -> File: ...


class TextToPdf(ObjToPdf):
    PARAGRAPH_VERT_SPACE: float = 0.1 * inch
    DEFAULT_FONT: str = "Times-Roman"
    DEFAULT_FONT_SIZE: int = 9
    DEFAULT_FIRST_LINE_INDENT: float = 0.2 * inch

    def __init__(self, text_blocks: list[str], text_settings: dict = None) -> None:
        self.text_blocks = self._trim_text_blocks(text_blocks)
        self.trimmed_text_blocks = []
        if text_settings:
            for attr_name, attr_value in text_settings.items():
                setattr(self, attr_name, attr_value)
        else:
            self._set_text_settings()

    def _set_text_settings(self):
        self.paragraph_vert_space = self.PARAGRAPH_VERT_SPACE
        self.font = self.DEFAULT_FONT
        self.font_size = self.DEFAULT_FONT_SIZE
        self.first_line_indent = self.DEFAULT_FIRST_LINE_INDENT

    def _trim_text_blocks(self, text_blocks: list[str]) -> list[str]:
        for block in text_blocks:
            self.trimmed_text_blocks.extend(block.split("\n"))

    def _page_settings(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.font, self.font_size)
        canvas.restoreState()

    def _buffer_text_blocks_to_pdf(
        self,
        page_size: tuple[float, float],
        left_margin: float,
        right_margin: float,
        top_margin: float,
        bottom_margin: float,
    ) -> BytesIO:
        buffer = BytesIO()

        doc = BaseDocTemplate(
            buffer,
            pagesize=page_size,
            leftMargin=left_margin,
            rightMargin=right_margin,
            topMargin=top_margin,
            bottomMargin=bottom_margin,
        )
        doc_content = []
        style_sheet = getSampleStyleSheet()
        style = style_sheet["Normal"]
        style.firstLineIndent = self.first_line_indent

        for text in self.text_blocks:
            paragrath = Paragraph(text, style)
            doc_content.append(paragrath)
            doc_content.append(Spacer(1, self.paragraph_vert_space))

        regular_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="regular")
        doc.addPageTemplates(PageTemplate(id="regular", frames=regular_frame, onPage=self._page_settings))
        doc.build(doc_content)

        return buffer

    def get_pdf_file(
        self,
        file_name: str,
        doc_settings: dict,
    ) -> File:
        buffer = self._buffer_text_blocks_to_pdf(
            page_size=doc_settings["page_size"],
            left_margin=doc_settings["left_margin"],
            right_margin=doc_settings["right_margin"],
            top_margin=doc_settings["top_margin"],
            bottom_margin=doc_settings["bottom_margin"],
        )

        created_filename = f"{file_name}.pdf"
        return File(buffer, created_filename)


class HtmlToPdf(ObjToPdf):
    def __init__(self, html_blocks: list[str]) -> None:
        self.html_blocks = html_blocks

    def _buffer_html_blocks_to_pdf(
        self,
        page_size: tuple[float, float],
        left_margin: float,
        right_margin: float,
        top_margin: float,
        bottom_margin: float,
    ) -> BytesIO:
        buffer = BytesIO()

        html_object = HTML(string="".join(self.text_blocks))
        css_object = CSS(
            string=(
                f"@page {{ size: {page_size}; "
                f"margin-top: {top_margin}px; "
                f"margin-right: {right_margin}px; "
                f"margin-bottom: {bottom_margin}px; "
                f"margin-left: {left_margin}px }}"
            )
        )
        html_object.write_pdf(buffer, stylesheets=[css_object])

        return buffer

    def get_pdf_file(
        self,
        file_name: str,
        doc_settings: dict,
    ) -> DjangoFile:
        buffer = self._buffer_html_blocks_to_pdf(
            page_size=doc_settings["page_size"],
            left_margin=doc_settings["left_margin"],
            right_margin=doc_settings["right_margin"],
            top_margin=doc_settings["top_margin"],
            bottom_margin=doc_settings["bottom_margin"],
        )

        created_filename = f"{file_name}.pdf"
        return DjangoFile(buffer, created_filename)


# 3. extension inheritance. Тут происходит расширение класса за счет добавления еще одного
# открытого метода set_footer_to_pdf_file(), которого нет в других классах-потомках ObjToPdf.
# Возможно, его следовало бы выделить в отдельный класс, но тут мои соображения были следущие:
# в остальных классах тоже могут появиться методы для установки коллонтитулов, которые сейчас
# пока не нужны; все эти объекты должны реализовывать интерфейс get_pdf_file() для передачи в
# сервисный класс и полиморфного вызова этого метода там.
class PdfToPdf(ObjToPdf):
    DEFAULT_FONT: str = "Times-Roman"
    DEFAULT_FONT_SIZE: int = 9
    DEFAULT_BOTTOM_MARGIN: float = 1 * inch
    DEFAULT_LEFT_MARGIN: float = 0.75 * inch
    DEFAULT_RIGHT_MARGIN: float = 0.5 * inch

    def __init__(self, input_file: DjangoFile) -> None:
        self.input_file = input_file

    def get_pdf_file(
        self,
        file_name: str,
        doc_settings: dict,
    ) -> DjangoFile:
        return self

    def set_footer_to_pdf_file(
        self,
        footer_text_lines: dict[int, str],
        left_margin: float = None,
        bottom_margin: float = None,
        right_margin: float = None,
        font: str = None,
        font_size: int = None,
    ) -> File:
        """Footer text is a dictionary with 1 to 3 items, where key is a line oreder started from 0
        and value is string to be placed there.
        There are space for three lines.
        Note, that placing another text on existing line will lead to mess. You should control this by yourself.
        """
        font = font or self.DEFAULT_FONT
        font_size = font_size or self.DEFAULT_FONT_SIZE
        left_margin = left_margin or self.DEFAULT_LEFT_MARGIN
        bottom_margin = bottom_margin or self.DEFAULT_BOTTOM_MARGIN
        right_margin = right_margin or self.DEFAULT_RIGHT_MARGIN
        output_file_name = self.input_file.name

        self.input_file.seek(0)
        output_buffer = BytesIO()

        # Get pages
        reader = PdfReader(self.input_file)
        pages = [pagexobj(p) for p in reader.pages]

        # Compose new pdf
        canvas = Canvas(output_buffer)

        for page_num, page in enumerate(pages, start=1):
            # Add page
            canvas.setPageSize((page.BBox[2], page.BBox[3]))
            canvas.doForm(makerl(canvas, page))

            # Draw footer
            canvas.saveState()
            canvas.setStrokeColorRGB(0, 0, 0)
            canvas.setLineWidth(0.5)
            canvas.line(left_margin, bottom_margin, page.BBox[2] - right_margin, bottom_margin)
            canvas.setFont(font, font_size)

            for line_num, line_text in footer_text_lines.items():
                canvas.drawString(
                    left_margin,
                    bottom_margin - 0.2 * inch - line_num * font_size,  # indent from the first line
                    line_text,
                )

            canvas.restoreState()

            canvas.showPage()

        canvas.save()

        return File(output_buffer, output_file_name)


# 2. restriction inheritance. Для Джанги это примеры с сериализаторами. Например, у нас есть
# общий сериализатор для работы со всеми полями модели и стандартной валидацией (на основе полей модели)
class GeneralSerializer(ModelSerializer):
    class Meta:
        model = SomeModel
        fields = "__all__"  # плохая практика, только для примера


# от него мы можем унаследовать сериалайзер с ограниченным набором полей и более строгой валидацией
class ParticularSerialiser(GeneralSerializer):
    field1 = ...
    field2 = ...

    class Meta(GeneralSerializer.Meta):
        fields = [
            "field1",
            "field2",
        ]

    def validate_field1(self, data):
        ...
        return data

    def validate(self, data):
        ...
        return data
