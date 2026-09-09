/* PocketGull - Neurotypographic Saccade & Board Engine */


    /* ========================================================================== */
    /* PROCEDURAL HEALING AUDIO & SOLFEGGIO RESONATOR                             */
    /* ========================================================================== */
    class SanctuaryAudio {
      constructor() {
        this.ctx = null;
        this.enabled = true;
        this.masterGain = null;
        this.currentFreq = 528;
        this.droneOsc = null;
        this.binauralOsc = null;
        this.sonarOsc = null;
        this.sonarPanner = null;
        this.sonarGain = null;
        this.isSonarActive = false;
      }

      init() {
        if (this.ctx) {
          if (this.ctx.state === 'suspended') {
            try { this.ctx.resume(); } catch (_) {}
          }
          return;
        }
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();
        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.setValueAtTime(0.18, this.ctx.currentTime);
        this.masterGain.connect(this.ctx.destination);
        this.startDrone();
      }

      startDrone() {
        if (!this.ctx || !this.enabled) return;
        const now = this.ctx.currentTime;

        // Base peaceful drone
        this.droneOsc = this.ctx.createOscillator();
        this.droneOsc.type = 'sine';
        this.droneOsc.frequency.setValueAtTime(this.currentFreq / 2, now);

        // Alpha / Theta binaural beat (6 Hz difference)
        this.binauralOsc = this.ctx.createOscillator();
        this.binauralOsc.type = 'triangle';
        this.binauralOsc.frequency.setValueAtTime(this.currentFreq / 2 + 6, now);

        const droneGain = this.ctx.createGain();
        droneGain.gain.setValueAtTime(0.08, now);

        this.droneOsc.connect(droneGain);
        this.binauralOsc.connect(droneGain);
        droneGain.connect(this.masterGain);

        this.droneOsc.start();
        this.binauralOsc.start();
      }

      setFrequency(freq) {
        this.currentFreq = freq;
        if (this.droneOsc && this.binauralOsc && this.ctx) {
          const now = this.ctx.currentTime;
          this.droneOsc.frequency.setTargetAtTime(freq / 2, now, 0.4);
          this.binauralOsc.frequency.setTargetAtTime(freq / 2 + 6, now, 0.4);
        }
      }

      initSonar() {
        if (!this.ctx || this.sonarOsc) return;
        try {
          const now = this.ctx.currentTime;
          this.sonarPanner = this.ctx.createStereoPanner ? this.ctx.createStereoPanner() : null;
          this.sonarOsc = this.ctx.createOscillator();
          this.sonarOsc.type = 'sine';
          this.sonarOsc.frequency.setValueAtTime(440, now);

          this.sonarGain = this.ctx.createGain();
          this.sonarGain.gain.setValueAtTime(0.0001, now);

          this.sonarOsc.connect(this.sonarGain);
          if (this.sonarPanner) {
            this.sonarGain.connect(this.sonarPanner);
            this.sonarPanner.connect(this.masterGain);
          } else {
            this.sonarGain.connect(this.masterGain);
          }
          this.sonarOsc.start(now);
        } catch (e) {}
      }

      setSonarActive(active) {
        this.isSonarActive = active;
        if (active) {
          this.init();
          this.initSonar();
          if (this.sonarGain && this.ctx) {
            this.sonarGain.gain.setTargetAtTime(0.08, this.ctx.currentTime, 0.08);
          }
        } else if (this.sonarGain && this.ctx) {
          this.sonarGain.gain.setTargetAtTime(0.0001, this.ctx.currentTime, 0.08);
        }
      }

      updateSonar(normX, normY, isNearStroke, isInsideStroke) {
        if (!this.isSonarActive || !this.ctx || !this.sonarOsc) return;
        const now = this.ctx.currentTime;
        // Panning: -1 (left) to +1 (right)
        if (this.sonarPanner) {
          const pan = Math.max(-1, Math.min(1, normX));
          this.sonarPanner.pan.setTargetAtTime(pan, now, 0.04);
        }
        // Pitch: -1 (top) -> High pitch (880 Hz), +1 (bottom) -> Low pitch (220 Hz)
        const pitch = 440 * Math.pow(2, -normY * 1.0);
        const clampedPitch = Math.max(160, Math.min(1200, pitch));
        this.sonarOsc.frequency.setTargetAtTime(clampedPitch, now, 0.04);

        if (this.sonarGain) {
          const targetVol = isInsideStroke ? 0.16 : (isNearStroke ? 0.09 : 0.025);
          this.sonarGain.gain.setTargetAtTime(targetVol, now, 0.05);
        }
      }

      playBeaconPing(panVal, distRatio) {
        if (!this.ctx || !this.enabled) return;
        try {
          const now = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          const panner = this.ctx.createStereoPanner ? this.ctx.createStereoPanner() : null;

          osc.type = 'sine';
          osc.frequency.setValueAtTime(880, now);
          osc.frequency.exponentialRampToValueAtTime(1320, now + 0.12);

          gain.gain.setValueAtTime(0.28, now);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.35);

          osc.connect(gain);
          if (panner) {
            panner.pan.setValueAtTime(Math.max(-1, Math.min(1, panVal)), now);
            gain.connect(panner);
            panner.connect(this.masterGain);
          } else {
            gain.connect(this.masterGain);
          }

          osc.start(now);
          osc.stop(now + 0.36);
        } catch (e) {}
      }

      playChimeAtFreq(freq, duration = 1.6) {
        if (!this.ctx || !this.enabled) return;
        try {
          const now = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();

          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now);

          gain.gain.setValueAtTime(0.28, now);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

          osc.connect(gain);
          gain.connect(this.masterGain);

          osc.start(now);
          osc.stop(now + duration + 0.1);
        } catch (e) {}
      }

      playChime(noteMultiplier = 1.0) {
        if (!this.ctx || !this.enabled) return;
        try {
          const now = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();

          osc.type = 'sine';
          osc.frequency.setValueAtTime(this.currentFreq * noteMultiplier, now);

          gain.gain.setValueAtTime(0.25, now);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.8);

          osc.connect(gain);
          gain.connect(this.masterGain);

          osc.start(now);
          osc.stop(now + 1.9);
        } catch (e) {}
      }

      playRipple() {
        if (!this.ctx || !this.enabled) return;
        try {
          const now = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();

          osc.type = 'triangle';
          osc.frequency.setValueAtTime(this.currentFreq * 1.5, now);
          osc.frequency.exponentialRampToValueAtTime(this.currentFreq * 0.75, now + 0.35);

          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

          osc.connect(gain);
          gain.connect(this.masterGain);

          osc.start(now);
          osc.stop(now + 0.36);
        } catch (e) {}
      }

      playTibetanBowl(freq = 432) {
        if (!this.ctx || !this.enabled) return;
        try {
          const now = this.ctx.currentTime;
          // Meditative partials: Fundamental (1.0), Octave+Fifth (2.76), High chime (5.4)
          const partials = [
            { ratio: 1.0, gain: 0.22, decay: 3.2 },
            { ratio: 2.76, gain: 0.10, decay: 2.4 },
            { ratio: 5.4, gain: 0.04, decay: 1.6 }
          ];
          partials.forEach(p => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq * p.ratio, now);
            gain.gain.setValueAtTime(p.gain, now);
            gain.gain.exponentialRampToValueAtTime(0.00005, now + p.decay);
            osc.connect(gain);
            gain.connect(this.masterGain);
            osc.start(now);
            osc.stop(now + p.decay + 0.1);
          });
        } catch (e) {}
      }

      /* ─── 03-02-1987 Acoustic Kinetic Harp Synthesis ─── */
      playHarpPluck(freq, pan = 0, velocity = 1.0) {
        if (!this.ctx || !this.enabled) return;
        try {
          if (this.ctx.state === 'suspended') this.ctx.resume();
          const now = this.ctx.currentTime;
          const clampedPan = Math.max(-1, Math.min(1, pan));
          const panner = this.ctx.createStereoPanner ? this.ctx.createStereoPanner() : null;

          // Fundamental string tone (triangle wave for warm acoustic timber)
          const oscFund = this.ctx.createOscillator();
          oscFund.type = 'triangle';
          oscFund.frequency.setValueAtTime(freq, now);

          // 3:2 Golden Diapente fifth overtone (pure sine shimmer)
          const oscFifth = this.ctx.createOscillator();
          oscFifth.type = 'sine';
          oscFifth.frequency.setValueAtTime(freq * 1.5, now);

          const gainNode = this.ctx.createGain();
          const targetVol = Math.max(0.04, Math.min(0.26, 0.18 * velocity));
          gainNode.gain.setValueAtTime(targetVol, now);
          gainNode.gain.exponentialRampToValueAtTime(0.0001, now + 0.65);

          oscFund.connect(gainNode);
          oscFifth.connect(gainNode);

          if (panner) {
            panner.pan.setValueAtTime(clampedPan, now);
            gainNode.connect(panner);
            panner.connect(this.masterGain);
          } else {
            gainNode.connect(this.masterGain);
          }

          oscFund.start(now);
          oscFifth.start(now);
          oscFund.stop(now + 0.66);
          oscFifth.stop(now + 0.66);
        } catch (e) {}
      }

      /* ─── 03-02-1987 Diapente Harmonic Chord (216 Hz : 432 Hz : 648 Hz : 864 Hz) ─── */
      playDiapenteChord(root = 432, duration = 2.8) {
        if (!this.ctx || !this.enabled) return;
        try {
          if (this.ctx.state === 'suspended') this.ctx.resume();
          const now = this.ctx.currentTime;
          const chord = [
            { f: root * 0.5, gain: 0.18, type: 'sine', pan: 0, decay: duration * 1.2 },
            { f: root, gain: 0.22, type: 'triangle', pan: -0.25, decay: duration },
            { f: root * 1.5, gain: 0.18, type: 'sine', pan: 0.25, decay: duration * 0.9 },
            { f: root * 2.0, gain: 0.12, type: 'sine', pan: 0.40, decay: duration * 0.7 }
          ];
          chord.forEach(c => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            const panner = this.ctx.createStereoPanner ? this.ctx.createStereoPanner() : null;

            osc.type = c.type;
            osc.frequency.setValueAtTime(c.f, now);
            gain.gain.setValueAtTime(c.gain, now);
            gain.gain.exponentialRampToValueAtTime(0.00005, now + c.decay);

            osc.connect(gain);
            if (panner) {
              panner.pan.setValueAtTime(c.pan, now);
              gain.connect(panner);
              panner.connect(this.masterGain);
            } else {
              gain.connect(this.masterGain);
            }
            osc.start(now);
            osc.stop(now + c.decay + 0.1);
          });
        } catch (e) {}
      }

      /* ─── Anatomical Landmark Chimes ─── */
      playLandmarkChime(landmarkType, pan = 0) {
        if (!this.ctx || !this.enabled) return;
        try {
          switch (landmarkType) {
            case 'ingress': // Ingress Gate Apex (Topmost): Bright 648 Hz Diapente + 864 Hz shimmer
              this.playHarpPluck(648, pan, 1.25);
              setTimeout(() => this.playHarpPluck(864, pan, 0.90), 55);
              break;
            case 'waist': // Optical Waist (540 UPM / em-center): 486 Hz harmonic pluck
              this.playHarpPluck(486, pan, 1.10);
              break;
            case 'crossing': // Midline Crossing: Bilateral stereo harmonic strum
              this.playHarpPluck(432, -0.6, 1.0);
              setTimeout(() => this.playHarpPluck(648, 0.6, 1.0), 45);
              break;
            case 'ground': // Root Grounding (Bottom Baseline): Deep 216 Hz Tibetan bowl
              this.playTibetanBowl(216);
              break;
            case 'circuit': // Circuit Resolution: Grand 03-02-1987 Diapente chord
              this.playDiapenteChord(432, 2.8);
              break;
          }
        } catch (e) {}
      }
    }

    const sound = new SanctuaryAudio();

    // ─── HAPTIC & SCREEN READER ACCESSIBILITY HELPERS ───
    function triggerHaptic(type) {
      if (typeof navigator === 'undefined' || !navigator.vibrate) return;
      try {
        switch (type) {
          case 'ingress': // Ingress Gate / Top Apex
            navigator.vibrate([18, 30, 18]);
            break;
          case 'waist': // Optical Waist (540 UPM em-center)
            navigator.vibrate(14);
            break;
          case 'crossing': // Midline Crossing (X = 0)
            navigator.vibrate([12, 24]);
            break;
          case 'ground': // Root Grounding (Bottom baseline)
            navigator.vibrate([28, 40, 20]);
            break;
          case 'circuit': // Full loop circuit completed
          case 'complete': // Board completed
            navigator.vibrate([35, 60, 35, 60, 45]);
            break;
          case 'detent': // Waypoint / Landmark reached
            navigator.vibrate([22, 38, 22]);
            break;
          case 'groove': // Inside letterform stroke
            navigator.vibrate(12);
            break;
          case 'wall': // Drifting off boundary
            navigator.vibrate([16, 20]);
            break;
          case 'pulse': // S1/S2 heart pulse
            navigator.vibrate([20, 70, 15]);
            break;
        }
      } catch (e) {}
    }

    function announceSR(msg) {
      const el = document.getElementById('srAnnouncement');
      if (el) {
        el.textContent = '';
        setTimeout(() => { el.textContent = msg; }, 40);
      }
    }

    /* ========================================================================== */
    /* LETTERFORM GAMEBOARD GEOMETRIES & TOPOLOGIES                               */
    /* ========================================================================== */
    const BOARDS = {
      zero: {
        id: 'zero',
        char: '0',
        name: 'ISMP Slashed Zero (0̸)',
        moralTitle: 'The Wisdom of Unambiguous Care',
        moralDesc: 'In healthcare as in life, clear boundaries bring safety. The slashed zero unequivocally separates the zero from the circle of confusion, ensuring remedies heal and never harm.',
        waypoints: [
          { x: 0, y: -220 },
          { x: 140, y: -120 },
          { x: 160, y: 0 },
          { x: 140, y: 120 },
          { x: 0, y: 220 },
          { x: -140, y: 120 },
          { x: -160, y: 0 },
          { x: -140, y: -120 },
          // The Slashed Zero Bridge
          { x: -130, y: 150 },
          { x: 0, y: 0 },
          { x: 130, y: -150 }
        ],
        paths: [
          // Outer Ellipse
          { type: 'ellipse', cx: 0, cy: 0, rx: 160, ry: 220 },
          // Diagonal Drawbridge
          { type: 'line', x1: -130, y1: 150, x2: 130, y2: -150 }
        ],
        targets: [
          { x: 0, y: -220, label: 'North Gate', collected: false },
          { x: 160, y: 0, label: 'East Aperture', collected: false },
          { x: 0, y: 220, label: 'South Anchor', collected: false },
          { x: -160, y: 0, label: 'West Portal', collected: false },
          { x: 0, y: 0, label: 'Bridge Center', collected: false }
        ]
      },

      eight: {
        id: 'eight',
        char: '8',
        name: 'Figure Eight / Dual Counter (8)',
        moralTitle: 'The Infinity of Reciprocal Renewal',
        moralDesc: 'Breath, circulation, and compassion form an unbroken figure eight. Giving and receiving flow through the same central heart.',
        waypoints: [
          { x: 0, y: 0 },
          { x: 55, y: -45 },
          { x: 95, y: -90 },
          { x: 75, y: -160 },
          { x: 0, y: -205 },
          { x: -75, y: -160 },
          { x: -95, y: -90 },
          { x: -55, y: -45 },
          { x: 0, y: 0 },
          { x: 65, y: 55 },
          { x: 115, y: 110 },
          { x: 90, y: 185 },
          { x: 0, y: 235 },
          { x: -90, y: 185 },
          { x: -115, y: 110 },
          { x: -65, y: 55 }
        ],
        paths: [
          { type: 'circle', cx: 0, cy: -100, r: 105 },
          { type: 'circle', cx: 0, cy: 110, r: 125 }
        ],
        targets: [
          { x: 0, y: -205, label: 'Crown', collected: false },
          { x: 105, y: -100, label: 'Upper Loop Right', collected: false },
          { x: 0, y: 0, label: 'Heart Junction', collected: false },
          { x: -125, y: 110, label: 'Lower Loop Left', collected: false },
          { x: 0, y: 235, label: 'Base Root', collected: false }
        ]
      },

      inuktitut: {
        id: 'inuktitut',
        char: 'ᐃ',
        name: 'Inuktitut Syllabic "I" (ᐃ)',
        moralTitle: 'Inuit Qaujimajatuqangit (IQ) Environmental Harmony',
        moralDesc: 'The upward triangular syllabic evokes the shelter of the igloo and the quiet mountain ridge, reminding us that we are guests on this sacred earth.',
        waypoints: [
          { x: 0, y: -220 },
          { x: 60, y: -80 },
          { x: 120, y: 50 },
          { x: 180, y: 180 },
          { x: 90, y: 180 },
          { x: 0, y: 180 },
          { x: -90, y: 180 },
          { x: -180, y: 180 },
          { x: -120, y: 50 },
          { x: -60, y: -80 }
        ],
        paths: [
          { type: 'poly', points: [{ x: 0, y: -220 }, { x: 180, y: 180 }, { x: -180, y: 180 }, { x: 0, y: -220 }] }
        ],
        targets: [
          { x: 0, y: -220, label: 'Pinnacle Summit', collected: false },
          { x: 180, y: 180, label: 'Right Grounding', collected: false },
          { x: 0, y: 180, label: 'Baseline Center', collected: false },
          { x: -180, y: 180, label: 'Left Grounding', collected: false }
        ]
      },

      pipa: {
        id: 'pipa',
        char: '𑲒',
        name: 'Chinuk Pipa WA (𑲒)',
        moralTitle: 'River Stone Gentle Flow (Kamloops Wawa)',
        moralDesc: 'Soft curves carved by cascading glacial meltwater. Gentleness outlasts violence; soft water shapes the hardest stone.',
        waypoints: [
          { x: -160, y: 160 },
          { x: -120, y: -40 },
          { x: -60, y: -180 },
          { x: 0, y: -200 },
          { x: 70, y: -170 },
          { x: 80, y: -80 },
          { x: 0, y: 0 },
          { x: 65, y: 60 },
          { x: 0, y: 170 },
          { x: -65, y: 60 },
          { x: 0, y: 0 }
        ],
        paths: [
          { type: 'bezier', p0: { x: -160, y: 160 }, p1: { x: -80, y: -220 }, p2: { x: 120, y: -180 }, p3: { x: 0, y: 0 } },
          { type: 'circle', cx: 0, cy: 80, r: 90 }
        ],
        targets: [
          { x: -160, y: 160, label: 'River Origin', collected: false },
          { x: 0, y: -200, label: 'Crest', collected: false },
          { x: 0, y: 0, label: 'Eddy Pool', collected: false },
          { x: 0, y: 170, label: 'River Mouth', collected: false }
        ]
      },

      s: {
        id: 's',
        char: 'S',
        name: 'Sloan S-Curve Saccade (S)',
        moralTitle: 'Saccadic Decompression & Flexibility',
        moralDesc: 'Rigidity snaps in high winds, while the supple willow bends and flourishes. Relax your focus across the gentle double arc.',
        waypoints: [
          { x: 120, y: -180 },
          { x: 50, y: -210 },
          { x: -40, y: -190 },
          { x: -90, y: -120 },
          { x: -60, y: -50 },
          { x: 0, y: 0 },
          { x: 60, y: 50 },
          { x: 90, y: 120 },
          { x: 40, y: 190 },
          { x: -50, y: 210 },
          { x: -120, y: 180 },
          { x: -50, y: 210 },
          { x: 40, y: 190 },
          { x: 90, y: 120 },
          { x: 60, y: 50 },
          { x: 0, y: 0 },
          { x: -60, y: -50 },
          { x: -90, y: -120 },
          { x: -40, y: -190 },
          { x: 50, y: -210 }
        ],
        paths: [
          { type: 'bezier', p0: { x: 120, y: -180 }, p1: { x: -150, y: -220 }, p2: { x: -40, y: -20 }, p3: { x: 0, y: 0 } },
          { type: 'bezier', p0: { x: 0, y: 0 }, p1: { x: 40, y: 20 }, p2: { x: 150, y: 220 }, p3: { x: -120, y: 180 } }
        ],
        targets: [
          { x: 120, y: -180, label: 'Upper Terminal', collected: false },
          { x: -90, y: -120, label: 'Upper Spine', collected: false },
          { x: 0, y: 0, label: 'Waist Axis', collected: false },
          { x: 90, y: 120, label: 'Lower Spine', collected: false },
          { x: -120, y: 180, label: 'Lower Terminal', collected: false }
        ]
      },

      a: {
        id: 'a',
        char: 'A',
        name: 'Pinnacle Temple (A)',
        moralTitle: 'The Bridge of Reciprocity',
        moralDesc: 'Twin pillars rising toward a single aspiration, joined at the center by a bridge of trust. We lift each other as we climb.',
        waypoints: [
          { x: -160, y: 200 },
          { x: -80, y: -10 },
          { x: 0, y: -220 },
          { x: 80, y: -10 },
          { x: 160, y: 200 },
          { x: 95, y: 50 },
          { x: 0, y: 50 },
          { x: -95, y: 50 }
        ],
        paths: [
          { type: 'line', x1: -160, y1: 200, x2: 0, y2: -220 },
          { type: 'line', x1: 0, y1: -220, x2: 160, y2: 200 },
          { type: 'line', x1: -95, y1: 50, x2: 95, y2: 50 }
        ],
        targets: [
          { x: -160, y: 200, label: 'Left Foot', collected: false },
          { x: 0, y: -220, label: 'Apex Pinnacle', collected: false },
          { x: 160, y: 200, label: 'Right Foot', collected: false },
          { x: 0, y: 50, label: 'Crossbar Sanctuary', collected: false }
        ]
      },

      xin: {
        id: 'xin',
        char: '心',
        name: 'TCM Xin (Heart & Shen) • 心',
        moralTitle: 'Nourishing the Shen (Spirit)',
        moralDesc: 'In Chinese Medicine, the Heart (心) houses Shen—the spirit, consciousness, and emotional peace. Tracing the 4 points releases chest tension and stills restless racing thoughts.',
        waypoints: [
          { x: -130, y: -20 },
          { x: -110, y: 40 },
          { x: -100, y: -20 },
          { x: -70, y: 70 },
          { x: -30, y: 130 },
          { x: 0, y: 155 },
          { x: 50, y: 150 },
          { x: 90, y: 110 },
          { x: 120, y: 40 },
          { x: -15, y: -20 },
          { x: 100, y: -80 }
        ],
        paths: [
          // Left dot
          { type: 'bezier', p0: { x: -130, y: -40 }, p1: { x: -150, y: 0 }, p2: { x: -120, y: 40 }, p3: { x: -100, y: 50 } },
          // Bottom sweeping cradle hook (wo gou)
          { type: 'bezier', p0: { x: -100, y: -20 }, p1: { x: -80, y: 150 }, p2: { x: 70, y: 170 }, p3: { x: 130, y: 40 } },
          // Center inner dot
          { type: 'circle', cx: -15, cy: -20, r: 25 },
          // Right outer dot
          { type: 'circle', cx: 100, cy: -80, r: 25 }
        ],
        targets: [
          { x: -110, y: 40, label: 'Left Reservoir', collected: false },
          { x: 0, y: 155, label: 'Shen Cradle', collected: false },
          { x: -15, y: -20, label: 'Inner Flame', collected: false },
          { x: 100, y: -80, label: 'Upper Ascendant', collected: false }
        ]
      },

      om: {
        id: 'om',
        char: 'ॐ',
        name: 'Vedic Pranava OM • ॐ',
        moralTitle: 'Pranic Grounding & Ojas Preservation',
        moralDesc: 'The primordial sound of wholeness in Ayurvedic medicine. The three curves represent waking, dreaming, and deep stillness. Tracing the loop pacifies hyperactive Vata air and rebuilds Ojas.',
        waypoints: [
          { x: -40, y: -110 },
          { x: 10, y: -150 },
          { x: 45, y: -110 },
          { x: 0, y: -70 },
          { x: -20, y: 0 },
          { x: 50, y: 60 },
          { x: 80, y: 130 },
          { x: 0, y: 180 },
          { x: -80, y: 130 },
          { x: -20, y: 70 },
          { x: 70, y: 70 },
          { x: 150, y: 20 },
          { x: 170, y: -40 },
          { x: 130, y: -90 },
          { x: 30, y: -180 },
          { x: 100, y: -150 },
          { x: 170, y: -180 },
          { x: 100, y: -215 }
        ],
        paths: [
          // Upper loop
          { type: 'circle', cx: -40, cy: -110, r: 85 },
          // Lower expansive belly loop
          { type: 'circle', cx: -20, cy: 70, r: 110 },
          // Right sweeping tail curve
          { type: 'bezier', p0: { x: 70, y: 70 }, p1: { x: 160, y: 60 }, p2: { x: 180, y: -40 }, p3: { x: 130, y: -90 } },
          // Crescent chandra-bindu
          { type: 'bezier', p0: { x: 30, y: -180 }, p1: { x: 80, y: -150 }, p2: { x: 130, y: -150 }, p3: { x: 170, y: -180 } },
          { type: 'circle', cx: 100, cy: -215, r: 18 }
        ],
        targets: [
          { x: -40, y: -110, label: 'Jagrat (Conscious)', collected: false },
          { x: -20, y: 70, label: 'Sushupti (Deep Stillness)', collected: false },
          { x: 150, y: -20, label: 'Swapna (Vision)', collected: false },
          { x: 100, y: -215, label: 'Bindu (Pure Awareness)', collected: false }
        ]
      },

      an: {
        id: 'an',
        char: '安',
        name: 'Ān (Refuge & Safety) • 安',
        moralTitle: 'Sanctuary Under a Protective Roof',
        moralDesc: 'Formed by a protective sheltering roof over a calm centered figure. An ancient ideograph signifying that trauma cannot penetrate once the boundaries of personal sanctuary are sealed.',
        waypoints: [
          { x: 0, y: -220 },
          { x: 0, y: -165 },
          { x: -160, y: -140 },
          { x: 0, y: -140 },
          { x: 160, y: -140 },
          { x: 150, y: -90 },
          { x: -150, y: 120 },
          { x: 0, y: 120 },
          { x: 150, y: 120 },
          { x: 0, y: -80 },
          { x: -50, y: 30 },
          { x: 0, y: 150 },
          { x: 80, y: 220 }
        ],
        paths: [
          // Crown dot
          { type: 'line', x1: 0, y1: -220, x2: 0, y2: -165 },
          // Roof canopy left hook & crossbar
          { type: 'line', x1: -160, y1: -140, x2: 160, y2: -140 },
          { type: 'line', x1: -160, y1: -140, x2: -170, y2: -90 },
          { type: 'line', x1: 160, y1: -140, x2: 150, y2: -90 },
          // Lower figure sanctuary cross and sweep
          { type: 'line', x1: -150, y1: 120, x2: 150, y2: 120 },
          { type: 'bezier', p0: { x: 0, y: -100 }, p1: { x: -80, y: -20 }, p2: { x: 0, y: 190 }, p3: { x: 80, y: 220 } }
        ],
        targets: [
          { x: 0, y: -200, label: 'Crown Keystone', collected: false },
          { x: -160, y: -120, label: 'West Eaves', collected: false },
          { x: 160, y: -120, label: 'East Eaves', collected: false },
          { x: 0, y: 120, label: 'Inner Hearth', collected: false },
          { x: 80, y: 220, label: 'Root Ground', collected: false }
        ]
      },

      shanti: {
        id: 'shanti',
        char: 'शान्ति',
        name: 'Shanti (Universal Peace) • शान्ति',
        moralTitle: 'Threefold Transcendent Peace',
        moralDesc: 'In Vedic Sanskrit, Shanti invoked thrice protects against adhyatmika (inner emotional strife), adhibhautika (relational conflict), and adhidaivika (environmental and cosmic chaos).',
        paths: [
          // Upper Shirorekha headline
          { type: 'line', x1: -180, y1: -160, x2: 180, y2: -160 },
          // Sha loop
          { type: 'circle', cx: -100, cy: -80, r: 55 },
          { type: 'line', x1: -45, y1: -160, x2: -45, y2: 180 },
          // Vertical spine pillar
          { type: 'line', x1: 45, y1: -160, x2: 45, y2: 180 },
          // Right Matra loop
          { type: 'bezier', p0: { x: 45, y: -20 }, p1: { x: 110, y: -20 }, p2: { x: 130, y: 80 }, p3: { x: 130, y: 180 } }
        ],
        targets: [
          { x: -140, y: -160, label: 'Headline Haven', collected: false },
          { x: -100, y: -80, label: 'Sha Chakra', collected: false },
          { x: -45, y: 160, label: 'Inner Shanti', collected: false },
          { x: 45, y: 160, label: 'Relational Shanti', collected: false },
          { x: 130, y: 160, label: 'Cosmic Shanti', collected: false }
        ]
      },

      tumtum: {
        id: 'tumtum',
        char: '𛰃𛱑𛰙',
        name: 'Kloshe Tumtum • 𛰃𛱑𛰙 (Good Heart / Clan Spirit)',
        moralTitle: 'The Law of the Canoe Journey: Pulling in Unity',
        moralDesc: 'In the Pacific Northwest Canoe Journey, Tumtum represents the unified pulse of the heart, mind, and spirit. When the clan pulls in unison, waves that would capsize a solitary canoe are safely navigated with grace.',
        paths: [
          // Left heart chamber loop
          { type: 'circle', cx: -65, cy: -60, r: 85 },
          // Right heart chamber loop
          { type: 'circle', cx: 65, cy: -60, r: 85 },
          // Convergent bottom keel stem
          { type: 'line', x1: -140, y1: -10, x2: 0, y2: 210 },
          { type: 'line', x1: 140, y1: -10, x2: 0, y2: 210 },
          { type: 'line', x1: -80, y1: 70, x2: 80, y2: 70 }
        ],
        targets: [
          { x: -65, y: -60, label: 'Left Atrium / Compassion', collected: false },
          { x: 65, y: -60, label: 'Right Atrium / Courage', collected: false },
          { x: 0, y: 70, label: 'Keel Crossbar', collected: false },
          { x: 0, y: 210, label: 'Canoe Prow Ground', collected: false }
        ]
      },

      tilikum: {
        id: 'tilikum',
        char: '𛰃𛱆𛰆',
        name: 'Tilikum • 𛰃𛱆𛰆 (Sacred Clan Kinship)',
        moralTitle: 'The Interconnected Circle of Belonging',
        moralDesc: 'Healing is never an isolated achievement. Tilikum honors the relations—elders, children, caregivers, and ancestors—who surround the recovering person with an unbroken ring of unconditional care.',
        paths: [
          // Outer protective community ring
          { type: 'circle', cx: 0, cy: 0, r: 190 },
          // Inner hearth ring
          { type: 'circle', cx: 0, cy: 0, r: 90 },
          // 4 radial kinship bridges
          { type: 'line', x1: -190, y1: 0, x2: 190, y2: 0 },
          { type: 'line', x1: 0, y1: -190, x2: 0, y2: 190 }
        ],
        targets: [
          { x: 0, y: -190, label: 'Elder Wisdom', collected: false },
          { x: 190, y: 0, label: 'Healer Support', collected: false },
          { x: 0, y: 190, label: 'Earth Ground', collected: false },
          { x: -190, y: 0, label: 'Youth Vitality', collected: false },
          { x: 0, y: 0, label: 'Community Hearth', collected: false }
        ]
      },

      dharmachakra: {
        id: 'dharmachakra',
        char: '☸',
        name: 'Dharmachakra • ☸ (Eightfold Path Wheel)',
        moralTitle: 'The Wheel of Mindful Equilibrium',
        moralDesc: 'The 8 spokes represent right understanding, thought, speech, action, livelihood, effort, mindfulness, and concentration. Rolling along the wheel restores equanimity and clears sensory overload.',
        paths: [
          { type: 'circle', cx: 0, cy: 0, r: 185 },
          { type: 'circle', cx: 0, cy: 0, r: 60 },
          // 8 Spokes
          { type: 'line', x1: -185, y1: 0, x2: 185, y2: 0 },
          { type: 'line', x1: 0, y1: -185, x2: 0, y2: 185 },
          { type: 'line', x1: -130, y1: -130, x2: 130, y2: 130 },
          { type: 'line', x1: -130, y1: 130, x2: 130, y2: -130 }
        ],
        targets: [
          { x: 0, y: -185, label: 'Right Mindfulness', collected: false },
          { x: 130, y: -130, label: 'Right Resolve', collected: false },
          { x: 185, y: 0, label: 'Right Action', collected: false },
          { x: 130, y: 130, label: 'Right Livelihood', collected: false },
          { x: 0, y: 185, label: 'Right Samadhi', collected: false },
          { x: -130, y: 130, label: 'Right Effort', collected: false },
          { x: -185, y: 0, label: 'Right Speech', collected: false },
          { x: -130, y: -130, label: 'Right View', collected: false }
        ]
      },

      magendavid: {
        id: 'magendavid',
        char: '✡',
        name: 'Magen David • ✡ (Hexagram Equilibrium)',
        moralTitle: 'Bikur Cholim: The Sacred Act of Visiting the Sick',
        moralDesc: 'Two interlocking equilateral triangles representing the balance between transcendence and earthly grounding. In Jewish pastoral tradition, visiting the sick lifts one-sixtieth of their illness.',
        paths: [
          // Upward pointing triangle
          { type: 'poly', points: [{ x: 0, y: -210 }, { x: 180, y: 105 }, { x: -180, y: 105 }] },
          // Downward pointing triangle
          { type: 'poly', points: [{ x: 0, y: 210 }, { x: 180, y: -105 }, { x: -180, y: -105 }] }
        ],
        targets: [
          { x: 0, y: -210, label: 'Crown / Keter', collected: false },
          { x: 180, y: -105, label: 'Wisdom / Chokhmah', collected: false },
          { x: 180, y: 105, label: 'Lovingkindness / Chesed', collected: false },
          { x: 0, y: 210, label: 'Kingdom / Malkhut', collected: false },
          { x: -180, y: 105, label: 'Strength / Gevurah', collected: false },
          { x: -180, y: -105, label: 'Understanding / Binah', collected: false }
        ]
      },

      celticcross: {
        id: 'celticcross',
        char: '✝',
        name: 'Celtic Monastic Cross • ✝ (Solar Nimbus Halo)',
        moralTitle: 'The 9th-Century Scriptorium Sanctuary',
        moralDesc: 'The ancient Celtic cross unites the four cardinal earthly directions with the eternal solar nimbus halo. It offers stability, grounding, and quiet shelter during profound vulnerability.',
        paths: [
          // Vertical pillar
          { type: 'line', x1: 0, y1: -220, x2: 0, y2: 220 },
          // Horizontal crossbar
          { type: 'line', x1: -160, y1: -50, x2: 160, y2: -50 },
          // Solar nimbus ring
          { type: 'circle', cx: 0, cy: -50, r: 100 }
        ],
        targets: [
          { x: 0, y: -220, label: 'Heavenly Crown', collected: false },
          { x: -160, y: -50, label: 'Western Gate', collected: false },
          { x: 0, y: -50, label: 'Central Nimbus', collected: false },
          { x: 160, y: -50, label: 'Eastern Gate', collected: false },
          { x: 0, y: 220, label: 'Earthly Anchor', collected: false }
        ]
      },

      hilal: {
        id: 'hilal',
        char: '☪',
        name: 'Hilal & Morning Star • ☪ (Nocturnal Serenity)',
        moralTitle: 'Dhikr & Tranquility in the Night',
        moralDesc: 'The slender crescent cradling the radiant star symbolizes guidance through darkness. In palliative care, it reminds us that light returns after the longest night.',
        paths: [
          // Outer sweeping crescent
          { type: 'bezier', p0: { x: 30, y: -180 }, p1: { x: -180, y: -120 }, p2: { x: -180, y: 120 }, p3: { x: 30, y: 180 } },
          // Inner crescent return
          { type: 'bezier', p0: { x: 30, y: 180 }, p1: { x: -100, y: 90 }, p2: { x: -100, y: -90 }, p3: { x: 30, y: -180 } },
          // Morning star sanctuary
          { type: 'circle', cx: 90, cy: 0, r: 40 }
        ],
        targets: [
          { x: 30, y: -180, label: 'Upper Crescent Horn', collected: false },
          { x: -130, y: 0, label: 'Deep Night Belly', collected: false },
          { x: 30, y: 180, label: 'Lower Crescent Horn', collected: false },
          { x: 90, y: 0, label: 'Morning Star of Guidance', collected: false }
        ]
      },

      world: {
        id: 'world',
        char: '🪐',
        name: 'The World Card (Major Arcana XXI) • 🪐 (Cosmic Laurel Wreath)',
        moralTitle: 'The Universal Mandorla of Wholeness & Completion',
        moralDesc: 'In archetypal psychology and Tarot, Card XXI (The World) marks the transcendent union of all life stages: the four elemental guardians (Air, Water, Fire, Earth) anchor the cosmic mandala, while the central path unites heart, breath, and stillness.',
        paths: [
          // Outer Mandorla Laurel Wreath (Ellipse)
          { type: 'ellipse', cx: 0, cy: 0, rx: 140, ry: 190 },
          // Top Lemniscate (Infinity Ribbon ∞)
          { type: 'circle', cx: -35, cy: -190, r: 25 },
          { type: 'circle', cx: 35, cy: -190, r: 25 },
          // Bottom Lemniscate (Infinity Ribbon ∞)
          { type: 'circle', cx: -35, cy: 190, r: 25 },
          { type: 'circle', cx: 35, cy: 190, r: 25 },
          // Vertical Saccade Spine of Wholeness
          { type: 'line', x1: 0, y1: -190, x2: 0, y2: 190 },
          // Horizontal Midline Balance Bar
          { type: 'line', x1: -140, y1: 0, x2: 140, y2: 0 }
        ],
        targets: [
          { x: -160, y: -160, label: 'Angel of Air (Mind)', collected: false },
          { x: 160, y: -160,  label: 'Eagle of Water (Heart)', collected: false },
          { x: 160, y: 160,   label: 'Lion of Fire (Strength)', collected: false },
          { x: -160, y: 160,  label: 'Bull of Earth (Soma)', collected: false },
          { x: 0, y: 0,       label: 'The Dancing Center of Wholeness', collected: false }
        ]
      },

      braille: {
        id: 'braille',
        char: '⠿',
        name: 'ISO/TR 11548 8-Dot Braille Cell • ⠿',
        moralTitle: 'Tactile & Sighted Parity (Pillar III & VIII)',
        moralDesc: 'In PocketGull, every Braille cell is optotypically enlarged (r=78 UPM) and grounded to the baseline so sighted clinicians can visually verify embossed blister packs alongside English text. Tracing each dot sounds an acoustic pitch.',
        paths: [
          // Bounding frame guide
          { type: 'poly', points: [{ x: -90, y: -190 }, { x: 90, y: -190 }, { x: 90, y: 190 }, { x: -90, y: 190 }] },
          // Vertical columns
          { type: 'line', x1: -60, y1: -160, x2: -60, y2: 160 },
          { type: 'line', x1: 60, y1: -160, x2: 60, y2: 160 }
        ],
        targets: [
          // Left column: Dot 1, 2, 3, 7
          { x: -60, y: -150, label: 'Dot 1 (Top Left)', collected: false },
          { x: -60, y: -50,  label: 'Dot 2 (Mid Left)', collected: false },
          { x: -60, y: 50,   label: 'Dot 3 (Baseline Left)', collected: false },
          { x: -60, y: 150,  label: 'Dot 7 (Lower Left)', collected: false },
          // Right column: Dot 4, 5, 6, 8
          { x: 60, y: -150,  label: 'Dot 4 (Top Right)', collected: false },
          { x: 60, y: -50,   label: 'Dot 5 (Mid Right)', collected: false },
          { x: 60, y: 50,    label: 'Dot 6 (Baseline Right)', collected: false },
          { x: 60, y: 150,   label: 'Dot 8 (Lower Right)', collected: false }
        ]
      }
    };

    /**
     * Universal Waypoint Resolver
     * Resolves explicit waypoints or dynamically computes smooth, dense path points
     * from board targets or optotype geometry so Auto-Flow works seamlessly on any glyph.
     */
    function getBoardWaypoints(board) {
      if (!board) return [];
      if (board.waypoints && board.waypoints.length > 1) {
        return board.waypoints;
      }
      if (board.targets && board.targets.length > 0) {
        const dense = [];
        const tLen = board.targets.length;
        for (let i = 0; i < tLen; i++) {
          const p1 = board.targets[i];
          const p2 = board.targets[(i + 1) % tLen];
          for (let step = 0; step < 10; step++) {
            const frac = step / 10;
            dense.push({
              x: p1.x + (p2.x - p1.x) * frac,
              y: p1.y + (p2.y - p1.y) * frac
            });
          }
        }
        return dense;
      }
      return [
        { x: 0, y: -200 }, { x: 140, y: -70 }, { x: 90, y: 140 },
        { x: -90, y: 140 }, { x: -140, y: -70 }, { x: 0, y: -200 }
      ];
    }

    /**
     * True Optical Glyph Outline Vector Engine
     * Extracts exact closed outer and inner vector contours from the live font glyph
     * with subpixel fidelity, enabling Auto-Flow and interactive touch to hug the real letter outline.
     */
    const GLYPH_OUTLINE_CACHE = {};
    let currentBoardOutlinePoints = [];

    function extractGlyphOutlines(char) {
      if (!char) return { loops: [], primaryContour: [], correctionX: 0, correctionY: 0 };
      if (GLYPH_OUTLINE_CACHE[char]) {
        return GLYPH_OUTLINE_CACHE[char];
      }

      const sampleFontSize = 260;
      const size = 380;
      const off = document.createElement('canvas');
      off.width = size;
      off.height = size;
      const octx = off.getContext('2d', { willReadFrequently: true });

      octx.fillStyle = '#000000';
      octx.fillRect(0, 0, size, size);

      octx.font = `800 ${sampleFontSize}px "PocketGull", "Noto Sans", sans-serif`;
      octx.textAlign = 'center';
      octx.textBaseline = 'alphabetic';

      const m = octx.measureText(char);
      const glyphOffsetX = (m.actualBoundingBoxLeft - m.actualBoundingBoxRight) / 2;
      const glyphOffsetY = (m.actualBoundingBoxAscent - m.actualBoundingBoxDescent) / 2;

      // Pass 1: Render character with Canvas2D metrics to measure actual raster ink centroid
      octx.fillStyle = '#ffffff';
      octx.fillText(char, size / 2 + glyphOffsetX, size / 2 + glyphOffsetY);

      const img1 = octx.getImageData(0, 0, size, size);
      const d1 = img1.data;

      let inkMinX = size, inkMaxX = 0, inkMinY = size, inkMaxY = 0;
      let hasInk = false;
      for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
          if (d1[(y * size + x) * 4] > 60) {
            if (x < inkMinX) inkMinX = x;
            if (x > inkMaxX) inkMaxX = x;
            if (y < inkMinY) inkMinY = y;
            if (y > inkMaxY) inkMaxY = y;
            hasInk = true;
          }
        }
      }

      let correctionX = 0;
      let correctionY = 0;
      if (hasInk) {
        const inkCenterX = (inkMinX + inkMaxX) / 2;
        const inkCenterY = (inkMinY + inkMaxY) / 2;
        correctionX = (inkCenterX - size / 2) / sampleFontSize;
        correctionY = (inkCenterY - size / 2) / sampleFontSize;
      }

      // Pass 2: Re-render with subpixel correction so ink centroid is 100.000% locked to size/2
      octx.fillStyle = '#000000';
      octx.fillRect(0, 0, size, size);
      octx.fillStyle = '#ffffff';
      octx.fillText(char, size / 2 + glyphOffsetX - correctionX * sampleFontSize, size / 2 + glyphOffsetY - correctionY * sampleFontSize);

      const img2 = octx.getImageData(0, 0, size, size);
      const data = img2.data;

      function isSolid(x, y) {
        if (x < 0 || x >= size || y < 0 || y >= size) return false;
        return data[(y * size + x) * 4] > 80;
      }

      const rawBoundary = [];
      for (let y = 1; y < size - 1; y++) {
        for (let x = 1; x < size - 1; x++) {
          if (isSolid(x, y)) {
            if (!isSolid(x + 1, y) || !isSolid(x - 1, y) || !isSolid(x, y + 1) || !isSolid(x, y - 1)) {
              rawBoundary.push({
                x: (x - size / 2) / sampleFontSize,
                y: (y - size / 2) / sampleFontSize
              });
            }
          }
        }
      }

      // Chain adjacent boundary pixels into continuous loops
      const unvisited = new Set(rawBoundary.map((_, i) => i));
      const loops = [];
      const maxNeighborDist = 3.8 / sampleFontSize;

      while (unvisited.size > 0) {
        const startIdx = unvisited.values().next().value;
        unvisited.delete(startIdx);
        const loop = [rawBoundary[startIdx]];
        let curr = rawBoundary[startIdx];
        let maxSteps = 3000;

        while (maxSteps-- > 0) {
          let nearestIdx = -1;
          let nearestDist = Infinity;
          for (const idx of unvisited) {
            const p = rawBoundary[idx];
            const d = Math.hypot(p.x - curr.x, p.y - curr.y);
            if (d < nearestDist && d <= maxNeighborDist) {
              nearestDist = d;
              nearestIdx = idx;
            }
          }
          if (nearestIdx !== -1) {
            unvisited.delete(nearestIdx);
            curr = rawBoundary[nearestIdx];
            loop.push(curr);
          } else {
            break;
          }
        }

        if (loop.length > 20) {
          loops.push(loop);
        }
      }

      // 5-Point Gaussian smoothing kernel (0.1, 0.2, 0.4, 0.2, 0.1) for silky-smooth contours
      function smoothLoop(lp) {
        if (!lp || lp.length < 5) return lp || [];
        const n = lp.length;
        const res = [];
        for (let i = 0; i < n; i++) {
          const pM2 = lp[(i - 2 + n) % n];
          const pM1 = lp[(i - 1 + n) % n];
          const p0  = lp[i];
          const pP1 = lp[(i + 1) % n];
          const pP2 = lp[(i + 2) % n];
          res.push({
            x: 0.10 * pM2.x + 0.20 * pM1.x + 0.40 * p0.x + 0.20 * pP1.x + 0.10 * pP2.x,
            y: 0.10 * pM2.y + 0.20 * pM1.y + 0.40 * p0.y + 0.20 * pP1.y + 0.10 * pP2.y
          });
        }
        return res;
      }

      // Sort loops descending: largest outer contour first
      loops.sort((a, b) => b.length - a.length);
      const smoothedLoops = loops.map(smoothLoop);

      // Construct seamless closed-contour primary path (pure outer perimeter loop)
      const primaryContour = smoothedLoops.length > 0 ? smoothedLoops[0] : [];

      const result = {
        loops: smoothedLoops,
        primaryContour: primaryContour.length > 0 ? primaryContour : (smoothedLoops[0] || []),
        correctionX,
        correctionY
      };

      GLYPH_OUTLINE_CACHE[char] = result;
      return result;
    }

    /* ========================================================================== */
    /* INTERACTIVE CANVAS RENDER LOOP & TOKEN PHYSICS                             */
    /* ========================================================================== */
    const canvas = document.getElementById('boardCanvas');
    const ctx = canvas.getContext('2d');
    const stageWrap = document.getElementById('stageWrap');
    const boardTitleBanner = document.getElementById('boardTitleBanner');
    const boardMoralTitle = document.getElementById('boardMoralTitle');
    const boardMoralDesc = document.getElementById('boardMoralDesc');
    const healingToast = document.getElementById('healingToast');
    const timerDisplay = document.getElementById('timerDisplay');

    let currentBoardKey = 'zero';
    let isZenMode = true;

    let currentGbLens = 'blend'; // 'blend', 'art', 'science'

    const GB_LENS_MORALS = {
      zero: {
        blend: {
          title: "The Wisdom of Unambiguous Care",
          desc: "In healthcare as in life, clear boundaries bring safety. The slashed zero unequivocally separates the zero from the circle of confusion, ensuring remedies heal and never harm."
        },
        art: {
          title: "The Circle with a Golden Diagonal Bridge",
          desc: "Roll the glowing pearl around the bright moon circle! Cross the friendly golden bridge in the middle to give both sides a happy hello."
        },
        science: {
          title: "ISMP Character Disambiguation (cv08 / Sloan 5:1)",
          desc: "Eliminates fatal 500 mg vs 50 Omg dosing confusions via an optical 45-degree stroke. Stroke junctions are thinned to prevent ink clotting at low visual acuity."
        }
      },
      eight: {
        blend: {
          title: "The Infinite Dance of Balance",
          desc: "The figure eight embodies eternal reciprocity. Moving through its crossing point teaches the mind to transition smoothly between opposing states without collision."
        },
        art: {
          title: "The Magic Rollercoaster of Light",
          desc: "Glide up and around the top loop, swoosh through the center cross, and loop smoothly around the bottom! You can keep rolling forever."
        },
        science: {
          title: "Lemniscate Oculomotor Midline Coordination",
          desc: "Continuous bi-directional curvature stimulates binocular smooth-pursuit tracking, synchronizing left and right cortical hemispheres across the corpus callosum."
        }
      },
      world: {
        blend: {
          title: "Cosmic Integration & Wholeness (Tarot XXI)",
          desc: "The laurel mandorla anchors the four elemental quadrants. Journeying through the four guardians unifies breath, intuition, vital courage, and somatic grounding."
        },
        art: {
          title: "The Four Friendly Animal Guardians & The Gold Ring",
          desc: "Say hello to the gentle Angel of the sky, the soaring Eagle of water, the brave Lion of fire, and the steady Bull of earth! Together they make a singing circle of stars."
        },
        science: {
          title: "Tetramorph Orthogonal Equilibrium (432–660 Hz)",
          desc: "Spatial quadrant distribution mirrors Louise Sloan 5:1 optotype symmetry. Multi-frequency acoustic stimulation harmonizes autonomic vagal tone across sensory channels."
        }
      }
    };

    function applyGbLens() {
      const moral = GB_LENS_MORALS[currentBoardKey];
      const titleEl = document.getElementById('moralTitle');
      const descEl = document.getElementById('moralDesc');
      if (moral && moral[currentGbLens]) {
        if (titleEl) titleEl.textContent = moral[currentGbLens].title;
        if (descEl) descEl.textContent = moral[currentGbLens].desc;
      }
    }

    let width = 600;
    let height = 600;
    let currentLetterScale = 1.0;

    // The Light Pearl (Player Token)
    const token = {
      x: 0,
      y: -220,
      targetX: 0,
      targetY: -220,
      vx: 0,
      vy: 0,
      radius: 16,
      trail: [],
      glowColor: '#14b8a6',
      activeChimeIndex: 0
    };

    // ─── 03-02-1987 NATAL HARMONICS & ACOUSTIC KINETIC HARP ───
    // Rooted in the 3:2 Golden Diapente (432 Hz : 648 Hz), sub-harmonic 216 Hz, and 864 Hz octave shimmer
    const NATAL_HARP_SCALE = [216, 288, 324, 432, 486, 576, 648, 768, 864];

    function getHarpPitchForY(y, emHalf) {
      const half = emHalf || 220;
      // y ranges from -half (top / high pitch 864 Hz) to +half (bottom / low pitch 216 Hz)
      const norm = Math.max(0, Math.min(1, (half - y) / (2 * half)));
      const idx = Math.min(NATAL_HARP_SCALE.length - 1, Math.floor(norm * NATAL_HARP_SCALE.length));
      return NATAL_HARP_SCALE[idx];
    }

    let lastHarpPluckTime = 0;
    let accumulatedHarpDistance = 0;
    let lastPearlX = 0;
    let lastPearlY = -220;
    let hasHitApex = false;
    let hasHitGround = false;
    let contourMinY = -220;
    let contourMaxY = 220;
    let lastRenderedBoardKey = null;

    let isDragging = false;
    let isKeyboardActive = false;
    // ─── SOMATIC PARADOXICAL PACER & POMODORO SANCTUARY ENGINE ───
    let pacerMode = 'timeless'; // 'timeless' | 'pomodoro' | 'numeric'
    let secondsCalm = 0;
    let pomodoroSeconds = 0;
    const POMODORO_FOCUS_DURATION = 20 * 60; // 20 minutes
    const POMODORO_REST_DURATION = 3 * 60;   // 3 minutes
    let isPomodoroRestPhase = false;

    // ─── PARADOXICAL FIREWEED BLOOM ENGINE (THE CLOCK THAT DISSOLVES TIME) ───
    let fireweedBloomSeconds = 0;
    const FIREWEED_FULL_BLOOM_SECONDS = 300; // 5 minutes = 30 vagal breath waves
    let hasSignaledFullBloom = false;

    const btnPacerTimeless = document.getElementById('btnPacerTimeless');
    const btnPacerPomodoro = document.getElementById('btnPacerPomodoro');
    const btnPacerNumeric = document.getElementById('btnPacerNumeric');
    const pacerBloomContainer = document.getElementById('pacerBloomContainer');
    const pacerNumericContainer = document.getElementById('pacerNumericContainer');
    const pacerStateTitle = document.getElementById('pacerStateTitle');
    const pacerCycleText = document.getElementById('pacerCycleText');
    const pacerStatusBadge = document.getElementById('pacerStatusBadge');
    const paradoxBloomSvg = document.getElementById('paradoxBloomSvg');
    const bloomPetalsGroup = document.getElementById('bloomPetalsGroup');

    function setPacerMode(mode) {
      pacerMode = mode;
      if (btnPacerTimeless) {
        btnPacerTimeless.classList.toggle('active', mode === 'timeless');
        btnPacerTimeless.style.borderColor = mode === 'timeless' ? 'rgba(45, 212, 191, 0.4)' : 'rgba(255, 255, 255, 0.15)';
        btnPacerTimeless.style.background = mode === 'timeless' ? 'rgba(45, 212, 191, 0.15)' : 'transparent';
        btnPacerTimeless.style.color = mode === 'timeless' ? '#2dd4bf' : '#94a3b8';
      }
      if (btnPacerPomodoro) {
        btnPacerPomodoro.classList.toggle('active', mode === 'pomodoro');
        btnPacerPomodoro.style.borderColor = mode === 'pomodoro' ? 'rgba(251, 113, 133, 0.4)' : 'rgba(255, 255, 255, 0.15)';
        btnPacerPomodoro.style.background = mode === 'pomodoro' ? 'rgba(251, 113, 133, 0.15)' : 'transparent';
        btnPacerPomodoro.style.color = mode === 'pomodoro' ? '#fb7185' : '#94a3b8';
      }
      if (btnPacerNumeric) {
        btnPacerNumeric.classList.toggle('active', mode === 'numeric');
        btnPacerNumeric.style.borderColor = mode === 'numeric' ? 'rgba(245, 158, 11, 0.4)' : 'rgba(255, 255, 255, 0.15)';
        btnPacerNumeric.style.background = mode === 'numeric' ? 'rgba(245, 158, 11, 0.15)' : 'transparent';
        btnPacerNumeric.style.color = mode === 'numeric' ? 'var(--accent-amber)' : '#94a3b8';
      }

      if (pacerBloomContainer && pacerNumericContainer) {
        if (mode === 'numeric') {
          pacerBloomContainer.style.display = 'none';
          pacerNumericContainer.style.display = 'block';
        } else {
          pacerBloomContainer.style.display = 'flex';
          pacerNumericContainer.style.display = 'none';
        }
      }
      if (mode === 'pomodoro') {
        pomodoroSeconds = 0;
        isPomodoroRestPhase = false;
        if (pacerStateTitle) pacerStateTitle.textContent = '20m Mindful Focus';
        if (pacerCycleText) pacerCycleText.textContent = '0% • Rest in 20m';
        showToast('🍅 Somatic Pomodoro: 20m Focus Session engaged');
      } else if (mode === 'timeless') {
        if (pacerStateTitle) pacerStateTitle.textContent = 'Timeless Flow';
        showToast('🌸 Timeless Flow: Breath-paced sanctuary with zero ticking digits');
      } else {
        showToast('⏱️ Clinical Telemetry Mode Active');
      }
    }

    if (btnPacerTimeless) btnPacerTimeless.addEventListener('click', () => setPacerMode('timeless'));
    if (btnPacerPomodoro) btnPacerPomodoro.addEventListener('click', () => setPacerMode('pomodoro'));
    if (btnPacerNumeric) btnPacerNumeric.addEventListener('click', () => setPacerMode('numeric'));

    setInterval(() => {
      secondsCalm++;
      if (timerDisplay) {
        const mins = String(Math.floor(secondsCalm / 60)).padStart(2, '0');
        const secs = String(secondsCalm % 60).padStart(2, '0');
        timerDisplay.textContent = `${mins}:${secs}`;
      }

      const breathWaveCount = Math.floor(secondsCalm / 10) + 1;
      if (pacerMode === 'timeless' && pacerCycleText) {
        pacerCycleText.textContent = `Cycle ${breathWaveCount} • Vagal Breath Wave`;
      } else if (pacerMode === 'pomodoro') {
        pomodoroSeconds++;
        if (!isPomodoroRestPhase) {
          const remaining = Math.max(0, POMODORO_FOCUS_DURATION - pomodoroSeconds);
          const remMin = Math.floor(remaining / 60);
          const remSec = remaining % 60;
          const progPercent = ((pomodoroSeconds / POMODORO_FOCUS_DURATION) * 100).toFixed(0);
          if (pacerStateTitle) pacerStateTitle.textContent = '20m Mindful Focus';
          if (pacerCycleText) pacerCycleText.textContent = `${progPercent}% • ${remMin}m ${remSec}s left`;
          if (pomodoroSeconds >= POMODORO_FOCUS_DURATION) {
            isPomodoroRestPhase = true;
            pomodoroSeconds = 0;
            sound.playLandmarkChime('circuit');
            triggerHaptic('complete');
            if (pacerStateTitle) pacerStateTitle.textContent = '🌸 3m Letterform Reset';
            if (pacerCycleText) pacerCycleText.textContent = 'Rest eyes • Glide along letterform';
            showToast('🌸 20m Focus Complete! Enjoy 3 minutes of gentle letterform rest');
            if (!isAutoFlow && typeof btnToggleAutoFlow !== 'undefined' && btnToggleAutoFlow) {
              btnToggleAutoFlow.click();
            }
          }
        } else {
          const remaining = Math.max(0, POMODORO_REST_DURATION - pomodoroSeconds);
          const remMin = Math.floor(remaining / 60);
          const remSec = remaining % 60;
          if (pacerCycleText) pacerCycleText.textContent = `Resting: ${remMin}m ${remSec}s left`;
          if (pomodoroSeconds >= POMODORO_REST_DURATION) {
            isPomodoroRestPhase = false;
            pomodoroSeconds = 0;
            sound.playTibetanBowl(432);
            triggerHaptic('pulse');
            if (pacerStateTitle) pacerStateTitle.textContent = '20m Mindful Focus';
            showToast('✨ Rest Complete • Ready for Next Focus Session');
          }
        }
      }

      // ─── Paradoxical Fireweed Blossom (5-Minute Full Bloom Resolution) ───
      fireweedBloomSeconds++;
      if (fireweedBloomSeconds >= FIREWEED_FULL_BLOOM_SECONDS) {
        if (!hasSignaledFullBloom) {
          hasSignaledFullBloom = true;
          sound.playTibetanBowl(216); // Deep meditative 216 Hz Singing Bowl Chord
          triggerHaptic('ground');    // Grounding haptic detent [28, 40, 20]
          showToast('🌸 Fireweed in Full Bloom • The Nervous System Has Settled');
          announceSR('Fireweed blossom in full bloom. Five minutes of restorative stillness completed.');
        }
        if (fireweedBloomSeconds >= FIREWEED_FULL_BLOOM_SECONDS + 8) {
          fireweedBloomSeconds = 0;
          hasSignaledFullBloom = false;
        }
      }
    }, 1000);

    // ─── Responsive Mobile View Tab Switcher ───
    const gameWorkspace = document.getElementById('gameWorkspace');
    const mobileTabButtons = document.querySelectorAll('.mobile-tab-btn');

    function setActiveView(view) {
      if (!gameWorkspace) return;
      gameWorkspace.setAttribute('data-active-view', view);
      mobileTabButtons.forEach(btn => {
        const isActive = btn.dataset.view === view;
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });
      if (view === 'stage') {
        // Allow layout to complete before calibrating canvas coordinates
        requestAnimationFrame(() => {
          resizeCanvas();
        });
        setTimeout(resizeCanvas, 60);
      }
    }

    mobileTabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        setActiveView(btn.dataset.view);
      });
    });

    function resizeCanvas() {
      if (!stageWrap || !canvas) return;
      const rect = stageWrap.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        width = canvas.width = Math.floor(rect.width);
        height = canvas.height = Math.floor(rect.height);
      }
    }
    window.addEventListener('resize', resizeCanvas);
    window.addEventListener('orientationchange', () => {
      setTimeout(resizeCanvas, 100);
    });
    resizeCanvas();

    // Prevent passive touch scrolling when dragging the light pearl
    if (canvas) {
      canvas.addEventListener('touchmove', (e) => {
        if (isDragging) {
          e.preventDefault();
        }
      }, { passive: false });
    }

    function setBoard(boardKey) {
      currentBoardKey = boardKey;
      const board = BOARDS[boardKey];
      if (!board) return;

      // Update HUD
      boardTitleBanner.innerHTML = `📜 Active Board: <strong>${board.name}</strong>`;
      boardMoralTitle.textContent = board.moralTitle;
      boardMoralDesc.textContent = board.moralDesc;
      announceSR(`Board changed to ${board.name}. ${board.moralTitle}. Use arrow keys to explore, B for acoustic beacon, S to toggle sonar.`);

      // Reset targets
      board.targets.forEach(t => t.collected = false);

      // Reset Token to first waypoint or target scaled to actual letterform
      const s = currentLetterScale || 0.6;
      const waypoints = getBoardWaypoints(board);
      if (waypoints && waypoints.length > 0) {
        token.x = token.targetX = waypoints[0].x * s;
        token.y = token.targetY = waypoints[0].y * s;
      } else if (board.targets && board.targets.length > 0) {
        token.x = token.targetX = board.targets[0].x * s;
        token.y = token.targetY = board.targets[0].y * s;
      }
      token.trail = [];
      autoFlowAngle = 0;
      accumulatedHarpDistance = 0;
      lastPearlX = token.x;
      lastPearlY = token.y;
      hasHitApex = false;
      hasHitGround = false;

      // Trigger Harmonic Chime
      if (isZenMode) {
        sound.playTibetanBowl(432);
      } else {
        sound.playChime(1.0);
      }
      showToast(`✨ Welcome to ${board.name} • Breathe Deeply`);

      // Update Zen Quick Board Chips
      document.querySelectorAll('.zen-glyph-chip').forEach(chip => {
        chip.classList.toggle('active', chip.dataset.board === boardKey);
      });

      // Smoothly close floating boards drawer on desktop
      const pBoards = document.getElementById('panelBoards');
      const tBoards = document.getElementById('btnToggleBoards');
      if (pBoards) pBoards.classList.remove('drawer-open');
      if (tBoards) tBoards.classList.remove('active');

      // On mobile viewports, smoothly transition back to the interactive stage
      if (window.innerWidth < 1024) {
        setActiveView('stage');
      }
    }

    function showToast(msg) {
      healingToast.textContent = msg;
      healingToast.classList.add('show');
      clearTimeout(healingToast._timer);
      healingToast._timer = setTimeout(() => {
        healingToast.classList.remove('show');
      }, 2200);
    }


    /* ========================================================================== */
    /* PHILOCARDIA, TOUCH AURA & S1/S2 AUSCULTATION ENGINE                        */
    /* ========================================================================== */
    let currentPhilocardiaMode = '72'; // '72', '60', 'breath', 'aura', 'static', 'off'
    let isTouchAuraActive = false;
    let isAuscultationActive = false;
    let isGlareSoftenerActive = false;
    let pointerCanvasX = 0;
    let pointerCanvasY = 0;
    let pointerRadius = 0;
    let heartParticles = [];
    let palpationSeconds = 0;
    let lastPalpationTime = performance.now();
    let eyeRestTimer = null;
    let eyeRestSeconds = 1200; // 20 minutes

    // S1/S2 Acoustic Heartbeat Synthesizer
    function playAuscultationBeat() {
      if (!isAuscultationActive || !sound.ctx || !sound.enabled) return;
      try {
        const now = sound.ctx.currentTime;
        // S1 "Lub" (lower pitch ~70 Hz, longer)
        const osc1 = sound.ctx.createOscillator();
        const gain1 = sound.ctx.createGain();
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(70, now);
        osc1.frequency.exponentialRampToValueAtTime(45, now + 0.08);
        gain1.gain.setValueAtTime(0.35, now);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
        osc1.connect(gain1);
        gain1.connect(sound.masterGain);
        osc1.start(now);
        osc1.stop(now + 0.1);

        // S2 "Dub" (slightly higher pitch ~95 Hz, crisp, 140ms later)
        const osc2 = sound.ctx.createOscillator();
        const gain2 = sound.ctx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(95, now + 0.14);
        osc2.frequency.exponentialRampToValueAtTime(55, now + 0.21);
        gain2.gain.setValueAtTime(0.28, now + 0.14);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
        osc2.connect(gain2);
        gain2.connect(sound.masterGain);
        osc2.start(now + 0.14);
        osc2.stop(now + 0.23);
      } catch (e) {}
    }

    // Heartbeat Interval Loop
    let heartbeatTimer = null;
    function scheduleHeartbeat() {
      if (heartbeatTimer) clearInterval(heartbeatTimer);
      let intervalMs = 833; // default 72 BPM
      if (currentPhilocardiaMode === '60') intervalMs = 1000;
      else if (currentPhilocardiaMode === 'breath') intervalMs = 2000;
      else if (currentPhilocardiaMode === 'aura') intervalMs = 1100;

      heartbeatTimer = setInterval(() => {
        if (currentPhilocardiaMode !== 'off') {
          playAuscultationBeat();
          // Micro pulse on palpation icon
          const icon = document.getElementById('palpationHeartIcon');
          if (icon) {
            icon.style.transform = 'scale(1.35)';
            setTimeout(() => { icon.style.transform = 'scale(1)'; }, 140);
          }
        }
      }, intervalMs);
    }
    scheduleHeartbeat();

    // Mode Selector Controls
    const philoChips = document.querySelectorAll('.philocardia-chip[data-mode]');
    philoChips.forEach(chip => {
      chip.addEventListener('click', () => {
        sound.init();
        philoChips.forEach(c => c.classList.remove('active', 'aura-active'));
        const mode = chip.dataset.mode;
        currentPhilocardiaMode = mode;
        chip.classList.add(mode === 'aura' ? 'aura-active' : 'active');
        isTouchAuraActive = (mode === 'aura');

        // Update Pacer Label
        const pacerLabel = document.getElementById('pacerLabel');
        if (pacerLabel) {
          if (mode === '72') pacerLabel.textContent = '♥ 72 BPM Normocardia • Radial Palpation Active (4s In / 6s Out)';
          else if (mode === '60') pacerLabel.textContent = '♥ 60 BPM Deep Rest • Parasympathetic Down-Regulation (5s In / 5s Out)';
          else if (mode === 'breath') pacerLabel.textContent = '🫁 4-7-8 Somatic Breath • Inhale 4s … Hold 7s … Exhale 8s';
          else if (mode === 'aura') pacerLabel.textContent = '✨ Touch Aura Active • Glyphs and Pearls Bloom Toward Cursor';
          else if (mode === 'static') pacerLabel.textContent = '♡ Static Hearts Sanctuary • Pure Calm Focus';
          else pacerLabel.textContent = '⚪ Standard Practice Mode • Clean Letterform Geometry';
        }

        showToast(`♥ Philocardia Mode: ${chip.textContent.trim()}`);
        scheduleHeartbeat();
      });
    });

    // Auscultation Sound Toggle
    const chipAuscultation = document.getElementById('chipAuscultation');
    const labelAuscultation = document.getElementById('labelAuscultation');
    if (chipAuscultation) {
      chipAuscultation.addEventListener('click', () => {
        sound.init();
        isAuscultationActive = !isAuscultationActive;
        chipAuscultation.classList.toggle('active', isAuscultationActive);
        labelAuscultation.textContent = isAuscultationActive ? 'Sound ON' : 'Sound OFF';
        if (isAuscultationActive) playAuscultationBeat();
        showToast(isAuscultationActive ? '🎧 S1/S2 Auscultation Acoustic Tone ON' : '🎧 Stethoscope Tone Muted');
      });
    }

    // 20-20-20 Ocular Rest Sanctuary
    const chipEyeRest = document.getElementById('chipEyeRest');
    const labelEyeRest = document.getElementById('labelEyeRest');
    if (chipEyeRest) {
      setInterval(() => {
        eyeRestSeconds--;
        if (eyeRestSeconds <= 0) {
          eyeRestSeconds = 1200;
          showToast('👁️ 20-20-20 Sanctuary: Look at an object 20 feet away for 20 seconds to relax eye muscles!');
        }
        const m = Math.floor(eyeRestSeconds / 60);
        const s = eyeRestSeconds % 60;
        if (labelEyeRest) labelEyeRest.textContent = `${m}:${s < 10 ? '0' : ''}${s}`;
      }, 1000);
      chipEyeRest.addEventListener('click', () => {
        showToast('👁️ 20-20-20 Sanctuary Active: Take 20 seconds to look out a window or gaze 20 ft away.');
      });
    }

    // Glare Softener Toggle
    const chipGlare = document.getElementById('chipGlare');
    const glareOverlay = document.getElementById('glareSoftenerOverlay');
    if (chipGlare && glareOverlay) {
      chipGlare.addEventListener('click', () => {
        isGlareSoftenerActive = !isGlareSoftenerActive;
        chipGlare.classList.toggle('active', isGlareSoftenerActive);
        glareOverlay.classList.toggle('active', isGlareSoftenerActive);
        showToast(isGlareSoftenerActive ? '🌙 Glare Softener Active • Warm Amber Micro-Luminance' : '🌙 Glare Softener Off');
      });
    }

    // Palpation Chronometer Click (Haptic Feedback)
    const palpationWidget = document.getElementById('palpationHudWidget');
    if (palpationWidget) {
      palpationWidget.addEventListener('click', () => {
        sound.init();
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
          navigator.vibrate([25, 85, 35]); // S1 + S2
        }
        playAuscultationBeat();
        showToast('♥ 15-Second Radial Pulse Check • Count pulses during 1 sweep, multiply by 4');
      });
    }




    /* ========================================================================== */
    /* STROKE RECOVERY & NEURO-REHABILITATION ENGINE                              */
    /* ========================================================================== */
    let currentRehabMode = 'tremor'; // 'tremor', 'mirror', 'midline', 'aphasia'
    let rawPointerHistory = [];
    let smoothedPointerX = 0;
    let smoothedPointerY = 0;
    let midlineCrossingsCount = 0;
    let lastTokenSignX = 0;

    const REHAB_PRESETS = {
      tremor: {
        badge: 'STAGE II / TREMOR SHIELD',
        desc: 'Adaptive tremor dampening (low-pass spatial EMA filter) absorbs 4-8 Hz involuntary oscillations, letting you draw smooth, elegant curves.',
        smoothingAlpha: 0.12, // High dampening
        auraRadius: 220
      },
      mirror: {
        badge: 'STAGE I / MIRROR NEURON',
        desc: 'Passive motor observation primes damaged premotor networks. The light-pearl traces the glyph hands-free at 60 BPM rest tempo.',
        smoothingAlpha: 0.25,
        auraRadius: 180
      },
      midline: {
        badge: 'STAGE III / MIDLINE CROSS',
        desc: 'Forces interhemispheric transfer across the corpus callosum. Continuous Figure-8 looping trains coordinated bilateral motor control.',
        smoothingAlpha: 0.18,
        auraRadius: 200
      },
      aphasia: {
        badge: 'APEX / APHASIA KINESTHETIC',
        desc: 'Scaffolds phonetic speech recall through tactile motor tracing. Tracing glyph anatomy triggers auditory phonetic resonance.',
        smoothingAlpha: 0.20,
        auraRadius: 190
      }
    };

    function setRehabMode(mode) {
      currentRehabMode = mode;
      const cfg = REHAB_PRESETS[mode] || REHAB_PRESETS.tremor;
      
      const badgeEl = document.getElementById('rehabBadge');
      const descEl = document.getElementById('rehabDesc');
      if (badgeEl) badgeEl.textContent = cfg.badge;
      if (descEl) descEl.textContent = cfg.desc;

      document.querySelectorAll('.rehab-pill').forEach(pill => {
        pill.classList.toggle('active', pill.dataset.rehab === mode);
      });

      if (mode === 'mirror') {
        // Activate continuous auto-flow
        if (!isAutoFlow && typeof btnToggleAutoFlow !== 'undefined' && btnToggleAutoFlow) {
          btnToggleAutoFlow.click();
        }
        showToast('🪞 Mirror Neuron Priming Active • Watch, Breathe & Absorb');
      } else if (mode === 'midline') {
        // Automatically switch to Figure Eight board for maximum midline crossing
        setBoard('eight');
        document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'eight'));
        showToast('♾️ Midline Cross Active • Figure Eight Board Initialized');
      } else if (mode === 'aphasia') {
        showToast('🗣️ Aphasia Kinesthetic Scribe • Motor Movement Unlocks Speech');
      } else {
        showToast('🛡️ Tremor Dampening Active • 4-8 Hz Involuntary Tremor Shielded');
      }
    }

    document.querySelectorAll('.rehab-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        sound.init();
        setRehabMode(pill.dataset.rehab);
      });
    });

    // Enhanced Responsive Pointer Handler
    function handleRehabPointer(clientX, clientY, isDown = false) {
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const rawX = clientX - rect.left - width / 2;
      const rawY = clientY - rect.top - height / 2;

      // If pointer just jumped into canvas, snap immediately to eliminate lag
      if (Math.hypot(smoothedPointerX - rawX, smoothedPointerY - rawY) > 280) {
        smoothedPointerX = rawX;
        smoothedPointerY = rawY;
      }

      // Responsive Exponential Moving Average:
      // High responsiveness (0.75) for effortless following, lower (0.22) only if Stage II Tremor Shield explicitly engaged
      const alpha = (currentRehabMode === 'tremor' && !isZenMode) ? 0.22 : 0.75;
      smoothedPointerX = (alpha * rawX) + ((1 - alpha) * smoothedPointerX);
      smoothedPointerY = (alpha * rawY) + ((1 - alpha) * smoothedPointerY);

      // Magnetic Soft-Spring Snap to nearest glyph path
      const board = BOARDS[currentBoardKey];
      let nearestDist = Infinity;
      let snapX = smoothedPointerX;
      let snapY = smoothedPointerY;

      // Magnetic Soft-Spring Snap directly to TRUE GLYPH OUTLINE CONTOUR!
      if (currentBoardOutlinePoints && currentBoardOutlinePoints.length > 0) {
        for (let i = 0; i < currentBoardOutlinePoints.length; i += 2) {
          const pt = currentBoardOutlinePoints[i];
          const d = Math.hypot(smoothedPointerX - pt.x, smoothedPointerY - pt.y);
          if (d < nearestDist && d < 65) {
            nearestDist = d;
            const pull = 0.50 * (1 - d / 65);
            snapX = smoothedPointerX + (pt.x - smoothedPointerX) * pull;
            snapY = smoothedPointerY + (pt.y - smoothedPointerY) * pull;
          }
        }
      } else if (board && board.targets) {
        board.targets.forEach(t => {
          const tx = t.x * currentLetterScale;
          const ty = t.y * currentLetterScale;
          const d = Math.hypot(smoothedPointerX - tx, smoothedPointerY - ty);
          if (d < nearestDist && d < 70) {
            nearestDist = d;
            const pull = 0.25 * (1 - d / 70);
            snapX = smoothedPointerX + (tx - smoothedPointerX) * pull;
            snapY = smoothedPointerY + (ty - smoothedPointerY) * pull;
          }
        });
      }

      token.targetX = snapX;
      token.targetY = snapY;

      // Track Midline Crossings (crossing x = 0 plane)
      const currentSignX = Math.sign(token.targetX);
      if (lastTokenSignX !== 0 && currentSignX !== 0 && currentSignX !== lastTokenSignX) {
        midlineCrossingsCount++;
        const crossEl = document.getElementById('valMidlinePasses');
        if (crossEl) crossEl.textContent = `${midlineCrossingsCount} CROSSINGS`;
        if (midlineCrossingsCount % 5 === 0) {
          sound.playChime(1.5);
          showToast(`🌟 ${midlineCrossingsCount} Midline Crossings! Corpus Callosum Re-Engaged`);
        }
      }
      lastTokenSignX = currentSignX;
    }


    /* ========================================================================== */
    /* TRI-PARADIGM ARBITER & PTSD EMDR GROUNDING ENGINE                          */
    /* ========================================================================== */
    let currentParadigm = 'allopathic'; // 'allopathic', 'tcm', 'ayurvedic'
    let isEmdrActive = false;
    let emdrDirection = 1;

    // Paradigm Arbiter
    document.querySelectorAll('.paradigm-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        sound.init();
        document.querySelectorAll('.paradigm-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentParadigm = btn.dataset.paradigm;

        if (currentParadigm === 'allopathic') {
          sound.setFrequency(528);
          setBoard('zero');
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'zero'));
          showToast('🔵 Western Allopathic: ISMP Disambiguation & Motor Mapping Active');
        } else if (currentParadigm === 'tcm') {
          sound.setFrequency(432);
          setBoard('xin');
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'xin'));
          showToast('🟢 TCM Qi & Meridian: Xin (Heart Shen) Acupoint Channel Active');
        } else if (currentParadigm === 'ayurvedic') {
          sound.setFrequency(136.1);
          setBoard('om');
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'om'));
          showToast('🟡 Ayurvedic Medicine: Pranava OM & Tridosha Grounding Active');
        } else if (currentParadigm === 'trible') {
          sound.setFrequency(432);
          setBoard('tumtum');
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'tumtum'));
          showToast('👥 Teachings of Tribility: Kloshe Tumtum & Canoe Journey Pulling Active');
        } else if (currentParadigm === 'sacred') {
          sound.setFrequency(528);
          setBoard('dharmachakra');
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'dharmachakra'));
          showToast('🕊️ Multi-Faith Chaplaincy: Dharmachakra & Palliative Directives Active');
        }
      });
    });

    // Emergency Grounding Anchor (Single-Tap PTSD De-escalation)
    const btnEmergencyGround = document.getElementById('btnEmergencyGround');
    if (btnEmergencyGround) {
      btnEmergencyGround.addEventListener('click', () => {
        sound.init();
        sound.setFrequency(136.1); // Earth OM 136.1 Hz for profound trauma calming
        if (typeof setHealerMode === 'function') setHealerMode('breath'); // 4-7-8 Breath
        
        // Turn on Glare Softener
        const glareEl = document.getElementById('glareSoftenerOverlay');
        const chipGlareEl = document.getElementById('chipGlare');
        if (glareEl) glareEl.classList.add('active');
        if (chipGlareEl) chipGlareEl.classList.add('active');

        // Select An (Sanctuary) or OM board
        setBoard('an');
        document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'an'));

        showToast('🛡️ GROUNDING SAFETY ACTIVATED • Feel Your Feet on the Floor • Breathe Deeply');
      });
    }

    // PTSD Somatic Protocol Buttons
    const traumaPills = document.querySelectorAll('.rehab-pill[data-trauma]');
    traumaPills.forEach(pill => {
      pill.addEventListener('click', () => {
        sound.init();
        traumaPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const mode = pill.dataset.trauma;

        if (mode === 'emdr') {
          isEmdrActive = true;
          setBoard('s'); // S-curve or Figure-8 for wide horizontal eye tracking
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 's'));
          if (!isAutoFlow && typeof btnToggleAutoFlow !== 'undefined' && btnToggleAutoFlow) {
            btnToggleAutoFlow.click();
          }
          showToast('👁️ EMDR Bilateral Eye-Tracker Active: Follow the pearl horizontally with eyes only');
        } else if (mode === 'discharge') {
          sound.setFrequency(432);
          showToast('🌊 Somatic Experiencing: Notice physical sensations, allow spontaneous sighing');
        } else if (mode === 'word') {
          setBoard('shanti');
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'shanti'));
          showToast('🔤 Sacred Words Active: Tracing Shanti (Universal Peace)');
        } else if (mode === 'vagal') {
          sound.setFrequency(528);
          setBoard('pipa');
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === 'pipa'));
          showToast('🛡️ Polyvagal Safety Shield: Dissolving freeze into social connection');
        }
      });
    });

    // Touch & Mouse Input Handlers
    function handlePointer(clientX, clientY) {
      const rect = canvas.getBoundingClientRect();
      const rawX = clientX - rect.left - width / 2;
      const rawY = clientY - rect.top - height / 2;

      token.targetX = rawX;
      token.targetY = rawY;
    }

    let isPointerOverCanvas = false;

    if (canvas) {
      canvas.addEventListener('pointerenter', () => {
        isPointerOverCanvas = true;
      });

      canvas.addEventListener('pointerleave', () => {
        isPointerOverCanvas = false;
        pointerRadius = 0;
      });

      canvas.addEventListener('pointerdown', (e) => {
        sound.init();
        isDragging = true;
        isPointerOverCanvas = true;
        try { canvas.setPointerCapture(e.pointerId); } catch (_) {}
        handleRehabPointer(e.clientX, e.clientY, true);
      });

      canvas.addEventListener('pointermove', (e) => {
        const rect = canvas.getBoundingClientRect();
        pointerCanvasX = e.clientX - rect.left - width / 2;
        pointerCanvasY = e.clientY - rect.top - height / 2;
        pointerRadius = 180;
        isPointerOverCanvas = true;
        handleRehabPointer(e.clientX, e.clientY, isDragging);
      });

      canvas.addEventListener('pointerup', (e) => {
        isDragging = false;
        try { canvas.releasePointerCapture(e.pointerId); } catch (_) {}
      });

      canvas.addEventListener('pointercancel', (e) => {
        isDragging = false;
        try { canvas.releasePointerCapture(e.pointerId); } catch (_) {}
      });
    }

    window.addEventListener('pointerup', () => {
      isDragging = false;
    });

    // Particle Swarm for Healing Wisps
    const wisps = [];
    for (let i = 0; i < 35; i++) {
      wisps.push({
        x: (Math.random() - 0.5) * 500,
        y: (Math.random() - 0.5) * 500,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        radius: Math.random() * 3 + 1.5,
        alpha: Math.random() * 0.6 + 0.2,
        phase: Math.random() * Math.PI * 2
      });
    }

    /* ─── MAIN ANIMATION LOOP ─── */
    function render() {
      ctx.clearRect(0, 0, width, height);
      const nowMs = Date.now();

      const cx = width / 2;
      const cy = height / 2;
      const board = BOARDS[currentBoardKey];

      ctx.save();
      ctx.translate(cx, cy);

      // ─── 1. ARCHITECTURAL 1:1 EM-SQUARE STUDIO FRAME & OPTICAL FOCUS MARKS ───
      const halfEm = Math.min(width, height) * 0.42;
      const cornerLen = Math.min(28, halfEm * 0.16);

      ctx.save();
      const isWashiTheme = (document.documentElement.getAttribute('data-theme') === 'washi');
      const frameColor = isWashiTheme ? 'rgba(120, 100, 80, 0.28)' : 'rgba(56, 189, 248, 0.25)';
      const crosshairColor = isWashiTheme ? 'rgba(120, 100, 80, 0.12)' : 'rgba(56, 189, 248, 0.10)';
      const reticleColor = isWashiTheme ? 'rgba(120, 100, 80, 0.35)' : 'rgba(56, 189, 248, 0.35)';

      // Architectural 1:1 Em-Square bounding perimeter
      ctx.strokeStyle = crosshairColor;
      ctx.lineWidth = 1;
      ctx.strokeRect(-halfEm, -halfEm, halfEm * 2, halfEm * 2);

      // 4 Outer Corner Registration Brackets: ┌ ┐ └ ┘
      ctx.strokeStyle = frameColor;
      ctx.lineWidth = 1.8;

      // Top-Left ┌
      ctx.beginPath();
      ctx.moveTo(-halfEm, -halfEm + cornerLen);
      ctx.lineTo(-halfEm, -halfEm);
      ctx.lineTo(-halfEm + cornerLen, -halfEm);
      ctx.stroke();

      // Top-Right ┐
      ctx.beginPath();
      ctx.moveTo(halfEm - cornerLen, -halfEm);
      ctx.lineTo(halfEm, -halfEm);
      ctx.lineTo(halfEm, -halfEm + cornerLen);
      ctx.stroke();

      // Bottom-Left └
      ctx.beginPath();
      ctx.moveTo(-halfEm, halfEm - cornerLen);
      ctx.lineTo(-halfEm, halfEm);
      ctx.lineTo(-halfEm + cornerLen, halfEm);
      ctx.stroke();

      // Bottom-Right ┘
      ctx.beginPath();
      ctx.moveTo(halfEm - cornerLen, halfEm);
      ctx.lineTo(halfEm, halfEm);
      ctx.lineTo(halfEm, halfEm - cornerLen);
      ctx.stroke();

      // 4 Cardinal Axis Focus Ticks (North, South, East, West)
      const tickSize = 9;
      ctx.beginPath();
      ctx.moveTo(0, -halfEm); ctx.lineTo(0, -halfEm + tickSize);
      ctx.moveTo(0, halfEm); ctx.lineTo(0, halfEm - tickSize);
      ctx.moveTo(-halfEm, 0); ctx.lineTo(-halfEm + tickSize, 0);
      ctx.moveTo(halfEm, 0); ctx.lineTo(halfEm - tickSize, 0);
      ctx.stroke();

      // Subtle Cardinal Axis Center Crosshairs (Meeting at Dead-Center 0, 0)
      ctx.save();
      ctx.setLineDash([3, 7]);
      ctx.strokeStyle = crosshairColor;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(-halfEm + tickSize, 0); ctx.lineTo(-14, 0);
      ctx.moveTo(14, 0); ctx.lineTo(halfEm - tickSize, 0);
      ctx.moveTo(0, -halfEm + tickSize); ctx.lineTo(0, -14);
      ctx.moveTo(0, 14); ctx.lineTo(0, halfEm - tickSize);
      ctx.stroke();
      ctx.restore();

      // Center Optical Reticle Whisper (+) & Sub-Pixel Anchor Detent
      ctx.strokeStyle = reticleColor;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(-12, 0); ctx.lineTo(12, 0);
      ctx.moveTo(0, -12); ctx.lineTo(0, 12);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(0, 0, 3, 0, Math.PI * 2);
      ctx.stroke();

      ctx.restore();

      // 0. Concentric Tea-Drop / Ink Water Ripples (Paradoxical Fluid Time)
      const teaCycle = (nowMs * 0.00012) % 1.0;
      ctx.save();
      ctx.lineWidth = 1.0;
      for (let rIdx = 0; rIdx < 3; rIdx++) {
        const rProg = (teaCycle + rIdx * 0.333) % 1.0;
        const rippleRadius = 36 + rProg * (halfEm * 0.90);
        const rippleAlpha = (1 - rProg) * (isZenMode ? 0.09 : 0.05);
        ctx.strokeStyle = `rgba(45, 212, 191, ${rippleAlpha})`;
        ctx.beginPath();
        ctx.arc(0, 0, rippleRadius, 0, Math.PI * 2);
        ctx.stroke();
      }
      ctx.restore();

      // 1. Draw Ambient Wisps & Cascading Stardust Embers
      for (let i = wisps.length - 1; i >= 0; i--) {
        const w = wisps[i];
        w.x += w.vx;
        w.y += w.vy;
        w.phase += 0.02;

        if (w.isEmber) {
          w.alpha *= 0.965;
          if (w.alpha <= 0.03) {
            wisps.splice(i, 1);
            continue;
          }
          ctx.fillStyle = `rgba(45, 212, 191, ${w.alpha})`;
          ctx.beginPath();
          ctx.arc(w.x, w.y, w.radius, 0, Math.PI * 2);
          ctx.fill();
        } else {
          if (Math.abs(w.x) > 300) w.vx *= -1;
          if (Math.abs(w.y) > 300) w.vy *= -1;

          ctx.fillStyle = `rgba(56, 189, 248, ${w.alpha * (0.5 + Math.sin(w.phase) * 0.3)})`;
          ctx.beginPath();
          ctx.arc(w.x, w.y, w.radius, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // ─── Touch Aura Proximity Calculation ───
      let auraProximityFactor = 0;
      if (pointerRadius > 0 && (isTouchAuraActive || currentPhilocardiaMode === 'aura')) {
        const distToPointer = Math.hypot(pointerCanvasX - token.x, pointerCanvasY - token.y);
        if (distToPointer < 220) {
          auraProximityFactor = 1 - (distToPointer / 220);
        }

        // Draw Touch Aura Halo around Cursor / Finger
        ctx.save();
        const auraGrad = ctx.createRadialGradient(pointerCanvasX, pointerCanvasY, 10, pointerCanvasX, pointerCanvasY, 180);
        auraGrad.addColorStop(0, 'rgba(251, 113, 133, 0.28)');
        auraGrad.addColorStop(0.5, 'rgba(45, 212, 191, 0.15)');
        auraGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = auraGrad;
        ctx.beginPath();
        ctx.arc(pointerCanvasX, pointerCanvasY, 180, 0, Math.PI * 2);
        ctx.fill();

        // Spawn gentle Heart Embers when near token or paths
        if (Math.random() < 0.25) {
          heartParticles.push({
            x: pointerCanvasX + (Math.random() - 0.5) * 40,
            y: pointerCanvasY + (Math.random() - 0.5) * 40,
            vx: (Math.random() - 0.5) * 0.8,
            vy: -Math.random() * 1.2 - 0.4,
            alpha: 1.0,
            scale: Math.random() * 0.6 + 0.6,
            char: (currentPhilocardiaMode === 'aura' || currentPhilocardiaMode === '72') ? '♥' : '✦'
          });
        }
        ctx.restore();
      }

      // Draw and Update Heart Embers
      for (let i = heartParticles.length - 1; i >= 0; i--) {
        const hp = heartParticles[i];
        hp.x += hp.vx;
        hp.y += hp.vy;
        hp.alpha -= 0.018;
        if (hp.alpha <= 0) {
          heartParticles.splice(i, 1);
          continue;
        }
        ctx.save();
        ctx.font = `${Math.round(14 * hp.scale)}px "PocketGull", sans-serif`;
        ctx.fillStyle = `rgba(251, 113, 133, ${hp.alpha})`;
        ctx.shadowColor = '#fb7185';
        ctx.shadowBlur = 8;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(hp.char, hp.x, hp.y);
        ctx.restore();
      }

      // Update 15-Second Radial Palpation Chronometer
      const nowTime = performance.now();
      const dt = (nowTime - lastPalpationTime) / 1000;
      lastPalpationTime = nowTime;
      palpationSeconds = (palpationSeconds + dt) % 15;
      const palpTimerEl = document.getElementById('palpationTimerText');
      if (palpTimerEl) palpTimerEl.textContent = `${palpationSeconds.toFixed(1)}s`;
      const arcMeterEl = document.getElementById('palpationArcMeter');
      if (arcMeterEl) {
        const totalLen = 75.4; // 2 * pi * 12
        const progress = palpationSeconds / 15;
        arcMeterEl.style.strokeDashoffset = (totalLen * (1 - progress)).toString();
      }

      // ─── 1.5 PROJECTION OF AUTHENTIC POCKETGULL LETTERFORM FIGURE ───
      let letterScale = 0.62;
      if (board && board.char) {
        ctx.save();

        const maxGlyphW = width * 0.70;
        const maxGlyphH = height * 0.68;
        let glyphFontSize = Math.min(440, Math.min(maxGlyphW * 1.45, maxGlyphH * 1.30));
        
        ctx.font = `800 ${glyphFontSize}px "PocketGull", "Noto Sans", sans-serif`;
        let m = ctx.measureText(board.char);
        if (m.width > maxGlyphW) {
          glyphFontSize *= (maxGlyphW / m.width);
          ctx.font = `800 ${glyphFontSize}px "PocketGull", "Noto Sans", sans-serif`;
          m = ctx.measureText(board.char);
        }

        const glyphH = m.actualBoundingBoxAscent + m.actualBoundingBoxDescent;
        const breathMod = isZenMode ? (Math.sin(nowTime * 0.000628) * 0.035) : 0;
        letterScale = Math.max(0.40, Math.min(1.0, (glyphH / 420) * (1 + breathMod)));
        currentLetterScale = letterScale;

        const activeFontSize = glyphFontSize * (1 + breathMod);
        ctx.font = `800 ${activeFontSize}px "PocketGull", "Noto Sans", sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'alphabetic';
        m = ctx.measureText(board.char);

        const glyphOffsetX = (m.actualBoundingBoxLeft - m.actualBoundingBoxRight) / 2;
        const glyphOffsetY = (m.actualBoundingBoxAscent - m.actualBoundingBoxDescent) / 2;

        // Resolve exact subpixel outline contour points & 2-pass ink centering corrections
        const outlines = extractGlyphOutlines(board.char);
        const renderOffsetX = glyphOffsetX - (outlines.correctionX || 0) * activeFontSize;
        const renderOffsetY = glyphOffsetY - (outlines.correctionY || 0) * activeFontSize;

        const topY = renderOffsetY - m.actualBoundingBoxAscent;
        const baseY = renderOffsetY;
        const waistY = renderOffsetY - (m.actualBoundingBoxAscent * 0.52);

        if (outlines && outlines.primaryContour && outlines.primaryContour.length > 0) {
          currentBoardOutlinePoints = outlines.primaryContour.map(p => ({
            x: p.x * activeFontSize,
            y: p.y * activeFontSize
          }));
          let minY = Infinity, maxY = -Infinity;
          for (let i = 0; i < currentBoardOutlinePoints.length; i++) {
            const py = currentBoardOutlinePoints[i].y;
            if (py < minY) minY = py;
            if (py > maxY) maxY = py;
          }
          contourMinY = minY;
          contourMaxY = maxY;

          if (lastRenderedBoardKey !== board.id) {
            lastRenderedBoardKey = board.id;
            if (currentBoardOutlinePoints.length > 0) {
              token.x = token.targetX = currentBoardOutlinePoints[0].x;
              token.y = token.targetY = currentBoardOutlinePoints[0].y;
              token.vx = 0;
              token.vy = 0;
              token.trail = [];
            }
          }
        }

        // A. Subtle Typographic Drafting Guidelines (Only in Studio / Telemetry Mode)
        if (!isZenMode) {
          ctx.save();
          ctx.setLineDash([4, 8]);
          ctx.lineWidth = 1;
          ctx.strokeStyle = 'rgba(56, 189, 248, 0.16)';
          ctx.fillStyle = 'rgba(148, 163, 184, 0.40)';
          ctx.font = '9px "PocketGull Mono", monospace';
          ctx.textAlign = 'left';
          ctx.textBaseline = 'bottom';

          const guideSpan = Math.max(m.width * 0.70, width * 0.38);

          // Cap-Height line
          ctx.beginPath();
          ctx.moveTo(-guideSpan, topY);
          ctx.lineTo(guideSpan, topY);
          ctx.stroke();
          ctx.fillText('CAP-HEIGHT [780 UPM]', -guideSpan + 4, topY - 3);

          // Optical Waist line
          ctx.beginPath();
          ctx.moveTo(-guideSpan, waistY);
          ctx.lineTo(guideSpan, waistY);
          ctx.stroke();
          ctx.fillText('OPTICAL WAIST [540 UPM]', -guideSpan + 4, waistY - 3);

          // Baseline
          ctx.beginPath();
          ctx.moveTo(-guideSpan, baseY);
          ctx.lineTo(guideSpan, baseY);
          ctx.stroke();
          ctx.fillText('BASELINE [0 UPM]', -guideSpan + 4, baseY - 3);

          ctx.restore();
        }

        // B. Illuminated Letterform Silhouette Fill & Glow
        ctx.save();
        ctx.font = `800 ${activeFontSize}px "PocketGull", "Noto Sans", sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'alphabetic';

        const isAuraWarm = (auraProximityFactor > 0.35 || currentPhilocardiaMode === 'aura');
        ctx.shadowColor = isAuraWarm ? '#fb7185' : '#38bdf8';
        ctx.shadowBlur = 32 + (auraProximityFactor * 24);
        ctx.fillStyle = isAuraWarm 
          ? `rgba(251, 113, 133, ${0.14 + auraProximityFactor * 0.16})`
          : `rgba(56, 189, 248, ${0.11 + auraProximityFactor * 0.14})`;
        ctx.fillText(board.char, renderOffsetX, renderOffsetY);

        // C. Vector Optotype Contour Stroke
        ctx.lineWidth = 5.5 + (auraProximityFactor * 3.5);
        ctx.strokeStyle = isAuraWarm
          ? `rgba(251, 113, 133, ${0.48 + auraProximityFactor * 0.25})`
          : `rgba(45, 212, 191, ${0.48 + auraProximityFactor * 0.25})`;
        ctx.shadowBlur = 18;
        ctx.strokeText(board.char, renderOffsetX, renderOffsetY);

        // D. Luminous Core Trace Vector
        ctx.lineWidth = 1.6;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.90)';
        ctx.shadowBlur = 4;
        ctx.shadowColor = '#ffffff';
        ctx.strokeText(board.char, renderOffsetX, renderOffsetY);

        // Special: If ISMP Slashed Zero, draw the clinical 45-degree safety slash bridge across counter
        if (board.id === 'zero' || board.char === '0̸' || board.char === '0') {
          const slashW = m.width * 0.28;
          const slashH = (m.actualBoundingBoxAscent + m.actualBoundingBoxDescent) * 0.40;
          ctx.beginPath();
          ctx.moveTo(-slashW, slashH);
          ctx.lineTo(slashW, -slashH);
          ctx.lineWidth = 6;
          ctx.strokeStyle = isAuraWarm ? 'rgba(251, 113, 133, 0.75)' : 'rgba(45, 212, 191, 0.75)';
          ctx.shadowBlur = 14;
          ctx.shadowColor = isAuraWarm ? '#fb7185' : '#14b8a6';
          ctx.stroke();
          ctx.lineWidth = 2;
          ctx.strokeStyle = '#ffffff';
          ctx.shadowBlur = 4;
          ctx.stroke();
        }

        ctx.restore();
        ctx.restore();
      }

      // 2. Interactive Tactile Felt-Marker Tracing Trail & 03-02-1987 Breath-Synced Auto-Glide
      const breathTimeMs = nowMs % 10000; // 10-second vagal breath cycle (4s Inhale / 6s Exhale)
      const isInhale = breathTimeMs < 4000;
      let speedMultiplier = 1.0;
      let breathAuraRadius = 14;
      let breathAuraColor = '#2dd4bf'; // Jade-teal
      let breathProg = 0;

      if (isInhale) {
        breathProg = breathTimeMs / 4000;
        // Inhale: Gentle 1.0x -> 1.35x acceleration
        speedMultiplier = 1.0 + 0.35 * Math.sin(breathProg * Math.PI);
        // Aura expands to 26px in warm rose-gold Yin Hearth Fire
        breathAuraRadius = 14 + 12 * Math.sin(breathProg * Math.PI);
        breathAuraColor = '#fb7185';
      } else {
        breathProg = (breathTimeMs - 4000) / 6000;
        // Exhale: Parasympathetic deceleration down to 0.80x
        speedMultiplier = 1.0 - 0.20 * Math.sin(breathProg * Math.PI);
        // Aura settles to calming jade-teal
        breathAuraRadius = 14 + 4 * (1 - breathProg);
        breathAuraColor = '#2dd4bf';
      }

      if (isAutoFlow) {
        autoFlowAngle += 0.014 * speedMultiplier;
        if (autoFlowAngle >= Math.PI * 2) {
          autoFlowAngle -= Math.PI * 2;
          sound.playLandmarkChime('circuit');
          triggerHaptic('circuit');
          showToast('✨ 03-02-1987 Circuit Complete • Natal Diapente Harmonic Resolved');
        }

        // Emit cascading stardust embers during unhurried exhale
        if (!isInhale && Math.random() < 0.28) {
          wisps.push({
            x: token.x + (Math.random() - 0.5) * 10,
            y: token.y + (Math.random() - 0.5) * 10,
            vx: (Math.random() - 0.5) * 0.3,
            vy: 0.15 + Math.random() * 0.35,
            radius: Math.random() * 2 + 1,
            alpha: 0.75,
            phase: Math.random() * Math.PI * 2,
            isEmber: true
          });
        }

        if (currentBoardOutlinePoints && currentBoardOutlinePoints.length > 1) {
          const ptLen = currentBoardOutlinePoints.length;
          const ptIdx = Math.floor((autoFlowAngle / (Math.PI * 2) * ptLen)) % ptLen;
          const nextIdx = (ptIdx + 1) % ptLen;
          const subProg = (autoFlowAngle / (Math.PI * 2) * ptLen) % 1;
          const currP = currentBoardOutlinePoints[ptIdx];
          const nextP = currentBoardOutlinePoints[nextIdx];
          token.targetX = currP.x + (nextP.x - currP.x) * subProg;
          token.targetY = currP.y + (nextP.y - currP.y) * subProg;
        } else {
          const waypoints = getBoardWaypoints(board);
          if (waypoints && waypoints.length > 1) {
            const wpLen = waypoints.length;
            const wpIdx = Math.floor((autoFlowAngle / (Math.PI * 2) * wpLen)) % wpLen;
            const nextIdx = (wpIdx + 1) % wpLen;
            const subProg = (autoFlowAngle / (Math.PI * 2) * wpLen) % 1;
            const currP = waypoints[wpIdx];
            const nextP = waypoints[nextIdx];
            token.targetX = (currP.x + (nextP.x - currP.x) * subProg) * letterScale;
            token.targetY = (currP.y + (nextP.y - currP.y) * subProg) * letterScale;
          }
        }
      }

      // Smooth organic dampening towards target (responsive 0.28 tracking)
      const distToTarget = Math.hypot(token.targetX - token.x, token.targetY - token.y);
      if (distToTarget > 90) {
        token.x = token.targetX;
        token.y = token.targetY;
        token.vx = 0;
        token.vy = 0;
        token.trail = [];
      } else {
        token.vx = (token.targetX - token.x) * 0.28;
        token.vy = (token.targetY - token.y) * 0.28;
        token.x += token.vx;
        token.y += token.vy;
      }

      // Append to fluid ink trail while interacting, dragging, or in auto-flow
      if (isDragging || isAutoFlow || isKeyboardActive) {
        token.trail.push({ x: token.x, y: token.y, alpha: 1.0 });
      } else if (isPointerOverCanvas) {
        // Soft aura trace on hover
        token.trail.push({ x: token.x, y: token.y, alpha: 0.35 });
      } else {
        // Slowly dissolve lingering trail when released
        for (let i = 0; i < token.trail.length; i++) {
          token.trail[i].alpha *= 0.92;
        }
        token.trail = token.trail.filter(pt => pt.alpha > 0.02);
      }
      if (token.trail.length > 40) token.trail.shift();

      // Draw Fluid Humanist Felt-Marker Ink Trail
      if (token.trail.length > 1) {
        ctx.save();
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        // Outer warm ink glow
        ctx.beginPath();
        ctx.moveTo(token.trail[0].x, token.trail[0].y);
        for (let i = 1; i < token.trail.length; i++) {
          ctx.lineTo(token.trail[i].x, token.trail[i].y);
        }
        const trailGlowColor = isAutoFlow ? breathAuraColor : (auraProximityFactor > 0.35 ? '#fb7185' : '#2dd4bf');
        ctx.strokeStyle = isAutoFlow 
          ? (isInhale ? 'rgba(251, 113, 133, 0.45)' : 'rgba(45, 212, 191, 0.38)') 
          : (auraProximityFactor > 0.35 ? 'rgba(251, 113, 133, 0.40)' : 'rgba(45, 212, 191, 0.35)');
        ctx.lineWidth = 18;
        ctx.shadowColor = trailGlowColor;
        ctx.shadowBlur = 18;
        ctx.stroke();

        // Inner luminous felt-marker core
        ctx.beginPath();
        ctx.moveTo(token.trail[0].x, token.trail[0].y);
        for (let i = 1; i < token.trail.length; i++) {
          ctx.lineTo(token.trail[i].x, token.trail[i].y);
        }
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.90)';
        ctx.lineWidth = 5;
        ctx.shadowBlur = 6;
        ctx.shadowColor = '#ffffff';
        ctx.stroke();
        ctx.restore();
      }

      // Draw subtle touch guide point / light pearl when active or hovering
      if (isDragging || isKeyboardActive || isAutoFlow || isPointerOverCanvas) {
        ctx.save();
        ctx.beginPath();
        const pearlRadius = isAutoFlow ? breathAuraRadius : (isDragging ? 11 : 8);
        const pearlColor = isAutoFlow ? breathAuraColor : (auraProximityFactor > 0.35 ? '#fb7185' : '#2dd4bf');
        ctx.arc(token.x, token.y, pearlRadius, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = pearlColor;
        ctx.shadowBlur = isAutoFlow ? (pearlRadius * 1.5) : (isDragging ? 22 : 14);
        ctx.fill();
        ctx.strokeStyle = pearlColor;
        ctx.lineWidth = 2.2;
        ctx.stroke();
        ctx.restore();
      }

      // ─── 03-02-1987 Acoustic Kinetic Harp & Landmark Detents ───
      const moveDist = Math.hypot(token.x - lastPearlX, token.y - lastPearlY);
      const isActiveMovement = isDragging || isAutoFlow || isKeyboardActive;
      const nowAudioTime = performance.now();

      if (isActiveMovement && moveDist > 0.35) {
        accumulatedHarpDistance += moveDist;

        // Continuous Micro-Harp Contour Strumming (delicate acoustic pluck every ~42px)
        if (accumulatedHarpDistance >= 42 && (nowAudioTime - lastHarpPluckTime > 70)) {
          const freq = getHarpPitchForY(token.y, halfEm);
          const pan = Math.max(-1, Math.min(1, token.x / (halfEm || 220)));
          sound.playHarpPluck(freq, pan, isAutoFlow ? 0.85 : 1.0);
          accumulatedHarpDistance = 0;
          lastHarpPluckTime = nowAudioTime;
        }

        // Landmark 1: Optical Waist Crossing (Y = 0 / 540 UPM optical midline)
        if ((lastPearlY < 0 && token.y >= 0) || (lastPearlY > 0 && token.y <= 0)) {
          const pan = Math.max(-1, Math.min(1, token.x / (halfEm || 220)));
          sound.playLandmarkChime('waist', pan);
          triggerHaptic('waist');
        }

        // Landmark 2: Midline Crossing (X = 0 / Corpus Callosum bilateral plane)
        if ((lastPearlX < 0 && token.x >= 0) || (lastPearlX > 0 && token.x <= 0)) {
          sound.playLandmarkChime('crossing', 0);
          triggerHaptic('crossing');
        }

        // Landmark 3: Ingress Gate Apex (Topmost contour point)
        if (token.y <= (contourMinY + 12) && !hasHitApex) {
          hasHitApex = true;
          const pan = Math.max(-1, Math.min(1, token.x / (halfEm || 220)));
          sound.playLandmarkChime('ingress', pan);
          triggerHaptic('ingress');
        } else if (token.y > (contourMinY + 36)) {
          hasHitApex = false;
        }

        // Landmark 4: Root Grounding Baseline (Bottommost contour point)
        if (token.y >= (contourMaxY - 12) && !hasHitGround) {
          hasHitGround = true;
          const pan = Math.max(-1, Math.min(1, token.x / (halfEm || 220)));
          sound.playLandmarkChime('ground', pan);
          triggerHaptic('ground');
        } else if (token.y < (contourMaxY - 36)) {
          hasHitGround = false;
        }
      }

      lastPearlX = token.x;
      lastPearlY = token.y;

      // Acoustic Sonar Spatial Update (for Blind & Low-Vision Orientation)
      if (sound.isSonarActive && (isDragging || isAutoFlow || isKeyboardActive)) {
        const normX = token.x / (width * 0.35);
        const normY = token.y / (height * 0.35);
        sound.updateSonar(normX, normY, true, true);
      }

      // Animate Paradoxical Bloom SVG with 10-second vagal breath wave
      if (bloomPetalsGroup && pacerMode !== 'numeric') {
        const petalScale = isInhale ? (0.86 + 0.22 * Math.sin(breathProg * Math.PI)) : (0.86 + 0.10 * (1 - breathProg));
        const rotDeg = (nowMs * 0.003) % 360;
        bloomPetalsGroup.setAttribute('transform', `scale(${petalScale.toFixed(3)}) rotate(${rotDeg.toFixed(2)} 50 50)`);
      }

      // Animate Paradoxical Fireweed Blossom in bottom rail (5-minute gradual unfurling)
      const fireweedPetalsEl = document.getElementById('fireweedPetals');
      if (fireweedPetalsEl) {
        const bloomProg = Math.min(1.0, fireweedBloomSeconds / FIREWEED_FULL_BLOOM_SECONDS);
        const baseScale = 0.70 + 0.55 * bloomProg;
        const breathScale = isInhale ? (1.0 + 0.16 * Math.sin(breathProg * Math.PI)) : (1.0 - 0.08 * Math.sin(breathProg * Math.PI));
        const currentScale = (baseScale * breathScale).toFixed(3);
        const rot = (fireweedBloomSeconds * 0.5 + breathProg * 10).toFixed(1);
        fireweedPetalsEl.setAttribute('transform', `scale(${currentScale}) rotate(${rot} 20 20)`);
      }

      ctx.restore();

      requestAnimationFrame(render);
    }

    function drawBoardPaths(paths) {
      paths.forEach(p => {
        ctx.beginPath();
        if (p.type === 'ellipse') {
          ctx.ellipse(p.cx, p.cy, p.rx, p.ry, 0, 0, Math.PI * 2);
        } else if (p.type === 'circle') {
          ctx.arc(p.cx, p.cy, p.r, 0, Math.PI * 2);
        } else if (p.type === 'line') {
          ctx.moveTo(p.x1, p.y1);
          ctx.lineTo(p.x2, p.y2);
        } else if (p.type === 'poly') {
          ctx.moveTo(p.points[0].x, p.points[0].y);
          for (let i = 1; i < p.points.length; i++) {
            ctx.lineTo(p.points[i].x, p.points[i].y);
          }
          ctx.closePath();
        } else if (p.type === 'bezier') {
          ctx.moveTo(p.p0.x, p.p0.y);
          ctx.bezierCurveTo(p.p1.x, p.p1.y, p.p2.x, p.p2.y, p.p3.x, p.p3.y);
        }
      });
    }

    /* ========================================================================== */
    /* EVENT LISTENERS & UI CONTROLS                                              */
    /* ========================================================================== */
    // Board Selection Cards
    document.querySelectorAll('.board-card').forEach(card => {
      card.addEventListener('click', () => {
        document.querySelectorAll('.board-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        setBoard(card.dataset.board);
      });
    });

    // Soundscape Selector
    document.querySelectorAll('.sound-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.sound-btn').forEach(b => {
          b.classList.remove('active');
          b.style.borderColor = 'rgba(255,255,255,0.2)';
          b.style.color = 'rgba(255,255,255,0.7)';
          b.style.background = 'transparent';
        });
        btn.classList.add('active');
        btn.style.borderColor = 'var(--accent-teal)';
        btn.style.color = 'var(--accent-teal)';
        btn.style.background = 'rgba(20, 184, 166, 0.15)';
        const freq = parseFloat(btn.dataset.freq);
        sound.setFrequency(freq);
        if (freq === 648) {
          sound.playTibetanBowl(432);
          showToast('🕊️ 3:2 Diapente Fifth (432:648 Hz) • Natal Harmonic Resonance Active');
        } else {
          sound.playChime(1.0);
          showToast(`🎶 Resonating at ${freq} Hz • Healing Wave Active`);
        }
      });
    });

    // Audio Toggle
    const btnToggleAudio = document.getElementById('btnToggleAudio');
    btnToggleAudio.addEventListener('click', () => {
      sound.enabled = !sound.enabled;
      btnToggleAudio.textContent = sound.enabled ? '🔊 Audio: ON' : '🔇 Audio: MUTED';
      if (sound.enabled) sound.playChime(1.0);
    });

    // Theme Toggle: 6-State Clinical Optical Preservation Cycle
    const CLINICAL_THEMES = [
      { id: 'dark', label: '🎨 Theme: Indigo Dark', toast: '🌌 Indigo Dark Floor Active • OLED Halation Shield' },
      { id: 'fl41', label: '🌸 Theme: FL-41 Rose', toast: '🌸 FL-41 Rose Active • 480-520nm Melanopsin Photophobia Notch' },
      { id: 'pbm', label: '🔴 Theme: 670nm PBM', toast: '🔴 670nm Retinal Photobiomodulation Active • Mitochondrial ATP Recharge' },
      { id: 'sage', label: '🍵 Theme: Sage Jade', toast: '🍵 Irlen Sage Jade Active • Visual Cortex V1/V2 Hyper-Excitability Quenched' },
      { id: 'washi', label: '📜 Theme: Washi Paper', toast: '📜 Washi Paper Active • 10:1 Tactile Reflection Ratio' },
      { id: 'amber', label: '🌙 Theme: Amber Night', toast: '🌙 Amber Night Shift Active • 550nm Cutoff Full Blue Suppression' }
    ];

    function applyClinicalTheme(themeId) {
      const match = CLINICAL_THEMES.find(t => t.id === themeId) || CLINICAL_THEMES[0];
      document.documentElement.setAttribute('data-theme', match.id);
      if (btnThemeToggle) btnThemeToggle.textContent = match.label;
      document.querySelectorAll('.btn-vis-filter').forEach(b => {
        b.classList.toggle('active', b.dataset.themeFilter === match.id);
      });
      sound.playRipple();
      triggerHaptic('detent');
      showToast(match.toast);
      announceSR(match.toast);
    }

    const btnThemeToggle = document.getElementById('btnThemeToggle');
    if (btnThemeToggle) {
      btnThemeToggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        const currentIndex = CLINICAL_THEMES.findIndex(t => t.id === current);
        const next = CLINICAL_THEMES[(currentIndex + 1) % CLINICAL_THEMES.length];
        applyClinicalTheme(next.id);
      });
    }

    // Visual Filter Bar Chips
    document.querySelectorAll('.btn-vis-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        sound.init();
        applyClinicalTheme(btn.dataset.themeFilter);
      });
    });

    // Luminance Clamping & Anti-Halation Toggles
    const toggleGammaClamp = document.getElementById('toggleGammaClamp');
    if (toggleGammaClamp) {
      document.documentElement.classList.add('filter-gamma-clamp');
      toggleGammaClamp.addEventListener('click', () => {
        sound.init();
        const isClamped = document.documentElement.classList.toggle('filter-gamma-clamp');
        toggleGammaClamp.classList.toggle('active', isClamped);
        toggleGammaClamp.textContent = isClamped ? '🔆 Luminance Clamp: ON' : '🔆 Luminance Clamp: OFF';
        showToast(isClamped ? '🔆 Luminance Clamping Active • Safe Retinal Photopic Ceiling' : '🔆 Luminance Clamping OFF');
        triggerHaptic('detent');
      });
    }

    const toggleAntiHalation = document.getElementById('toggleAntiHalation');
    if (toggleAntiHalation) {
      toggleAntiHalation.addEventListener('click', () => {
        sound.init();
        const isHalation = document.documentElement.classList.toggle('filter-anti-halation');
        toggleAntiHalation.classList.toggle('active', isHalation);
        toggleAntiHalation.textContent = isHalation ? '🌫️ Anti-Halation: ON' : '🌫️ Anti-Halation: OFF';
        showToast(isHalation ? '🌫️ Anti-Halation Micro-Diffusion Active • Soft Vector Edges' : '🌫️ Anti-Halation OFF');
        triggerHaptic('detent');
      });
    }

    // Collapsible Floating Drawers (Boards & Wisdom)
    const panelBoards = document.getElementById('panelBoards');
    const panelWisdom = document.getElementById('panelWisdom');
    const btnToggleBoards = document.getElementById('btnToggleBoards');
    const btnToggleWisdom = document.getElementById('btnToggleWisdom');
    const btnCloseBoards = document.getElementById('btnCloseBoards');
    const btnCloseWisdom = document.getElementById('btnCloseWisdom');

    if (btnToggleBoards && panelBoards) {
      btnToggleBoards.addEventListener('click', () => {
        sound.init();
        if (panelWisdom) {
          panelWisdom.classList.remove('drawer-open');
          if (btnToggleWisdom) btnToggleWisdom.classList.remove('active');
        }
        const isOpen = panelBoards.classList.toggle('drawer-open');
        btnToggleBoards.classList.toggle('active', isOpen);
      });
    }

    if (btnToggleWisdom && panelWisdom) {
      btnToggleWisdom.addEventListener('click', () => {
        sound.init();
        if (panelBoards) {
          panelBoards.classList.remove('drawer-open');
          if (btnToggleBoards) btnToggleBoards.classList.remove('active');
        }
        const isOpen = panelWisdom.classList.toggle('drawer-open');
        btnToggleWisdom.classList.toggle('active', isOpen);
      });
    }

    if (btnCloseBoards && panelBoards) {
      btnCloseBoards.addEventListener('click', () => {
        panelBoards.classList.remove('drawer-open');
        if (btnToggleBoards) btnToggleBoards.classList.remove('active');
      });
    }

    if (btnCloseWisdom && panelWisdom) {
      btnCloseWisdom.addEventListener('click', () => {
        panelWisdom.classList.remove('drawer-open');
        if (btnToggleWisdom) btnToggleWisdom.classList.remove('active');
      });
    }

    // Acoustic Sonar & Haptic Mode for Blind & Low-Vision Users
    const btnSonarMode = document.getElementById('btnSonarMode');
    if (btnSonarMode) {
      btnSonarMode.addEventListener('click', () => {
        sound.init();
        const nextState = !sound.isSonarActive;
        sound.setSonarActive(nextState);
        btnSonarMode.classList.toggle('sonar-active', nextState);
        btnSonarMode.textContent = nextState ? '🦯 Sonar: ON' : '🦯 Sonar: OFF';
        if (nextState) {
          triggerHaptic('complete');
          announceSR('Acoustic Sonar and Haptic Guidance activated. Pitch reflects vertical height, stereo panning reflects lateral position. Press B for directional landmark beacon. Use arrow keys to explore.');
          showToast('🦯 Acoustic Sonar & Haptics Active • Feel & Hear the Letterform');
        } else {
          announceSR('Acoustic Sonar deactivated.');
          showToast('🦯 Acoustic Sonar Deactivated');
        }
      });
    }

    // ─── Continuous Gentle Auto-Flow Engine ───
    let isAutoFlow = false;
    let autoFlowAngle = 0;
    const btnToggleAutoFlow = document.getElementById('btnToggleAutoFlow');

    if (btnToggleAutoFlow) {
      btnToggleAutoFlow.addEventListener('click', () => {
        sound.init();
        isAutoFlow = !isAutoFlow;
        token.trail = [];
        btnToggleAutoFlow.textContent = isAutoFlow ? '🌊 Auto-Flow: ON' : '🌊 Auto-Flow: OFF';
        btnToggleAutoFlow.style.borderColor = isAutoFlow ? '#10b981' : 'var(--accent-cyan)';
        btnToggleAutoFlow.style.color = isAutoFlow ? '#10b981' : 'var(--accent-cyan)';
        if (isAutoFlow) showToast('🌊 Gentle Auto-Flow Active • Rest Your Hands & Breathe');
      });
    }

    // ─── Super-Chill Mode Engine (Aggressive Gentleness) ───
    let isGameboardSuperChill = false;
    const btnGameboardSuperChill = document.getElementById('btnSuperChill');
    if (btnGameboardSuperChill) {
      btnGameboardSuperChill.addEventListener('click', () => {
        sound.init();
        isGameboardSuperChill = !isGameboardSuperChill;
        btnGameboardSuperChill.textContent = isGameboardSuperChill ? '🌱 Super-Chill: ON' : '🌱 Super-Chill: OFF';
        btnGameboardSuperChill.style.background = isGameboardSuperChill ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.15)';
        btnGameboardSuperChill.style.boxShadow = isGameboardSuperChill ? '0 0 16px rgba(16, 185, 129, 0.5)' : 'none';

        if (isGameboardSuperChill) {
          // 1. Enable Auto-Flow if off
          if (!isAutoFlow && btnToggleAutoFlow) btnToggleAutoFlow.click();
          // 2. Set calm 60 BPM or 4-7-8 breath
          if (typeof setHealerMode === 'function') setHealerMode('breath');
          // 3. Set restorative frequency
          sound.setFrequency(528);
          showToast('🌱 Super-Chill Active • Hands-Free Restorative Flow • Zero Effort');
        } else {
          if (isAutoFlow && btnToggleAutoFlow) btnToggleAutoFlow.click();
          showToast('🌱 Super-Chill Standard Mode');
        }
      });
    }

    // ─── Custom Glyph Board Generator ───
    const inputCustomGlyph = document.getElementById('inputCustomGlyph');
    const btnBuildCustomBoard = document.getElementById('btnBuildCustomBoard');

    function buildGlyphBoard(glyphChar) {
      const ch = (glyphChar || 'B').trim().toUpperCase();
      const boardKey = 'custom_' + ch;

      // Calculate procedural paths based on letterform geometry
      const paths = [];
      const targets = [];

      if (ch === 'B' || ch === 'P' || ch === 'R') {
        // Vertical spine
        paths.push({ type: 'line', x1: -120, y1: -220, x2: -120, y2: 220 });
        // Upper bowl
        paths.push({ type: 'circle', cx: -20, cy: -110, r: 100 });
        targets.push({ x: -120, y: -220, label: 'Spine Top', collected: false });
        targets.push({ x: 80, y: -110, label: 'Upper Crest', collected: false });
        targets.push({ x: -120, y: 0, label: 'Waist Cross', collected: false });

        if (ch === 'B') {
          // Lower bowl
          paths.push({ type: 'circle', cx: -10, cy: 110, r: 110 });
          targets.push({ x: 100, y: 110, label: 'Lower Swell', collected: false });
          targets.push({ x: -120, y: 220, label: 'Spine Base', collected: false });
        } else if (ch === 'R') {
          // Diagonal leg
          paths.push({ type: 'line', x1: -120, y1: 0, x2: 120, y2: 220 });
          targets.push({ x: 120, y: 220, label: 'Diagonal Terminal', collected: false });
        }
      } else if (ch === 'C' || ch === 'G' || ch === 'O' || ch === 'Q') {
        // Broad sweeping counter loop
        paths.push({ type: 'ellipse', cx: 0, cy: 0, rx: 170, ry: 220 });
        targets.push({ x: 0, y: -220, label: 'North Arch', collected: false });
        targets.push({ x: -170, y: 0, label: 'West Wall', collected: false });
        targets.push({ x: 0, y: 220, label: 'South Arch', collected: false });
        if (ch === 'C') {
          targets.push({ x: 140, y: -120, label: 'Upper Beak', collected: false });
          targets.push({ x: 140, y: 120, label: 'Lower Foot', collected: false });
        } else {
          targets.push({ x: 170, y: 0, label: 'East Wall', collected: false });
        }
      } else {
        // Universal Humanist Grid
        paths.push({ type: 'line', x1: -140, y1: -220, x2: 140, y2: -220 });
        paths.push({ type: 'line', x1: 0, y1: -220, x2: 0, y2: 220 });
        paths.push({ type: 'line', x1: -140, y1: 220, x2: 140, y2: 220 });
        paths.push({ type: 'circle', cx: 0, cy: 0, r: 120 });
        targets.push({ x: 0, y: -220, label: 'Crown Pillar', collected: false });
        targets.push({ x: 120, y: 0, label: 'Harmonic Ring', collected: false });
        targets.push({ x: 0, y: 220, label: 'Root Ground', collected: false });
        targets.push({ x: -120, y: 0, label: 'Saccade Pivot', collected: false });
      }

      BOARDS[boardKey] = {
        id: boardKey,
        char: ch,
        name: `PocketGull Custom '${ch}' Sanctuary`,
        moralTitle: `The Inherent Harmony of Letter '${ch}'`,
        moralDesc: `Every character in the alphabet holds a natural architectural rhythm. Gliding along '${ch}' grounds the thoughts, restores bilateral coordination, and fosters gentle mindfulness.`,
        paths: paths,
        targets: targets
      };

      setBoard(boardKey);
    }

    if (btnBuildCustomBoard) {
      btnBuildCustomBoard.addEventListener('click', () => {
        sound.init();
        buildGlyphBoard(inputCustomGlyph.value);
      });
    }

    if (inputCustomGlyph) {
      inputCustomGlyph.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          sound.init();
          buildGlyphBoard(inputCustomGlyph.value);
        }
      });
    }

    // Reset Token Button
    
    // Gameboard Lens Selector
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

        currentGbLens = btn.dataset.lens;
        applyGbLens();
        sound.playChime(currentGbLens === 'art' ? 660 : (currentGbLens === 'science' ? 432 : 528));
      });
    });


    // ─── ZEN SANCTUARY INTERACTION CONTROLS ───
    // Quick 1-Touch Glyph Selector
    document.querySelectorAll('.zen-glyph-chip[data-board]').forEach(chip => {
      chip.addEventListener('click', () => {
        sound.init();
        setBoard(chip.dataset.board);
      });
    });

    const btnToggleStudio = document.getElementById('btnToggleStudio');
    const btnReturnToZen = document.getElementById('btnReturnToZen');
    if (btnToggleStudio) {
      btnToggleStudio.addEventListener('click', () => {
        sound.init();
        isZenMode = false;
        document.body.classList.remove('zen-mode');
        showToast('⚙️ Clinical Studio & Telemetry Controls Active');
        resizeCanvas();
      });
    }

    if (btnReturnToZen) {
      btnReturnToZen.addEventListener('click', () => {
        sound.init();
        isZenMode = true;
        document.body.classList.add('zen-mode');
        showToast('⛩️ Welcome back to Zen Sanctuary');
        sound.playTibetanBowl(432);
        resizeCanvas();
      });
    }

    const btnZenTheme = document.getElementById('btnZenTheme');
    const zenThemeIcon = document.getElementById('zenThemeIcon');
    const zenThemeText = document.getElementById('zenThemeText');
    if (btnZenTheme) {
      btnZenTheme.addEventListener('click', () => {
        sound.init();
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const nextTheme = currentTheme === 'washi' ? 'dark' : 'washi';
        applyClinicalTheme(nextTheme);
        if (zenThemeIcon) zenThemeIcon.textContent = nextTheme === 'washi' ? '🌌' : '🍵';
        if (zenThemeText) zenThemeText.textContent = nextTheme === 'washi' ? 'Dark' : 'Washi';
      });
    }

    const btnZenAudio = document.getElementById('btnZenAudio');
    const zenAudioIcon = document.getElementById('zenAudioIcon');
    if (btnZenAudio) {
      btnZenAudio.addEventListener('click', () => {
        sound.init();
        sound.enabled = !sound.enabled;
        if (zenAudioIcon) zenAudioIcon.textContent = sound.enabled ? '🔊' : '🔇';
        if (sound.enabled) sound.playTibetanBowl(432);
        showToast(sound.enabled ? '🔊 Sound: Resonating' : '🔇 Sound: Muted');
      });
    }

    const btnZenOpenDrawer = document.getElementById('btnZenOpenDrawer');
    if (btnZenOpenDrawer && panelBoards) {
      btnZenOpenDrawer.addEventListener('click', () => {
        sound.init();
        panelBoards.classList.toggle('drawer-open');
      });
    }

    document.getElementById('btnResetBoard').addEventListener('click', () => {
      setBoard(currentBoardKey);
    });

    // ─── NON-VISUAL AUDITORY & HAPTIC ACCESSIBILITY KEYBOARD CONTROLS ───
    const QUICK_BOARDS = ['zero', 'eight', 's', 'a', 'braille', 'xin', 'om', 'an', 'shanti'];

    window.addEventListener('keydown', (e) => {
      // Ignore keystrokes when user is typing in form inputs or contenteditables
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) {
        return;
      }

      sound.init();

      if (e.key === 'Escape') {
        if (mdcpModal && mdcpModal.style.display !== 'none') {
          e.preventDefault();
          closeMdcpModal();
          return;
        }
      }

      // 'S' or 's' hotkey: Toggle Acoustic Sonar Mode
      if ((e.key === 's' || e.key === 'S') && !e.ctrlKey && !e.altKey && !e.metaKey) {
        if (btnSonarMode) {
          e.preventDefault();
          btnSonarMode.click();
          return;
        }
      }

      // 'R' or 'r' hotkey: Reset Board
      if ((e.key === 'r' || e.key === 'R') && !e.ctrlKey && !e.altKey && !e.metaKey) {
        e.preventDefault();
        setBoard(currentBoardKey);
        announceSR('Board reset to starting position.');
        return;
      }

      // Number keys 1-9: Quick Jump to Canonical Boards
      if (/^[1-9]$/.test(e.key) && !e.ctrlKey && !e.altKey && !e.metaKey) {
        const idx = parseInt(e.key, 10) - 1;
        if (idx < QUICK_BOARDS.length) {
          e.preventDefault();
          const targetKey = QUICK_BOARDS[idx];
          setBoard(targetKey);
          document.querySelectorAll('.board-card').forEach(c => c.classList.toggle('active', c.dataset.board === targetKey));
          return;
        }
      }

      const board = BOARDS[currentBoardKey];
      if (!board) return;
      const s = currentLetterScale || 0.6;

      // 'B' or 'b' hotkey: Acoustic Landmark Beacon Ping
      if ((e.key === 'b' || e.key === 'B') && !e.ctrlKey && !e.altKey && !e.metaKey) {
        e.preventDefault();
        // Find nearest uncollected target
        let nearestTarget = null;
        let minTargetDist = Infinity;

        board.targets.forEach(t => {
          if (!t.collected) {
            const tx = t.x * s;
            const ty = t.y * s;
            const dist = Math.hypot(token.x - tx, token.y - ty);
            if (dist < minTargetDist) {
              minTargetDist = dist;
              nearestTarget = t;
            }
          }
        });

        if (!nearestTarget) {
          announceSR('All targets on this board have been reached! Press R to reset or press 1 through 9 for another board.');
          showToast('🌟 All targets reached on this board! Great work.');
          sound.playChime(1.5);
          triggerHaptic('complete');
          return;
        }

        const dx = (nearestTarget.x * s) - token.x;
        const dy = (nearestTarget.y * s) - token.y;
        const panVal = Math.max(-1, Math.min(1, dx / (width * 0.35)));

        // Intuitive Spatial Orientation (Natural Compass)
        const angleDeg = (Math.atan2(dx, -dy) * (180 / Math.PI) + 360) % 360;
        let spatialDir = 'directly ahead';
        if (angleDeg >= 337.5 || angleDeg < 22.5) spatialDir = 'directly above';
        else if (angleDeg >= 22.5 && angleDeg < 67.5) spatialDir = 'to the upper right';
        else if (angleDeg >= 67.5 && angleDeg < 112.5) spatialDir = 'to the right';
        else if (angleDeg >= 112.5 && angleDeg < 157.5) spatialDir = 'to the lower right';
        else if (angleDeg >= 157.5 && angleDeg < 202.5) spatialDir = 'directly below';
        else if (angleDeg >= 202.5 && angleDeg < 247.5) spatialDir = 'to the lower left';
        else if (angleDeg >= 247.5 && angleDeg < 292.5) spatialDir = 'to the left';
        else if (angleDeg >= 292.5 && angleDeg < 337.5) spatialDir = 'to the upper left';

        sound.playBeaconPing(panVal, minTargetDist / 400);
        triggerHaptic('pulse');

        const distStr = Math.round(minTargetDist);
        announceSR(`Beacon: Target ${nearestTarget.label} is ${spatialDir}, distance ${distStr} pixels.`);
        showToast(`🧭 Beacon: ${nearestTarget.label} (${spatialDir}, ${distStr}px)`);
        return;
      }

      // Arrow Key Movement
      const step = e.shiftKey ? 36 : 18;
      let moved = false;

      if (e.key === 'ArrowUp') {
        token.targetY -= step;
        moved = true;
      } else if (e.key === 'ArrowDown') {
        token.targetY += step;
        moved = true;
      } else if (e.key === 'ArrowLeft') {
        token.targetX -= step;
        moved = true;
      } else if (e.key === 'ArrowRight') {
        token.targetX += step;
        moved = true;
      }

      if (moved) {
        e.preventDefault();
        isKeyboardActive = true;

        // Clamp to stage bounds
        const maxBoundX = width * 0.46;
        const maxBoundY = height * 0.46;
        token.targetX = Math.max(-maxBoundX, Math.min(maxBoundX, token.targetX));
        token.targetY = Math.max(-maxBoundY, Math.min(maxBoundY, token.targetY));

        triggerHaptic('groove');

        // Check if pearl stepped into any uncollected target
        board.targets.forEach((t, idx) => {
          if (!t.collected) {
            const tx = t.x * s;
            const ty = t.y * s;
            const d = Math.hypot(token.targetX - tx, token.targetY - ty);
            if (d < 30) {
              t.collected = true;
              token.targetX = tx;
              token.targetY = ty;

              // Braille Solfeggio Scale or standard chime
              if (currentBoardKey === 'braille') {
                const solfeggioPitches = [528, 639, 741, 852, 963, 417, 396, 285];
                sound.playChimeAtFreq(solfeggioPitches[idx % solfeggioPitches.length]);
              } else {
                sound.playChime(1.0 + (idx * 0.12));
              }

              triggerHaptic('detent');
              const remaining = board.targets.filter(x => !x.collected).length;
              if (remaining === 0) {
                triggerHaptic('complete');
                announceSR(`Harmonic completion! Reached final target: ${t.label}. All targets collected.`);
                showToast(`🌟 Sacred Path Completed! All Targets Reached`);
              } else {
                announceSR(`Reached ${t.label}! ${remaining} targets remaining.`);
                showToast(`✨ Target Reached: ${t.label}`);
              }
            }
          }
        });
      }
    });

    /* ─── MDCP CLINICAL & TELEMETRY SUITE CONTROLLER ─── */
    const mdcpModal = document.getElementById('mdcpModal');
    const btnZenMdcp = document.getElementById('btnZenMdcp');
    const btnToggleMdcp = document.getElementById('btnToggleMdcp');
    const btnCloseMdcpModal = document.getElementById('btnCloseMdcpModal');
    const mdcpTabBtns = document.querySelectorAll('.mdcp-tab-btn');
    const mdcpTabPanels = document.querySelectorAll('.mdcp-tab-panel');
    const btnToggleJitterDemo = document.getElementById('btnToggleJitterDemo');
    const jitterDemoBox = document.getElementById('jitterDemoBox');
    const ecgCanvas = document.getElementById('ecgCanvas');
    const vitalHrVal = document.getElementById('vitalHrVal');
    const vitalSpo2Val = document.getElementById('vitalSpo2Val');
    const vitalBpVal = document.getElementById('vitalBpVal');
    const vitalEtco2Val = document.getElementById('vitalEtco2Val');
    let ecgAnimId = null;
    let isJitterActive = false;
    let jitterInterval = null;

    function openMdcpModal(initialTab = 'telemetry') {
      if (!mdcpModal) return;
      mdcpModal.style.display = 'flex';
      switchMdcpTab(initialTab);
      startEcgWave();
      announceSR('Opened MDCP Clinical and Telemetry Suite modal');
    }

    function closeMdcpModal() {
      if (!mdcpModal) return;
      mdcpModal.style.display = 'none';
      stopEcgWave();
      if (jitterInterval) {
        clearInterval(jitterInterval);
        jitterInterval = null;
      }
      isJitterActive = false;
      if (btnToggleJitterDemo && jitterDemoBox) {
        btnToggleJitterDemo.textContent = '⚡ Compare: Standard Jitter';
        jitterDemoBox.style.fontFamily = 'var(--font-mono)';
        jitterDemoBox.textContent = '120 / 80 mmHg • 72 BPM • 98% SpO2';
      }
      announceSR('Closed MDCP Clinical Suite modal');
    }

    function switchMdcpTab(tabName) {
      mdcpTabBtns.forEach(btn => {
        const isActive = (btn.dataset.mdcpTab === tabName);
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });
      mdcpTabPanels.forEach(panel => {
        const targetId = `panelMdcp${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`;
        panel.style.display = (panel.id === targetId) ? 'flex' : 'none';
      });
    }

    if (btnZenMdcp) btnZenMdcp.addEventListener('click', () => openMdcpModal('telemetry'));
    if (btnToggleMdcp) btnToggleMdcp.addEventListener('click', () => openMdcpModal('telemetry'));
    if (btnCloseMdcpModal) btnCloseMdcpModal.addEventListener('click', closeMdcpModal);

    if (mdcpModal) {
      mdcpModal.addEventListener('click', (e) => {
        if (e.target === mdcpModal) closeMdcpModal();
      });
    }

    mdcpTabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.dataset.mdcpTab;
        switchMdcpTab(tab);
        if (tab === 'telemetry') startEcgWave();
      });
    });

    // Tabular Jitter vs PocketGull Mono Invariant Demo
    if (btnToggleJitterDemo && jitterDemoBox) {
      btnToggleJitterDemo.addEventListener('click', () => {
        isJitterActive = !isJitterActive;
        if (isJitterActive) {
          btnToggleJitterDemo.textContent = '✓ PocketGull Fixed Pitch Active';
          jitterDemoBox.style.fontFamily = 'system-ui, -apple-system, sans-serif';
          let step = 0;
          const jitterValues = [
            '120 / 80 mmHg • 72 BPM • 98% SpO2',
            '111 / 71 mmHg • 71 BPM • 97% SpO2',
            '128 / 84 mmHg • 74 BPM • 99% SpO2',
            '119 / 79 mmHg • 73 BPM • 98% SpO2'
          ];
          jitterInterval = setInterval(() => {
            step = (step + 1) % jitterValues.length;
            jitterDemoBox.textContent = jitterValues[step];
          }, 450);
          showToast('⚠️ Standard font tabular jitter demonstrated (digits shifting)');
        } else {
          clearInterval(jitterInterval);
          jitterInterval = null;
          btnToggleJitterDemo.textContent = '⚡ Compare: Standard Jitter';
          jitterDemoBox.style.fontFamily = 'var(--font-mono)';
          jitterDemoBox.textContent = '120 / 80 mmHg • 72 BPM • 98% SpO2';
          showToast('✓ PocketGull Mono 600 UPM fixed pitch locked (zero jitter)');
        }
      });
    }

    // Real-Time Animated ECG Oscilloscope Waveform & Vitals Sync
    function startEcgWave() {
      if (!ecgCanvas || ecgAnimId) return;
      const ctxEcg = ecgCanvas.getContext('2d');
      let t = 0;
      let lastVitalsUpdate = 0;
      const width = ecgCanvas.width;
      const height = ecgCanvas.height;
      const midY = height / 2;
      const points = [];

      function getEcgY(phase) {
        const p = phase % 1.0;
        if (p < 0.15) return 0;
        if (p < 0.25) return -Math.sin((p - 0.15) / 0.1 * Math.PI) * 7;  // P wave
        if (p < 0.32) return 0;
        if (p < 0.36) return Math.sin((p - 0.32) / 0.04 * Math.PI) * 5;   // Q dip
        if (p < 0.44) return -Math.sin((p - 0.36) / 0.08 * Math.PI) * 38; // R spike
        if (p < 0.49) return Math.sin((p - 0.44) / 0.05 * Math.PI) * 11;  // S dip
        if (p < 0.60) return 0;
        if (p < 0.78) return -Math.sin((p - 0.60) / 0.18 * Math.PI) * 12; // T wave
        return 0;
      }

      function drawEcg() {
        if (!mdcpModal || mdcpModal.style.display === 'none') {
          stopEcgWave();
          return;
        }

        ctxEcg.fillStyle = 'rgba(3, 10, 19, 0.22)';
        ctxEcg.fillRect(0, 0, width, height);

        // Oscilloscope phosphor grid lines
        ctxEcg.strokeStyle = 'rgba(16, 185, 129, 0.08)';
        ctxEcg.lineWidth = 1;
        ctxEcg.beginPath();
        for (let x = 0; x < width; x += 40) {
          ctxEcg.moveTo(x, 0); ctxEcg.lineTo(x, height);
        }
        for (let y = 0; y < height; y += 20) {
          ctxEcg.moveTo(0, y); ctxEcg.lineTo(width, y);
        }
        ctxEcg.stroke();

        // Wave trace
        t += 0.018;
        const currentY = midY + getEcgY(t);
        points.push(currentY);
        if (points.length > width) points.shift();

        ctxEcg.strokeStyle = '#10b981';
        ctxEcg.shadowColor = '#34d399';
        ctxEcg.shadowBlur = 8;
        ctxEcg.lineWidth = 2.2;
        ctxEcg.beginPath();
        for (let i = 0; i < points.length; i++) {
          if (i === 0) ctxEcg.moveTo(i, points[i]);
          else ctxEcg.lineTo(i, points[i]);
        }
        ctxEcg.stroke();
        ctxEcg.shadowBlur = 0;

        // Current sweep head
        if (points.length > 0) {
          ctxEcg.fillStyle = '#ffffff';
          ctxEcg.beginPath();
          ctxEcg.arc(points.length - 1, points[points.length - 1], 3.5, 0, Math.PI * 2);
          ctxEcg.fill();
        }

        // Slight live physiological variance
        const now = Date.now();
        if (now - lastVitalsUpdate > 1800) {
          lastVitalsUpdate = now;
          if (vitalHrVal) vitalHrVal.textContent = (71 + Math.floor(Math.sin(now * 0.001) * 3));
          if (vitalSpo2Val) vitalSpo2Val.textContent = (98 + Math.floor(Math.random() * 2));
        }

        ecgAnimId = requestAnimationFrame(drawEcg);
      }

      drawEcg();
    }

    function stopEcgWave() {
      if (ecgAnimId) {
        cancelAnimationFrame(ecgAnimId);
        ecgAnimId = null;
      }
    }

    // Start
    setBoard('zero');
    requestAnimationFrame(render);
  
