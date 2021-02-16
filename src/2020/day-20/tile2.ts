import { intersection, transpose, zip } from 'ramda';
import { DEFAULT_EDGE_STATE, EDGE_LABEL, EDGE_STATES, SIDE } from './constants';

class Tile {
  readonly NUM_SIDES = 4;
  flipped = false;
  numRotations = 0;
  edgeHash = new Map<EDGE_LABEL, string>();
  dataCache = new Map<string, string[]>();

  private _allEdges: string[] = [];

  get data(): string[] {
    const lookupKey = [this.flipped, this.numRotations].toString();
    if (!this.dataCache.has(lookupKey)) {
      const v = this.refresh();
      if (v) {
        this.dataCache.set(lookupKey, v);
      }
    }
    return this.dataCache.get(lookupKey) || [];
  }

  constructor(readonly id: string, private readonly _data: string[]) {
    const edgeH = zip(DEFAULT_EDGE_STATE, Array.from(this.allEdges()));
    edgeH.forEach(([label, edge]) => {
      this.edgeHash.set(label, edge);
    });
  }

  allEdges() {
    if (this._allEdges.length === 0) {
      // N E S W edges
      const edges = [
        this._data.slice(0, 1)[0],
        this._data.map((r) => r[r.length - 1]).join(''),
        this._data.slice(this._data.length - 1)[0],
        this._data.map((r) => r[0]).join(''),
      ];
      this._allEdges = [
        ...edges,
        ...edges.map((e) => e.split('').reverse().join('')),
      ];
    }
    return this._allEdges;
  }

  flip() {
    this.flipped = !this.flipped;
  }

  rotate() {
    this.numRotations = (this.numRotations + 1) % this.NUM_SIDES;
  }

  edgeFor(label: EDGE_LABEL): string {
    return this.edgeHash.get(label) || '';
  }

  edgeAt(direction: SIDE): string {
    const edgeIndex = this.flipped ? direction + this.NUM_SIDES : direction;
    return this.edgeFor(EDGE_STATES[this.numRotations][edgeIndex]);
  }

  sharedEdges(tile: Tile): string[] {
    return intersection(this.allEdges(), tile.allEdges());
  }

  neighborOf(tile: Tile) {
    return this !== tile && this.sharedEdges(tile).length > 0;
  }

  hasEdge(edge: string) {
    return this.allEdges().includes(edge);
  }

  arrange(dir: SIDE, edge: string) {
    if (!this.hasEdge(edge)) {
      return false;
    }
    for (let i = 0; i < 8; i++) {
      if (this.edgeAt(dir) === edge) {
        return true;
      }
      i === this.NUM_SIDES - 1 ? this.flip() : this.rotate();
    }
  }

  refresh() {
    let rows = this._data.map((r) => r.split(''));
    for (let i = 0; i < this.numRotations; i++) {
      rows = transpose(rows).map((r) => r.reverse());
    }
    if (this.flipped) {
      rows.map((r) => r.reverse());
    }
    return rows.map((r) => r.join(''));
  }

  removeBorders() {
    const rows = this.data.slice(0);
    const newRows = rows.slice(1, rows.length - 1);
    const dropEdges = newRows.map((r) => r.slice(1, r.length - 1));
    return dropEdges;
  }

  length() {
    return this.data[0].length;
  }

  width() {
    return this.data.length;
  }

  count(char: string) {
    return this.data
      .map((row) => (row.match(new RegExp(char, 'g')) || []).length)
      .reduce((acc, v) => (acc += v), 0);
  }

  toString() {
    return this.data.join('\n');
  }
}

export { Tile };
