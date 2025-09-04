open Expecto
open src.Lazy

[<Tests>]
let LazyTests =
  testList "Lazy tests" [
    testCase "Lazy nth" <| fun _ ->
      Expect.equal (nth n0 3000000) 3000000 "nth = 30000"

  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args LazyTests

