open Expecto
open src.SequenceGen

[<Tests>]
let SequenceGenTests =
  testList "Sequence tests" [
    testCase "Sequence even_seq " <| fun _ ->
      Expect.equal (Seq.item 8 even_seq) 18 "even_seq 8th item = 18"

    testCase "Sequence fac_seq " <| fun _ ->
      Expect.equal (Seq.item 5 fac_seq) 120 "fac_seq 5th item = 120"

    testCase "Sequence seq_seq 5 " <| fun _ ->
      Expect.equal (Seq.item 5 seq_seq) -3 "seq_seq 5th item = -3"

    testCase "Sequence seq_seq 7 " <| fun _ ->
      Expect.equal (Seq.item 7 seq_seq) -4 "seq_seq 7th item = -4"

    testCase "Sequence seq_seq 8 " <| fun _ ->
      Expect.equal (Seq.item 8 seq_seq) 4 "seq_seq 8th item = 4"

  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args SequenceGenTests

