export const enum SIDE {
  N,
  E,
  S,
  W,
}

export const enum EDGE_LABEL {
  A,
  B,
  C,
  D,
  E,
  F,
  G,
  H,
}

export const DEFAULT_EDGE_STATE = [
  EDGE_LABEL.A,
  EDGE_LABEL.B,
  EDGE_LABEL.C,
  EDGE_LABEL.D,
  EDGE_LABEL.E,
  EDGE_LABEL.F,
  EDGE_LABEL.G,
  EDGE_LABEL.H,
];

export const EDGE_STATES = [
  [
    EDGE_LABEL.A,
    EDGE_LABEL.B,
    EDGE_LABEL.C,
    EDGE_LABEL.D,
    EDGE_LABEL.E,
    EDGE_LABEL.D,
    EDGE_LABEL.G,
    EDGE_LABEL.B,
  ], // 0°
  [
    EDGE_LABEL.H,
    EDGE_LABEL.A,
    EDGE_LABEL.F,
    EDGE_LABEL.C,
    EDGE_LABEL.D,
    EDGE_LABEL.C,
    EDGE_LABEL.B,
    EDGE_LABEL.A,
  ], // 90°
  [
    EDGE_LABEL.G,
    EDGE_LABEL.H,
    EDGE_LABEL.E,
    EDGE_LABEL.F,
    EDGE_LABEL.C,
    EDGE_LABEL.F,
    EDGE_LABEL.A,
    EDGE_LABEL.H,
  ], // 180°
  [
    EDGE_LABEL.B,
    EDGE_LABEL.G,
    EDGE_LABEL.D,
    EDGE_LABEL.E,
    EDGE_LABEL.F,
    EDGE_LABEL.E,
    EDGE_LABEL.H,
    EDGE_LABEL.G,
  ], // 270°
];
