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

  describe(`recurrsive combat`, () => {
    it(`end game with player 1 winning if hands are seen`, () => {
      const player1Cards = game.players[0].sortedCards;
      const player2Cards = game.players[1].sortedCards;
      game.playRound();
      game.playRound();
      game.players[0].sortedCards = [...player1Cards];
      game.players[1].sortedCards = [...player2Cards];
      game.playRound();
      game.checkCardsBeenPlayed();

      expect(game.hasWinner()).toBe(true);
      expect(game.winner.name).toBe('Player 1');
    });

    describe(`playRound() with checkForRecursiveGame`, () => {
      beforeEach(() => {
        jest.spyOn(game, 'triggerRecursiveGame');
        game.isRecursive = true;
      });

      it(`should call triggerRecursiveGame`, () => {
        game.players[0].sortedCards = [
          ...game.players[0].sortedCards,
          5,
          8,
          4,
          7,
          2,
        ];
        game.players[1].sortedCards = [
          ...game.players[1].sortedCards,
          5,
          8,
          4,
          7,
        ];
        game.playRound();
        expect(game.triggerRecursiveGame).toHaveBeenCalled();
      });

      it(`should call place card in correct order`, () => {
        game.players[0].sortedCards = [4, 9, 8, 5, 2];
        game.players[1].sortedCards = [3, 10, 1, 7, 6];
        game.playRound();
        expect(game.players[0].sortedCards).toEqual([9, 8, 5, 2]);
        expect(game.players[1].sortedCards).toEqual([10, 1, 7, 6, 3, 4]);
      });

      it(`should call place card in correct order`, () => {
        game.players[0].sortedCards = [3, 10, 1, 7, 6];
        game.players[1].sortedCards = [4, 9, 8, 5, 2];
        game.playRound();
        expect(game.players[0].sortedCards).toEqual([10, 1, 7, 6, 3, 4]);
        expect(game.players[1].sortedCards).toEqual([9, 8, 5, 2]);
      });

      it(`should not call triggerRecursiveGame for one player`, () => {
        game.players[1].sortedCards = [...game.players[1].sortedCards];
        game.playRound();
        expect(game.triggerRecursiveGame).not.toHaveBeenCalled();
      });

      it(`should not call triggerRecursiveGame`, () => {
        game.playRound();
        expect(game.triggerRecursiveGame).not.toHaveBeenCalled();
      });

      it(`playGame`, () => {
        expect(game.playGame()).toBe(291);
      });
    });
  });
});
