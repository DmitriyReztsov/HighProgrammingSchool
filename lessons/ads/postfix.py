from typing import List


def calculate_postfix(postfix: List[str]) -> int:
    aux_stack: List = []
    for position in postfix:
        if position.isdigit():
            aux_stack.append(position)
        elif position == "=":
            return aux_stack[0]
        else:
            second_operand = aux_stack.pop()
            first_operand = aux_stack.pop()
            res = eval(first_operand + position + second_operand)
            aux_stack.append(str(res))
