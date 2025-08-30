namespace src


module Continuations =
    // 48.4.1
    let rec fibo1 n n1 n2 =
        if n = 0 then n2
        elif n = 1 then n1
        else fibo1 (n - 1) (n1 + n2) n1

    // 48.4.2
    let rec fibo2 n c =
        if n = 0 then c 0
        elif n = 1 then c 1
        else 
            fibo2 (n - 1) (fun f1 ->
                fibo2 (n - 2) (fun f2 ->
                    c (f1 + f2)))

    // 48.4.3
    let rec bigList n k = 
        let rec helper n acc =
            if n = 0 then acc
            else helper (n-1) (1:: k(acc))
        helper n []
    