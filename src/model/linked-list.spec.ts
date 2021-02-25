import { LinkedList, ListEmptyError } from './linked-list';

describe(`LinkedList`, () => {
  let list: LinkedList<string>;

  beforeEach(() => {
    list = new LinkedList<string>();
  });

  it('is created and empty', () => {
    expect(list.isEmpty()).toBe(true);
  });

  describe(`getFirst()`, () => {
    it('should throw if empty', () => {
      try {
        expect(list.getFirst()).toThrowError();
      } catch (e) {
        expect(e.message).toBe('List is empty.');
      }
    });
  });

  describe(`contains()`, () => {
    it('should throw if empty', () => {
      try {
        expect(list.contains('40')).toThrowError();
      } catch (e) {
        expect(e.message).toBe('List is empty.');
      }
    });
  });

  describe(`remove()`, () => {
    it('should throw if empty', () => {
      try {
        expect(list.remove('40')).toThrowError();
      } catch (e) {
        expect(e.message).toBe('List is empty.');
      }
    });
  });

  describe(`removeFirst()`, () => {
    it('should throw if empty', () => {
      try {
        expect(list.removeFirst()).toThrowError();
      } catch (e) {
        expect(e.message).toBe('List is empty.');
      }
    });
  });

  describe(`with values`, () => {
    const expectedBaseOrder = ['3', '8', '9', '1', '2', '5', '4', '6', '7'];
    beforeEach(() => {
      '389125467'
        .split('')
        .reverse()
        .map((v) => list.insertFirst(v));
    });

    it('should have 9 items', () => {
      expect(list.listContents().length).toBe(9);
    });

    it('should insert first', () => {
      list.insertFirst('11');
      expect(list.listContents()).toEqual(['11', ...expectedBaseOrder]);
    });

    it('should insert last', () => {
      list.insertLast('11');
      expect(list.listContents()).toEqual([...expectedBaseOrder, '11']);
    });

    describe(`getFirst()`, () => {
      it('should return first item', () => {
        expect(list.getFirst()?.item).toBe('3');
      });
    });

    describe(`contains()`, () => {
      it('should contain 1', () => {
        expect(list.contains('1')).toBe(true);
      });

      it('should not contain 20', () => {
        expect(list.contains('20')).toBe(false);
      });
    });

    describe(`removeFirst()`, () => {
      it('should remove first item', () => {
        list.removeFirst();
        expect(list.listContents()).toEqual([
          '8',
          '9',
          '1',
          '2',
          '5',
          '4',
          '6',
          '7',
        ]);
      });
    });

    describe(`remove()`, () => {
      it('should remove 1', () => {
        list.remove('1');
        expect(list.listContents()).toEqual([
          '3',
          '8',
          '9',
          '2',
          '5',
          '4',
          '6',
          '7',
        ]);
      });

      it('should remove first item', () => {
        list.remove('3');
        expect(list.listContents()).toEqual([
          '8',
          '9',
          '1',
          '2',
          '5',
          '4',
          '6',
          '7',
        ]);
      });

      it('should remove last item', () => {
        list.remove('7');
        expect(list.listContents()).toEqual([
          '3',
          '8',
          '9',
          '1',
          '2',
          '5',
          '4',
          '6',
        ]);
      });
    });
  });
});
