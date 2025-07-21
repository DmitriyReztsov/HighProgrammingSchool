// 16.1
let notDivisible (n, m) =
    if n = 0 then false
    else m % n = 0

// 16.2
let prime n =
    if n <= 1 then false
    elif n = 2 then true
    else
    let mutable pivot = int(System.Math.Sqrt(n))
    let mutable is_prime = true
    while pivot > 1 && is_prime do
        if n % pivot = 0 then is_prime <- false
        pivot <- pivot - 1
    is_prime