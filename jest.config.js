module.exports = {
  transform: {
    '^.+\\.(ts|js|html)$': 'ts-jest',
  },
  testEnvironment: 'node',
  testMatch: ['**/+(*.)+(spec|test).+(ts|js)?(x)'],
  moduleFileExtensions: ['ts', 'js', 'html'],
  coverageReporters: ['html'],
  roots: ['<rootDir>/src/'],
  moduleNameMapper: {
    '^util/(.*)': '<rootDir>/src/util',
    '^util/list/(.*)': '<rootDir>/src/util/list/$1',
    '^testing/(.*)': '<rootDir>/src/testing',
    '^testing/util/(.*)': '<rootDir>/src/testing/util/$1',
    '^model/(.*)': '<rootDir>/src/model',
  },
};
