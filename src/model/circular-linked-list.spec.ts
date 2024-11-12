import { CircularLinkedList } from './circular-linked-list';

describe(`CircularLinkedList`, () => {
  let list: CircularLinkedList<string>;

  beforeEach(() => {
    list = new CircularLinkedList<string>();
  });

  it('is created and empty', () => {
    expect(list.isEmpty()).toBe(true);
  });

  it.skip('is created and links tail to head', () => {
    expect(list.getLast()?.next).toEqual(list.getFirst());
  });

  describe(`with values`, () => {
    // const expectedBaseOrder = ['3', '8', '9', '1', '2', '5', '4', '6', '7'];
    beforeEach(() => {
      '389125467'
        .split('')
        .reverse()
        .map((v) => list.insertFirst(v));
    });

    it.skip(`tail should reference head`, () => {
      console.log(list.getLast());
      expect(list.getLast()?.next?.item).toBe('3');
    });
  });
});
