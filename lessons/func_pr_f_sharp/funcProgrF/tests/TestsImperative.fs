open Expecto
open src.Imperative

[<Tests>]
let ImperativeTests =
  testList "Imperative tests" [
    testCase "Imperative f 0" <| fun _ ->
      Expect.equal (f 0) 1 "0! = 1"

    testCase "Imperative f 1" <| fun _ ->
      Expect.equal (f 1) 1 "1! = 1"

    testCase "Imperative f 5" <| fun _ ->
      Expect.equal (f 5) 120 "5! = 120"

    testCase "Imperative fibo 4" <| fun _ ->
      Expect.equal (fibo 4) 3 "fibo 4 = 3"

    testCase "Imperative fibo 0" <| fun _ ->
      Expect.equal (fibo 0) 0 "fibo 0 = 0"

    testCase "Imperative fibo 1" <| fun _ ->
      Expect.equal (fibo 1) 1 "fibo 1 = 1"

    testCase "Imperative fibo 2" <| fun _ ->
      Expect.equal (fibo 2) 1 "fibo 2 = 1"

  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args ImperativeTests

