namespace src


module Practice =
    // 40.1
    let rec sum (p, xs) =
        match xs with
        | [] -> 0
        | elem :: l when p elem -> elem + sum (p, l)
        | _ :: l -> sum (p, l)

    // 40.2.1
    let rec count (xs, n: int) =
        match xs with
        | [] -> 0
        | elem :: l when elem > n -> 0
        | elem :: l when elem = n -> 1 + count (l, n)
        | _ :: l -> count (l, n)

    // 40.2.2
    let rec insert (xs, n: int) =
        match xs with
        | [] -> [n]
        | elem :: l when n <= elem -> n :: elem :: l
        | elem :: l -> elem :: insert (l, n)

    // 40.2.3
    let rec intersect (xs1: list<int>, xs2: list<int>) =
        match xs1, xs2 with
        | l1, l2 when l1 = [] || l2 = [] -> []
        | el1 :: l1, el2 :: l2 when el1 = el2 -> el1 :: intersect (l1, l2)
        | el1 :: l1, (el2 :: l as l2) when el1 < el2 -> intersect (l1, l2)
        | (el1 :: l as l1), el2 :: l2 when el1 > el2 -> intersect (l1, l2)
        | _, _ -> []

    // 40.2.4
    let rec plus (xs1: list<int>, xs2: list<int>) =
        match xs1, xs2 with
        | [], [] -> []
        | [], l2 -> l2
        | l1, [] -> l1
        | el1 :: l1, el2 :: l2 when el1 = el2 -> el1 :: el2 :: plus (l1, l2)
        | el1 :: l1, (el2 :: _ as l2) when el1 < el2 -> el1 :: plus (l1, l2)
        | (el1 :: _ as l1), el2 :: l2 when el1 > el2 -> el2 :: plus (l1, l2)
        | _, _ -> []

    // 40.2.5
    let rec minus (xs1: list<int>, xs2: list<int>) =
        match xs1, xs2 with
        | [], _ -> []
        | l1, []  -> l1
        | el1 :: l1, el2 :: l2 when el1 = el2 -> minus (l1, l2)
        | el1 :: l1, (el2 :: _ as l2) when el1 < el2 -> el1 :: minus (l1, l2)
        | (el1 :: _ as l1), el2 :: l2 when el1 > el2 -> minus (l1, l2)
        | _, _ -> []

    // 40.3.1
    let rec smallest =
        function
        | [] -> None
        | elem :: [] -> Some(elem): Option<int>
        | elem :: l ->
            if elem < Option.get(smallest l) then Some(elem)
            else smallest l

    // 40.3.2
    let rec delete (n: int, xs: list<int>) =
        match xs with
        | [] -> []
        | elem :: l when elem = n -> l
        | elem :: l -> elem :: delete (n, l)

    // 40.3.3
    let rec sort = function
        | [] -> []
        | l -> Option.get (smallest l) :: sort (delete (Option.get (smallest l), l))

    let splitList list =
        let rec split count acc rest =
            match count, rest with
            | 0, _ -> (acc, rest)
            | _, [] -> (acc, [])
            | n, x::xs -> split (n-1) (x::acc) xs

        let half = List.length list / 2
        split half [] list

    let rec sort2 = function
        | [] -> []
        | [elem] -> [elem]
        | [elem1; elem2] -> plus([elem1], [elem2])
        | l ->
            let left, right = splitList l
            plus (sort2 left, sort2 right)


    // 40.4
    let rec revrev = function
        | [] -> []
        | elem :: l -> revrev l @ [List.rev elem]
