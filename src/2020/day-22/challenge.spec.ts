import { infiniteGame, inputs, sample } from './inputs';
import { Game } from './game';
import { Player } from './player';

describe(`Day 22: Crab Combat`, () => {
  it(`should process data`, () => {
    const playerData = sample;
    expect(playerData.length).toBe(2);
    expect(playerData[0][0]).toBe('Player 1');
    expect(playerData[0][1]).toEqual([9, 2, 6, 3, 1]);
  });

  it(`play game`, () => {
    const players = inputs.map((pData) => new Player(...pData));
    const game = new Game(players);
    const gameResult = game.playGame();
    expect(gameResult).toBeGreaterThan(6822);
    expect(gameResult).toBe(34664);
  });

  describe(`part II`, () => {
    it(`should handle infinite game`, () => {
      const players = infiniteGame.map((pData) => new Player(...pData));
      const game = new Game(players);
      const gameResult = game.playGame();
      expect(gameResult).toBe(105);
      expect(game.winner.name).toBe('Player 1');
    });

    it(`triggerRecursiveGame`, () => {
      const players = inputs.map((pData) => new Player(...pData));
      players[0].sortedCards = [4, 9, 8, 5, 2];
      players[1].sortedCards = [3, 10, 1, 7, 6];
      const game = new Game(players);
      const newGame = game.triggerRecursiveGame();
      expect(newGame.winner.name).toBe('Player 2');
    });

    it.skip(`play game`, () => {
      const players = inputs.map((pData) => new Player(...pData));
      const game = new Game(players);
      game.isRecursive = true;
      const gameResult = game.playGame();
      expect(gameResult).toBeLessThan(32186);
      expect(gameResult).toBeLessThan(34640);
    });
  });
});
