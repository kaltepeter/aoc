import { LinkedListItem } from './linked-list-item';

export const ListEmptyError = () => new Error('List is empty.');
export const ItemNotFoundError = (item: any) =>
  new Error(`Item "${item}" not found.`);

export class LinkedList<T> {
  protected head: LinkedListItem<T>;
  protected tail: LinkedListItem<T>;

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

  insertBeforeFirst(searchItem: T, item: T): void {
    const newItem = new LinkedListItem<T>(item);
    let cur: LinkedListItem<T> | null = this.head;
    let found = false;

    while (cur && cur.next !== this.tail) {
      if (cur.next && cur.next.item === searchItem) {
        newItem.next = cur.next;
        cur.next = newItem;
        found = true;
        break;
      }

      cur = cur.next;
    }

    if (!found) {
      throw ItemNotFoundError(searchItem);
    }
  }

  insertAfterFirst(searchItem: T, item: T): void {
    const newItem = new LinkedListItem<T>(item);
    let cur: LinkedListItem<T> | null = this.head;
    let found = false;

    while (cur) {
      if (cur.item === searchItem) {
        newItem.next = cur.next;
        cur.next = newItem;
        found = true;
        break;
      }

      cur = cur.next;
    }

    if (!found) {
      throw ItemNotFoundError(searchItem);
    }
  }

  splice(searchItem: T, items: T[]) {
    let cur: LinkedListItem<T> | null = this.head;
    let found = false;

    while (cur && cur.next !== null) {
      if (cur.item === searchItem) {
        let targetItem = cur;
        items.forEach((itemVal) => {
          const item = new LinkedListItem<T>(itemVal);
          item.next = targetItem.next;
          targetItem.next = item;
          targetItem = item;
        });

        found = true;
        break;
      }

      cur = cur.next;
    }

    if (!found) {
      throw ItemNotFoundError(searchItem);
    }
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

  removeFrom(searchKey: T, count: number): T[] {
    if (this.isEmpty()) {
      throw ListEmptyError();
    }

    const rv: T[] = [];
    let cur: LinkedListItem<T> = this.head;
    while (cur.next && cur.next.item !== searchKey) {
      cur = cur.next;
    }

    for (let i = 0; i < count; i++) {
      if (cur.next) {
        if (cur.next.item) {
          rv.push(cur.next.item);
        }
        cur.next = cur.next.next;
      }
    }

    return rv;
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

  getLast(): LinkedListItem<T> | null {
    if (this.isEmpty()) {
      throw ListEmptyError();
    }
    let cur: LinkedListItem<T> | null = this.head;

    while (cur && cur.next !== this.tail) {
      cur = cur.next;
    }
    return cur;
  }

  findByItem(searchItem: T): LinkedListItem<T> | null {
    if (this.isEmpty()) {
      throw ListEmptyError();
    }
    let cur: LinkedListItem<T> | null = this.head;

    while (cur && cur.next !== this.tail) {
      if (cur.next && cur.next.item === searchItem) {
        return cur.next;
      }

      cur = cur.next;
    }
    return null;
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
