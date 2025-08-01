namespace src


module DiscriminatedUnion =
    type F = 
        | AM
        | PM

    type TimeOfDay = { hours: int; minutes: int; f: F }

    let time_as_int (x: TimeOfDay) = 
        if x.f = PM then (x.hours + 12) * 60 + x.minutes
        else x.hours * 60 + x.minutes

    let (.>.) x y = (time_as_int x) > (time_as_int y)
