open Expecto
open src.Recursion

[<Tests>]
let mathTests =
  testList "Math tests" [
    testCase "Recursion Fibonacci 0" <| fun _ ->
      Expect.equal (fibo 0) 0 "fibo(0) = 0"

    testCase "Recursion Fibonacci 1" <| fun _ ->
      Expect.equal (fibo 1) 1 "fibo(1) = 1"

    testCase "Recursion Fibonacci 2" <| fun _ ->
      Expect.equal (fibo 2) 1 "fibo(2) = 1"

    testCase "Recursion Fibonacci 3" <| fun _ ->
      Expect.equal (fibo 3) 2 "fibo(3) = 2"

    testCase "Recursion Fibonacci 7" <| fun _ ->
      Expect.equal (fibo 7) 13 "fibo(7) = 13"

    testCase "Recursion Sum 0" <| fun _ ->
      Expect.equal (sum 0) 0 "sum(0) = 0"

    testCase "Recursion Sum 1" <| fun _ ->
      Expect.equal (sum 1) 1 "sum(1) = 1"

    testCase "Recursion Sum 7" <| fun _ ->
      Expect.equal (sum 7) (1 + 2 + 3 + 4 + 5 + 6 + 7) "sum(7) = 28"

    testCase "Recursion Sum2 0 0" <| fun _ ->
      Expect.equal (sum2 (0, 0)) 0 "sum2(0 0) = 0"

    testCase "Recursion Sum2 12 0" <| fun _ ->
      Expect.equal (sum2 (12, 0)) 12 "sum2(12, 0) = 12"

    testCase "Recursion Sum2 12 5" <| fun _ ->
      Expect.equal (sum2 (12, 5)) (12 + 13 + 14 + 15 + 16 + 17) "sum2(12, 5) = 87"
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args mathTests

