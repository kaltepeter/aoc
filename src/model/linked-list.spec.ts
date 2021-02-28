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

  describe(`findByItem('20')`, () => {
    it('should throw if empty', () => {
      try {
        expect(list.findByItem('20')).toThrowError();
      } catch (e) {
        expect(e.message).toBe('List is empty.');
      }
    });
  });

  describe(`getLast()`, () => {
    it('should throw if empty', () => {
      try {
        expect(list.getLast()).toThrowError();
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

  describe(`insertFirstBefore()`, () => {
    it(`should throw error `, () => {
      try {
        expect(list.insertBeforeFirst('20', '11')).toThrowError();
      } catch (e) {
        expect(e.message).toBe('Item "20" not found.');
      }
    });
  });

  describe(`insertFirstAfter()`, () => {
    it(`should throw error `, () => {
      try {
        expect(list.insertAfterFirst('20', '11')).toThrowError();
      } catch (e) {
        expect(e.message).toBe('Item "20" not found.');
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

    describe.each([
      ['9', '11', ['3', '8', '11', '9', '1', '2', '5', '4', '6', '7']],
      ['3', '11', ['11', '3', '8', '9', '1', '2', '5', '4', '6', '7']],
      ['7', '11', ['3', '8', '9', '1', '2', '5', '4', '6', '11', '7']],
    ])(
      `insertBeforeFirst(%s, %s)`,
      (searchItem: string, newItem: string, expectedResult: string[]) => {
        it(`should return ${expectedResult}`, () => {
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
        it(`should return ${expectedResult}`, () => {
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
  });
});
