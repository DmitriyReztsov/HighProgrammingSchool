open Expecto
open src.Practice

[<Tests>]
let PracticeTests =
  testList "Practice tests" [
    testCase "Practice sum ((fun x -> x % 2 = 0), [1; 2; 3; 4]), 6" <| fun _ ->
      Expect.equal (sum ((fun x -> x % 2 = 0), [1; 2; 3; 4])) 6 "sum ((fun x -> x % 2 = 0), [1; 2; 3; 4]) = 6"

    testCase "Practice sum ((fun x -> x > 0), [-1; -2; -3; -4]), 0" <| fun _ ->
      Expect.equal (sum ((fun x -> x > 0), [-1; -2; -3; -4])) 0 "sum ((fun x -> x > 0), [-1; -2; -3; -4]) = 0"

    testCase "Practice count ([-1; -2; -3; -4], 2), 0" <| fun _ ->
      Expect.equal (count ([-1; -2; -3; -4], 2)) 0 "count ([-1; -2; -3; -4], 2)) = 0"

    testCase "Practice count ([1; 2; 2; 3; 4], 2), 2" <| fun _ ->
      Expect.equal (count ([1; 2; 2; 3; 4], 2)) 2 "count ([1; 2; 2; 3; 4], 2) = 2"

    testCase "Practice insert ([1; 2; 2; 3; 4], 2), [1; 2; 2; 2; 3; 4]" <| fun _ ->
      Expect.equal (insert ([1; 2; 2; 3; 4], 2)) [1; 2; 2; 2; 3; 4] "count ([1; 2; 2; 3; 4], 2) = [1; 2; 2; 2; 3; 4]"

    testCase "Practice insert ([1; 2; 2; 3; 4], 0), [0; 1; 2; 2; 3; 4]" <| fun _ ->
      Expect.equal (insert ([1; 2; 2; 3; 4], 0)) [0; 1; 2; 2; 3; 4] "count ([1; 2; 2; 3; 4], 0) = [0; 1; 2; 2; 3; 4]"

    testCase "Practice insert ([0; 1; 2; 2; 3; 4], 4), [0; 1; 2; 2; 3; 4; 4]" <| fun _ ->
      Expect.equal (insert ([0; 1; 2; 2; 3; 4], 4)) [0; 1; 2; 2; 3; 4; 4] "count ([0; 1; 2; 2; 3; 4], 4) = [0; 1; 2; 2; 3; 4; 4]"

    testCase "Practice insert ([0; 1; 2; 2; 3; 4], 5), [0; 1; 2; 2; 3; 4; 5]" <| fun _ ->
      Expect.equal (insert ([0; 1; 2; 2; 3; 4], 5)) [0; 1; 2; 2; 3; 4; 5] "count ([0; 1; 2; 2; 3; 4], 5) = [0; 1; 2; 2; 3; 4; 5]"

    testCase "Practice intersect ([0; 1; 2; 2; 3; 4], [1; 2; 4]), [1; 2; 4]" <| fun _ ->
      Expect.equal (intersect ([0; 1; 2; 2; 3; 4], [1; 2; 4])) [1; 2; 4] "intersect ([0; 1; 2; 2; 3; 4], [1; 2; 4]) = [1; 2; 4]"

    testCase "Practice intersect ([0; 1; 2; 2; 3; 4], [2; 2; 2; 3; 3; 4]), [2; 2; 3; 4]" <| fun _ ->
      Expect.equal (intersect ([0; 1; 2; 2; 3; 4], [2; 2; 2; 3; 3; 4])) [2; 2; 3; 4] "intersect ([0; 1; 2; 2; 3; 4], [2; 2; 2; 3; 3; 4]) = [2; 2; 3; 4]"

    testCase "Practice intersect ([4], [2; 2; 2; 3; 3; 4]), [4]" <| fun _ ->
      Expect.equal (intersect ([4], [2; 2; 2; 3; 3; 4])) [4] "intersect ([4], [2; 2; 2; 3; 3; 4]) = [4]"
    testCase "Practice intersect ([4], [2; 2; 2; 3; 3]), []" <| fun _ ->
      Expect.equal (intersect ([4], [2; 2; 2; 3; 3])) [] "intersect ([4], [2; 2; 2; 3; 3]) = []"

    testCase "Practice plus ([0], [2]), [0; 2]" <| fun _ ->
      Expect.equal (plus ([0], [2])) [0; 2] "plus ([0], [2]) = [0; 2]"

    testCase "Practice plus ([0; 2], [2]), [0; 2; 2]" <| fun _ ->
      Expect.equal (plus ([0; 2], [2])) [0; 2; 2] "plus ([0; 2], [2]) = [0; 2; 2]"

    testCase "Practice plus ([0; 1; 2; 4], [3; 3]), [0; 1; 2; 3; 3; 4]" <| fun _ ->
      Expect.equal (plus ([0; 1; 2; 4], [3; 3])) [0; 1; 2; 3; 3; 4] "plus ([0; 1; 2; 4], [3; 3]) = [0; 1; 2; 3; 3; 4]"

    testCase "Practice plus ([0; 1], [3; 3; 5]), [0; 1; 3; 3; 5]" <| fun _ ->
      Expect.equal (plus ([0; 1], [3; 3; 5])) [0; 1; 3; 3; 5] "plus ([0; 1], [3; 3; 5]) = [0; 1; 3; 3; 5]"

    testCase "Practice minus ([0; 1; 3], [3; 3; 5]), [0; 1]" <| fun _ ->
      Expect.equal (minus ([0; 1; 3], [3; 3; 5])) [0; 1] "minus ([0; 1; 3], [3; 3; 5]) = [0; 1]"

    testCase "Practice minus ([0; 1; 3; 3; 3], [3; 3; 5]), [0; 1; 3]" <| fun _ ->
      Expect.equal (minus ([0; 1; 3; 3; 3], [3; 3; 5])) [0; 1; 3] "minus ([0; 1; 3; 3; 3], [3; 3; 5]) = [0; 1; 3]"

    testCase "Practice minus ([0; 1; 3; 3; 3; 4; 5; 6], [3; 3; 5; 5; 5]), [0; 1; 3; 4; 6]" <| fun _ ->
      Expect.equal (minus ([0; 1; 3; 3; 3; 4; 5; 6], [3; 3; 5; 5; 5])) [0; 1; 3; 4; 6] "minus ([0; 1; 3; 3; 3; 4; 5; 6], [3; 3; 5; 5; 5]) = [0; 1; 3; 4; 6]"

    testCase "Practice smallest [3; 2; 5; 4; 1], 1" <| fun _ ->
      Expect.equal (smallest [3; 2; 5; 4; 1]) (Some 1) "smallest [3; 2; 5; 4; 1] = Some 1"

    testCase "Practice smallest [3; 2; 5; 4], 2" <| fun _ ->
      Expect.equal (smallest [3; 2; 5; 4]) (Some 2) "smallest [3; 2; 5; 4] = Some 2"

    testCase "Practice smallest [], 1" <| fun _ ->
      Expect.equal (smallest []) None "smallest [] = None"

    testCase "Practice delete (1, [2; 3; 1; 1; 2]), [2; 3; 1; 2]" <| fun _ ->
      Expect.equal (delete (1, [2; 3; 1; 1; 2])) [2; 3; 1; 2] "delete (1, [2; 3; 1; 1; 2]) = [2; 3; 1; 2]"

    testCase "Practice sort [2; 3; 1; 1; 2], [1; 1; 2; 2; 3]" <| fun _ ->
      Expect.equal (sort [2; 3; 1; 1; 2]) [1; 1; 2; 2; 3] "sort [2; 3; 1; 1; 2] = [1; 1; 2; 2; 3]"

    testCase "Practice sort2 [2; 3; 1; 1; 2], [1; 1; 2; 2; 3]" <| fun _ ->
      Expect.equal (sort2 [2; 3; 1; 1; 2]) [1; 1; 2; 2; 3] "sort2 [2; 3; 1; 1; 2] = [1; 1; 2; 2; 3]"

    testCase "Practice revrev [[1; 2]; [3; 4; 5]], [[5; 4; 3]; [2; 1]]" <| fun _ ->
      Expect.equal (revrev [[1; 2]; [3; 4; 5]]) [[5; 4; 3]; [2; 1]] "revrev [[1; 2]; [3; 4; 5]] = [[5; 4; 3]; [2; 1]]"
  
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args PracticeTests

