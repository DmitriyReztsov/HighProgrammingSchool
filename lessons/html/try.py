class A:
    def __new__(cls):
        cls.a = 1
        return super().__new__(cls)
    
    def __init__(self) -> None:
        self.a = 2

a = A()
pass
