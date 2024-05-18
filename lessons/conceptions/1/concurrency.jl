import Base.Threads

# Threads.@threads for i = 1:10
#     println("i = $i on thread $(Threads.threadid())")
# end


# x = 0
# Threads.@threads for i = 1:10
#     global x = i
# end
# println(x)

acc = Ref(0)
Threads.@threads for i in 1:1000
    acc[] += 1
end
println(acc[])