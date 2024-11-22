export class ItemNotFoundError extends Error {
  constructor(item: any) {
    super(`Item "${item}" not found.`);
  }
}
