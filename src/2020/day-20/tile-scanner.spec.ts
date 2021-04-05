import { TileImage } from './tile-image';
import { Tile } from './tile2';
import { TileScanner } from './tile-scanner';

describe(`tile scanner`, () => {
  let tile: Tile;
  let image: Tile;
  let scanner: TileScanner;

  beforeEach(() => {
    const imageData = ['##', '.#'];
    const tileData = [
      '......',
      '.##...',
      '..#...',
      '..#....',
      '......',
      '##...#',
    ];
    tile = new Tile('1', tileData);
    image = new Tile('2', imageData);
    scanner = new TileScanner(tile, '#');
  });

  describe('image coordinates', () => {
    it(`returns (x,y) coordinates for an image`, () => {
      expect(scanner.coordinates(image.data)).toEqual([
        [0, 0],
        [0, 1],
        [1, 1],
      ]);
    });
  });

  describe('scan', () => {
    it(`returns the number of images in a tiles current orientation`, () => {
      expect(scanner.scan(image)).toBe(1);
    });
  });

  describe('num images', () => {
    it(`returns the number of images in all 8 tile orientations`, () => {
      expect(scanner.numImages(image)).toBe(1);
    });
  });
});
