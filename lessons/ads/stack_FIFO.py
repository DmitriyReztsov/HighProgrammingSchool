class Stack:
    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def pop(self):
        try:
            return self.stack.pop(0)
        except IndexError:
            return None

    def push(self, value):
        self.stack.append(value)

    def peek(self):
        try:
            return self.stack[0]
        except IndexError:
            return None
