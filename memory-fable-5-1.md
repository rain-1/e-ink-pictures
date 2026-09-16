# Memory (Claude Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(This file was `memory.md` on day one; the routine now asks for `memory-fable-5-1.md`,
so I renamed it on day two and kept the history.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  Day one landed on `main`. Day two was pushed to the session branch the harness assigned
  (`claude/exciting-goldberg-hae5ua`) because I was told not to push elsewhere; if the
  screen reads `main`, Edward has to merge. Check `git log main` next time to see whether
  the day-two commit was merged and which branch the routine hands me.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made
    them. Each generate.py is self-contained; run `python3 generate.py outdir` to reproduce.
- Environment: fresh container each run. `pip install pillow numpy` first (not preinstalled).
  Fonts: DejaVu (sans/serif/mono, bold variants), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (IPAGothic — kanji + kana work).
  `WebSearch` works; `WebFetch` is blocked for many sites (theskylive, timeanddate).
  Don't rely on fetching an almanac page — compute the sky instead (see ephemeris below).

## Craft notes (what I've learned about making things for this panel)

- Two rendering modes, both at 3× (1200×900) then LANCZOS downscale:
  - **hard-edge**: quantize with `Dither.NONE` — crisp curves, poster look.
  - **tonal**: Floyd–Steinberg dither — grain, gradients, sky, sea.
- **Text on tonal pieces must not go through the dither** or it speckles into mush.
  Day-two fix: draw all text onto separate 3× "ink" masks, downscale, threshold at ~96/255,
  then stamp the palette index onto the already-dithered image (`Ink` class in
  `archive/2026-09-16/generate.py`). Use bold faces for anything under ~9 px; regular
  weights at 7 px are unreadable after thresholding.
- Rotated text: render on an RGBA layer, `rotate(expand=True)`, paste with alpha. Check the
  pasted box stays inside 400×300 — I ran text off the canvas once.
- Red reads *bright* on these panels. It carries enormous weight; one red element per
  composition is usually enough. Red on black works for a filled shape but not for thin text.
- Real moon phases: I embedded a truncated Meeus Sun/Moon ephemeris (`jd_utc`, `sun_lon`,
  `moon_lon_lat`, `illum`) in the day-two generator. It matched published illumination to
  within a percent. Reuse it rather than the uniform-age cosine model, which was 10 points off.
- **My mark**: a 6 px red square, 6 px in from the bottom-right corner, on every image.
  Keep it. It's the one thing that says all of these came from the same hand.

## Style, as it's forming

I seem to like: one big idea per image, no clutter; a strong single shape (wedge, crescent,
globe, sun) plus a strip of small factual data (a moon row, a date line) in bold mono; a mix
of hard-edge poster pieces and one or two dithered "woodcut" scenes per day; Japanese
crest-and-textile geometry; sky facts as the thread that makes each day *today*. The
"almanac object" idea is the spine: the screen should be able to tell you something true
about the day, beautifully.

## Standing interests

- Sky almanac data — moon phases, conjunctions, meteor showers, planets at their best.
- Japanese pattern mathematics — hitomezashi (done day 1), kamon (done day 2), still to
  mine: kumiko lattices, seigaiha as a full field, asanoha, shippō, yagasuri arrows.
- Constructivism / Lissitzky / Rodchenko — did one on day 2. Could revisit as a *series*
  (each with a different geometric "argument"), but not two days in a row.
- Folk cut-paper: papel picado (done day 2), Chinese jianzhi, Polish wycinanki (symmetrical,
  layered, often red!), Scherenschnitte. All are natively 2–3 color.
- Calendars, festivals, "on this day" — gives each set a reason to exist today.

## Upcoming sky & calendar hooks

- **Sep 18** — Venus greatest brilliancy, mag −4.8, low west after sunset (evening star)
- **Sep 22** — Equinox 00:05 UTC
- **Sep 25** — Tsukimi / Chūshū no meigetsu (Mid-Autumn moon viewing; rabbit on the moon,
  susuki grass, dango pyramid) — perfect kamon/ukiyo-e material
- **Sep 25–26** — Neptune at opposition
- **Sep 26** — Full Harvest Moon, rises near Saturn
- **Oct 8** — Draconids (evening shower); **Oct 21** — Orionids
- **Oct 26** — Hunter's Moon (Oct full moon)
- **Nov 1–2** — Día de Muertos (papel picado with calaveras — a natural sequel to day 2)
- **Nov 17** — Leonids; **Dec 13–14** — Geminids

## Ideas backlog (unmade)

- Truchet tiles (Smith quarter-circle variant), multi-scale; fill regions in 2 colors with one
  red path traced through the maze
- Wang tiles / maze from a cellular automaton; Conway's Life long-exposure trails; sandpile
- Great Wave / sumi-e sea as the *whole* image (day 2's sea was a background — make it the subject)
- Word of the day: one word huge, etymology tiny (try a Japanese word with kanji + gloss)
- Moon-phase dashboard for notable moon days (Sep 25/26 is the next one)
- Wycinanki rooster / tree-of-life in red-black-white layered cut paper
- Ozone Day (Sep 16) — a stratosphere cross-section infographic; didn't fit this year
- Analemma / sun-path diagram for the equinox week; day-length curve for the year with today marked
- Hokusai "36 views" homage series: same red Fuji-like mountain, different foregrounds, over several days
- Kumiko lattice sampler (asanoha, kikkō, goma) — like the kamon sheet but for lattices
- Anniversary posters template: bold date, one fact, one shape

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped the repo conventions. Made: Amanogawa night scene; hitomezashi stitch
pattern; last-quarter moon almanac card; Summer Triangle star chart; generative ridgelines.
Lesson: first runs are mostly plumbing.

### 2026-09-16 — day 2. (Two-month gap since day 1 — the routine didn't run in between.)
Mexican Independence Day (Grito de Dolores 1810); Mayflower left Plymouth 1620; waxing
crescent 28%; Venus peaking; equinox in 6 days. Made:
1. **Papel picado** — three strings of cut-tissue pennants on black, ¡VIVA·MÉXICO! letters
   cut through the middle row; folded-paper lace, doves, flowers, stars; two reds per row.
2. **Red wedge** — Lissitzky homage as a calendar poster: red wedge into a white circle on
   a black diagonal field, "SEPTEMBER 16 / day 259 of 365 / 6 DAYS TO EQUINOX".
3. **Kamon** — six procedurally drawn crests (tsuki, nami, kikyō, mitsuboshi, hishi, igeta),
   moon crest in red; kanji + romaji labels.
4. **Equinox** — dithered terminator globe with red equator, serif text, and a real
   moon-phase strip for Sep 16–30 (today and the Harvest Moon ringed in red).
5. **Mayflower** — woodcut ship silhouette with hatched sails on nine layered wave bands,
   Hokusai foam claws, big red sun behind streak clouds.
Lessons: the Ink text layer (above) was the big technical win; the ephemeris was the big
accuracy win. Doves in cut-paper read only just — silhouettes need a clearer gesture.
Kamon sheet is my favourite; the Mayflower sails are stiff, boxes stacked — next ship,
draw the curves from a single spline. Next time: Tsukimi/Harvest Moon is on the 25th–26th;
don't repeat a globe or a crest sheet; try Truchet or the word-of-the-day.
