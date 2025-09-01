namespace src


module Sequence =
    // 49.5.1
    let even_seq = Seq.initInfinite (fun i -> i * 2)

    // 49.5.2
    let rec factorial i = 
        match i with
        | i when i = 0 -> 1
        | i -> i * factorial (i-1)

    let fac_seq = Seq.initInfinite (fun i -> factorial i)
        
    // 49.5.3
    let seq_seq = Seq.initInfinite (
        fun i ->
            if i % 2 = 1 then -1 * (i / 2 + 1)
            else i / 2
        )