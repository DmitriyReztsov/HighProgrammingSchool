namespace src


module Lazy =
    type 'a cell = Nil | Cons of 'a * Lazy<'a cell>

    let hd (s : 'a cell) : 'a =
        match s with
        | Nil -> failwith "hd"
        | Cons (x, _) -> x

    let tl (s : 'a cell) : Lazy<'a cell> =
        match s with
        | Nil -> failwith "tl"
        | Cons (_, g) -> g


    // 51.3
    let rec nth (s : 'a cell) (n : int) : 'a =
        match n with
        | 0 -> hd s
        | i -> 
            let new_s = tl s
            nth (new_s.Force()) (i - 1)

    let rec nat (n: int) : int cell = Cons (n, lazy(nat(n+1)))

    let n0 = nat 0
    // например, получить 30000-й элемент:
    // nth n0 30000