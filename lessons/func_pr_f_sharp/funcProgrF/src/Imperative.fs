namespace src


module Imperative =
    // 47.4.1
    let f n =
        if n = 0 then 1
        else
            let mutable fact = 1
            let f_helper result = fact <- fact * result
            List.iter f_helper [1 .. n]
            fact


    // 47.4.2
    let fibo n =
        let mutable pre_pre = 0
        let mutable pre = 1
        let i = ref 3

        while ! i <= n do
            let new_pre = pre + pre_pre
            pre_pre <- pre
            pre <- new_pre
            i := ! i + 1
        
        pre
