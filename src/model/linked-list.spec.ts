import { range } from 'ramda';
import { LinkedList } from './linked-list';
import { ListEmptyError } from './list-empty-error';
import { ItemNotFoundError } from './item-not-found-error';

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
      expect(() => list.getFirst()).toThrowError(ListEmptyError);
    });
  });

  describe(`findByItem('20')`, () => {
    it('should throw if empty', () => {
      expect(() => list.findByItem('20')).toThrowError(ListEmptyError);
    });
  });

  describe(`getLast()`, () => {
    it('should throw if empty', () => {
      expect(() => list.getLast()).toThrowError(ListEmptyError);
    });
  });

  describe(`contains()`, () => {
    it('should throw if empty', () => {
      expect(() => list.contains('40')).toThrowError(ListEmptyError);
    });
  });

  describe(`remove()`, () => {
    it('should throw if empty', () => {
      expect(() => list.remove('40')).toThrowError(ListEmptyError);
    });
  });

  describe(`removeFirst()`, () => {
    it('should throw if empty', () => {
      expect(() => list.removeFirst()).toThrowError(ListEmptyError);
    });
  });

  describe(`insertFirstBefore()`, () => {
    it(`should throw error `, () => {
      expect(() => list.insertBeforeFirst('20', '11')).toThrowError(
        new ItemNotFoundError('20')
      );
    });
  });

  describe(`insertFirstAfter()`, () => {
    it(`should throw error `, () => {
      expect(() => list.insertAfterFirst('20', '11')).toThrowError(
        new ItemNotFoundError('20')
      );
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

    it('should insert first multiple times', () => {
      list.insertFirst('11');
      list.insertFirst('21');
      list.insertFirst('31');
      expect(list.listContents()).toEqual([
        '31',
        '21',
        '11',
        ...expectedBaseOrder,
      ]);
    });

    describe.each([
      ['9', '11', ['3', '8', '11', '9', '1', '2', '5', '4', '6', '7']],
      ['3', '11', ['11', '3', '8', '9', '1', '2', '5', '4', '6', '7']],
      ['7', '11', ['3', '8', '9', '1', '2', '5', '4', '6', '11', '7']],
    ])(
      `insertBeforeFirst(%s, %s)`,
      (searchItem: string, newItem: string, expectedResult: string[]) => {
        it(`should return ${expectedResult.toString()}`, () => {
          list.insertBeforeFirst(searchItem, newItem);
          expect(list.listContents()).toEqual(expectedResult);
        });
      }
    );

    describe.each([
      ['9', '11', ['3', '8', '9', '11', '1', '2', '5', '4', '6', '7']],
      ['3', '11', ['3', '11', '8', '9', '1', '2', '5', '4', '6', '7']],
      ['7', '11', ['3', '8', '9', '1', '2', '5', '4', '6', '7', '11']],
    ])(
      `insertAfterFirst(%s, %s)`,
      (searchItem: string, newItem: string, expectedResult: string[]) => {
        it(`should return ${expectedResult.toString()}`, () => {
          list.insertAfterFirst(searchItem, newItem);
          expect(list.listContents()).toEqual(expectedResult);
        });
      }
    );

    it('should insert last', () => {
      list.insertLast('11');
      expect(list.listContents()).toEqual([...expectedBaseOrder, '11']);
    });

    it('should splice items', () => {
      const partialList = ['20', '21', '22'];
      list.splice('2', partialList);
      expect(list.listContents()).toEqual([
        '3',
        '8',
        '9',
        '1',
        '2',
        '20',
        '21',
        '22',
        '5',
        '4',
        '6',
        '7',
      ]);
    });

    describe(`getFirst()`, () => {
      it('should return first item', () => {
        expect(list.getFirst()?.item).toBe('3');
      });
    });

    describe(`findByItem('2')`, () => {
      it('should return first item', () => {
        expect(list.findByItem('2')?.item).toBe('2');
        expect(list.findByItem('2')?.next?.item).toBe('5');
      });
    });

    describe(`getLast()`, () => {
      it('should return last item', () => {
        expect(list.getLast()?.item).toBe('7');
      });

      it('should return null', () => {
        expect(list.getLast()?.next?.item).toBe(null);
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

      it('should remove a string of items', () => {
        // const targetCup = list.c
        const res = list.removeFrom('8', 3);
        expect(list.listContents()).toEqual(['3', '2', '5', '4', '6', '7']);
        expect(res).toEqual(['8', '9', '1']);
      });

      it('should remove a string of items ast end of list', () => {
        const res = list.removeFrom('6', 3);
        expect(list.listContents()).toEqual([
          '3',
          '8',
          '9',
          '1',
          '2',
          '5',
          '4',
        ]);
        expect(res).toEqual(['6', '7']);
      });
    });

    it(`combinesLists`, () => {
      const list2 = new LinkedList<string>();
      list2.addAllSync(['22', '23', '24']);
      list.merge(list2);
      expect(list.listContents()).toEqual([
        '22',
        '23',
        '24',
        ...expectedBaseOrder,
      ]);
    });
  });

  it(`addAllSync([])`, () => {
    const expectedList = ['2', '3', '6', '1', '20', '10', '7'];
    const newList = new LinkedList<string>();
    newList.addAllSync([...expectedList]);
    expect(newList.listContents()).toEqual([...expectedList]);
  });

  describe(`large lists: 1 million`, () => {
    let largeList: LinkedList<number>;

    beforeEach(async () => {
      largeList = new LinkedList<number>();
      const nums = range(1, 1000001);
      await largeList.addAll(nums.slice(0, 200000));
    });

    it(`1 million number`, () => {
      expect(largeList.getFirst()?.item).toBe(1);
      const lastItem = largeList.getLast();
      expect(lastItem?.item).toBe(200000);
      // expect(lastItem?.item).toBe(1000000);
    });
  });
});
