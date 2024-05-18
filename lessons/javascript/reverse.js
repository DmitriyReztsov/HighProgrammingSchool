// BEGIN (write your solution here)
const _convertTrueText = (text) => (text[0] === text[0].toUpperCase() ? text : [...text].reverse().join(""));

const convertText = (text) => (text === "" ? "" : _convertTrueText(text))
// END

console.log(convertText(""))
console.log(convertText("hey"))
console.log(convertText("Hey"))