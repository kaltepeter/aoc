/* eslint-disable */
export default {
  displayName: 'aoc-2019',
  preset: '../../jest.preset.js',
  globals: {
    'ts-jest': {
      tsconfig: '<rootDir>/tsconfig.spec.json',
    },
  },
  testEnvironment: 'node',
  transform: {
    '^.+\\.[tj]s$': 'ts-jest',
  },
  moduleFileExtensions: ['ts', 'js', 'html'],
  coverageDirectory: '../../coverage/apps/aoc-2019',
  moduleNameMapper: {
    'src/(.*)': '<rootDir>/src/$1',
  },
};
