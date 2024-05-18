const reverseString = (str) => {
  let result = '';
  for (let i = 0; i < str.length; i += 1) {
    result = `${str[i]}${result}`;
   }
 
   return result;
};
  