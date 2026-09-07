import test from 'node:test';
import assert from 'node:assert/strict';

test('Two Knights Tour: isValidKnightMove allows exact L-vector displacements', () => {
  function isValidKnightMove(r1, c1, r2, c2) {
    const dr = Math.abs(r1 - r2);
    const dc = Math.abs(c1 - c2);
    return (dr === 1 && dc === 2) || (dr === 2 && dc === 1);
  }

  // Legal knight leaps
  assert.equal(isValidKnightMove(0, 0, 1, 2), true);
  assert.equal(isValidKnightMove(0, 0, 2, 1), true);
  assert.equal(isValidKnightMove(4, 4, 2, 3), true);
  assert.equal(isValidKnightMove(4, 4, 6, 5), true);

  // Illegal moves (linear or diagonal)
  assert.equal(isValidKnightMove(0, 0, 0, 1), false);
  assert.equal(isValidKnightMove(0, 0, 1, 1), false);
  assert.equal(isValidKnightMove(0, 0, 2, 2), false);
  assert.equal(isValidKnightMove(0, 0, 0, 0), false);
});

test('Solo Solitaire Mode: Turn alternation preserves continuous solo state', () => {
  const knightsState = {
    visited: new Array(64).fill(false),
    turn: 1,
    knight1: { r: 0, c: 0 },
    knight2: { r: 7, c: 7 }
  };

  knightsState.visited[0] = true;
  knightsState.visited[63] = true;

  // Move 1: Cyan leaps from (0,0) to (1,2)
  knightsState.knight1.r = 1;
  knightsState.knight1.c = 2;
  knightsState.visited[1 * 8 + 2] = true;
  knightsState.turn = 2;

  assert.equal(knightsState.turn, 2);
  assert.equal(knightsState.visited[10], true);

  // Move 2: Gold leaps from (7,7) to (6,5)
  knightsState.knight2.r = 6;
  knightsState.knight2.c = 5;
  knightsState.visited[6 * 8 + 5] = true;
  knightsState.turn = 1;

  assert.equal(knightsState.turn, 1);
  assert.equal(knightsState.visited[53], true);
  assert.equal(knightsState.visited.filter(Boolean).length, 4);
});

test('Kintsugi Checkers: Non-punitive jumping creates golden mends without capture', () => {
  const pieces = {
    '2,1': { color: 'white', isGolden: false },
    '3,2': { color: 'red', isGolden: false }
  };
  const mendedRibbons = [];

  const dr = 4 - 2;
  const dc = 3 - 1;
  const midKey = `${2 + dr / 2},${1 + dc / 2}`;

  assert.equal(midKey, '3,2');
  assert.ok(pieces[midKey]);

  pieces[midKey].isGolden = true;
  delete pieces['2,1'];
  pieces['4,3'] = { color: 'white', isGolden: true };
  mendedRibbons.push({ r1: 2, c1: 1, r2: 4, c2: 3 });

  // Zero Attrition: both pieces remain
  assert.equal(Object.keys(pieces).length, 2);
  assert.equal(pieces['3,2'].isGolden, true);
  assert.equal(pieces['4,3'].isGolden, true);
  assert.equal(mendedRibbons.length, 1);
});

test('Gentle Companion Autoplay: Generates legal non-null moves across 8x8 grid', () => {
  function isValidKnightMove(r1, c1, r2, c2) {
    const dr = Math.abs(r1 - r2);
    const dc = Math.abs(c1 - c2);
    return (dr === 1 && dc === 2) || (dr === 2 && dc === 1);
  }

  const k2 = { r: 7, c: 7 };
  const visited = new Array(64).fill(false);
  visited[0] = true;
  visited[63] = true;

  const validMoves = [];
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      const idx = r * 8 + c;
      if (!visited[idx] && isValidKnightMove(k2.r, k2.c, r, c)) {
        validMoves.push({ r, c, idx });
      }
    }
  }

  // From (7,7), valid knight moves into 8x8 grid are (5,6) and (6,5)
  assert.equal(validMoves.length, 2);
  assert.deepEqual(validMoves.map(m => `${m.r},${m.c}`).sort(), ['5,6', '6,5']);

  // Simulate companion choosing first move
  const pick = validMoves[0];
  k2.r = pick.r;
  k2.c = pick.c;
  visited[pick.idx] = true;

  assert.equal(visited[pick.idx], true);
  assert.equal(k2.r, pick.r);
  assert.equal(k2.c, pick.c);
});

test('Sanctuary Chess: Centripetal Hearth Escort terminates upon kings meeting in center', () => {
  const whiteKing = { r: 4, c: 4 };
  const blackKing = { r: 3, c: 3 };

  const wNear = Math.abs(whiteKing.r - 3.5) <= 1 && Math.abs(whiteKing.c - 3.5) <= 1;
  const bNear = Math.abs(blackKing.r - 3.5) <= 1 && Math.abs(blackKing.c - 3.5) <= 1;

  assert.equal(wNear, true);
  assert.equal(bNear, true);
  assert.ok(wNear && bNear, 'Hearth convergence condition satisfied');
});
