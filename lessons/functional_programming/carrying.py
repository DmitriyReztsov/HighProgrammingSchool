from pymonad.tools import curry


#  2.3.1. Напишите каррированную функцию с двумя строковыми параметрами,
# которая вычисляет их сцепленное значение. Создайте на её основе функцию,
# которая получает один параметр и возвращает
# 
# Hello, значение-параметра
# 
# Это требуется, чтобы можно было выводить стандартное приветствие, задавая
# только имя.
@curry(2)
def concat_strs(first_str: str, second_str: str) -> str:
    return first_str + second_str


def say_hello(name: str) -> str:
    hello = concat_strs("Hello, ")
    return hello("Dolly")


print(say_hello("Dolly"))  # Hello, Dolly


# 2.3.2. Придумайте функцию, которая получает на вход четыре аргумента: слово
# привествия, знак препинания за ним, имя приветствуемого, и заключительный знак.

# Как сделать так, чтобы вариант её частичного применения получал бы в качестве
# единственного параметра только имя, а все остальные параметры настраивались бы
# другим вызовом?

# Например:

# final = first_step("Hello")(",")("!")
# final("Petya")

# Результатом будет

# Hello, Petya!
@curry(4)
def concat_four(hello: str, comma: str, exclamation: str, name: str) -> str:
    return f"{hello}{comma} {name}{exclamation}"


def say_another_hello(name: str) -> str:
    hello_partial = concat_four("Hello")(",")("!")
    return hello_partial(name)


print(say_another_hello("Petya"))
