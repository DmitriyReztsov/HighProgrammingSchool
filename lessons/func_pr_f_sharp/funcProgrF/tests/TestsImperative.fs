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

    testCase "Imperative fibo 5" <| fun _ ->
      Expect.equal (fibo 5) 3 "fibo 5 = 3"

  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args ImperativeTests

