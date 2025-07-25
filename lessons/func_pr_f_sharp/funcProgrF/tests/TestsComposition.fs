open Expecto
open src.Composition

[<Tests>]
let compositionTests =
  testList "Composition tests" [
    testCase "Composition vat 0 10" <| fun _ ->
      Expect.equal (vat 0 10) 10 "vat 0 10 = 10"

    testCase "Composition vat 20 10" <| fun _ ->
      Expect.equal (vat 20 10) 12 "vat 20 10 = 12"

    testCase "Composition vat 100 10" <| fun _ ->
      Expect.equal (vat 100 10) 20 "vat 100 10 = 20"

    testCase "Composition unvat 0 (vat 0 10)" <| fun _ ->
      Expect.equal (unvat 0 (vat 0 10)) 10.0 "unvat 0 (vat 0 10) = 10"

    testCase "Composition unvat 10 (vat 20 10)" <| fun _ ->
      Expect.equal (unvat 10 (vat 20 10)) (12.0 / 1.1) "unvat 10 (vat 20 10) = 12.0 / 1.1"

    testCase "Composition unvat 20 (vat 20 10)" <| fun _ ->
      Expect.equal (unvat 20 (vat 20 10)) 10.0 "unvat 20 (vat 20 10) = 10"

    testCase "Composition min (fun 11 - n)" <| fun _ ->
      Expect.equal (min (fun n -> 11 - n)) 11 "min (fun n -> 11 - n) = 11"

  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args compositionTests

