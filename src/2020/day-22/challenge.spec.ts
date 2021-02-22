import { inputs, sample } from './inputs';
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
});
