def brackets_are_correct(inp: str) -> bool:
    stack = []
    for sk in inp:
        if sk == "(":
            stack.append(sk)
        elif len(stack) > 0 and sk == ")":
            stack.pop()
        else:
            return False
    return len(stack) == 0
