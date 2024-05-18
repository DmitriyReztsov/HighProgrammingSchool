for s in ["one", "two", "three"]
    println(s)
end

for n in 1:10
    println(n)
end

n = 10
while n > 0
   println(n)
   #= n -= 1  переменная n локальна внутри цикла while
   (переменная n из присваивания n=10 -- это глобальная по отношению к циклу переменная),
   поэтому когда выполняется команда n -= 1, возникает ошибка,
   так как локальная переменная n пока не имеет значения.

   к этому комментарию есть вопросы...
   =#
   global n -= 1
end

println(">>>----------<<<<")

gl = 10
function try_gl()
    gl = 20
    while gl >= 9
        global gl -= 1
        println(gl)
    end
end
try_gl()