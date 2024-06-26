[1,2,3,5,8]
x = [] # пустой список

#=  Новый узел записывается как H|T, где H -- значение нового элемента,
и T -- оставшаяся часть цепочки узлов. Например, начинаем со списка Z=[].
Добавляем первый узел Y=7|Z, и затем второй узел X=6|Y.
Теперь X ссылается на список из двух узлов, который может быть записан как [6, 7].

Узел H|T часто называется cons -- термин, который пришёл из языка Лисп.
=#

Z = [6, 7]
pushfirst!(Z, 5) # Z == [5,6,7]
#= Символ ! в конце функции добавления означает, что она модифицирует значение своих аргументов
(в данном случае, изменится значение списка Z).
По умолчанию все аргументы передаются в функции Julia по ссылке, если позволяет их тип.

К последнему элементу массива можно обратиться с помощью условного индекса end: 
Z[end] # 7
Z[end - 1] # 6
=#

popfirst!(Z) # Z == [6,7]

#= Сцепление списков (добавление второго списка в хвост первого списка) выполняет команда append!
Добавление элемента в хвост списка выполняет команда push!
Создание массива длиной N вещественных чисел, заполненного нулями, выполняет команда zeros:
=#

X = [8, 9, 10]
append!(Z, X)
println("After apend $(Z)")

push!(X, 11)
println("After push $(X)")

a = zeros(5)
println("Zeros $(a)")  # [0.0, 0.0, 0.0, 0.0, 0.0]
