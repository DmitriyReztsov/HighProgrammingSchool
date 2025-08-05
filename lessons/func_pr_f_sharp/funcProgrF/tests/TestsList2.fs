open Expecto
open src.List2

[<Tests>]
let ListTests2 =
  testList "List2 tests" [
    testCase "List2 rmodd [1], []" <| fun _ ->
      Expect.equal (rmodd [1]) [] "rmodd [1] = []"
  
    testCase "List2 rmodd [1; 2], [2]" <| fun _ ->
      Expect.equal (rmodd [1; 2]) [2] "rmodd [1; 2] = [2]"

    testCase "List2 rmodd ['a'; 's'; 'q'], ['s']" <| fun _ ->
      Expect.equal (rmodd ['a'; 's'; 'q']) ['s'] "rmodd ['a'; 's'; 'q'] = ['s']"

    testCase "List2 rmodd ['a'; 's'; 'q'; '1'], ['s'; '1']" <| fun _ ->
      Expect.equal (rmodd ['a'; 's'; 'q'; '1']) ['s'; '1'] "rmodd ['a'; 's'; 'q'; '1'] = ['s'; '1']"

    testCase "List2 del_even [1], [1]" <| fun _ ->
      Expect.equal (del_even [1]) [1] "del_even [1] = [1]"

    testCase "List2 del_even [1; 1; 1; 2; 2; 4; 5], [1; 1; 1; 5]" <| fun _ ->
      Expect.equal (del_even [1; 1; 1; 2; 2; 4; 5]) [1; 1; 1; 5] "del_even [1; 1; 1; 2; 2; 4; 5] = [1; 1; 1; 5]"

    testCase "List2 del_even [1; 2; 1; 2; 2; 4], [1; 1]" <| fun _ ->
      Expect.equal (del_even [1; 2; 1; 2; 2; 4]) [1; 1] "del_even [1; 2; 1; 2; 2; 4] = [1; 1]"

    testCase "List2 multiplicity 1 [1], 1" <| fun _ ->
      Expect.equal (multiplicity 1 [1]) 1 "multiplicity 1 [1] = 1"

    testCase "List2 multiplicity 'a' ['a'; 'b'; 'c'; '1'; 'a'], 2" <| fun _ ->
      Expect.equal (multiplicity 'a' ['a'; 'b'; 'c'; '1'; 'a']) 2 "multiplicity 'a' ['a'; 'b'; 'c'; '1'; 'a'] = 2"

    testCase "List2 split ['a'; 'b'; 'c'; '1'; 'a'], (['a'; 'c'; 'a'], ['b'; '1'])" <| fun _ ->
      Expect.equal (split ['a'; 'b'; 'c'; '1'; 'a']) (['a'; 'c'; 'a'], ['b'; '1']) "split ['a'; 'b'; 'c'; '1'; 'a'] = (['a'; 'c'; 'a'], ['b'; '1'])"

    testCase "List2 split ['a'], (['a'], [])" <| fun _ ->
      Expect.equal (split ['a']) (['a'], []) "split ['a'] = (['a'; 'c'; 'a'], [])"

    testCase "List2 zip (['a'], ['b']], [('a', 'b')])" <| fun _ ->
      Expect.equal (zip (['a'], ['b'])) [('a', 'b')] "zip (['a'], ['b']) = [('a', 'b')]"

    testCase "List2 zip ([1; 2; 3], [4; 5; 6]), [(1, 4); (2, 5); (3, 6)])" <| fun _ ->
      Expect.equal (zip ([1; 2; 3], [4; 5; 6])) [(1, 4); (2, 5); (3, 6)] "zip ([1; 2; 3], [4; 5; 6]) = [(1, 4); (2, 5); (3, 6)]"

    testCase "List2 zip ([1; 2; 3], [4; 5]), Exception)" <| fun _ ->
      Expect.throws (fun () -> zip ([1; 2; 3], [4; 5]) |> ignore) "Exception"
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args ListTests2

