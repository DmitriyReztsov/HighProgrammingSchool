open Expecto
open src.String

[<Tests>]
let stringTests =
  testList "String tests" [
    testCase "String pow asd, 0" <| fun _ ->
      Expect.equal (pow ("asd", 0)) "" "pow(asd, 0) = ''"

    testCase "String pow asd, 1" <| fun _ ->
      Expect.equal (pow ("asd", 1)) "asd" "pow(asd, 1) = asd"

    testCase "String pow 0, 2" <| fun _ ->
      Expect.equal (pow ("0", 2)) "00" "pow(0, 2) = 00"

    testCase "String pow asd, 3" <| fun _ ->
      Expect.equal (pow ("asd", 3)) "asdasdasd" "pow(asd, 3) = asdasdasd"

    testCase "String isIthChar (asd, 1, s)" <| fun _ ->
      Expect.equal (isIthChar ("asd", 1, 's')) true "isIthChar(asd, 1, s) = true"

    testCase "String isIthChar (asd, 3, s)" <| fun _ ->
      Expect.equal (isIthChar ("asd", 3, 's')) false "isIthChar(asd, 3, s) = false"

    testCase "String isIthChar (asd, 1, a)" <| fun _ ->
      Expect.equal (isIthChar ("asd", 1, 'a')) false "isIthChar(asd, 1, a) = false"

    testCase "String occFromIth (asdasdasd, 1, s)" <| fun _ ->
      Expect.equal (occFromIth ("asdasdasd", 1, 's')) 3 "occFromIth(asdasdasd, 1, s) = 3"

    testCase "String occFromIth (asdasdasd, 11, s)" <| fun _ ->
      Expect.equal (occFromIth ("asdasdasd", 11, 's')) 0 "occFromIth(asdasdasd, 11, s) = 0"

    testCase "String occFromIth (asdasdasd, 3, a)" <| fun _ ->
      Expect.equal (occFromIth ("asdasdasd", 3, 'a')) 2 "occFromIth(asdasdasd, 3, a) = 2"
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args stringTests

