#=
Некоторую классическую версию сопоставления с образцом можно добавить в Julia,
установив пакет Match.jl. Для этого надо запустить среду Julia, и в командной строке поочерёдно ввести две команды:

using Pkg
Pkg.add("Match")
=#

using Match
item = 1
@match item begin
    1 => println("one")
    2 => println("two")
    _ => println("Something else...")
 end
@ismatch [1,2,3] [a, b...]

# @match([1 2 3; 4 5 6], [[1,4], a, b]) не работает, в предыдущей версии вернуло бы а = [2,5], b = [3,6]
