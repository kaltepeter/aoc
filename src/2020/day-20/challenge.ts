const calcResult = (corners: string[]): number => {
  return corners.map((v) => +v).reduce((acc, v) => (acc *= v), 1);
};

export { calcResult };
