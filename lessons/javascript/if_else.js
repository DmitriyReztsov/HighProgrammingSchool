const getTypeOfSentence = (sentence) => {
    const lastChar = sentence[sentence.length - 1];
    let sentenceType;
  
    if (lastChar === '?') {
        sentenceType = 'question';
      } else if (lastChar === '!') {
        sentenceType = 'exclamation';
      } else {
        sentenceType = 'normal';
      }
  
    return `Sentence is ${sentenceType}`;
  };

const abs = (number) => {
  return number >= 0 ? number : -number;
};

const abs_ = (number) => (number >= 0 ? number : -number);

  
  