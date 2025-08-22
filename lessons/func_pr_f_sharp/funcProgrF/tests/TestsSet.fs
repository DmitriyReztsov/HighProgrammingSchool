open Expecto
open src.Set

[<Tests>]
let SetTests =
  testList "Set tests" [
    testCase "Set allSubsets 3 2" <| fun _ ->
      Expect.equal (allSubsets 3 2) (Set [Set [1; 2]; Set [1; 3]; Set [2; 3]]) "allSubsets 3 2 = set [set [1; 2]; set [1; 3]; set [2; 3]]"

  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args SetTests

