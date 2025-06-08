from typing import Callable

from pymonad.tools import curry
from pymonad.reader import Compose


# 3.1. Напишите функцию частичного применения tag(), которая получает на вход два строковых параметра: название
# HTML-тега, и значение. Эта функция оборачивает значение тегом с учётом открывающего и закрывающего тега, например:
# tag('b', 'string') # <b>string</b>
# На основе tag подготовьте две функции bold и italic, которые оборачивают значение в теги b и i.
@curry(2)
def tag(tag_name: str, text: str) -> str:
    return f"<{tag_name}>{text}</{tag_name}>"


bold = tag("b")
italic = tag("i")

print(bold("bold text"))  # <b>bold text</b>
print(italic("italic text"))  # <i>italic text</i>


# 3.2. Расширьте функцию tag третьим параметром attr (тип словарь), который добавляет к тегу набор свойств (их может
# быть несколько).
# Например:
# tag('li', {'class': 'list-group'}, 'item 23')
# Результатом будет
# <li class="list-group">item 23</li>
@curry(3)
def tag(tag_name: str, attr: dict, text: str) -> str:
    attrs_list = []
    for at_key, at_value in attr.items():
        attrs_list.append(f" {at_key}={at_value},")
    attrs_list[-1] = attrs_list[-1][:-1]
    attrs_text = "".join(attrs_list)
    return f"<{tag_name}{attrs_text}>{text}</{tag_name}>"


bold_list = tag("b", {"class": "list-group"})
italic_list = tag("i", {"class": "list-group"})

print(bold_list("bold text"))  # <b class=list-group>bold text</b>
print(italic_list("italic text"))  # <i class=list-group>italic text</i>


def bold_tag(curried_func: Callable) -> Callable:
    return curried_func("b")


def italic_tag(curried_func: Callable) -> Callable:
    return curried_func("i")


def list_class(curried_func: Callable) -> Callable:
    return curried_func({"class": "list-group"})


@curry(3)
def tag2(text: str, tag_name: str, attr: dict) -> str:
    attrs_list = []
    for at_key, at_value in attr.items():
        attrs_list.append(f" {at_key}={at_value},")
    attrs_list[-1] = attrs_list[-1][:-1]
    attrs_text = "".join(attrs_list)
    return f"<{tag_name}{attrs_text}>{text}</{tag_name}>"


bold_list = Compose(tag2).then(bold_tag).then(list_class)
print(bold_list("bold text"))  # <b class=list-group>bold text</b>
print(italic_list("italic text"))  # <i class=list-group>italic text</i>
