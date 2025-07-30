type TimeOfDay = { hours: int; minutes: int; f: string }

let (.>.) x y =
    match x.hours, x.minutes, x.f, y.hours, y.minutes, y.f with
        | hl, ml, fl, hr, mr, fr when fl > fr -> true
        | hl, ml, fl, hr, mr, fr when fl = fr && hl > hr -> true
        | hl, ml, fl, hr, mr, fr when fl = fr && hl = hr && ml > mr -> true
        | _ -> false
