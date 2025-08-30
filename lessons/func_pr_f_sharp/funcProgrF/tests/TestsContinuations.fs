open Expecto
open src.Continuations

[<Tests>]
let ContinuationsTests =
  testList "Continuations tests" [
    testCase "Continuations bigList 23000 id" <| fun _ ->
      Expect.equal (bigList 230000 id) (List.replicate 230000 1) "bigList 230000 id = [1] * 23000"

    testCase "Continuations fibo1 6 1 0" <| fun _ ->
      Expect.equal (fibo1 6 1 0) 8 "fibo1 6 1 0 = 8"

    testCase "Continuations fibo1 6 5 3" <| fun _ ->
      Expect.equal (fibo1 6 5 3) 55 "fibo1 6 5 3 = 55"

    testCase "Continuations fibo1 0 5 3" <| fun _ ->
      Expect.equal (fibo1 0 5 3) 3 "fibo1 0 5 3 = 3"

    testCase "Continuations fibo2 6 id" <| fun _ ->
      Expect.equal (fibo2 6 id) 8 "fibo2 6 id = 8"

    testCase "Continuations fibo2 0 id" <| fun _ ->
      Expect.equal (fibo2 0 id) 0 "fibo2 0 id = 0"

  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args ContinuationsTests

