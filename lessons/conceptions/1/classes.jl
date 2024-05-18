#=
Было бы удобно, если объекты из предыдущей секции можно было создавать массово по одному шаблону.
Допустим, нам надо 10 функций с внутренним состоянием, но каждый объект -- это уникальное описание функции,
поэтому в коде потребуется явно создать 10 формально разных, а фактически одинаковых объектов (функций с внутренней памятью).

Для этого можно создать "фабрику", которая может штамповать такие объекты автоматически в любом нужном количестве.
Такая фабрика называется класс.

Класс -- это функция, которая внутри себя создаёт новый объект и возвращает его как свой результат.
Такая возможность возврата функции (объект -- это функция) как результата работы функции -- типична для программирования высшего порядка.

В современном объектно-ориентированном программировании классы из соображений простоты и удобства трактуются как типы данных,
дополненные специальным синтаксисом (например, особой операцией создания нового экземпляра класса).
Класс объединяет некоторые данные (которые можно скрыть, инкапсулировать внутри класса) и операции над этими данными,
которые обычно называют методы. У каждого объекта, созданного по шаблону класса, своя собственная внутренняя память,
изолированная от других.

Такая парадигма называется объектно-базированной. Когда к ней добавляется концепция наследования, мы получаем классическое
объектно-ориентированное программирование. Наследование подразумевает, что новый класс может быть определён в терминах уже
существующих классов: достаточно лишь специфицировать, в чём новый класс от них отличается. У этого подхода имеется много
специфических особенностей реализации в каждом языке, которые приходится детально изучать. 
=#

#= OOP
1. Пользовательские типы данных в Julia

В Julia отсутствует понятие "класс" из классического ООП. Julia допускает определение типов данных на основе так называемых
структур или записей, имеющихся во многих популярных языках программирования.
Прим.: статическая проверка типов в Julia отсутствует.

Структура объединяет только именованые значения, она фактически то же самое, что и класс, в котором отсутствуют методы.
Экземпляр структуры создаётся с помощью условного "конструктора" -- имени структуры (типа),
за которым в скобках перечислены начальные значения его полей в том порядке, в каком они определены в описании структуры.

Например, следующий код задаёт структуру (тип) данных Tiger с двумя полями -- taillength вещественного типа,
и coatcolor строкового типа. Далее создаётся экземпляр Tiger (объект) с именем tigger.

struct Tiger
    taillength::Float64
    coatcolor::String
end

tigger = Tiger(3.5, "orange")
println(tigger) # Tiger(3.5, "orange")

Тип любого объекта можно получить с помощью функции typeof(tigger)

typeof(tigger) # Tiger

Однако принципиальный момент, что "объекты" Julia по умолчанию иммутабельны -- значения их полей изменять нельзя.
Так, следующий код выдаст ошибку:

tigger.taillength = 3.3

Можно явно указать, что структура мутабельна, с помощью ключевого слова mutable:

mutable struct Tiger
    taillength::Float64
    coatcolor::String
end

tigger = Tiger(3.5, "orange")
tigger.taillength = 3.3
println(tigger) # Tiger(3.3, "orange")

Но такой подход настоятельно не рекомендуется, независимо от того, в какой парадигме вы работаете.
Когда используются только иммутабельные структуры, конечно, каждый раз чистые функции будут создавать их копии,
что создаёт дополнительную нагрузку, и тем не менее её стоит принести в жертву общей выразительности и чистоте кода.

В ситуациях, когда всё же имеются очень веские основания создавать мутабельные объекты, порекомендую библиотеку Accessors.jl
("to make updating immutable data simple"):
github.com/JuliaObjects/Accessors.jl

2. Наследование в Julia

В Julia можно создавать новые типы данных на основе ранее определённых структур, однако "наследование в лоб"
не поддерживается по достаточно глубоким причинам. В частности, из-за того, что структуры -- это совсем не классы,
а обрабатываются они с помощью так называемой схемы multiple dispatch.

Простой способ, в детали которого вдаваться не будем -- это объявить родительский класс абстрактным с помощью
ключевого слова abstract, что означает, что создание реальных объектов на его основе не допускается.

abstract type Cat end

Но зато теперь на его основе можно создавать другие структуры (типы данных) с помощью "оператора" наследования <: ,
который на самом деле в computer science и теории ООП известен как subtyping operator.

На основе типа Cat создадим его "наследников" (правильно говорить subtype, но на русском, к сожалению,
так и не появилось качественного перевода):

abstract type Cat end

struct Lion <: Cat
    maneColor::String
    roar::String
end

struct Panther <: Cat
    eyeColor::String
end

li = Lion("green", "rrr")
println(li) # Lion("green", "rrr")

3. subtype() и supertype()

Функция supertype(тип) возвращает "родительский" тип для типа-аргумента.
Самым верхним супертипом в иерархии типов Julia будет тип Any.
Например:

supertype(Int64)    # => Signed
supertype(Signed)   # => Integer
supertype(Integer)  # => Real
supertype(Real)     # => Number
supertype(Number)   # => Any

Соответственно, фунция subtypes() возвращает список типов-"наследников" данного.
Список, потому что их может быть больше одного, в отличие от "предка" (когда множественное наследование не поддерживается).

4. Передача по ссылке и по значению

Хотя в других языках программирования структуры обычно передаются по значению, в Julia они передаются по ссылке,
как обычные объекты.

abstract type Cat end

mutable struct Lion <: Cat
    maneColor::String
    roar::String
end

function change(l::Lion)
    l.roar = "GHr"
end

li = Lion("green", "rrr")
println(li) # Lion("green", "rrr")
change(li)
println(li) # Lion("green", "GHr")

5. "Полиморфизм" в Julia

Так как методы в структурах Julia недопустимы, применяется потенциально более мощный механизм,
называемый multiple dispatch. Наивное объяснение его таково, что в программе допускается определить сколько угодно функций
с одинаковыми именами и одинаковыми количествами параметров, которые будут отличаться только типами своих параметров.

Выбор подходящей функции в момент её вызова будет выполнен автоматически в зависимости от типов конкретных аргументов.
В классической реализации ООП такой полиморфизм реализуется в более простой форме, на основании типа только первого параметра
метода (this, self, ...).

abstract type Cat end

struct Lion <: Cat
    maneColor::String
    roar::String
end

struct Panther <: Cat
    eyeColor::String
end

mutable struct Tiger
    taillength::Float64
    coatcolor::String
end

function test(t::Tiger)
    t.taillength += 15.0
    t.taillength
end

function test(p::Panther)
    "grrr"
end

function test(l::Lion)
    l.roar
end

li = Lion("green", "rrr")
pant = Panther("gray")
t = Tiger(55.5, "white")

println(test(li))   # "rrr"
println(test(pant)) # "grrr"
println(test(t))    # 70.5

Чуть более сложный пример по multiple dispatch:

mutable struct Tiger
    taillength::Float64
    coatcolor::String
end

#

abstract type Cat end

struct Lion <: Cat
    maneColor::String
    roar::String
end

struct Panther <: Cat
    eyeColor::String
end

#

function fight(t::Tiger, c::Cat)
    println("The $(t.coatcolor) tiger wins!")
end

fight(t::Tiger, l::Lion) = println("The $(l.maneColor)-maned lion wins!")

#

tigra = Tiger(55.5, "white")

fight(tigra, Panther("blue")) # The white tiger wins!
fight(tigra, Lion("yellow","R")) # The yellow-maned lion wins!

fight(Panther("brown"), Lion("red","RAWR"))
# Load Error: no method matching fight(::Panther, ::Lion)
 

Чтобы избежать последнего бага, надо добавить такую функцию:

fight(c::Cat, l::Lion) = println("The cat beats the Lion")
fight(Panther("brown"), Lion("red","RAWR")) # The cat beats the Lion  

Запомните этот пример, он потребуется в последующих тестах. 
=#

# struct Tiger
#     taillength::Float64
#     coatcolor::String
# end

# tigger = Tiger(3.5, "orange")
# sherekhan = typeof(tigger)(5.6, "fire")

# mutable struct Tiger
#     taillength::Float64
#     coatcolor::String
# end

# abstract type Cat end

# supertype(Cat) == supertype(Tiger)

mutable struct Tiger
    taillength::Float64
    coatcolor::String
end

#

abstract type Cat end

struct Lion <: Cat
    maneColor::String
    roar::String
end

struct Panther <: Cat
    eyeColor::String
end

#

function fight(t::Tiger, c::Cat)
    println("The $(t.coatcolor) tiger wins!")
end

fight(t::Tiger, l::Lion) = println("The $(l.maneColor)-maned lion wins!")

#

tigra = Tiger(55.5, "white")

fight(tigra, Panther("blue")) # The white tiger wins!
fight(tigra, Lion("yellow","R")) # The yellow-maned lion wins!

# fight(Panther("brown"), Lion("red","RAWR"))
# Load Error: no method matching fight(::Panther, ::Lion)

fight(c::Cat, l::Lion) = println("The cat beats the Lion")
fight(Panther("brown"), Lion("red","RAWR")) # The cat beats the Lion

fight(c::Lion, l::Cat) = println("The Lion beats cat!")
fight(Lion("yellow","R"), Lion("brown","Rr"))  # ERROR: MethodError: fight(::Lion, ::Lion) is ambiguous.