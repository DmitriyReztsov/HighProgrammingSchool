from abc import ABC, abstractmethod


class WeaponBehavior(ABC):
    @abstractmethod
    def use_weapon(self):
        pass


class KnifeBehavior(WeaponBehavior):
    def use_weapon(self): ...


class SwordBehavior(WeaponBehavior):
    def use_weapon(self): ...


class Character:
    def set_weapon(self, weapon: WeaponBehavior):
        self.weapon = weapon

    def fight(self):
        ...
        self.weapon.use_weapon()


class King(Character): ...


class Knight(Character): ...


king = King()
sword = SwordBehavior()

king.set_weapon(sword)
king.fight()

"""В Питоне по сути все объекты имеют позднее, динамическое связывание. С теоретическй точки зрения если разобрать
вышеприведенный код, то можно сказать, что метод use_weapon() имеет (имел бы в Java) динамическое связывание,
поскольку вызывается на объекте, который определяется в моменте работы программы, может изменяться, но в любом
случае класс этого объекта должен реализовывать интерфейс WeaponBehavior (в Питоне - абстрактный класс) с этим методом.
"""
