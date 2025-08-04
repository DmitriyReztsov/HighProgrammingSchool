open Expecto
open src.List

[<Tests>]
let ListTests =
  testList "List tests" [
    testCase "List upto 1, [1]" <| fun _ ->
      Expect.equal (upto 1) [1] "upto 1 = [1]"

    testCase "List upto 5, [1; 2; 3; 4; 5]" <| fun _ ->
      Expect.equal (upto 5) [1; 2; 3; 4; 5] "upto 5 = [1; 2; 3; 4; 5]"

    testCase "List dnto 1, [1]" <| fun _ ->
      Expect.equal (dnto 1) [1] "dnto 1 = [1]"

    testCase "List dnto 5, [5; 4; 3; 2; 1]" <| fun _ ->
      Expect.equal (dnto 5) [5; 4; 3; 2; 1] "dnto 5 = [5; 4; 3; 2; 1]"

    testCase "List evenn 1, [2]" <| fun _ ->
      Expect.equal (evenn 1) [0] "evenn 1 = [0]"

    testCase "List evenn 6, [0; 2; 4; 6; 8; 10]" <| fun _ ->
      Expect.equal (evenn 6) [0; 2; 4; 6; 8; 10] "evenn 6 = [0; 2; 4; 6; 8; 10]"

  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args ListTests

