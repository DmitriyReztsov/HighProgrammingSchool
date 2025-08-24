open Expecto
open src.Map

[<Tests>]
let MapTests =
  testList "Map tests" [
    testCase "Map try_find 3 {1:1, 2:2, 3:3}" <| fun _ ->
      Expect.equal (try_find 3 (Map [(1, 1); (2, 2); (3, 3)])) (Some (3)) "try_find 3 {1:1, 2:2, 3:3} = 3"

    testCase "Map try_find 3 {1:1, 2:2, 13:3}" <| fun _ ->
      Expect.equal (try_find 3 (Map [(1, 1); (2, 2); (13, 3)])) (None) "try_find 3 {1:1, 2:2, 13:3} = None"
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args MapTests

