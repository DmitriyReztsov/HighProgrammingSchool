// 17.1
let rec pow = function
    | (s, n) when n < 1 -> ""
    | (s, 1) -> s
    | (s, n) -> s + string (pow (s, n - 1))

// 17.2
let rec isIthChar = function
    | (s, n, c) when n >= String.length(s) -> false
    | (s, n, c) -> s.[n] = c

// 17.3
let rec occFromIth = function
    | (s, n, c) when n >= String.length(s) -> 0
    | (s, n, c) when s.[n] = c -> 1 + occFromIth (s, n + 1, c)
    | (s, n, c) -> occFromIth (s, n + 1, c)