export class LinkedListItem<T> {
  item: T | null;
  next: LinkedListItem<T> | null;

  constructor(item: T | null = null) {
    this.item = item;
    this.next = null;
  }
}
