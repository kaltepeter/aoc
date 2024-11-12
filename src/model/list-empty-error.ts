export class ListEmptyError extends Error {
  constructor() {
    super('List is empty.');
  }
}
