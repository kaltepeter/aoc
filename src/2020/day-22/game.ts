import { Player } from './player';

export class Game {
  isRecursive = false;

  private _numRounds = 0;
  private readonly MAX_ROUNDS = 1000;
  private totalCards = 0;

  constructor(public readonly players: Player[]) {
    this.totalCards = this.players.reduce(
      (acc, p) => (acc += p.sortedCards.length),
      0
    );
  }

  get rounds() {
    return this._numRounds;
  }

  get winner() {
    return this.players.filter((p) => p.sortedCards.length > 0)[0];
  }

  playRound() {
    const subGamePlayed = this.checkForRecursiveGame();
    if (this.hasWinner()) {
      return;
    }
    if (!subGamePlayed) {
      const topCards = this.players
        .map((p) => [p, [...p.sortedCards.slice(0, 1)][0]] as [Player, number])
        .sort((a, b) => b[1] - a[1]);
      const [winner, otherPlayer] = topCards;

      winner[0].winRound(otherPlayer[1]);
      otherPlayer[0].loseRound();
    }
    this._numRounds += 1;
  }

  hasWinner() {
    return (
      this.players.map((p) => p.sortedCards.length).filter((p) => p === 0)
        .length > 0
    );
  }

  calculateScore() {
    const winnerCards = this.winner.sortedCards.reverse();
    // idx + 1 (start at 1), card value is reverse position * face value
    return winnerCards.reduce((acc, v, idx) => (acc += v * (idx + 1)), 0);
  }

  checkCardsBeenPlayed() {
    const haveCardsBeenSeen = this.players.filter(
      (p) => p.hasHandBeenPlayed() === true
    );
    if (haveCardsBeenSeen.length === this.players.length) {
      const player2 = this.findPlayerByName('Player 2');
      player2.sortedCards = []; // force player 1 win
      return true;
    }
    return false;
  }

  checkForRecursiveGame() {
    if (this.isRecursive) {
      const shouldRecurse =
        this.players.filter((p) => p.checkForRecursiveGame() === true)
          .length === 2;
      if (shouldRecurse) {
        const subGameResult = this.triggerRecursiveGame();
        const winner = this.findPlayerByName(subGameResult.winner.name);
        const otherPlayer = this.findOtherPlayersByNAme(
          subGameResult.winner.name
        );
        winner.winRound([...otherPlayer.sortedCards.slice(0, 1)][0]);
        otherPlayer.loseRound();
        return true;
      }
    }
    return false;
  }

  playGame() {
    do {
      if (!this.checkCardsBeenPlayed()) {
        this.playRound();
      }
      // if (this._numRounds > this.MAX_ROUNDS) {
      //   console.log('max rounds');
      // }
    } while (this.hasWinner() === false);

    return this.calculateScore();
  }

  triggerRecursiveGame() {
    const players = this.players.map(
      (p) => new Player(p.name, [...p.sortedCards.slice(1, p.sortedCards[0])])
    );
    const subGame = new Game(players);
    subGame.playGame();
    return subGame;
  }

  findPlayerByName(name: string) {
    return this.players.filter((p) => p.name === name)[0];
  }

  findOtherPlayersByNAme(name: string) {
    return this.players.filter((p) => p.name !== name)[0];
  }
}
