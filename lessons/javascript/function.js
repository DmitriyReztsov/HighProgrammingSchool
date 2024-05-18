const showGreeting = () => {
  // Внутри тела отступ 2 пробела для удобства чтения
  const text = 'Hello, Hexlet!';
  console.log(text);
  return text;
};

let hello = showGreeting();
console.log(hello);

const sum = (a, b = 1) => {
  return a+ b;
}

console.log(sum(1))