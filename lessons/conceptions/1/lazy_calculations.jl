#=
 В Julia ленивые вычисления поддерживаются пакетом Lazy. Добавьте его в систему:

using Pkg
Pkg.add("Lazy")

В простейшем случае, ленивые вычисления означают, что например элементы списка не будут вычисляться,
пока они не затребованы непосредственно.
Пакет Lazy вводит новый тип List (ленивый список), который сам по себе содержит базовые операции
для классической работы со списками.

Например, список 1,2,3 с помощью этого ленивого типа запишется так:

using Lazy
x = list(1,2,3)
println(x) # List: (1 2 3)

Над списком возможны операции first (получить голову) и tail (получить хвост):

println(first(x)) # 1
println(tail(x)) # List: (2 3)

в Julia разрешается запись списков в каноническом виде:

H|T

(вместо "|" в Julia используется ":" ).
Например,

1:list(2,3)

означает список list(1,2,3).
При этом связок элементов ":" в такой записи списка может быть несколько,
а между ними разрешается использовать не только константы, но и выражения,
что сразу даёт нам мощный механизм формирования ленивых конструкций.

Например, мы хотим определить функцию, которая генерирует бесконечный ленивый список
последовательных целых чисел, начиная с заданного. В компактной форме она запишется так:

lazy(n) = n:lazy(n+1)

Однако при её вызове, например, lazy(5) система вылетит с ошибкой времени выполнения --
переполнение стека. Это понятно: функция начинает сразу энергично генерировать бесконечный список,
хотя пока им никто пользоваться не собирается.

Поэтому подключим модуль Lazy и инструкцией @lazy укажем, что вычисление должно проходить лениво:

using Lazy
lazy(n) = @lazy n:lazy(n+1)
print(lazy(5))

Мы мгновенно получим результат:
List: (5 6 7 8 9 10 11 12 13 14 15 ...)
где многоточие в конце намекает, что список бесконечный. На самом деле, конечно, он не вычислялся,
а просто при запросе print() было сгененировано несколько первых значений.

В Julia существует специальная команда take, которая позволяет получить нужное количество значений
от генератора таких бесконечных последовательностей (они обычно называются итераторы).
Например, получить список из первых пяти значений:

println(take(5, lazy(25))) # List: (25 26 27 28 29)

=#

using Lazy
lazy(n) = @lazy n:lazy(n+1)
println(lazy(5))
println(take(5, lazy(25)))

#=
Обобщённая версия генератора последовательностей. Её можно сделать, передав функцию, вычисляющую следующее значение,
как аргумент нашей функции lazy. Вот такая способность передавать функции в другие функции через их параметры --
когда функции сами выступают значениями -- и называется программирование высшего порядка
(в русскоязычной программистской литературе более распространён термин "функции высшего порядка").

lazy(n, f) = @lazy n:lazy(f(n), f) 

Например, мы хотим вычислить последовательность, каждый следующий элемент которой в два раза больше предыдущего.
Определим соответствующую функцию:

function f2(x) 
  return x * 2
end

И вызовем lazy (запросим первые пять значений, начиная с 7):

take(5, lazy(7, f2)) # List: (7 14 28 56 112)
=#

lazy(n, f) = @lazy n:lazy(f(n), f) 

function f2(x) 
    return x * 2
end

take(5, lazy(7, f2))

#=
Функция constantly() из пакета Lazy.jl создаёт бесконечный ленивый список,
составленный из повторения аргумента constantly

Функция repeatedly() по аналогии с constantly() создаёт бесконечный ленивый список,
только получает в качестве аргумента функцию, а не значение, и заполняет список вызовами этой функции.
=#