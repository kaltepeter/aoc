import { TileImage } from './tile-image';
import { TileScanner } from './tile-scanner';
import { Tile } from './tile2';

const calcResult = (corners: string[]): number => {
  return corners.map((v) => +v).reduce((acc, v) => (acc *= v), 1);
};

const findRoughness = (tiles: Tile[]) => {
  const monsterData = [
    '..................#.',
    '#....##....##....###',
    '.#..#..#..#..#..#...',
  ];
  const monsterSize = monsterData
    .map((row) => (row.match(/#/g) || []).length)
    .reduce((acc, v) => (acc += v), 0);
  const image = new TileImage(tiles);
  const reassembledImage = image.reassemble();
  const imageTile = new Tile('1234', [...reassembledImage]);
  const monster = new Tile('666', [...monsterData]);
  const scanner = new TileScanner(imageTile, '#');

  const numMonsters = scanner.numImages(monster);
  const totalHashes = imageTile.count('#');
  return totalHashes - numMonsters * monsterSize;
};

export { calcResult, findRoughness };
