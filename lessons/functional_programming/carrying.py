from pymonad.tools import curry


@curry(2)
def concat_strs(first_str: str, second_str: str) -> str:
    return first_str + second_str


def say_hello(name: str) -> str:
    hello = concat_strs("Hello, ")
    return hello("Dolly")


print(say_hello("Dolly"))  # Hello, Dolly


@curry(4)
def concat_four(hello: str, comma: str, exclamation: str, name: str) -> str:
    return f"{hello}{comma} {name}{exclamation}"


def say_another_hello(name: str) -> str:
    hello_partial = concat_four("Hello")(",")("!")
    return hello_partial(name)


print(say_another_hello("Petya"))
