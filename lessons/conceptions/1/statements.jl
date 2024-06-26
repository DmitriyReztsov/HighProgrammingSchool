#=
В идеале функция должна иметь какую-то внутреннюю память. Тогда функция может как-то менять своё поведение
от вызова к вызову, для примера, улучшая его. Такого рода память называется явное (эксплицитное) состояние.
Как и в случае с параллелизмом, явные состояния в существенной степени моделируют реальный мир.

Например, мы хотим знать, сколько раз вызовется некая функция f(). Для этого в неё надо добавить явное состояние.

Существует множество способов определения явного состояния. Самый простой -- это выделить для него одну ячейку памяти.
Это своего рода коробка, в которую можно поместить любое содержимое. Во многих языках программирования её называют "переменная".
Пока мы будем называть её "ячейка" (физически существующая в памяти компьютера),
чтобы избежать путаницы с переменными, которые больше похожи на математические переменные, т.е. служат просто ярлыками
для значений на фазе компиляции.

Формально для работы с ячейкой требуются три операции: создание (выделение) ячейки памяти,
запись значения в ячейку и считывание значения из ячейки. На практике они скрыты за классическими переменными.

count = 0

function f(x)
    global count += 1
    return x*x
end

f(1)
f(1)
f(12)
println(count) # 3

=#

someVar = 5
try
    someOtherVar
catch e
    println(e)  # UndefVarError(:someOtherVar)
end

ку = 0.00001
привет = "Hello"
привет = ку
println(привет)

# print(pi)
pi = 3
print(pi)

#= Objects
Функции с внутренним состоянием, которое в них интегрировано и недоступно за пределами функции,
обычно называются объекты (которые не надо путать с объектами из объектно-ориентированного программирования).
Это естественный переход - от предыдущего варианта, когда пришлось определять отдельную переменную
count во всей программе, а внутри функции обращаться к ней с префиксом global, - к концепции объекта,
расширяющего функцию внутренней памятью. Причём эта внутренняя память скрывается от внешнего мира внутри функции --
инкапсулируется, и доступа к ней никакого нету.

Поддержка такой парадигмы (функция с локальной ячейкой внутри как одно целое -- объект) сегодня реализована
в единичных довольно экзотических языках. 
=#