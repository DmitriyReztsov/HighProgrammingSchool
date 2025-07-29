open Expecto
open src.Operators

[<Tests>]
let operatorsTests =
  testList "Operators tests" [
    testCase "Operators (0, 0, 0) .+. (0, 0, 12)" <| fun _ ->
      Expect.equal ((0, 0, 0) .+. (0, 0, 12)) (0, 1, 0) "(0, 0, 0) .+. (0, 0, 12) = (0, 1, 0)"

    testCase "Operators (10, 10, 10) .+. (2, 11, 2)" <| fun _ ->
      Expect.equal ((10, 10, 10) .+. (2, 11, 2)) (13, 2, 0) "(10, 10, 10) .+. (2, 11, 2) = (13, 2, 0)"

    testCase "Operators (1, 1, 1) .+. (1, 1, 2)" <| fun _ ->
      Expect.equal ((1, 1, 1) .+. (1, 1, 2)) (2, 2, 3) "(1, 1, 1) .+. (1, 1, 2) = (2, 2, 3)"

    testCase "Operators (1, 1, 2) .-. (1, 1, 2)" <| fun _ ->
      Expect.equal ((1, 1, 2) .-. (1, 1, 2)) (0, 0, 0) "(1, 1, 2) .-. (1, 1, 2) = (0, 0, 0)"

    testCase "Operators (11, 1, 1) .-. (0, 1, 2)" <| fun _ ->
      Expect.equal ((11, 1, 1) .-. (0, 1, 2)) (10, 19, 11) "(11, 1, 1) .-. (0, 1, 2) = (10, 19, 11)"

    testCase "Operators (10, 1, 1) .-. (1, 19, 11)" <| fun _ ->
      Expect.equal ((10, 1, 1) .-. (1, 19, 11)) (8, 1, 2) "(10, 1, 1) .-. (1, 19, 11) = (8, 1, 2)"

    testCase "Operators (1, 3) .+ (4, -5)" <| fun _ ->
      Expect.equal ((1, 3) .+ (4, -5)) (5, -2) "(1, 3) .+ (4, -5) = (5, -2)"

    testCase "Operators (-1, 1) .+ (1.5, 5)" <| fun _ ->
      Expect.equal ((-1, 1) .- (1.5, 5)) (-2.5, -4) "(-1, 1) .- (1.5, 5) = (-2.5, -4)"

    testCase "Operators (1, -1) .* (3, 6)" <| fun _ ->
      Expect.equal ((1, -1) .* (3, 6)) (9, 3) "(1, -1) .* (3, 6) = (9, 3)"

    testCase "Operators (13, 1) ./ (7, -6)" <| fun _ ->
      Expect.equal ((13, 1) ./ (7, -6)) (1, 1) "(13, 1) ./ (7, -6) = (1, 1)"
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args operatorsTests

