const calculateScore = (winningHand: number[]) => {
  const winnerCards = winningHand.reverse();
  return winnerCards.reduce((acc, v, idx) => (acc += v * (idx + 1)), 0);
};

const recursiveGame = (playerHands: number[][]): [number, number[]] => {
  const seen = new Set<string>();
  const [player1Hand, player2Hand] = playerHands;
  while (player1Hand.length > 0 && player2Hand.length > 0) {
    const state = `${player1Hand}:${player2Hand}`;
    if (seen.has(state)) {
      return [1, [...player1Hand]];
    }
    seen.add(state);
    let winner: [number, number[]] = [0, []];

    const [c1, c2] = playerHands.map((h) => h.shift()) as [number, number];
    if (player1Hand.length >= c1 && player2Hand.length >= c2) {
      // recurse
      winner = recursiveGame([
        player1Hand.slice(0, c1),
        player2Hand.slice(0, c2),
      ]);
    } else {
      winner = c1 > c2 ? [1, [...player1Hand]] : [2, [...player2Hand]];
    }

    if (winner[0] === 1) {
      player1Hand.push(c1);
      player1Hand.push(c2);
    } else {
      player2Hand.push(c2);
      player2Hand.push(c1);
    }
  }

  return [
    player1Hand.length > 0 ? 1 : 2,
    player1Hand.length > 0 ? player1Hand : player2Hand,
  ];
};

export { recursiveGame, calculateScore };
