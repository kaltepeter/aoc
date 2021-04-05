export class Player {
  private roundHands = new Set<string>();

  constructor(public readonly name: string, public sortedCards: number[]) {}

  loseRound() {
    if (this.checkCanPlay()) {
      return;
    }
    this._playRound();
    this.sortedCards = [...this.sortedCards.slice(1)];
  }

  winRound(theirCard: number) {
    if (this.checkCanPlay()) {
      return;
    }
    this._playRound();

    const [topCard, ...cards] = this.sortedCards;
    this.sortedCards = [...cards, topCard, theirCard];
  }

  checkCanPlay() {
    return this.sortedCards.length < 1;
  }

  hasHandBeenPlayed() {
    return this.roundHands.has(this.sortedCards.join(','));
  }

  checkForRecursiveGame() {
    return this.sortedCards.length - 1 >= this.sortedCards.slice(0, 1)[0];
  }

  private _playRound() {
    this.roundHands.add(this.sortedCards.join(','));
  }
}
