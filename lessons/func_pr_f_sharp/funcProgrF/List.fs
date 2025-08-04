// 34.1
let rec upto n =
    
    let rec make_list i =
        match i with
            | i when i = n -> [i]
            | i -> i :: make_list (i + 1)
    make_list 1

// 34.2
let rec dnto n =
    match n with
    | n when n = 0 -> []
    | n -> n :: dnto (n - 1)

// 34.3
let rec evenn n =
    let rec make_list i =
        match i with
            | i when i = n -> [2 * (i - 1)]
            | i -> 2 * (i - 1) :: make_list (i + 1)
    make_list 1