using Currier

@curried function foo(x, y, z)
    return x + y + z    
end

println(foo(1, 2, 3))
println(foo(1)(2)(3))

f = foo(1)(2)
println(f(3))

f = foo(1, 2)
println(f(3))