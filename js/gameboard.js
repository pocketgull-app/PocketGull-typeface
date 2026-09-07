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
      }

      init() {
        if (this.ctx) return;
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
    }

    const sound = new SanctuaryAudio();

    /* ========================================================================== */
    /* LETTERFORM GAMEBOARD GEOMETRIES & TOPOLOGIES                               */
    /* ========================================================================== */
    const BOARDS = {
      zero: {
        id: 'zero',
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
        name: 'Figure Eight / Dual Counter (8)',
        moralTitle: 'The Infinity of Reciprocal Renewal',
        moralDesc: 'Breath, circulation, and compassion form an unbroken figure eight. Giving and receiving flow through the same central heart.',
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
        name: 'Inuktitut Syllabic "I" (ᐃ)',
        moralTitle: 'Inuit Qaujimajatuqangit (IQ) Environmental Harmony',
        moralDesc: 'The upward triangular syllabic evokes the shelter of the igloo and the quiet mountain ridge, reminding us that we are guests on this sacred earth.',
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
        name: 'Chinuk Pipa WA (𑲒)',
        moralTitle: 'River Stone Gentle Flow (Kamloops Wawa)',
        moralDesc: 'Soft curves carved by cascading glacial meltwater. Gentleness outlasts violence; soft water shapes the hardest stone.',
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
        name: 'Sloan S-Curve Saccade (S)',
        moralTitle: 'Saccadic Decompression & Flexibility',
        moralDesc: 'Rigidity snaps in high winds, while the supple willow bends and flourishes. Relax your focus across the gentle double arc.',
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
        name: 'Pinnacle Temple (A)',
        moralTitle: 'The Bridge of Reciprocity',
        moralDesc: 'Twin pillars rising toward a single aspiration, joined at the center by a bridge of trust. We lift each other as we climb.',
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
        name: 'TCM Xin (Heart & Shen) • 心',
        moralTitle: 'Nourishing the Shen (Spirit)',
        moralDesc: 'In Chinese Medicine, the Heart (心) houses Shen—the spirit, consciousness, and emotional peace. Tracing the 4 points releases chest tension and stills restless racing thoughts.',
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
        name: 'Vedic Pranava OM • ॐ',
        moralTitle: 'Pranic Grounding & Ojas Preservation',
        moralDesc: 'The primordial sound of wholeness in Ayurvedic medicine. The three curves represent waking, dreaming, and deep stillness. Tracing the loop pacifies hyperactive Vata air and rebuilds Ojas.',
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
        name: 'Ān (Refuge & Safety) • 安',
        moralTitle: 'Sanctuary Under a Protective Roof',
        moralDesc: 'Formed by a protective sheltering roof over a calm centered figure. An ancient ideograph signifying that trauma cannot penetrate once the boundaries of personal sanctuary are sealed.',
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

    let isDragging = false;
    let secondsCalm = 0;
    setInterval(() => {
      secondsCalm++;
      const mins = String(Math.floor(secondsCalm / 60)).padStart(2, '0');
      const secs = String(secondsCalm % 60).padStart(2, '0');
      timerDisplay.textContent = `${mins}:${secs}`;
    }, 1000);

    function resizeCanvas() {
      const rect = stageWrap.getBoundingClientRect();
      width = canvas.width = rect.width;
      height = canvas.height = rect.height;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function setBoard(boardKey) {
      currentBoardKey = boardKey;
      const board = BOARDS[boardKey];
      if (!board) return;

      // Update HUD
      boardTitleBanner.innerHTML = `📜 Active Board: <strong>${board.name}</strong>`;
      boardMoralTitle.textContent = board.moralTitle;
      boardMoralDesc.textContent = board.moralDesc;

      // Reset targets
      board.targets.forEach(t => t.collected = false);

      // Reset Token to first target
      token.x = token.targetX = board.targets[0].x;
      token.y = token.targetY = board.targets[0].y;
      token.trail = [];

      // Trigger Harmonic Chime
      sound.playChime(1.0);
      showToast(`✨ Welcome to ${board.name} • Breathe Deeply`);
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

    // Canvas Pointer Hover Tracking for Touch Aura
    canvas.addEventListener('pointermove', (e) => {
      const rect = canvas.getBoundingClientRect();
      pointerCanvasX = e.clientX - rect.left - width / 2;
      pointerCanvasY = e.clientY - rect.top - height / 2;
      pointerRadius = 180; // 180px aura proximity radius
    });

    canvas.addEventListener('pointerleave', () => {
      pointerRadius = 0;
    });


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

    // Enhanced Tremor-Dampened Pointer Handler
    function handleRehabPointer(clientX, clientY) {
      const rect = canvas.getBoundingClientRect();
      const rawX = clientX - rect.left - width / 2;
      const rawY = clientY - rect.top - height / 2;

      // Exponential Moving Average (EMA) Low-Pass Filter
      const alpha = REHAB_PRESETS[currentRehabMode] ? REHAB_PRESETS[currentRehabMode].smoothingAlpha : 0.15;
      smoothedPointerX = (alpha * rawX) + ((1 - alpha) * smoothedPointerX);
      smoothedPointerY = (alpha * rawY) + ((1 - alpha) * smoothedPointerY);

      // Magnetic Soft-Spring Snap to nearest glyph path
      const board = BOARDS[currentBoardKey];
      let nearestDist = Infinity;
      let snapX = smoothedPointerX;
      let snapY = smoothedPointerY;

      // Check targets for gravitational assist
      board.targets.forEach(t => {
        const d = Math.hypot(smoothedPointerX - t.x, smoothedPointerY - t.y);
        if (d < nearestDist && d < 120) {
          nearestDist = d;
          // Soft-spring interpolation toward target
          const pull = 0.35 * (1 - d / 120);
          snapX = smoothedPointerX + (t.x - smoothedPointerX) * pull;
          snapY = smoothedPointerY + (t.y - smoothedPointerY) * pull;
        }
      });

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

    window.addEventListener('pointerdown', (e) => {
      sound.init();
      isDragging = true;
      handleRehabPointer(e.clientX, e.clientY);
    });

    window.addEventListener('pointermove', (e) => {
      if (isDragging) {
        handleRehabPointer(e.clientX, e.clientY);
      }
    });

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

      const cx = width / 2;
      const cy = height / 2;
      const board = BOARDS[currentBoardKey];

      ctx.save();
      ctx.translate(cx, cy);

      // 1. Draw Ambient Wisps (Pacing Particles)
      wisps.forEach(w => {
        w.x += w.vx;
        w.y += w.vy;
        w.phase += 0.02;
        if (Math.abs(w.x) > 300) w.vx *= -1;
        if (Math.abs(w.y) > 300) w.vy *= -1;

        ctx.fillStyle = `rgba(56, 189, 248, ${w.alpha * (0.5 + Math.sin(w.phase) * 0.3)})`;
        ctx.beginPath();
        ctx.arc(w.x, w.y, w.radius, 0, Math.PI * 2);
        ctx.fill();
      });

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

      // 2. Draw Letterform Stroke Tracks (The Gameboard)
      // Variable Font Stroke Weight Bloom via Touch Aura
      const baseOuterWidth = 42 + (auraProximityFactor * 24); // 42px -> 66px
      const baseInnerWidth = 14 + (auraProximityFactor * 8);   // 14px -> 22px
      ctx.save();
      ctx.lineWidth = baseOuterWidth;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      // Outer Stroke Glow (shifts rose when Touch Aura is strong)
      ctx.strokeStyle = auraProximityFactor > 0.4 ? 'rgba(251, 113, 133, 0.22)' : 'rgba(20, 184, 166, 0.12)';
      ctx.shadowColor = auraProximityFactor > 0.4 ? '#fb7185' : '#14b8a6';
      ctx.shadowBlur = 25 + (auraProximityFactor * 15);
      drawBoardPaths(board.paths);
      ctx.stroke();

      // Inner Tactile Groove
      ctx.lineWidth = 14;
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.55)';
      ctx.shadowBlur = 10;
      drawBoardPaths(board.paths);
      ctx.stroke();

      // Centerline Navigation Vector
      ctx.lineWidth = 2;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.85)';
      ctx.shadowBlur = 0;
      drawBoardPaths(board.paths);
      ctx.stroke();
      ctx.restore();

      // 3. Draw Target Nodes / Sanctuaries
      board.targets.forEach((target, idx) => {
        const distToToken = Math.hypot(token.x - target.x, token.y - target.y);
        
        // Collect Target
        if (distToToken < 35 && !target.collected) {
          target.collected = true;
          sound.playChime(1.0 + idx * 0.2);
          showToast(`🌸 Reached ${target.label} • Peace Anchored`);

          // Check if all collected
          if (board.targets.every(t => t.collected)) {
            setTimeout(() => {
              showToast(`🌟 Sanctuary Complete: ${board.name} • Harmony Achieved`);
              board.targets.forEach(t => t.collected = false);
            }, 600);
          }
        }

        ctx.save();
        ctx.beginPath();
        ctx.arc(target.x, target.y, target.collected ? 12 : 18, 0, Math.PI * 2);
        ctx.fillStyle = target.collected ? '#10b981' : 'rgba(245, 158, 11, 0.3)';
        ctx.strokeStyle = target.collected ? '#34d399' : '#f59e0b';
        ctx.lineWidth = 3;
        ctx.shadowColor = target.collected ? '#10b981' : '#f59e0b';
        ctx.shadowBlur = 15;
        ctx.fill();
        ctx.stroke();

        // Target Label
        ctx.font = '10px "PocketGull Mono", monospace';
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.fillText(target.label, target.x, target.y + 32);
        ctx.restore();
      });

      // 4. Update & Draw Token (Light Pearl)
      if (isAutoFlow) {
        autoFlowAngle += 0.015;
        // Orbit through board targets gracefully
        const tLen = board.targets.length;
        if (tLen > 0) {
          const tIdx = Math.floor((autoFlowAngle / (Math.PI * 2) * tLen)) % tLen;
          const nextIdx = (tIdx + 1) % tLen;
          const subProg = (autoFlowAngle / (Math.PI * 2) * tLen) % 1;
          const currT = board.targets[tIdx];
          const nextT = board.targets[nextIdx];

          token.targetX = currT.x + (nextT.x - currT.x) * subProg;
          token.targetY = currT.y + (nextT.y - currT.y) * subProg;
        }
      }
      // Smooth dampening towards target
      token.vx = (token.targetX - token.x) * 0.08;
      token.vy = (token.targetY - token.y) * 0.08;
      token.x += token.vx;
      token.y += token.vy;

      // Add to motion trail
      token.trail.push({ x: token.x, y: token.y, alpha: 1.0 });
      if (token.trail.length > 20) token.trail.shift();

      // Draw Motion Trail
      if (token.trail.length > 1) {
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(token.trail[0].x, token.trail[0].y);
        for (let i = 1; i < token.trail.length; i++) {
          ctx.lineTo(token.trail[i].x, token.trail[i].y);
        }
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
        ctx.lineWidth = 10;
        ctx.lineCap = 'round';
        ctx.stroke();
        ctx.restore();
      }

      // Draw Glowing Light Pearl
      ctx.save();
      ctx.shadowColor = '#38bdf8';
      ctx.shadowBlur = 30;

      // Outer Aura
      ctx.beginPath();
      ctx.arc(token.x, token.y, token.radius * 1.5, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(56, 189, 248, 0.25)';
      ctx.fill();

      // Core Pearl
      ctx.beginPath();
      ctx.arc(token.x, token.y, token.radius, 0, Math.PI * 2);
      const pearlGrad = ctx.createRadialGradient(token.x - 4, token.y - 4, 2, token.x, token.y, token.radius);
      pearlGrad.addColorStop(0, '#ffffff');
      pearlGrad.addColorStop(0.6, '#38bdf8');
      pearlGrad.addColorStop(1, '#0284c7');
      ctx.fillStyle = pearlGrad;
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.restore();

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
        sound.playChime(1.0);
        showToast(`🎶 Resonating at ${freq} Hz • Healing Wave Active`);
      });
    });

    // Audio Toggle
    const btnToggleAudio = document.getElementById('btnToggleAudio');
    btnToggleAudio.addEventListener('click', () => {
      sound.enabled = !sound.enabled;
      btnToggleAudio.textContent = sound.enabled ? '🔊 Audio: ON' : '🔇 Audio: MUTED';
      if (sound.enabled) sound.playChime(1.0);
    });

    // Theme Toggle: 3-State Cycle (Dark -> Washi -> 670nm PBM -> Dark)
    const btnThemeToggle = document.getElementById('btnThemeToggle');
    btnThemeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      let next = 'washi';
      let label = '🎨 Theme: Washi (和紙)';
      
      if (current === 'dark') {
        next = 'washi';
        label = '🎨 Theme: Washi (和紙)';
      } else if (current === 'washi') {
        next = 'pbm';
        label = '🔴 Theme: 670nm PBM Night Shift';
        showToast('🔴 670nm Retinal Photobiomodulation Active • Melatonin-Preserving Deep Red');
      } else {
        next = 'dark';
        label = '🎨 Theme: Dark';
      }

      document.documentElement.setAttribute('data-theme', next);
      btnThemeToggle.textContent = label;
      sound.playRipple();
    });

    // ─── Continuous Gentle Auto-Flow Engine ───
    let isAutoFlow = false;
    let autoFlowAngle = 0;
    const btnToggleAutoFlow = document.getElementById('btnToggleAutoFlow');

    if (btnToggleAutoFlow) {
      btnToggleAutoFlow.addEventListener('click', () => {
        sound.init();
        isAutoFlow = !isAutoFlow;
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


    document.getElementById('btnResetBoard').addEventListener('click', () => {
      setBoard(currentBoardKey);
    });

    // Start
    setBoard('zero');
    requestAnimationFrame(render);
  
