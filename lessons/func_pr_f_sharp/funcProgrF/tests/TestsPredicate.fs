open Expecto
open src.Predicate

[<Tests>]
let mathTests =
  testList "Math tests" [
    testCase "Predicate notDivisible 0, 10" <| fun _ ->
      Expect.equal (notDivisible (0, 10)) false "notDivisible(0, 10) = false"

    testCase "Predicate notDivisible 1, 11" <| fun _ ->
      Expect.equal (notDivisible (1, 11)) true "notDivisible(1, 11) = true"

    testCase "Predicate notDivisible 3, 12" <| fun _ ->
      Expect.equal (notDivisible (3, 12)) true "notDivisible(3, 12) = true"

    testCase "Predicate notDivisible (3, 20)" <| fun _ ->
      Expect.equal (notDivisible (3, 20)) false "notDivisible(3, 20) = false"

    testCase "Predicate prime 7" <| fun _ ->
      Expect.equal (prime 7) true "prime(7) = true"

    testCase "Predicate prime 0" <| fun _ ->
      Expect.equal (prime 0) false "prime(0) = false"

    testCase "Predicate prime 1" <| fun _ ->
      Expect.equal (prime 1) false "prime(1) = false"

    testCase "Predicate prime 127" <| fun _ ->
      Expect.equal (prime 12) false "prime(12) = false"
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args mathTests

