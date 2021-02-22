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
});
