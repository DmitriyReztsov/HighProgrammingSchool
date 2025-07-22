// 16.1
let notDivisible (n, m) = n <> 0 && m % n = 0

// 16.2
let prime n =
    let rec checkDivisor pivot =
        pivot > 1 && (n % pivot = 0 || checkDivisor (pivot - 1))
    
    n > 1 && not (checkDivisor (int(System.Math.Sqrt(n))))