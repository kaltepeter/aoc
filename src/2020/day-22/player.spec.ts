import { sample } from './inputs';
import { Player } from './player';

describe(`Player`, () => {
  let player: Player;

  beforeEach(() => {
    player = new Player(...sample[0]);
  });

  it(`loseRound()`, () => {
    player.loseRound();
    expect(player.sortedCards).toEqual([2, 6, 3, 1]);
  });

  it(`winRound(20)`, () => {
    player.winRound(20);
    expect(player.sortedCards).toEqual([2, 6, 3, 1, 9, 20]);
  });

  describe(`part II`, () => {
    it(`hasHandBeenPlayed() is true`, () => {
      const playerCards = player.sortedCards;
      player.loseRound();
      player.sortedCards = [...playerCards];
      expect(player.hasHandBeenPlayed()).toBe(true);
    });

    it(`hasHandBeenPlayed() is false`, () => {
      player.loseRound();
      expect(player.hasHandBeenPlayed()).toBe(false);
    });

    it(`checkForRecursiveGame() to be false`, () => {
      expect(player.checkForRecursiveGame()).toBe(false);
    });

    it(`checkForRecursiveGame() to be true`, () => {
      player.sortedCards = [...player.sortedCards, 5, 8, 4, 7, 2];
      expect(player.checkForRecursiveGame()).toBe(true);
    });
  });
});
