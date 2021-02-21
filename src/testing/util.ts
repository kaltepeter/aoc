import { TestScheduler } from 'rxjs/testing';

// https://medium.com/angular-in-depth/how-to-test-observables-a00038c7faad
// https://kevinkreuzer.medium.com/marble-testing-with-rxjs-testing-utils-3ae36ac3346a
// https://dev.to/noor0/marble-testing-with-rxjs-h06
// https://github.com/ReactiveX/rxjs/blob/master/docs_app/content/guide/testing/marble-testing.md

const getTestScheduler = () =>
  new TestScheduler((actual, expected) => {
    expect(actual).toEqual(expected);
  });

export { getTestScheduler };
