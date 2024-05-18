/*while (true) {
  // Что-то делаем
}*/

const joinNumbersFromRange = (from_num, till_num) => {
  let i = from_num;
  let string = "";

  while (i <= till_num) {
    string = `${string}${i}`;
    i += i;
  }
}

const countChars = (text, char) => {
  let i = 0;
  let count = 0;

  while (i < text.length) {
    if (text[i].toLowerCase() === char.toLowerCase()) {
      console.log("HERE")
      count += 1;
    }
    i += 1;
  }
  return count;
}

console.log(countChars("axea", "a"))