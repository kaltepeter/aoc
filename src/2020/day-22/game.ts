import { Player } from './player';

export class Game {
  private _numRounds = 0;
  private readonly MAX_ROUNDS = 1000;

  get rounds() {
    return this._numRounds;
  }

  constructor(public readonly players: Player[]) {}

  playRound() {
    const topCards = this.players
      .map((p) => [p, p.sortedCards.slice(0, 1)[0]] as [Player, number])
      .sort((a, b) => b[1] - a[1]);
    const [winner, otherPlayer] = topCards;
    winner[0].winRound(otherPlayer[1]);
    otherPlayer[0].loseRound();
    this._numRounds += 1;
  }

  hasWinner() {
    return (
      this.players.map((p) => p.sortedCards.length).filter((p) => p === 0)
        .length > 0
    );
  }

  calculateScore() {
    const winner = this.players.filter((p) => p.sortedCards.length > 0)[0];
    const winnerCards = winner.sortedCards.reverse();
    // idx + 1 (start at 1), card value is reverse position * face value
    return winnerCards.reduce((acc, v, idx) => (acc += v * (idx + 1)), 0);
  }

  playGame() {
    do {
      this.playRound();
      if (this._numRounds > this.MAX_ROUNDS) {
        console.log('max rounds');
      }
    } while (this.hasWinner() === false);
    return this.calculateScore();
  }
}
