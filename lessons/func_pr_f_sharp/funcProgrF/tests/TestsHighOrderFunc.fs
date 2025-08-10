open Expecto
open src.HighOrderFunc

[<Tests>]
let HighOrderFuncTests =
  testList "HighOrderFunc tests" [
    testCase "HighOrderFunc list_filter fun x -> x = 1, [2; 4; 1; 4]" <| fun _ ->
      Expect.equal (list_filter (fun x -> x = 1) [2; 4; 1; 4]) [1] "list_filter fun x -> x = 1, [2; 4; 1; 4] = [1]"

    testCase "HighOrderFunc list_filter fun x -> x > 1 && x < 10, [2; 4; 1; 4; 0; -1; 10; 11]" <| fun _ ->
      Expect.equal (list_filter (fun x -> x > 1 && x < 10) [2; 4; 1; 4; 0; -1; 10; 11]) [2; 4; 4] "list_filter fun x -> x > 1 && x < 10) [2; 4; 1; 4; 0; -1; 10; 11] = [2; 4; 4]"

    testCase "HighOrderFunc sum fun x -> x > 1 && x < 10, [2; 4; 1; 4; 0; -1; 10; 11]" <| fun _ ->
      Expect.equal (sum ((fun x -> x > 1 && x < 10), [2; 4; 1; 4; 0; -1; 10; 11])) 10 "sum fun x -> x > 1 && x < 10) [2; 4; 1; 4; 0; -1; 10; 11] = 10"

    testCase "HighOrderFunc revrev [[1; 2]; [3; 4; 5]], [[5; 4; 3]; [2; 1]]" <| fun _ ->
      Expect.equal (revrev [[1; 2]; [3; 4; 5]]) [[5; 4; 3]; [2; 1]] "revrev [[1; 2]; [3; 4; 5]] = [[5; 4; 3]; [2; 1]]"
  
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args HighOrderFuncTests

