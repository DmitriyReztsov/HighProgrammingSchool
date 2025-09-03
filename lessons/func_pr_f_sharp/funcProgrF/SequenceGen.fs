// 49.5.2
let fac_seq = seq {
    let i = ref 0
    let mutable result = 1

    while true do
        if ! i = 0 then yield result
        else
            result <- result * ! i
            yield result
        i := ! i + 1
}
    
// 49.5.3
let seq_seq = seq {
    let i = ref 0

    while true do
        if ! i % 2 = 1 then -1 * (! i / 2 + 1)
        else ! i / 2
        i := ! i + 1
}
