/* PocketGull - Healing Games Parlor & Ludology Engine */


    /* ========================================================================== */
    /* ACOUSTIC HARMONICS & SOUND ENGINE                                          */
    /* ========================================================================== */
    class ParlorAudio {
      constructor() {
        this.ctx = null;
        this.enabled = true;
      }
      init() {
        if (this.ctx) return;
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();
      }
      playStoneThunk(freq = 280) {
        if (!this.ctx || !this.enabled) return;
        try {
          const now = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now);
          osc.frequency.exponentialRampToValueAtTime(80, now + 0.08);
          gain.gain.setValueAtTime(0.4, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(now);
          osc.stop(now + 0.13);
        } catch (e) {}
      }
      
      playPentatonic(noteIndex = 0) {
        if (!this.ctx || !this.enabled) return;
        // Pentatonic C major / A minor soothing scale (Hz): C5(523), D5(587), E5(659), G5(784), A5(880), C6(1046)
        const scale = [523.25, 587.33, 659.25, 783.99, 880.00, 1046.50];
        const freq = scale[Math.abs(noteIndex) % scale.length];
        this.playChime(freq);
      }

      playChime(note = 528) {
        if (!this.ctx || !this.enabled) return;
        try {
          const now = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(note, now);
          gain.gain.setValueAtTime(0.25, now);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.6);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(now);
          osc.stop(now + 1.7);
        } catch (e) {}
      }
    }
    const sound = new ParlorAudio();

    /* ========================================================================== */
    /* PARLOR CANVAS & GAME ENGINES                                               */
    /* ========================================================================== */
    const canvas = document.getElementById('parlorCanvas');
    const ctx = canvas.getContext('2d');
    let currentGame = 'knights';
    let currentLens = 'blend';

    /* ========================================================================== */
    /* PLAY MODE ENGINE: SOLO SOLITAIRE • COMPANION AUTO-TURN • CO-OP DUET        */
    /* ========================================================================== */
    let currentPlayMode = 'solo'; // 'solo' | 'companion' | 'duet'

    // Companion Auto-Response Delay for natural contemplative pacing
    function triggerCompanionTurnIfNeeded() {
      if (currentPlayMode !== 'companion') return;

      setTimeout(() => {
        if (currentGame === 'knights' && knightsState.turn === 2) {
          makeCompanionKnightMove();
        } else if (currentGame === 'go' && goState.turn === 'W') {
          makeCompanionGoMove();
        } else if (currentGame === 'checkers' && checkersState.turn === 'white') {
          makeCompanionCheckersMove();
        } else if (currentGame === 'chess' && chessState.turn === 'black') {
          makeCompanionChessMove();
        }
      }, 750);
    }

    function makeCompanionKnightMove() {
      const k2 = knightsState.knight2;
      const size = 8;
      const validMoves = [];
      for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
          const idx = r * size + c;
          if (!knightsState.visited[idx] && isValidKnightMove(k2.r, k2.c, r, c)) {
            validMoves.push({ r, c, idx });
          }
        }
      }
      if (validMoves.length > 0) {
        const choice = validMoves[Math.floor(Math.random() * validMoves.length)];
        k2.r = choice.r;
        k2.c = choice.c;
        knightsState.visited[choice.idx] = true;
        sound.playChime(432);
        knightsState.turn = 1;
        updateKnightsUI();
        triggerCompanionTurnIfNeeded();
      }
    }

    function makeCompanionGoMove() {
      const size = goState.size;
      const candidates = [];
      for (let r = 1; r < size - 1; r++) {
        for (let c = 1; c < size - 1; c++) {
          const k = `${r},${c}`;
          if (!goState.stones[k]) candidates.push(k);
        }
      }
      if (candidates.length > 0) {
        const pick = candidates[Math.floor(Math.random() * candidates.length)];
        goState.stones[pick] = 'W';
        sound.playStoneThunk(320);
        goState.turn = 'B';
        updateGoUI();
      }
    }

    function makeCompanionCheckersMove() {
      // Find a white piece to glide or jump toward red pieces
      const whiteKeys = Object.keys(checkersState.pieces).filter(k => checkersState.pieces[k].color === 'white');
      if (whiteKeys.length === 0) return;
      
      for (const k of whiteKeys) {
        const [r, c] = k.split(',').map(Number);
        // Try forward steps: (r+1, c-1) or (r+1, c+1)
        const moves = [{ r: r + 1, c: c - 1 }, { r: r + 1, c: c + 1 }];
        for (const m of moves) {
          if (m.r >= 0 && m.r < 8 && m.c >= 0 && m.c < 8 && !checkersState.pieces[`${m.r},${m.c}`]) {
            const piece = checkersState.pieces[k];
            delete checkersState.pieces[k];
            checkersState.pieces[`${m.r},${m.c}`] = piece;
            sound.playStoneThunk(280);
            checkersState.turn = 'red';
            updateCheckersUI();
            return;
          }
        }
      }
      // If no normal step found, pass turn back to red
      checkersState.turn = 'red';
      updateCheckersUI();
      triggerCompanionTurnIfNeeded();
    }

    function makeCompanionChessMove() {
      // Companion Black pieces escort Black King toward center hearth
      const blackKeys = Object.keys(chessState.pieces).filter(k => chessState.pieces[k].side === 'black');
      if (blackKeys.length === 0) return;

      // Prefer moving black king towards (3.5, 3.5)
      const bk = chessState.blackKing;
      const targetR = 3;
      const targetC = 3;
      const dr = Math.sign(targetR - bk.r);
      const dc = Math.sign(targetC - bk.c);

      const nr = bk.r + dr;
      const nc = bk.c + dc;
      const oldKey = `${bk.r},${bk.c}`;
      const newKey = `${nr},${nc}`;

      if (chessState.pieces[oldKey]) {
        const kingPiece = chessState.pieces[oldKey];
        delete chessState.pieces[oldKey];
        chessState.pieces[newKey] = kingPiece;
        chessState.blackKing = { r: nr, c: nc };
        sound.playStoneThunk(300);
      }

      chessState.turn = 'white';
      updateChessUI();
      triggerCompanionTurnIfNeeded();
    }


    /* ========================================================================== */
    /* ART & WONDER: INTERACTIVE SPARKLE & PARTICLE SYSTEM                        */
    /* ========================================================================== */
    const wonderParticles = [];

    function addSparkle(x, y, count = 4, color = null) {
      const colors = color ? [color] : ['#38bdf8', '#34d399', '#fbbf24', '#f43f5e', '#c084fc', '#ffffff'];
      for (let i = 0; i < count; i++) {
        wonderParticles.push({
          x: x + (Math.random() - 0.5) * 20,
          y: y + (Math.random() - 0.5) * 20,
          vx: (Math.random() - 0.5) * 3,
          vy: (Math.random() - 0.5) * 3 - 0.8,
          radius: Math.random() * 4.5 + 2,
          color: colors[Math.floor(Math.random() * colors.length)],
          alpha: 1,
          decay: Math.random() * 0.02 + 0.015,
          glyph: Math.random() > 0.6 ? (['✨', '⭐', '🌸', '💫', '⚪'][Math.floor(Math.random() * 5)]) : null
        });
      }
    }

    function renderAndCleanParticles() {
      for (let i = wonderParticles.length - 1; i >= 0; i--) {
        const p = wonderParticles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.alpha -= p.decay;

        if (p.alpha <= 0) {
          wonderParticles.splice(i, 1);
          continue;
        }

        ctx.save();
        ctx.globalAlpha = p.alpha;
        if (p.glyph) {
          ctx.font = `${Math.round(p.radius * 3.5)}px "PocketGull", sans-serif`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(p.glyph, p.x, p.y);
        } else {
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.shadowColor = p.color;
          ctx.shadowBlur = 10;
          ctx.fill();
        }
        ctx.restore();
      }
    }
 // 'blend', 'art', 'science' // 'knights', 'go', 'checkers', 'chess', 'euchre'

    // Letters hidden under 8x8 squares for Knights' Tour
    const KNIGHT_LETTERS = [
      'P','E','A','C','E','T','I','L',
      'I','K','U','M','S','H','A','N',
      'T','I','H','E','A','L','I','N',
      'G','K','L','O','S','H','E','T',
      'U','M','T','U','M','C','A','R',
      'E','B','R','E','A','T','H','E',
      'V','A','G','A','L','R','E','S',
      'T','O','J','A','S','A','N','N'
    ];

    // 1. Two Knights' State
    const knightsState = {
      gridSize: 8,
      visited: new Array(64).fill(false),
      knight1: { r: 0, c: 0, color: '#38bdf8', label: '♞ Cyan' },
      knight2: { r: 7, c: 7, color: '#f59e0b', label: '♘ Gold' },
      turn: 1, // 1 or 2
      history: []
    };

    // 2. Cooperative Go State (9x9)
    const goState = {
      size: 9,
      stones: {}, // 'r,c' => 'B' or 'W'
      liberties: {},
      turn: 'B', // 'B' (Slate) or 'W' (Shell)
      harmonizedGroups: 0
    };

    // 3. Kintsugi Checkers State (8x8)
    const checkersState = {
      size: 8,
      pieces: {}, // 'r,c' => { color: 'red' | 'white', isGolden: bool }
      mendedRibbons: [], // array of { r1, c1, r2, c2 }
      turn: 'red',
      selected: null
    };

    // 4. Sanctuary Chess State (8x8)
    const chessState = {
      size: 8,
      pieces: {}, // 'r,c' => { type: 'K'|'Q'|'R'|'B'|'N'|'P', side: 'white'|'black', glyph: '♔' }
      whiteKing: { r: 7, c: 4 },
      blackKing: { r: 0, c: 4 },
      hearthReached: false,
      turn: 'white',
      selected: null
    };

    // 6. The World Card (Major Arcana XXI) State
    const worldState = {
      angle: 0, // rotation angle of the wreath
      wreathR1: 150,
      wreathR2: 190,
      guardians: [
        { title: 'Human / Angel (Air)', glyph: '🪽', desc: 'Consciousness & Clarity', angle: -Math.PI * 0.75, x: 90, y: 90, color: '#38bdf8' },
        { title: 'Eagle (Water)', glyph: '🦅', desc: 'Emotional Elevation', angle: -Math.PI * 0.25, x: 510, y: 90, color: '#2dd4bf' },
        { title: 'Lion (Fire)', glyph: '🦁', desc: 'Heart Courage & Vitality', angle: Math.PI * 0.25, x: 510, y: 510, color: '#f59e0b' },
        { title: 'Bull (Earth)', glyph: '🐂', desc: 'Somatic Grounding & Physical Form', angle: Math.PI * 0.75, x: 90, y: 510, color: '#10b981' }
      ],
      activeGuardian: 0,
      wandsHarmonized: 0,
      ribbonLoops: []
    };

    // 5. Canoe Euchre State (2v2 Cooperative Trick-Passing)
    const euchreState = {
      trump: '♠', // Spades, Hearts, Diamonds, Clubs
      playerHand: [
        { rank: 'J', suit: '♠', name: 'Right Bower', value: 14, color: '#38bdf8' },
        { rank: 'J', suit: '♣', name: 'Left Bower', value: 13, color: '#2dd4bf' },
        { rank: 'A', suit: '♠', name: 'Ace of Spades', value: 12, color: '#38bdf8' },
        { rank: 'K', suit: '♥', name: 'King of Hearts', value: 10, color: '#fb7185' },
        { rank: '10', suit: '♦', name: 'Ten of Diamonds', value: 8, color: '#fbbf24' }
      ],
      partnerCard: { rank: 'Q', suit: '♠', name: 'Queen of Spades', value: 11, color: '#38bdf8' },
      tableTrick: [], // cards played on table
      tricksShared: 0,
      harmonyScore: 100
    };

    // Reset Knights
    function resetKnights() {
      knightsState.visited = new Array(64).fill(false);
      knightsState.knight1 = { r: 0, c: 0, color: '#38bdf8', label: '♞ Cyan' };
      knightsState.knight2 = { r: 7, c: 7, color: '#f59e0b', label: '♘ Gold' };
      knightsState.visited[0] = true;
      knightsState.visited[63] = true;
      knightsState.turn = 1;
      updateKnightsUI();
    }

    // Reset Go
    function resetGo() {
      goState.stones = {};
      goState.turn = 'B';
      goState.harmonizedGroups = 0;
      updateGoUI();
      triggerCompanionTurnIfNeeded();
    }

    function resetCheckers() {
      checkersState.pieces = {};
      checkersState.mendedRibbons = [];
      checkersState.turn = 'red';
      checkersState.selected = null;
      // Setup pieces on dark squares: rows 0..2 for white, rows 5..7 for red
      for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
          if ((r + c) % 2 === 1) {
            if (r < 3) checkersState.pieces[`${r},${c}`] = { color: 'white', isGolden: false };
            else if (r > 4) checkersState.pieces[`${r},${c}`] = { color: 'red', isGolden: false };
          }
        }
      }
      updateCheckersUI();
    }

    function resetChess() {
      chessState.pieces = {};
      chessState.whiteKing = { r: 7, c: 4 };
      chessState.blackKing = { r: 0, c: 4 };
      chessState.hearthReached = false;
      chessState.turn = 'white';
      chessState.selected = null;

      // Sanctuary Chess Board Setup
      const backRankW = ['♖','♘','♗','♕','♔','♗','♘','♖'];
      const backRankB = ['♜','♞','♝','♛','♚','♝','♞','♜'];
      const types = ['R','N','B','Q','K','B','N','R'];

      for (let c = 0; c < 8; c++) {
        chessState.pieces[`7,${c}`] = { side: 'white', type: types[c], glyph: backRankW[c] };
        chessState.pieces[`6,${c}`] = { side: 'white', type: 'P', glyph: '♙' };
        chessState.pieces[`1,${c}`] = { side: 'black', type: 'P', glyph: '♟' };
        chessState.pieces[`0,${c}`] = { side: 'black', type: types[c], glyph: backRankB[c] };
      }
      updateChessUI();
    }

    function updateCheckersUI() {
      const ribbonCount = checkersState.mendedRibbons.length;
      document.getElementById('statBigVal').textContent = `${ribbonCount} Ribbons`;
      document.getElementById('statSubLabel').textContent = '24k Gold Kintsugi Mends';
      const turnEl = document.getElementById('turnIndicator');
      turnEl.textContent = checkersState.turn === 'red' ? 'Turn: Vermilion Stone (Player 1)' : 'Turn: Pearl Stone (Player 2)';
      turnEl.style.color = checkersState.turn === 'red' ? '#f43f5e' : '#f8fafc';
      turnEl.style.borderColor = checkersState.turn === 'red' ? '#f43f5e' : '#f8fafc';
    }

    function updateChessUI() {
      const hearthCenter = (chessState.whiteKing.r === 4 || chessState.whiteKing.r === 3) &&
                           (chessState.whiteKing.c === 3 || chessState.whiteKing.c === 4) &&
                           (chessState.blackKing.r === 3 || chessState.blackKing.r === 4) &&
                           (chessState.blackKing.c === 3 || chessState.blackKing.c === 4);
      document.getElementById('statBigVal').textContent = hearthCenter ? 'Hearth Joined! 🕊️' : 'Sanctuary Pilgrimage';
      document.getElementById('statSubLabel').textContent = 'Escorting Kings to Hearth';
      const turnEl = document.getElementById('turnIndicator');
      turnEl.textContent = chessState.turn === 'white' ? 'Turn: Ivory Fellowship' : 'Turn: Obsidian Fellowship';
      turnEl.style.color = chessState.turn === 'white' ? '#38bdf8' : '#cbd5e1';
      turnEl.style.borderColor = chessState.turn === 'white' ? '#38bdf8' : '#94a3b8';
    }

    function resetWorld() {
      worldState.angle = 0;
      worldState.wandsHarmonized = 0;
      worldState.ribbonLoops = [];
      updateWorldUI();
    }

    function updateWorldUI() {
      document.getElementById('statBigVal').textContent = `XXI • Wholeness`;
      document.getElementById('statSubLabel').textContent = 'Four Elements Harmonized';
      const turnEl = document.getElementById('turnIndicator');
      turnEl.textContent = 'Harmonize: Touch Wreath or Guardians to Weave Light';
      turnEl.style.color = '#c084fc';
      turnEl.style.borderColor = '#c084fc';
    }

    function resetEuchre() {
      euchreState.playerHand = [
        { rank: 'J', suit: '♠', name: 'Right Bower', value: 14, color: '#38bdf8' },
        { rank: 'J', suit: '♣', name: 'Left Bower', value: 13, color: '#2dd4bf' },
        { rank: 'A', suit: '♠', name: 'Ace of Spades', value: 12, color: '#38bdf8' },
        { rank: 'K', suit: '♥', name: 'King of Hearts', value: 10, color: '#fb7185' },
        { rank: '10', suit: '♦', name: 'Ten of Diamonds', value: 8, color: '#fbbf24' }
      ];
      euchreState.tableTrick = [];
      euchreState.tricksShared = 0;
      euchreState.harmonyScore = 100;
      updateEuchreUI();
    }

    function updateEuchreUI() {
      document.getElementById('statBigVal').textContent = `${euchreState.tricksShared} / 5 Tricks`;
      document.getElementById('statSubLabel').textContent = 'Shared in Kinship & Flow';
      const turnEl = document.getElementById('turnIndicator');
      turnEl.textContent = 'Trump: ♠ Spades • Your Turn to Play Card';
      turnEl.style.color = '#38bdf8';
      turnEl.style.borderColor = '#38bdf8';
    }

    // Knights valid leap: (dr=1, dc=2) or (dr=2, dc=1)
    function isValidKnightMove(r1, c1, r2, c2) {
      const dr = Math.abs(r1 - r2);
      const dc = Math.abs(c1 - c2);
      return (dr === 1 && dc === 2) || (dr === 2 && dc === 1);
    }

    function updateKnightsUI() {
      const count = knightsState.visited.filter(Boolean).length;
      document.getElementById('statBigVal').textContent = `${count} / 64`;
      document.getElementById('statSubLabel').textContent = currentLens === 'art' ? 'Magic Stars Awakened ✨' : 'Squares Illuminated';
      const turnEl = document.getElementById('turnIndicator');
      
      if (currentPlayMode === 'solo') {
        const knightName = knightsState.turn === 1 ? 'Cyan Knight' : 'Gold Knight';
        turnEl.textContent = `Solo Solitaire • Move ${knightName}`;
        turnEl.style.color = knightsState.turn === 1 ? '#38bdf8' : '#f59e0b';
        turnEl.style.borderColor = knightsState.turn === 1 ? '#38bdf8' : '#f59e0b';
      } else if (currentPlayMode === 'companion') {
        if (knightsState.turn === 1) {
          turnEl.textContent = 'Your Turn: Move Cyan Knight';
          turnEl.style.color = '#38bdf8';
          turnEl.style.borderColor = '#38bdf8';
        } else {
          turnEl.textContent = '🕊️ Companion is Gliding Gold Knight...';
          turnEl.style.color = '#f59e0b';
          turnEl.style.borderColor = '#f59e0b';
        }
      } else {
        if (knightsState.turn === 1) {
          turnEl.textContent = 'Turn: Cyan Knight (Player 1)';
          turnEl.style.color = '#38bdf8';
          turnEl.style.borderColor = '#38bdf8';
        } else {
          turnEl.textContent = 'Turn: Gold Knight (Player 2)';
          turnEl.style.color = '#f59e0b';
          turnEl.style.borderColor = '#f59e0b';
        }
      }
    }

    function updateGoUI() {
      const count = Object.keys(goState.stones).length;
      document.getElementById('statBigVal').textContent = `${count} Stones`;
      document.getElementById('statSubLabel').textContent = 'Placed with Living Breath';
      const turnEl = document.getElementById('turnIndicator');
      turnEl.textContent = goState.turn === 'B' ? 'Turn: Black Slate (Yin Grounding)' : 'Turn: White Shell (Yang Clarity)';
      turnEl.style.color = goState.turn === 'B' ? '#cbd5e1' : '#fef08a';
      turnEl.style.borderColor = goState.turn === 'B' ? '#94a3b8' : '#fef08a';
    }

    /* ─── RENDERING ─── */
    function render() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (currentGame === 'knights') {
        renderKnights();
      } else if (currentGame === 'go') {
        renderGo();
      } else if (currentGame === 'checkers') {
        renderCheckers();
      } else if (currentGame === 'chess') {
        renderChess();
      } else if (currentGame === 'euchre') {
        renderEuchre();
      } else if (currentGame === 'world') {
        renderWorld();
      } else {
        renderPlaceholder();
      }

      renderAndCleanParticles();

      requestAnimationFrame(render);
    }


    /* ========================================================================== */
    /* SUPER-CHILL SANCTUARY ENGINE (AGGRESSIVE GENTLENESS)                       */
    /* ========================================================================== */
    let isSuperChillActive = false;
    let autoPlayTimer = null;
    const btnSuperChill = document.getElementById('btnSuperChill');

    if (btnSuperChill) {
      btnSuperChill.addEventListener('click', () => {
        sound.init();
        isSuperChillActive = !isSuperChillActive;
        btnSuperChill.textContent = isSuperChillActive ? '🌱 Super-Chill: ON' : '🌱 Super-Chill: OFF';
        btnSuperChill.style.background = isSuperChillActive ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.15)';
        btnSuperChill.style.boxShadow = isSuperChillActive ? '0 0 16px rgba(16, 185, 129, 0.5)' : 'none';

        if (isSuperChillActive) {
          document.getElementById('pacerLabel').textContent = '🌱 Super-Chill Active • Magnetic Assistance Max • No Wrong Answers • Pure Ease';
          startChillAutoPlay();
        } else {
          document.getElementById('pacerLabel').textContent = 'Inhale (4s) … Contemplate & Glide Exhale (6s)';
          if (autoPlayTimer) clearInterval(autoPlayTimer);
        }
      });
    }

    // Auto-Assisted Gentle Move in Knights' Tour when Chill is active
    function startChillAutoPlay() {
      if (autoPlayTimer) clearInterval(autoPlayTimer);
      autoPlayTimer = setInterval(() => {
        if (!isSuperChillActive) return;
        if (currentGame === 'knights') {
          makeGentleKnightMove();
        } else if (currentGame === 'go') {
          makeGentleGoMove();
        }
      }, 3500); // Gentle 3.5s rhythm
    }

    function makeGentleKnightMove() {
      const activeK = knightsState.turn === 1 ? knightsState.knight1 : knightsState.knight2;
      const size = 8;
      const validMoves = [];

      for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
          const idx = r * size + c;
          if (!knightsState.visited[idx] && isValidKnightMove(activeK.r, activeK.c, r, c)) {
            validMoves.push({ r, c, idx });
          }
        }
      }

      if (validMoves.length > 0) {
        // Pick the most harmonic move
        const choice = validMoves[Math.floor(Math.random() * validMoves.length)];
        activeK.r = choice.r;
        activeK.c = choice.c;
        knightsState.visited[choice.idx] = true;
        sound.playChime(knightsState.turn === 1 ? 528 : 432);
        knightsState.turn = knightsState.turn === 1 ? 2 : 1;
        updateKnightsUI();

        if (knightsState.visited.every(Boolean)) {
          sound.playChime(660);
          resetKnights();
        }
      } else {
        // If stranded, softly open a visited square so play never stops
        const unvisited = [];
        for (let i = 0; i < 64; i++) {
          if (!knightsState.visited[i]) unvisited.push(i);
        }
        if (unvisited.length > 0) {
          const jumpIdx = unvisited[0];
          activeK.r = Math.floor(jumpIdx / size);
          activeK.c = jumpIdx % size;
          knightsState.visited[jumpIdx] = true;
          sound.playChime(528);
          knightsState.turn = knightsState.turn === 1 ? 2 : 1;
          updateKnightsUI();
        }
      }
    }

    function makeGentleGoMove() {
      const size = goState.size;
      const emptySpots = [];
      for (let r = 1; r < size - 1; r++) {
        for (let c = 1; c < size - 1; c++) {
          const key = `${r},${c}`;
          if (!goState.stones[key]) emptySpots.push({ r, c, key });
        }
      }
      if (emptySpots.length > 0) {
        const pick = emptySpots[Math.floor(Math.random() * emptySpots.length)];
        goState.stones[pick.key] = goState.turn;
        sound.playStoneThunk(goState.turn === 'B' ? 240 : 320);
        goState.turn = goState.turn === 'B' ? 'W' : 'B';
        updateGoUI();
      }
    }

    // Render 8x8 Knights' Tour Board
    function renderKnights() {
      const size = 8;
      const cell = canvas.width / size;

      for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
          const idx = r * size + c;
          const isVisited = knightsState.visited[idx];
          const isDarkSquare = (r + c) % 2 === 1;

          ctx.save();
          // Square background
          if (isVisited) {
            ctx.fillStyle = 'rgba(20, 184, 166, 0.28)';
          } else {
            ctx.fillStyle = isDarkSquare ? '#0f172a' : '#1e293b';
          }
          ctx.fillRect(c * cell, r * cell, cell, cell);

          // Border
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
          ctx.strokeRect(c * cell, r * cell, cell, cell);

          // Letterform on visited squares
          if (isVisited) {
            ctx.font = '700 20px "PocketGull", sans-serif';
            ctx.fillStyle = '#f8fafc';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(KNIGHT_LETTERS[idx], c * cell + cell / 2, r * cell + cell / 2);
          }
          ctx.restore();
        }
      }

      // Draw Valid Move Hints for active knight
      const activeK = knightsState.turn === 1 ? knightsState.knight1 : knightsState.knight2;
      for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
          const idx = r * size + c;
          if (!knightsState.visited[idx] && isValidKnightMove(activeK.r, activeK.c, r, c)) {
            ctx.save();
            ctx.beginPath();
            ctx.arc(c * cell + cell / 2, r * cell + cell / 2, 8, 0, Math.PI * 2);
            ctx.fillStyle = activeK.color === '#38bdf8' ? 'rgba(56, 189, 248, 0.5)' : 'rgba(245, 158, 11, 0.5)';
            ctx.fill();
            ctx.restore();
          }
        }
      }

      // Draw Knight 1
      drawKnightPiece(knightsState.knight1.r, knightsState.knight1.c, cell, '#38bdf8', '♞');
      // Draw Knight 2
      drawKnightPiece(knightsState.knight2.r, knightsState.knight2.c, cell, '#f59e0b', '♘');
    }

    function drawKnightPiece(r, c, cell, color, glyph) {
      const x = c * cell + cell / 2;
      const y = r * cell + cell / 2;
      ctx.save();
      ctx.shadowColor = color;
      ctx.shadowBlur = 18;
      ctx.font = '34px "PocketGull", sans-serif';
      ctx.fillStyle = color;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(glyph, x, y);
      ctx.restore();
    }

    // Render 9x9 Cooperative Go Board
    function renderGo() {
      const size = goState.size;
      const margin = 50;
      const step = (canvas.width - margin * 2) / (size - 1);

      // Kaya wood warm background
      ctx.save();
      ctx.fillStyle = '#1c1917';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Grid lines
      ctx.strokeStyle = 'rgba(245, 158, 11, 0.35)';
      ctx.lineWidth = 1.5;
      for (let i = 0; i < size; i++) {
        // Horizontal
        ctx.beginPath();
        ctx.moveTo(margin, margin + i * step);
        ctx.lineTo(canvas.width - margin, margin + i * step);
        ctx.stroke();

        // Vertical
        ctx.beginPath();
        ctx.moveTo(margin + i * step, margin);
        ctx.lineTo(margin + i * step, canvas.height - margin);
        ctx.stroke();
      }

      // Star points (Hoshi) for 9x9: center (4,4) and corners (2,2), (6,2), (2,6), (6,6)
      const hoshi = [[2,2],[6,2],[4,4],[2,6],[6,6]];
      hoshi.forEach(([r, c]) => {
        ctx.beginPath();
        ctx.arc(margin + c * step, margin + r * step, 4, 0, Math.PI * 2);
        ctx.fillStyle = '#f59e0b';
        ctx.fill();
      });

      // Draw Stones
      for (const [key, stone] of Object.entries(goState.stones)) {
        const [r, c] = key.split(',').map(Number);
        const sx = margin + c * step;
        const sy = margin + r * step;

        ctx.save();
        ctx.beginPath();
        ctx.arc(sx, sy, step * 0.44, 0, Math.PI * 2);

        if (stone === 'B') {
          // Black Slate (Matte Obsidian)
          const grad = ctx.createRadialGradient(sx - 4, sy - 4, 2, sx, sy, step * 0.44);
          grad.addColorStop(0, '#334155');
          grad.addColorStop(1, '#020617');
          ctx.fillStyle = grad;
          ctx.shadowColor = '#000';
          ctx.shadowBlur = 12;
        } else {
          // White Shell (Luminous Pearl)
          const grad = ctx.createRadialGradient(sx - 4, sy - 4, 2, sx, sy, step * 0.44);
          grad.addColorStop(0, '#ffffff');
          grad.addColorStop(1, '#cbd5e1');
          ctx.fillStyle = grad;
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 12;
        }
        ctx.fill();

        // Subtle living pulse indicator
        ctx.strokeStyle = 'rgba(20, 184, 166, 0.4)';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.restore();
      }

      ctx.restore();
    }


    // Render 8x8 Kintsugi Checkers Board
    function renderCheckers() {
      const size = 8;
      const cell = canvas.width / size;

      // Board squares
      for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
          const isDarkSquare = (r + c) % 2 === 1;
          ctx.fillStyle = isDarkSquare ? '#1e1b18' : '#292524';
          ctx.fillRect(c * cell, r * cell, cell, cell);
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
          ctx.strokeRect(c * cell, r * cell, cell, cell);
        }
      }

      // Draw 24k Gold Kintsugi Ribbons between jumped/mended coordinates
      checkersState.mendedRibbons.forEach(ribbon => {
        const x1 = ribbon.c1 * cell + cell / 2;
        const y1 = ribbon.r1 * cell + cell / 2;
        const x2 = ribbon.c2 * cell + cell / 2;
        const y2 = ribbon.r2 * cell + cell / 2;
        const midX = (x1 + x2) / 2;
        const midY = (y1 + y2) / 2 - 12;

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.quadraticCurveTo(midX, midY, x2, y2);
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 4.5;
        ctx.shadowColor = '#f59e0b';
        ctx.shadowBlur = 12;
        ctx.stroke();

        // Second subtle highlight line
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.quadraticCurveTo(midX, midY, x2, y2);
        ctx.strokeStyle = '#fffbeb';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.restore();
      });

      // Highlight selected square
      if (checkersState.selected) {
        const { r, c } = checkersState.selected;
        ctx.save();
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#fbbf24';
        ctx.shadowBlur = 14;
        ctx.strokeRect(c * cell + 2, r * cell + 2, cell - 4, cell - 4);
        ctx.restore();
      }

      // Draw Checkers stones
      for (const [key, piece] of Object.entries(checkersState.pieces)) {
        const [r, c] = key.split(',').map(Number);
        const cx = c * cell + cell / 2;
        const cy = r * cell + cell / 2;
        const radius = cell * 0.38;

        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, Math.PI * 2);

        if (piece.color === 'red') {
          const grad = ctx.createRadialGradient(cx - 3, cy - 3, 2, cx, cy, radius);
          grad.addColorStop(0, '#fb7185');
          grad.addColorStop(1, '#9f1239');
          ctx.fillStyle = grad;
          ctx.shadowColor = '#f43f5e';
          ctx.shadowBlur = piece.isGolden ? 18 : 8;
        } else {
          const grad = ctx.createRadialGradient(cx - 3, cy - 3, 2, cx, cy, radius);
          grad.addColorStop(0, '#ffffff');
          grad.addColorStop(1, '#94a3b8');
          ctx.fillStyle = grad;
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = piece.isGolden ? 18 : 8;
        }
        ctx.fill();

        // If mended / golden, draw 24k gold lacquer ring and leaf motif
        if (piece.isGolden) {
          ctx.strokeStyle = '#fbbf24';
          ctx.lineWidth = 3;
          ctx.stroke();

          ctx.font = '16px "PocketGull", sans-serif';
          ctx.fillStyle = '#fbbf24';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('✨', cx, cy);
        } else {
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
          ctx.lineWidth = 1.5;
          ctx.stroke();
        }
        ctx.restore();
      }
    }

    // Render The World Card (Major Arcana XXI) Sanctuary
    function renderWorld() {
      worldState.angle += 0.008; // Gentle cosmic gyre
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;

      // Deep cosmic indigo canvas background
      ctx.save();
      const bgGrad = ctx.createRadialGradient(cx, cy, 50, cx, cy, 320);
      bgGrad.addColorStop(0, '#1e1138');
      bgGrad.addColorStop(0.6, '#0c071e');
      bgGrad.addColorStop(1, '#030209');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Gold Filigree Card Border
      ctx.strokeStyle = 'rgba(245, 158, 11, 0.35)';
      ctx.lineWidth = 2;
      ctx.strokeRect(18, 18, canvas.width - 36, canvas.height - 36);

      // Inner header banner: XXI • THE WORLD
      ctx.font = '800 15px "PocketGull Bold", sans-serif';
      ctx.fillStyle = '#c084fc';
      ctx.textAlign = 'center';
      ctx.fillText('XXI • THE WORLD (LE MONDE) • COSMIC WHOLENESS', cx, 46);

      // Draw the Four Tetramorph / Elemental Guardians in the 4 Corners
      worldState.guardians.forEach((g, idx) => {
        ctx.save();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.04)';
        ctx.strokeStyle = g.color;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(g.x, g.y, 38, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        ctx.font = '28px "PocketGull", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(g.glyph, g.x, g.y);

        ctx.font = '700 9px "PocketGull Mono", monospace';
        ctx.fillStyle = g.color;
        ctx.fillText(g.title.split(' ')[0], g.x, g.y + 48);
        ctx.restore();
      });

      // Draw the Sacred Mandorla / Laurel Ouroboros Wreath
      ctx.save();
      ctx.translate(cx, cy);
      const rx = 140;
      const ry = 190;

      // Wreath golden glow
      ctx.shadowColor = '#fbbf24';
      ctx.shadowBlur = 20;
      ctx.strokeStyle = 'rgba(245, 158, 11, 0.65)';
      ctx.lineWidth = 14;
      ctx.beginPath();
      ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Inner Laurel Leaf Ring
      ctx.shadowBlur = 0;
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Ouroboros Red Infinity Ribbons (Top & Bottom lemniscates)
      ctx.fillStyle = '#ef4444';
      ctx.font = '24px "PocketGull", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('∞', 0, -ry);
      ctx.fillText('∞', 0, ry);

      // Central Dancing Anima (The Healer of Wholeness)
      // Represented by two golden wands and radiant spiral of light
      const wandLen = 70;
      const wandRot = Math.sin(worldState.angle * 2) * 0.35;

      // Left Wand (Creation / Breath)
      ctx.save();
      ctx.rotate(wandRot);
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(-35, -wandLen/2);
      ctx.lineTo(-35, wandLen/2);
      ctx.stroke();
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath();
      ctx.arc(-35, -wandLen/2, 6, 0, Math.PI*2);
      ctx.arc(-35, wandLen/2, 6, 0, Math.PI*2);
      ctx.fill();
      ctx.restore();

      // Right Wand (Integration / Healing)
      ctx.save();
      ctx.rotate(-wandRot);
      ctx.strokeStyle = '#fbbf24';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(35, -wandLen/2);
      ctx.lineTo(35, wandLen/2);
      ctx.stroke();
      ctx.fillStyle = '#fbbf24';
      ctx.beginPath();
      ctx.arc(35, -wandLen/2, 6, 0, Math.PI*2);
      ctx.arc(35, wandLen/2, 6, 0, Math.PI*2);
      ctx.fill();
      ctx.restore();

      // Central Heart of Wholeness
      ctx.font = '36px "PocketGull", sans-serif';
      ctx.fillStyle = '#f43f5e';
      ctx.shadowColor = '#f43f5e';
      ctx.shadowBlur = 18;
      ctx.fillText('♥', 0, 8);
      ctx.restore();

      // Bottom guidance
      ctx.font = '12px "PocketGull Mono", monospace';
      ctx.fillStyle = '#a78bfa';
      ctx.textAlign = 'center';
      ctx.fillText('Tap any corner guardian or the laurel wreath to harmonize cosmic unity', cx, canvas.height - 32);
      ctx.restore();
    }

    // Render Canoe Euchre 2v2 Table
    function renderEuchre() {
      // Warm felt canoe table background
      ctx.save();
      const grad = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 40, canvas.width/2, canvas.height/2, canvas.width/2);
      grad.addColorStop(0, '#0f2922');
      grad.addColorStop(1, '#05130e');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Border rail
      ctx.strokeStyle = 'rgba(45, 212, 191, 0.25)';
      ctx.lineWidth = 3;
      ctx.strokeRect(15, 15, canvas.width - 30, canvas.height - 30);

      // Table Header: Trump Indicator
      ctx.font = '700 16px "PocketGull", sans-serif';
      ctx.fillStyle = '#2dd4bf';
      ctx.textAlign = 'center';
      ctx.fillText('🌲 Canoe Euchre • Cooperative 2v2 Kinship Sanctuary', canvas.width / 2, 45);

      // Partner Across the Table (Top)
      ctx.font = '14px "PocketGull Mono", monospace';
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('🤝 Cooperative Partner (North)', canvas.width / 2, 75);

      // Draw Partner's Face-Down / Uplifted Cards
      const partnerCardW = 60;
      const partnerCardH = 85;
      const partnerStartX = canvas.width / 2 - (3 * 40);
      for (let i = 0; i < 3; i++) {
        ctx.save();
        ctx.fillStyle = '#091e17';
        ctx.strokeStyle = '#2dd4bf';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(partnerStartX + i * 50, 90, partnerCardW, partnerCardH, 6);
        ctx.fill();
        ctx.stroke();
        ctx.font = '22px "PocketGull", sans-serif';
        ctx.fillStyle = '#2dd4bf';
        ctx.textAlign = 'center';
        ctx.fillText('🪶', partnerStartX + i * 50 + partnerCardW / 2, 140);
        ctx.restore();
      }

      // Center Hearth / Active Trick Area
      ctx.save();
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
      ctx.setLineDash([6, 6]);
      ctx.beginPath();
      ctx.arc(canvas.width / 2, canvas.height / 2 + 10, 80, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);

      if (euchreState.tableTrick.length === 0) {
        ctx.font = '14px "PocketGull", sans-serif';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
        ctx.textAlign = 'center';
        ctx.fillText('Play a card into the hearth', canvas.width / 2, canvas.height / 2 + 15);
      } else {
        // Draw cards in trick
        euchreState.tableTrick.forEach((card, idx) => {
          const tx = canvas.width / 2 - 35 + (idx * 40 - 20);
          const ty = canvas.height / 2 - 35;
          drawEuchreCard(tx, ty, 70, 100, card, false);
        });
      }
      ctx.restore();

      // Bottom Area: Player's Hand
      ctx.font = '14px "PocketGull Mono", monospace';
      ctx.fillStyle = '#38bdf8';
      ctx.textAlign = 'center';
      ctx.fillText('🖐️ Your Hand (Click to Pass or Play)', canvas.width / 2, 440);

      const hand = euchreState.playerHand;
      const cardW = 75;
      const cardH = 110;
      const totalW = hand.length * (cardW + 14);
      let startX = (canvas.width - totalW) / 2;

      hand.forEach((card, idx) => {
        const cx = startX + idx * (cardW + 14);
        const cy = 460;
        card._x = cx;
        card._y = cy;
        card._w = cardW;
        card._h = cardH;
        drawEuchreCard(cx, cy, cardW, cardH, card, true);
      });

      ctx.restore();
    }

    function drawEuchreCard(x, y, w, h, card, isInteractive) {
      ctx.save();
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = card.color || '#38bdf8';
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.roundRect(x, y, w, h, 8);
      ctx.fill();
      ctx.shadowBlur = 0;

      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Card Rank & Suit in PocketGull
      const isRed = card.suit === '♥' || card.suit === '♦';
      ctx.fillStyle = isRed ? '#e11d48' : '#0f172a';
      ctx.font = '800 18px "PocketGull Bold", sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(card.rank, x + 8, y + 22);

      ctx.font = '16px "PocketGull", sans-serif';
      ctx.fillText(card.suit, x + 8, y + 42);

      // Center Large Suit
      ctx.font = '32px "PocketGull", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(card.suit, x + w / 2, y + h / 2 + 10);

      // Small caption
      if (card.name && isInteractive) {
        ctx.font = '700 9px "PocketGull Mono", monospace';
        ctx.fillStyle = '#475569';
        ctx.textAlign = 'center';
        ctx.fillText(card.name.slice(0, 10), x + w / 2, y + h - 8);
      }

      ctx.restore();
    }

    // Render 8x8 Sanctuary Chess Board
    function renderChess() {
      const size = 8;
      const cell = canvas.width / size;

      // Board squares
      for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
          const isDarkSquare = (r + c) % 2 === 1;
          const isHearthSquare = (r === 3 || r === 4) && (c === 3 || c === 4);

          ctx.save();
          if (isHearthSquare) {
            // Central Tilikum Hearth glowing warm
            ctx.fillStyle = 'rgba(245, 158, 11, 0.2)';
            ctx.fillRect(c * cell, r * cell, cell, cell);
            ctx.strokeStyle = 'rgba(245, 158, 11, 0.6)';
            ctx.lineWidth = 2;
            ctx.strokeRect(c * cell + 2, r * cell + 2, cell - 4, cell - 4);
          } else {
            ctx.fillStyle = isDarkSquare ? '#0f172a' : '#1e293b';
            ctx.fillRect(c * cell, r * cell, cell, cell);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
            ctx.strokeRect(c * cell, r * cell, cell, cell);
          }
          ctx.restore();
        }
      }

      // Draw central hearth icon
      ctx.save();
      ctx.font = '22px "PocketGull", sans-serif';
      ctx.fillStyle = 'rgba(245, 158, 11, 0.45)';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('🕊️ Hearth', canvas.width / 2, canvas.height / 2);
      ctx.restore();

      // Highlight selected square
      if (chessState.selected) {
        const { r, c } = chessState.selected;
        ctx.save();
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#38bdf8';
        ctx.shadowBlur = 12;
        ctx.strokeRect(c * cell + 3, r * cell + 3, cell - 6, cell - 6);
        ctx.restore();
      }

      // Draw Chess pieces
      for (const [key, piece] of Object.entries(chessState.pieces)) {
        const [r, c] = key.split(',').map(Number);
        const cx = c * cell + cell / 2;
        const cy = r * cell + cell / 2;

        ctx.save();
        ctx.font = '36px "PocketGull", "Segoe UI Symbol", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        if (piece.side === 'white') {
          ctx.fillStyle = '#f8fafc';
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 10;
        } else {
          ctx.fillStyle = '#cbd5e1';
          ctx.shadowColor = '#f59e0b';
          ctx.shadowBlur = 10;
        }
        ctx.fillText(piece.glyph, cx, cy);
        ctx.restore();
      }
    }

    function renderPlaceholder() {
      ctx.save();
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.font = '800 24px "PocketGull", sans-serif';
      ctx.fillStyle = 'var(--accent-teal)';
      ctx.textAlign = 'center';
      ctx.fillText('🏛️ Cooperative Sanctuary Studio Active', canvas.width / 2, canvas.height / 2 - 20);
      ctx.font = '14px "PocketGull Mono", monospace';
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('Select Two Knights\' Tour or Cooperative Go from the left panel', canvas.width / 2, canvas.height / 2 + 15);
      ctx.restore();
    }

    /* ─── CLICK HANDLERS ─── */
    
    let pentatonicStep = 0;
    canvas.addEventListener('mousemove', (e) => {
      if (currentLens === 'art' || currentLens === 'blend') {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        if (Math.random() > 0.4) {
          addSparkle(mx, my, currentLens === 'art' ? 2 : 1);
        }
      }
    });

    canvas.addEventListener('pointerdown', (e) => {
      sound.init();
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      addSparkle(mx, my, currentLens === 'art' ? 12 : 6);
      if (currentLens === 'art') {
        sound.playPentatonic(pentatonicStep++);
      }
    });


    canvas.addEventListener('click', (e) => {
      sound.init();
      const rect = canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;

      if (currentGame === 'knights') {
        handleKnightsClick(clickX, clickY);
      } else if (currentGame === 'go') {
        handleGoClick(clickX, clickY);
      } else if (currentGame === 'checkers') {
        handleCheckersClick(clickX, clickY);
      } else if (currentGame === 'chess') {
        handleChessClick(clickX, clickY);
      } else if (currentGame === 'euchre') {
        handleEuchreClick(clickX, clickY);
      } else if (currentGame === 'world') {
        handleWorldClick(clickX, clickY);
      }
    });

    function handleKnightsClick(clickX, clickY) {
      const size = 8;
      const cell = canvas.width / size;
      const col = Math.floor(clickX / cell);
      const row = Math.floor(clickY / cell);
      if (col < 0 || col >= size || row < 0 || row >= size) return;

      const targetIdx = row * size + col;
      if (knightsState.visited[targetIdx]) return; // already visited

      const activeK = knightsState.turn === 1 ? knightsState.knight1 : knightsState.knight2;
      
      // If direct valid move: take it
      if (isValidKnightMove(activeK.r, activeK.c, row, col)) {
        activeK.r = row;
        activeK.c = col;
        knightsState.visited[targetIdx] = true;
        sound.playChime(knightsState.turn === 1 ? 528 : 432);
        knightsState.turn = knightsState.turn === 1 ? 2 : 1;
        updateKnightsUI();
      } else if (isSuperChillActive) {
        // ZERO WRONG ANSWERS: Soft-snap to the nearest valid unvisited square!
        let nearestMove = null;
        let nearestDist = Infinity;
        for (let r = 0; r < size; r++) {
          for (let c = 0; c < size; c++) {
            const idx = r * size + c;
            if (!knightsState.visited[idx] && isValidKnightMove(activeK.r, activeK.c, r, c)) {
              const d = Math.hypot(r - row, c - col);
              if (d < nearestDist) {
                nearestDist = d;
                nearestMove = { r, c, idx };
              }
            }
          }
        }
        if (nearestMove) {
          activeK.r = nearestMove.r;
          activeK.c = nearestMove.c;
          knightsState.visited[nearestMove.idx] = true;
          sound.playChime(knightsState.turn === 1 ? 528 : 432);
          knightsState.turn = knightsState.turn === 1 ? 2 : 1;
          updateKnightsUI();
        }
      }

      // Check Victory
      if (knightsState.visited.every(Boolean)) {
        setTimeout(() => {
          sound.playChime(660);
          alert('🌟 Harmony Complete! Both Knights have woven all 64 letters across the sacred grid together.');
        }, 300);
      }
    }

    function handleCheckersClick(clickX, clickY) {
      const size = 8;
      const cell = canvas.width / size;
      const col = Math.floor(clickX / cell);
      const row = Math.floor(clickY / cell);
      if (col < 0 || col >= size || row < 0 || row >= size) return;

      const key = `${row},${col}`;
      const piece = checkersState.pieces[key];

      // If no piece is selected, select friendly piece
      if (!checkersState.selected) {
        if (piece && piece.color === checkersState.turn) {
          checkersState.selected = { r: row, c: col };
          sound.playChime(432);
        }
        return;
      }

      // If piece is already selected
      const { r: sr, c: sc } = checkersState.selected;
      const selKey = `${sr},${sc}`;
      const selPiece = checkersState.pieces[selKey];

      // If clicking same piece or another friendly piece, reselect
      if (piece && piece.color === checkersState.turn) {
        checkersState.selected = { r: row, c: col };
        sound.playChime(432);
        return;
      }

      // Check move: 1 step diagonal (glide) or 2 step diagonal (kintsugi jump)
      const dr = Math.abs(row - sr);
      const dc = Math.abs(col - sc);

      if ((row + col) % 2 === 1 && !piece) {
        if (dr === 1 && dc === 1) {
          // Gentle glide
          delete checkersState.pieces[selKey];
          checkersState.pieces[key] = selPiece;
          checkersState.selected = null;
          sound.playStoneThunk(checkersState.turn === 'red' ? 320 : 260);
          checkersState.turn = checkersState.turn === 'red' ? 'white' : 'red';
          updateCheckersUI();
        } else if (dr === 2 && dc === 2) {
          // Kintsugi Jump: Partner stone is mended with 24k gold!
          const midR = (row + sr) / 2;
          const midC = (col + sc) / 2;
          const midKey = `${midR},${midC}`;
          const jumpedPiece = checkersState.pieces[midKey];

          if (jumpedPiece) {
            // Rather than capturing/deleting, both become golden!
            jumpedPiece.isGolden = true;
            selPiece.isGolden = true;
            delete checkersState.pieces[selKey];
            checkersState.pieces[key] = selPiece;
            checkersState.mendedRibbons.push({ r1: sr, c1: sc, r2: row, c2: col });
            checkersState.selected = null;
            sound.playChime(528); // 528 Hz DNA repair / golden chime
            checkersState.turn = checkersState.turn === 'red' ? 'white' : 'red';
            updateCheckersUI();
          }
        } else if (isSuperChillActive) {
          // Super-Chill: Glide gracefully anyway (Zero Wrong Answers)
          delete checkersState.pieces[selKey];
          checkersState.pieces[key] = selPiece;
          checkersState.selected = null;
          sound.playChime(432);
          checkersState.turn = checkersState.turn === 'red' ? 'white' : 'red';
          updateCheckersUI();
        }
      }
    }



    function handleWorldClick(clickX, clickY) {
      sound.init();
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;
      const distFromCenter = Math.hypot(clickX - cx, clickY - cy);

      // Check if clicking near any guardian
      for (const g of worldState.guardians) {
        if (Math.hypot(clickX - g.x, clickY - g.y) < 50) {
          sound.playChime(528);
          setTimeout(() => sound.playChime(660), 200);
          const wisTitle = document.getElementById('wisdomTitle');
          const wisText = document.getElementById('wisdomText');
          wisTitle.textContent = g.title;
          wisText.textContent = `The guardian of ${g.title}: ${g.desc}. In the journey toward recovery, all four elements are held in balance without judgment or exclusion.`;
          updateWorldUI();
          return;
        }
      }

      // If clicking wreath or center
      sound.playChime(432);
      setTimeout(() => sound.playChime(528), 180);
      worldState.wandsHarmonized++;
      updateWorldUI();
    }

    function handleEuchreClick(clickX, clickY) {
      const hand = euchreState.playerHand;
      for (let i = 0; i < hand.length; i++) {
        const c = hand[i];
        if (clickX >= c._x && clickX <= c._x + c._w && clickY >= c._y && clickY <= c._y + c._h) {
          // Play this card into the trick
          const played = hand.splice(i, 1)[0];
          euchreState.tableTrick = [played, euchreState.partnerCard];
          sound.playStoneThunk(380);
          euchreState.tricksShared++;
          updateEuchreUI();

          // Harmonic chime
          setTimeout(() => {
            sound.playChime(528);
          }, 300);

          // Clear trick after 2.5 seconds to proceed with calm pacing
          setTimeout(() => {
            euchreState.tableTrick = [];
            if (euchreState.playerHand.length === 0) {
              sound.playChime(660);
              setTimeout(() => {
                alert('🌲 Canoe Fellowship Complete! All 5 tricks peacefully woven with your partner.');
                resetEuchre();
              }, 400);
            }
          }, 2200);

          break;
        }
      }
    }

    function handleChessClick(clickX, clickY) {
      const size = 8;
      const cell = canvas.width / size;
      const col = Math.floor(clickX / cell);
      const row = Math.floor(clickY / cell);
      if (col < 0 || col >= size || row < 0 || row >= size) return;

      const key = `${row},${col}`;
      const piece = chessState.pieces[key];

      if (!chessState.selected) {
        if (piece && piece.side === chessState.turn) {
          chessState.selected = { r: row, c: col };
          sound.playChime(432);
        }
        return;
      }

      const { r: sr, c: sc } = chessState.selected;
      const selKey = `${sr},${sc}`;
      const selPiece = chessState.pieces[selKey];

      if (piece && piece.side === chessState.turn) {
        chessState.selected = { r: row, c: col };
        sound.playChime(432);
        return;
      }

      // Sanctuary Chess: Move without elimination
      // Pieces can step toward the center hearth
      delete chessState.pieces[selKey];
      chessState.pieces[key] = selPiece;
      chessState.selected = null;

      if (selPiece.type === 'K') {
        if (selPiece.side === 'white') chessState.whiteKing = { r: row, c: col };
        else chessState.blackKing = { r: row, c: col };
      }

      sound.playStoneThunk(340);
      chessState.turn = chessState.turn === 'white' ? 'black' : 'white';
      updateChessUI();

      // Check if both kings reached the central 2x2 hearth
      const wNear = Math.abs(chessState.whiteKing.r - 3.5) <= 1 && Math.abs(chessState.whiteKing.c - 3.5) <= 1;
      const bNear = Math.abs(chessState.blackKing.r - 3.5) <= 1 && Math.abs(chessState.blackKing.c - 3.5) <= 1;
      if (wNear && bNear && !chessState.hearthReached) {
        chessState.hearthReached = true;
        sound.playChime(528);
        setTimeout(() => sound.playChime(660), 400);
      }
    }

    function handleGoClick(clickX, clickY) {
      const size = goState.size;
      const margin = 50;
      const step = (canvas.width - margin * 2) / (size - 1);

      const col = Math.round((clickX - margin) / step);
      const row = Math.round((clickY - margin) / step);
      if (col < 0 || col >= size || row < 0 || row >= size) return;

      const key = `${row},${col}`;
      if (goState.stones[key]) return; // Space occupied

      // Place Stone with Breath
      goState.stones[key] = goState.turn;
      sound.playStoneThunk(goState.turn === 'B' ? 240 : 320);

      // Alternate turn
      goState.turn = goState.turn === 'B' ? 'W' : 'B';
      updateGoUI();
    }

    
    const LENS_DATA = {
      knights: {
        title: {
          blend: "🐴 Two Knights' Tour • Bilateral Saccade Mode",
          art: "🦄 The Dancing Pony & Unicorn's Trail",
          science: "🔬 Bilateral Midline Oculomotor Neuro-Rehabilitation (8×8)"
        },
        cardTitle: {
          blend: "🐴 Two Knights' Tour",
          art: "🦄 The Dancing Ponies",
          science: "🐴 Bilateral Midline Tour"
        },
        cardBadge: {
          blend: "BILATERAL / MIDLINE",
          art: "🌈 WONDER & PLAY",
          science: "EMA COHERENCE: 0.10 Hz"
        },
        cardDesc: {
          blend: "Two allied knights leap in 'L' strokes across the 8×8 grid, illuminating letters to weave words of healing without getting stranded.",
          art: "Two gentle ponies leap through a meadow of hidden stars! When they jump, golden letters light up like magic stepping stones.",
          science: "Quadratic L-vector knight displacement trains voluntary saccadic jumps across the vertical midline, breaking motor perseveration in stroke rehab."
        },
        wisdomTitle: {
          blend: "The Symmetry of the Knight",
          art: "How the Ponies Jump Together",
          science: "Midline Saccades & Callosal Transfer"
        },
        wisdomText: {
          blend: "Unlike rigid linear rooks, the Knight leaps over obstacles with an 'L' vector. In neuro-rehabilitation, it breaks motor perseveration and trains flexible lateral problem solving across the body's midline.",
          art: "Ponies don't run in straight lines—they leap gracefully over hurdles! Each step reveals a friendly sparkling letter to guide you home.",
          science: "Bi-hemispheric cooperation engages the corpus callosum at 0.10 Hz resonance. Magnetic snap eliminates frustration while retraining visual search pathways."
        },
        subLabel: {
          blend: "Squares Illuminated Together",
          art: "Magic Stars Awakened ✨",
          science: "Cooperative Glyphic Intersections"
        }
      },
      go: {
        title: {
          blend: "⚪ Cooperative Go (Weiqi) • Breathing Liberties & Living Qi",
          art: "⚪ River Pebbles & Rippling Waters",
          science: "🔬 Combinatorial Liberty Matrix & Parasympathetic Pacing"
        },
        cardTitle: {
          blend: "⚪ Cooperative Go (Weiqi)",
          art: "⚪ River Pebbles",
          science: "⚪ 9×9 Kaya Liberty Matrix"
        },
        cardBadge: {
          blend: "QI / BREATHING ROOM",
          art: "🍃 PEACEFUL FLOW",
          science: "NON-ZERO-SUM TONE"
        },
        cardDesc: {
          blend: "Place Black Slate & White Shell stones on a 9×9 Kaya grid. Cooperate to give every stone living eyes and breathing liberties.",
          art: "Drop smooth river stones into calm water. Watch the golden water ripples float out with warm singing bowl sounds!",
          science: "Reverses zero-sum territorial encirclement. Both players maintain interconnected breathing eyes, pacifying sympathetic fight-or-flight arousal."
        },
        wisdomTitle: {
          blend: "Qi (氣) & Living Eyes",
          art: "The Singing River Stones",
          science: "Autonomic Down-Regulation via Weiqi"
        },
        wisdomText: {
          blend: "Created over 4,000 years ago as a cognitive pacifier. In our cooperative sanctuary, players place Black Slate and White Shell stones together so every group maintains liberties to breathe.",
          art: "In ancient times, wise travelers dropped stones in the river to make music. Every stone is cozy and has plenty of room to breathe under the warm sun.",
          science: "The 240 Hz and 320 Hz acoustic thunk mimics haptic Kaya wood vibration, stimulating vagal parasympathetic afferents to lower heart rate."
        },
        subLabel: {
          blend: "Placed with Living Breath",
          art: "Smooth River Pebbles Gathered 🍃",
          science: "Non-Zero-Sum Liberties Preserved"
        }
      },
      checkers: {
        title: {
          blend: "🔴 Kintsugi Checkers • Mending Fractures with Gold",
          art: "✨ Golden Spark Trails & Mending Friends",
          science: "🔬 Reversible Non-Punitive Mosaic Kinematics"
        },
        cardTitle: {
          blend: "🔴 Kintsugi Checkers",
          art: "✨ Golden Ribbon Trail",
          science: "🔴 Kintsugi Fracture Repair"
        },
        cardBadge: {
          blend: "REPAIR & MENDING",
          art: "💛 SHINING GOLD",
          science: "ZERO ATTRITION"
        },
        cardDesc: {
          blend: "Leaping over a stone leaves an unbroken 24k burnished gold ribbon, mending broken pathways into a radiant mosaic.",
          art: "Jump over your friends to give them a glowing golden hug! Nobody gets taken away—we just paint gold bridges between everyone.",
          science: "Eliminates piece capture trauma. Every jump synthesizes a 24k urushi gold lacquer vector, transforming loss metrics into restorative completion."
        },
        wisdomTitle: {
          blend: "The Art of Kintsugi (金継ぎ)",
          art: "The Golden Hug Bridge",
          science: "Psychological Safety in Non-Elimination"
        },
        wisdomText: {
          blend: "When jumping over a partner's checker, you do not eliminate it; you weave a 24k gold leaf ribbon connecting the squares, transforming obstacles into permanent resilience.",
          art: "When a cup gets a little crack, in Japan they fix it with real gold so it becomes even more beautiful than before. We do that with our game!",
          science: "Removes loss aversion and cortisol spikes inherent in capture mechanics. Patient remains in restorative flow state without defensive posturing."
        },
        subLabel: {
          blend: "24k Gold Kintsugi Mends",
          art: "Golden Bridges Built Together 💛",
          science: "Continuous Seam Transformations"
        }
      },
      chess: {
        title: {
          blend: "👑 Sanctuary Chess • The Village Hearth",
          art: "🏰 King & Queen Warm Campfire Hug",
          science: "🔬 Cooperative Centripetal Trajectory Convergence"
        },
        cardTitle: {
          blend: "👑 Sanctuary Chess",
          art: "🏰 Campfire Hug Chess",
          science: "👑 Centripetal Hearth Escort"
        },
        cardBadge: {
          blend: "HEARTH PROTECTION",
          art: "🔥 WARM HEARTH",
          science: "528 HZ HARMONIC"
        },
        cardDesc: {
          blend: "No captures or combat: escort both Kings to the central Tilikum hearth while exchanging 528 Hz harmonic chords.",
          art: "Walk the gentle King and Queen through the garden so they can sit together by the cozy campfire and listen to sweet bells.",
          science: "Transforms antagonistic checkmate into convergent centripetal escort, exchanging 528 Hz chords when Kings unify in the central quadrant."
        },
        wisdomTitle: {
          blend: "Escorting to the Hearth",
          art: "The Cozy Campfire",
          science: "Centripetal Kinship & Acoustic Chords"
        },
        wisdomText: {
          blend: "Pieces are not combatants, but clan travelers escorting both Kings to the center Tilikum square, chiming in resonant 528 Hz fifths upon meeting.",
          art: "No battles here! Everyone in the castle walks peacefully together to gather around the warm, crackling hearth fire.",
          science: "Centripetal movement vectors converge on the 2×2 center hearth, activating spatial depth perception without combat stress hormones."
        },
        subLabel: {
          blend: "Escorting Kings to Hearth",
          art: "Steps Toward the Cozy Fire 🔥",
          science: "Centripetal Vector Alignment"
        }
      },
      euchre: {
        title: {
          blend: "🃏 Canoe Euchre • 2v2 Relational Partnership",
          art: "🛶 Canoe Story Cards with Friends",
          science: "🔬 Procedural Memory Activation & Bower Hierarchy"
        },
        cardTitle: {
          blend: "🃏 Canoe Euchre",
          art: "🛶 Canoe Story Cards",
          science: "🃏 2v2 Procedural Activation"
        },
        cardBadge: {
          blend: "INTERGENERATIONAL",
          art: "🌟 TOGETHER",
          science: "COGNITIVE PRESERVATION"
        },
        cardDesc: {
          blend: "2v2 cooperative trick-passing with large-print PocketGull figures, procedural memory activation, and zero penalty traps.",
          art: "Share fun picture cards with your partner in a calm wooden canoe! You take turns peacefully paddling down the river.",
          science: "Reactivates deep procedural card-play memories in mild cognitive impairment and stroke recovery through large-print high-contrast figures."
        },
        wisdomTitle: {
          blend: "Silent Kinship & Procedural Flow",
          art: "Paddling the Canoe Together",
          science: "Procedural Card Play in Neuro-Geriatrics"
        },
        wisdomText: {
          blend: "Euchre requires profound trust in your partner across the table. For dementia and stroke recovery, card play awakens deep procedural memory without verbal strain.",
          art: "When you sit in a canoe, you paddle in gentle rhythm with your friend. You don't need any words—just smiles and teamwork!",
          science: "Trump suit identification and bower hierarchies stimulate working memory while the cooperative scoring structure completely eliminates performance anxiety."
        },
        subLabel: {
          blend: "Shared in Kinship & Flow",
          art: "Peaceful River Paddles 🛶",
          science: "Cognitive Tricks Harmonized"
        }
      },
      world: {
        title: {
          blend: "🪐 XXI • The World (Le Monde) • Cosmic Integration & Wholeness",
          art: "🪐 The Cosmic Animal Wreath & Magic Ring",
          science: "🔬 Tetramorph Orthogonal Equilibrium & 432–660 Hz Harmonics"
        },
        cardTitle: {
          blend: "🪐 The World (XXI)",
          art: "🪐 The Magic Animal Ring",
          science: "🪐 Tetramorph Mandorla (XXI)"
        },
        cardBadge: {
          blend: "INTEGRATION / WHOLENESS",
          art: "🕊️ WHOLENESS & JOY",
          science: "FOURIER GAUSSIAN FIT"
        },
        cardDesc: {
          blend: "The cosmic wreath of completion: four cherubic guardians anchoring the corners while the dancing anima unites mind, body, spirit, and cosmos.",
          art: "Touch the friendly bird, lion, angel, and bull! Watch the magical golden leaf ring spin and shower sparkling star bubbles.",
          science: "Vesica Piscis laurel geometry calibrated to 1000 UPM em-square metrics, coordinating 432 Hz, 528 Hz, 660 Hz, and 330 Hz elemental acoustic frequencies."
        },
        wisdomTitle: {
          blend: "The Crown of the Major Arcana",
          art: "The Four Friendly Animals & The Ring",
          science: "Tetramorph Equilibrium & Somatic Wholeness"
        },
        wisdomText: {
          blend: "The final card of the Tarot journey represents complete integration, somatic closure, and the joy of arriving home in one's own healed body and peaceful spirit.",
          art: "The kind Angel brings fresh air, the Eagle brings clear water, the Lion brings warm courage, and the Bull keeps our feet gently on the earth. Everything is happy and complete!",
          science: "Orthogonal quadrant balancing (Air 432 Hz, Water 528 Hz, Fire 660 Hz, Earth 330 Hz) mirrors Louise Sloan 5:1 optotype spatial symmetry and direct retinal grounding."
        },
        subLabel: {
          blend: "Four Elements Harmonized",
          art: "All Animal Friends Singing! 🌈",
          science: "Orthogonal Quadrant Coherence"
        }
      }
    };

    function applyLensToUI() {
      const data = LENS_DATA[currentGame];
      if (!data) return;

      const bannerTitle = document.getElementById('gameTitleBanner');
      const wisTitle = document.getElementById('wisdomTitle');
      const wisText = document.getElementById('wisdomText');
      const statSub = document.getElementById('statSubLabel');

      if (bannerTitle) bannerTitle.innerHTML = data.title[currentLens];
      if (wisTitle) wisTitle.textContent = data.wisdomTitle[currentLens];
      if (wisText) wisText.textContent = data.wisdomText[currentLens];
      if (statSub) statSub.textContent = data.subLabel[currentLens];

      // Update sidebar card descriptions according to active lens
      document.querySelectorAll('.game-card').forEach(card => {
        const g = card.dataset.game;
        const gData = LENS_DATA[g];
        if (gData) {
          const titleEl = card.querySelector('.game-card-title');
          const badgeEl = card.querySelector('.game-card-badge');
          const descEl = card.querySelector('.game-card-desc');
          if (titleEl) titleEl.textContent = gData.cardTitle[currentLens];
          if (badgeEl) badgeEl.textContent = gData.cardBadge[currentLens];
          if (descEl) descEl.textContent = gData.cardDesc[currentLens];
        }
      });
    }

    // Lens Switching Buttons
    
    // Player Mode Selector Buttons (Solo vs Companion vs Duet)
    document.querySelectorAll('.btn-player-mode').forEach(btn => {
      btn.addEventListener('click', () => {
        sound.init();
        document.querySelectorAll('.btn-player-mode').forEach(b => {
          b.classList.remove('active');
          b.style.background = 'transparent';
          b.style.borderColor = 'transparent';
          b.style.color = '#94a3b8';
        });
        btn.classList.add('active');
        btn.style.background = 'rgba(20, 184, 166, 0.25)';
        btn.style.borderColor = 'rgba(45, 212, 191, 0.5)';
        btn.style.color = '#fff';

        currentPlayMode = btn.dataset.mode;
        sound.playChime(currentPlayMode === 'solo' ? 528 : (currentPlayMode === 'companion' ? 660 : 432));
        
        // Refresh UI banner
        if (currentGame === 'knights') updateKnightsUI();
        else if (currentGame === 'go') updateGoUI();
        else if (currentGame === 'checkers') updateCheckersUI();
        else if (currentGame === 'chess') updateChessUI();
        else if (currentGame === 'euchre') updateEuchreUI();

        triggerCompanionTurnIfNeeded();
      });
    });


    document.querySelectorAll('.btn-lens').forEach(btn => {
      btn.addEventListener('click', () => {
        sound.init();
        document.querySelectorAll('.btn-lens').forEach(b => {
          b.classList.remove('active');
          b.style.background = 'transparent';
          b.style.borderColor = 'transparent';
          b.style.color = '#cbd5e1';
        });
        btn.classList.add('active');
        btn.style.background = 'linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(56, 189, 248, 0.3))';
        btn.style.borderColor = 'rgba(45, 212, 191, 0.5)';
        btn.style.color = '#fff';

        currentLens = btn.dataset.lens;
        applyLensToUI();
        sound.playChime(currentLens === 'art' ? 660 : (currentLens === 'science' ? 432 : 528));
      });
    });


    /* ─── UI CONTROLS ─── */
    document.querySelectorAll('.game-card').forEach(card => {
      card.addEventListener('click', () => {
        sound.init();
        document.querySelectorAll('.game-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        currentGame = card.dataset.game;

        const bannerTitle = document.getElementById('gameTitleBanner');
        const wisTitle = document.getElementById('wisdomTitle');
        const wisText = document.getElementById('wisdomText');

        if (currentGame === 'knights') {
          bannerTitle.innerHTML = '🐴 Active: <strong>The Two Knights\' Tour • Bilateral Saccade Mode</strong>';
          applyLensToUI(); // update with current lens
          wisTitle.textContent = LENS_DATA['knights'].wisdomTitle[currentLens];
          wisText.textContent = 'Unlike rigid linear rooks, the Knight leaps over obstacles with an \'L\' vector. In neuro-rehabilitation, it breaks motor perseveration and trains flexible lateral problem solving across the body\'s midline.';
          resetKnights();
        } else if (currentGame === 'go') {
          bannerTitle.innerHTML = '⚪ Active: <strong>Cooperative Go (Weiqi) • Breathing Liberties & Living Qi</strong>';
          applyLensToUI();
          wisTitle.textContent = LENS_DATA['go'].wisdomTitle[currentLens];
          wisText.textContent = 'Created over 4,000 years ago as a cognitive pacifier. In our cooperative sanctuary, players place Black Slate and White Shell stones together so every group maintains liberties to breathe.';
          resetGo();
        } else if (currentGame === 'checkers') {
          bannerTitle.innerHTML = '🔴 Active: <strong>Kintsugi Checkers • Mending Fractures with Gold</strong>';
          applyLensToUI();
          wisTitle.textContent = LENS_DATA['checkers'].wisdomTitle[currentLens];
          wisText.textContent = 'When jumping over a partner\'s checker, you do not eliminate it; you weave a 24k gold leaf ribbon connecting the squares, transforming obstacles into permanent resilience.';
          resetCheckers();
        } else if (currentGame === 'chess') {
          bannerTitle.innerHTML = '👑 Active: <strong>Sanctuary Chess • The Village Hearth</strong>';
          applyLensToUI();
          wisTitle.textContent = LENS_DATA['chess'].wisdomTitle[currentLens];
          wisText.textContent = 'Pieces are not combatants, but clan travelers escorting both Kings to the center Tilikum square, chiming in resonant 528 Hz fifths upon meeting.';
          resetChess();
        } else if (currentGame === 'euchre') {
          bannerTitle.innerHTML = '🃏 Active: <strong>Canoe Euchre • 2v2 Relational Partnership</strong>';
          applyLensToUI();
          wisTitle.textContent = LENS_DATA['euchre'].wisdomTitle[currentLens];
          wisText.textContent = 'Euchre requires profound trust in your partner across the table. For dementia and stroke recovery, card play awakens deep procedural memory without verbal strain.';
          resetEuchre();
        } else if (currentGame === 'world') {
          bannerTitle.innerHTML = '🪐 Active: <strong>XXI • The World (Le Monde) • Cosmic Integration & Wholeness</strong>';
          applyLensToUI();
          wisTitle.textContent = LENS_DATA['world'].wisdomTitle[currentLens];
          wisText.textContent = 'The final card of the Tarot journey represents complete integration, somatic closure, and the joy of arriving home in one\'s own healed body and peaceful spirit.';
          resetWorld();
        }
      });
    });

    document.getElementById('btnResetGame').addEventListener('click', () => {
      sound.init();
      if (currentGame === 'knights') resetKnights();
      else if (currentGame === 'go') resetGo();
      else if (currentGame === 'checkers') resetCheckers();
      else if (currentGame === 'chess') resetChess();
      else if (currentGame === 'euchre') resetEuchre();
      else if (currentGame === 'world') resetWorld();
    });

    document.getElementById('btnAudioToggle').addEventListener('click', function() {
      sound.init();
      sound.enabled = !sound.enabled;
      this.textContent = sound.enabled ? '🔊 Audio: ON' : '🔇 Audio: MUTED';
    });

    // Theme Switcher 3-cycle
    document.getElementById('btnThemeToggle').addEventListener('click', function() {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      let next = 'washi';
      let label = '🎨 Theme: Washi (和紙)';
      if (current === 'dark') {
        next = 'washi';
        label = '🎨 Theme: Washi (和紙)';
      } else if (current === 'washi') {
        next = 'pbm';
        label = '🔴 Theme: 670nm PBM Night Shift';
      } else {
        next = 'dark';
        label = '🎨 Theme: Dark';
      }
      document.documentElement.setAttribute('data-theme', next);
      this.textContent = label;
    });

    // Initialize
    applyLensToUI();
    resetKnights();
    requestAnimationFrame(render);
  
