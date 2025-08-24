namespace src


module Map =
    // 43.3
    let try_find key m =
        let rec find_helper = function
            | [] -> None
            | (k, value) :: _ when k = key -> Some(value)
            | (_, _) :: l -> find_helper l

        find_helper (Map.toList m)
