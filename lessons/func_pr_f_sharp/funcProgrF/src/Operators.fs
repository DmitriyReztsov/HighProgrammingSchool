namespace src


module Operators =
    // 23.4.1
    let (.+.) x y = 
        let (gold_left, silver_left, cuprum_left) = x
        let (gold_right, silver_right, cuprum_right) = y
        let cuprum = (cuprum_left + cuprum_right) % 12
        let silver = (silver_left + silver_right + (cuprum_left + cuprum_right) / 12) % 20
        let gold = (
            gold_left
            + gold_right
            + (
                silver_left
                + silver_right
                + (cuprum_left + cuprum_right) / 12
            ) / 20
        )
        (gold, silver, cuprum)

            

    let (.-.) x y =
        let (gold_left, silver_left, cuprum_left) = x
        let (gold_right, silver_right, cuprum_right) = y
        let gold = gold_left - gold_right
        let silver = silver_left - silver_right

        let gold = if silver < 0 then gold - 1 else gold
        let silver = if silver < 0 then 20 + silver else silver

        let cuprum = cuprum_left - cuprum_right
        let silver = if cuprum < 0 then silver - 1 else silver
        let cuprum = if cuprum < 0 then 12 + cuprum else cuprum

        let gold = if silver < 0 then gold - 1 else gold
        let silver = if silver < 0 then 20 + silver else silver

        (gold, silver, cuprum)

    // 23.4.2
    let (.+) x y =
        let (a: float, b: float) = x
        let (c: float, d: float) = y
        (a + c, b + d)


    let (.-) x y =
        let (a: float, b: float) = x
        let (c: float, d: float) = y
        let (c, d) = (-c, -d)
        (a + c, b + d)


    let (.*) x y =
        let (a: float, b: float) = x
        let (c: float, d: float) = y
        (a * c - b * d, b * c + a * d)


    let (./) x y =
        let (a: float, b: float) = x
        let (c: float, d: float) = y
        let (c, d) = (
            float c / ((float c)**2.0 + (float d)**2.0),
            -(float d)/((float c)**2.0 + (float d)**2.0)
        )
        (a * c - b * d, b * c + a * d)
