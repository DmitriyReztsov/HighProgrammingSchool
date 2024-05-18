print("Hello word!\n")
print(10÷3, "\n");
#= comment
on more than one
line
=#
# and on one line #
println(2 + 3.4)
println("Hello")
println("Hello"[2])  # e
n = 123
x = 23
println("n = $n ;") # n = 123 ;
println(" $(n*n-x)") # 15106
println('a')  # '' for char
println(" $(n=x)")

function fact(n)
    if n < 0
        return 1
    elseif n == 0
        return 1
    else
        return n * fact(n-1)
    end
end

println("fuctorial $(fact(BigInt(50)))")

function comb(n, r)
    div(fact(n), fact(r)*fact(n-r))
end
# the same, short form
comb(n, r) = div(fact(n), fact(r)*fact(n-r))
println(comb(10, 3))

function varargs(args...)
    return args
end
println("varargs $(varargs(1))")

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

