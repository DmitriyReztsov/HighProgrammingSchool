// 16.1
let notDivisible = fun (n, m) -> n <> 0 && m % n = 0

// 16.2
let prime =
    let rec checkDivisor (n, pivot) =
        pivot > 1 && (n % pivot = 0 || checkDivisor (n, pivot - 1))
    
    fun n -> n > 1 && not (checkDivisor (n, int(System.Math.Sqrt(float n))))