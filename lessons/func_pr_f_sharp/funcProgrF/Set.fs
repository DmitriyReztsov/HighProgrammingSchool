// 42.3
let rec allSubsets n k =
    printf "Iteration %d %d\n" n k
    match n, k with
    | _, 0 -> set [Set.empty]
    | 0, _ -> Set.empty
    | n, k when k > n -> Set.empty
    | n, k ->
        let withoutN = allSubsets (n - 1) k
        let withN = Set.map (Set.add n) (allSubsets (n - 1) (k - 1))
        Set.union withoutN withN
