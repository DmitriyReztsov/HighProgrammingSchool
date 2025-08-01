open Expecto
open src.DiscriminatedUnion

[<Tests>]
let DiscriminatedUnionTests =
  testList "DiscriminatedUnion tests" [
    testCase "DiscriminatedUnion (1, 11, AM) .>. (1, 11, PM)" <| fun _ ->
      Expect.equal ({hours=1; minutes=11; f=AM} .>. {hours=1; minutes=11; f=PM}) false "(1, 11, AM) less (1, 11, PM)"

    testCase "DiscriminatedUnion (1, 11, AM) .>. (1, 11, AM)" <| fun _ ->
      Expect.equal ({hours=1; minutes=11; f=AM} .>. {hours=1; minutes=11; f=AM}) false "(1, 11, AM) equals (1, 11, PM)"

    testCase "DiscriminatedUnion (1, 11, PM) .>. (1, 11, AM)" <| fun _ ->
      Expect.equal ({hours=1; minutes=11; f=PM} .>. {hours=1; minutes=11; f=AM}) true "(1, 11, PM) greater (1, 11, AM)"
  ]

[<EntryPoint>]
let main args =
    runTestsWithCLIArgs [] args DiscriminatedUnionTests

