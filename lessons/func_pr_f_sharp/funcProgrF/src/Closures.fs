namespace src


module Closures =
    let curry f = fun (x: int) -> fun (y: int) -> f (x, y): int

    let uncurry f = fun (x: int, y: int) -> f x y: int