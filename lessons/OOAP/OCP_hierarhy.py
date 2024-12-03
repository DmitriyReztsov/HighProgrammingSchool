from typing import Final, final


class General:
    VAR: Final[int] = 10

    @final
    def do_smth(self):
        print("Do smth from General")


class Any(General):
    VAR: int = 1

    def do_smth(self):
        print("Do smth from Any")


class AnotherAny(General):
    pass


any_object = Any()
any_object.do_smth()
# >>> Do smth from Any
print(any_object.VAR)
# >>> 1

another_any_object = AnotherAny()
another_any_object.do_smth()
# >>> Do smth from General
print(another_any_object.VAR)
# >>> 10


"""Только проверка тайп-чекером (mypy, например) укажет на ошибку:
HighProgrammingSchool/lessons/OOAP/OCP_hierarhy.py:13: error: Cannot assign to final name "VAR"  [misc]
HighProgrammingSchool/lessons/OOAP/OCP_hierarhy.py:15: error: Cannot override final attribute "do_smth" 
(previously declared in base class "General")  [misc]
Found 2 errors in 1 file (checked 1 source file)

Т.о. запрета на уровне языка нет, только на уровне договороенности и проверки типов.
"""
