namespace src


module HighOrderFunc =
    // 41.4.1
    let list_filter f xs =
        List.foldBack (
            fun head tail ->
                match head with
                    | head when f head -> head :: tail
                    | _ -> tail
            ) xs []

    // 41.4.2
    let sum (p, xs) =
        List.fold (
            fun result elem ->
                match elem with
                | elem when p elem -> result + elem
                | _ -> result
        ) 0 xs

        // List.foldBack (
        //     fun elem result ->
        //         match elem with
        //             | elem when p elem -> elem + result
        //             | _ -> result
        // ) xs 0

    // 41.4.3
    let revrev = fun xs ->
        List.fold (fun r el -> List.fold (fun rr ell -> ell :: rr) [] el :: r) [] xs
