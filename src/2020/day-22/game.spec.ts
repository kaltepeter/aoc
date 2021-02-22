import { Game } from './game';
import { sample } from './inputs';
import { Player } from './player';

describe(`Game`, () => {
  let game: Game;

  beforeEach(() => {
    const players = sample.map((pData) => new Player(...pData));
    game = new Game(players);
  });

  it(`playRound()`, () => {
    game.playRound();
    expect(game.players[0].sortedCards).toEqual([2, 6, 3, 1, 9, 5]);
    expect(game.players[1].sortedCards).toEqual([8, 4, 7, 10]);
  });

  it(`hasWinner() is false`, () => {
    expect(game.hasWinner()).toBe(false);
  });

  describe(`game is won`, () => {
    beforeEach(() => {
      game.players[0].sortedCards = [];
      game.players[1].sortedCards = [3, 2, 10, 6, 8, 5, 9, 4, 7, 1];
    });

    it(`hasWinner() is true`, () => {
      expect(game.hasWinner()).toBe(true);
    });

    it(`calculate score`, () => {
      expect(game.calculateScore()).toBe(306);
    });
  });

  it(`playGame`, () => {
    expect(game.playGame()).toBe(306);
  });
});
