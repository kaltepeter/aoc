export class Player {
  constructor(public readonly name: string, public sortedCards: number[]) {}

  loseRound() {
    this.sortedCards = this.sortedCards.slice(1);
  }

  winRound(theirCard: number) {
    const [topCard, ...cards] = this.sortedCards;
    this.sortedCards = [...cards, topCard, theirCard];
  }
}
