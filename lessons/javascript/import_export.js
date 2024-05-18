import { surfaceArea, square } from './math.js';
import * as mathematics from './math.js';


// ----------------

export const pi = 3.14;
export const e = 2.718;

export const square = (x) => {
  return x * x;
};

export const surfaceArea = (r) => {
  return 4 * pi * square(r);
};

// -----------------

const pi = 3.14;
const e = 2.718;

const square = (x) => {
  return x * x;
};

const surfaceArea = (r) => {
  return 4 * pi * square(r);
};

export { pi, e, square, surfaceArea };
