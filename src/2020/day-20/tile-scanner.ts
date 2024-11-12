import { all } from 'ramda';
import { Tile } from './tile2';

class TileScanner {
  private _data: string[];
  private _size = 0;

  constructor(readonly tile: Tile, readonly char: string) {
    this._data = tile.data;
    this._size = this._data.length;
  }

  coordinates(image: string[]) {
    return image.flatMap((row, x) =>
      row
        .split('')
        .map((col, y) => (col === this.char ? [x, y] : []))
        .filter((coords) => coords.length > 0)
    );
  }

  numImages(image: Tile) {
    let numImages = 0;
    for (let i = 0; i < 8; i++) {
      numImages = this.scan(image);
      if (numImages > 0) {
        break;
      }
      if (i === 3) {
        image.flip();
      } else {
        image.rotate();
      }
    }
    return numImages;
  }

  // scans through the tile looking for images
  // images are matched one character at a time.
  // each match attempt is abandoned upon the first failed comparison
  scan(image: Tile): number {
    let numImages = 0;
    const imageHeight = image.length();
    const imageWidth = image.width();

    const xLoopLen = this._size - imageWidth - 1;
    const yLoopLen = this._size - imageHeight - 1;

    const coords = this.coordinates(image.data);
    for (let x = 0; x <= xLoopLen; x++) {
      for (let y = 0; y <= yLoopLen; y++) {
        const match = coords.map(([x1, y1]) => {
          if (this._data[x + x1][y + y1] !== this.char) {
            return false;
          } else {
            return true;
          }
        });
        const allMatch = all((m) => m === true, match);
        if (allMatch === true) {
          numImages += 1;
        }
      }
    }
    return numImages;
  }
}

export { TileScanner };
