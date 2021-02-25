import { LinkedListItem } from './linked-list-item';

export const ListEmptyError = () => new Error('List is empty.');

export class LinkedList<T> {
  private head: LinkedListItem<T>;
  private tail: LinkedListItem<T>;

  constructor() {
    this.head = new LinkedListItem<T>();
    this.tail = new LinkedListItem<T>();
    this.head.next = this.tail;
  }

  isEmpty(): boolean {
    return this.head.next === this.tail;
  }

  insertFirst(item: T): void {
    const newItem = new LinkedListItem<T>(item);
    newItem.next = this.head.next;
    this.head.next = newItem;
  }

  insertLast(item: T): void {
    const newItem = new LinkedListItem<T>(item);
    let cur: LinkedListItem<T> | null = this.head;

    while (cur && cur.next !== this.tail) {
      cur = cur.next;
    }
    if (cur) {
      newItem.next = this.tail;
      cur.next = newItem;
    }
  }

  removeFirst(): T | null {
    if (this.isEmpty()) {
      throw ListEmptyError();
    }

    const rv: LinkedListItem<T> | null = this.head.next;

    if (rv) {
      this.head.next = rv.next;
      rv.next = null;
    }

    return rv ? rv.item : null;
  }

  remove(searchKey: T): T | null {
    if (this.isEmpty()) {
      throw ListEmptyError();
    }

    let rv: LinkedListItem<T> | null = null;
    let cur: LinkedListItem<T> = this.head;
    while (cur.next && cur.next.item !== searchKey) {
      cur = cur.next;
    }

    if (cur.next) {
      rv = cur.next;
      cur.next = cur.next.next;
      rv.next = null;
    }

    return rv && rv.item ? rv.item : null;
  }

  contains(searchItem: T): boolean {
    if (this.isEmpty()) {
      throw ListEmptyError();
    }

    let rv = false;
    let cur: LinkedListItem<T> | null = this.head;

    while (cur && cur.next !== this.tail) {
      if (cur.next && cur.next.item === searchItem) {
        rv = true;
        break;
      }

      cur = cur.next;
    }

    return rv;
  }

  getFirst(): LinkedListItem<T> | null {
    if (this.isEmpty()) {
      throw ListEmptyError();
    }
    return this.head.next;
  }

  listContents(): T[] {
    let cur = this.head.next;
    let rv: T[] = [];
    while (cur && cur !== this.tail) {
      rv = cur.item ? [...rv, cur.item] : [...rv];
      cur = cur.next;
    }
    return rv;
  }
}
