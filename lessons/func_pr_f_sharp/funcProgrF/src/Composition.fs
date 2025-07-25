namespace src


module Composition =

    // 20.3.1
    let vat n x = x + x * float n / 100.0

    // 20.3.2
    let unvat n x = x / (1.0 + float n / 100.0)

    // 20.3.3
    let rec min f =
        let rec minF n =
            if f n = 0 then n
            else minF (n + 1)
        minF 0
