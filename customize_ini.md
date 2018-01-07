HOW   TO   CUSTOMIZE   .INI   FILES PARAMETERS
==============================================

Required Parameters
-------------------

List of params:
 - complexity:   determines the complexity of the chord progressions (`super_simple`, `simple`, `semi_complex`
 - section: this will always be labeled as consecutive id and should not be changed (i.e. section: id:   0).
 - tse:  time signature   (i.e.   `tse:   ‘4/4’`).
 - bpm: tempo in  beats   per   minute   (i.e.   `bpm:100`)
 - energy:  the number of layers in a range playing during a section (`low`, `medium`, `high`). Each of these categories   represents   a   range   of   layers   that   can   be   playing.   For   instance, 'low'   can   be   1   -   4   layers   while   'high'   can   be   3   -   12   layers.
  - duration:  min   and   max   number   of   seconds   a   section   can   be   (i.e.   'duration:   10   to   20 seconds').
  - durationInMeasures: number of measures a section can be. Can be one or two options to choose between (i.e.   `durationInMeasures:   '4'`,   `durationInMeasures:   '2   or   4'`).
  - slope: the rate of change in the density level of a section (`stay`, `gradual`, `steep`). 
  - direction:   determines   whether   layers   will   be   added   or   removed   during   a   section   (`up`   - adds   layers,   `down`   -   removes   layers).

Optional  Parameters
--------------------

List of params:
  - similarTo:  this   allows   the   user   to   repeat   previous   sections   specified   by   the   section   id (i.e.   `similarTo:0`).
  - mustHaveLayer: midi layers specified by the user that will be included in a given section (i.e. `mustHaveLayer1:   'bass1'`).   Multiple   layers   can   be   included   by   enumerating each   paramater   (i.e.   `mustHaveLayer1:   'bass1',   mustHaveLayer2:   'bass2'`).
  - mustNotHaveLayer: midi layers specified by the user that will be excluded in a given section (i.e. `mustNotHaveLayer1:   'bass1'`).   Multiple layers can be excluded by enumerating each paramater (i.e. `mustNotHaveLayer1:   'bass1',   mustNotHaveLayer2: 'bass2'`).

[Refer to the provided .ini files](./src/Ini)   for   further   examples   of   how   to   implement   parameters.

MIDI   LAYER   NAMES
--------------------

Instruments:
  - bass1 (simple bass with root motion)
  - bass2 (slightly more complex, adds some rhythmic variation and the fifth)
  - bass3 (more complex rhythmically and harmonically)
  - loStrings (includes cellos and basses, sustained notes, follows root, low register)
  - midStrings (includes viola, sustained notes, chord tone, mid register)
  - hiStrings (includes violin 1 and violin 2, sustained notes, chord tone, high register)
  - arpStrings (sustained notes, scale tones, meant to be used with arpeggiators)
  - leftPianoBass (root notes + octave above)
  - rightPiano (chords with different voicings, rhythm follows chord progression rhythm)
  - rightPiano2 (chords with different voicings, rhythm follows chord progression rhythm)
  - piano1 (arpeggiated piano texture)
  - brassRhythms (chords with different voicings, rhythm linked to bass 3)
  - rhythmChords (chords with different voicings, varied rhythm)
  - mel5 (melody / lead)
  - drumsKit (drums - includes kick, snare, hi-hat)
  - fillsForDrums (drum fills - includes kick, snare, hi-hat, toms, crash)
  - drumsLatinPop (Latin percussion, syncopated rhythms)
  - drumsBass (bass drum, slower rhythms)
  - notationLP (root notes, meant for exporting to notation and not playback)
  - notationRP (chords, meant for exporting to notation and not playback)
  
