exception LengthListsException

// 39.1
let rec rmodd =
    function
    | [] -> []
    | [even] -> []
    | even :: (odd :: l) -> [odd] @ rmodd l

// 39.2
let rec del_even =
    function
    | [] -> []
    | elem :: l when elem % 2 = 0 -> del_even l
    | elem :: l -> [elem] @ del_even l

// 39.3
let rec multiplicity x xs =
    match xs with
    | [] -> 0
    | head :: l when x = head -> 1 + multiplicity x l
    | _ :: l -> multiplicity x l

// 39.4
let rec split =
    function
    | [] -> ([], [])
    | left :: l when l = [] -> ([left], [])
    | left :: (right :: l) -> 
        let (lefts, rights) = split l
        (left :: lefts, right :: rights)
    | _ -> ([], [])

// 39.5
let rec zip (xs1, xs2) =
    match xs1, xs2 with
    | [], [] -> []
    | x::xs, y::ys -> (x, y) :: zip (xs, ys)
    | _ -> raise LengthListsException
