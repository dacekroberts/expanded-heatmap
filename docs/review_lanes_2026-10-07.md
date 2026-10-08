# Review lanes, 2026-10-07: the large review

The lane kit is `docs/review_lane_kit.md`; read it in full. This file is the
run's own plan: who takes what. Every row of `docs/rendered_surfaces.md`
(206 city pages, 4 fixed pages, the Overview, 29 rendered docs, 2 app data
files) is assigned below.

## The batch

Pinned commit: given in Cleanup's message (branch `review-batch-2026-10-07`).
It carries, on master:

- **39 new cities**: Abroad 6 (Gimpo, Siheung, Geneva (Regional),
  Thessaloniki, Gelsenkirchen, Bremen), East-1 12, Kansai-1 7, Regional-1 11.
- **3 renames to "(Regional)"**: Anyang, Mexico City, Copenhagen.
- **The Europe split** (Europe West, Europe East, Benelux, Germany views) and
  **Japan's 13 views** (8 regions, 5 prefecture views), with the label
  competition, every country's top city first, and the nesting rule.
- **Labels drop " (Regional)"** on the macro map; Benelux names "City of
  Brussels" beside "Brussels (Regional)".
- **One pin colour per meaning**: olive food shops (56 maps), violet shops
  and services (6 maps), menus matching legends, eight approved legend
  wordings for the blue licensed slices.
- **Back links**: "← Back to <city or region>" on the four fixed pages
  (`?from=`), the Overview opening on `?region=`, and a "← <region>" button
  beside every map's own Global View button. EVERY map was re-rendered for
  it.

The checks read first (kit section 4): `python scripts/check_all.py` on the
pinned commit. Known failures at the pin, not findings: the master list's
counts (Staging writes them at landing) and `fingerprint.py coverage` for
Kansai-1's seven maps (the owner's key, at landing).

## Every lane

- Worktree `.claude/worktrees/review-lane-N`, detached at the pinned commit;
  ports and folders per the kit's section 2 table.
- **Widths 375, 768 and 1200; light and dark.** The map button row wraps to
  two lines at phone width and the open legend's cap follows it
  (`--hm-actions-clear`): check it at 375 on every map you open.
- **On every map you open**: the pins' colours match the legend; the layer
  menu says what the legend says; the "← <region>" button opens the Overview
  on that region; the line highlight on hover and tap; the attribution.
- Captures with one browser through the heavy-job gate (kit 5). Prose as
  proposals, never edits (kit 6). Report and message Cleanup (kit 7).
- **Deploy-verify, `scope: map-chrome`, on your own city pages** (kit 7b):
  four Streamlit servers, no static ones, every lane on `srcdoc`; load each
  page in an `<iframe>` of the exact size; reload every ten maps.

## Lane 1: Japan (64 city pages)

All 64 Japanese city pages, and on the Overview the 13 Japan views and East
Asia (labels, the nesting rule: a city named in a wider view is named in
every narrower one, caption arithmetic).

Kobe, Osaka, Sapporo, Fukuoka, Kyoto, Tokyo, Yokohama, Hiroshima, Matsuyama,
Toyama, Kumamoto, Fukui, Nagasaki, Utsunomiya, Kitakyushu, Sakai, Hakodate,
Kagoshima, Okayama, Kōchi, Kawasaki, Yokosuka, Himeji, Nishinomiya,
Takamatsu, Toyota, Yokkaichi, Ōtsu, Nara, Hamamatsu, Higashiōsaka, Kurume,
Sasebo, Shimonoseki; new: Higashiyamato, Nishitōkyō, Tama, Higashimurayama,
Ageo (Regional), Sōka, Tokorozawa, Kasukabe, Fuchū (Tokyo), Chōfu,
Tachikawa, Hino, Toyonaka, Hirakata, Suita, Itami, Kakogawa, Amagasaki, Uji,
Maebashi, Fukuyama, Ichinomiya, Tsu, Fukushima, Iwaki, Akita, Ōita, Gifu,
Mito, Morioka.

Focus: the olive "Food shops (no general retail is published)" legend; the
builds' render items (East-1: labels on the short stubs at Higashiyamato's
Haijima, Hino's Dobutsuen, Tachikawa's Chuo and Ome, Higashi-Tokorozawa; the
same colour on Higashimurayama's Tamako and Tokorozawa's Leo Liner; ten pins
with a blank trade name); Uji, Ichinomiya and Mito re-placed at the merge.

## Lane 2: Europe and the Abroad batch (63 city pages)

The European city pages outside the UK and Czechia, the Abroad batch's
non-European pages, and on the Overview the Europe West, Europe East,
Benelux and Germany views (the landing view's European labels too).

Mexico City (Regional), Madrid, Barcelona, Dublin, Milan, Paris, Marseille,
Toulouse, Lille (Regional), Rennes, Oslo, Copenhagen (Regional), Amsterdam,
Rome, Rotterdam, Riga, Berlin, Stockholm, Bucharest, Bergen, Aarhus, Palma,
Anyang (Regional), Le Mans, Besançon, Avignon, Tours, Dijon, Reims,
Orléans, Mulhouse, Brest, Saint-Étienne, Nice, Montpellier, Strasbourg, Le
Havre, Caen, Rouen (Regional), Bordeaux (Regional), Nantes (Regional),
Grenoble (Regional), Valenciennes (Regional), Angers, Odense, Liepāja,
Daugavpils, Florence, Göteborg, Den Haag, Zurich, Brussels, Antwerp, Ghent,
Charleroi, Liège, Brussels (Regional), Gimpo, Siheung, Geneva (Regional),
Thessaloniki, Gelsenkirchen, Bremen.

Focus: the six violet "Shops and services" maps (Amsterdam, Rotterdam, Den
Haag, Riga, Liepāja, Daugavpils); labels without " (Regional)" and "City of
Brussels" in Benelux; Abroad's 45 approved sentences as rendered; the S-tog
Bx frequency flag (Copenhagen).

## Lane 3: the shared surfaces and the rest of the world (62 city pages)

The Overview itself (every view not named above, the region selector, the
city list, opening on `?region=`, the caption arithmetic), the four fixed
pages (About the Data, What Is Excluded, Why the Maps Differ, Required
Notices) with their back links from a city and from a region, and these city
pages:

San Diego, San Francisco, Los Angeles (Regional), Chicago, New York,
Philadelphia, Miami (Regional), Boston, Washington D.C., Vancouver
(Regional), Montréal, Calgary, Edmonton, Toronto, Guadalajara (Regional), São
Paulo, Rio de Janeiro (Regional), Belo Horizonte (Regional), Brasília,
Salvador, Fortaleza (Regional), Porto Alegre (Regional), Recife (Regional),
Santos (Regional), Hong Kong, Seoul, Taichung, Taoyuan, Taipei (Regional),
Monterrey (Regional), Daegu, Busan, Buenos Aires, Sydney, Melbourne,
Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Buffalo, Sacramento,
Houston, Ottawa, Minneapolis, Pittsburgh, Kitchener–Waterloo (Regional),
Namyangju, Ansan, Uijeongbu, Dallas, Kansas City, Tucson, New Orleans,
Seattle (Regional), Tbilisi, Daejeon, Gwangju, Gimhae, Mendoza, Tacoma.

Focus: the eight new legend wordings for the blue licensed slices
(Philadelphia, Boston, New York, Buffalo, Toronto, Seoul, Daegu, Busan);
Ottawa's magenta "Restaurants and food shops" layer; the olive maps among
these (Hong Kong, Minneapolis, Pittsburgh, Kitchener–Waterloo).

## Lane 4: prose, notices and records, plus the UK and Czechia (17 city pages)

Reading, mostly without a browser: the rendered docs (`docs/data_sources.md`,
every `docs/data_sources/*.md` including the new `greece.md`,
`docs/excluded_categories.md`), the notices 154-186 on the Required Notices
page, the builds' proposals for review time (each build's drafts file:
`worktree-abroad-batch`, `worktree-japan-east-1`, `worktree-japan-kansai-1`,
`worktree-japan-regional-1`, `pin-colours-backlinks`, `review-batch-2026-10-07`),
`docs/privacy_verdicts.md` rows for the 39 cities, and `app/ring_shares.json`
and `app/macro_facts.json` as the pages show them. Then these city pages in
the browser:

Prague, London, Glasgow, Newcastle (Regional), Brno, Plzeň, Olomouc,
Ostrava, Liberec (Regional), Most (Regional), Manchester (Regional),
Birmingham (Regional), Edinburgh, Sheffield, Nottingham (Regional), Blackpool
(Regional), Liverpool (Regional).

Focus: the line-name consistency question (Ōita's "JR Hohi Main Line"
against Kumamoto's "JR Hohi Line"); Hirakata's unlinked credit; Amagasaki's
and Suita's undefined clauses; the olive UK food-hygiene maps.

## After the lanes

Cleanup fixes on the batch branch; a lane re-checks only its own defect.
Owner only: the iPhone check, the fingerprint table for Kansai-1's seven,
the reboot, and the calls the lanes surface. Then Staging's master-list
rows, the fold of every drafts file, the push and a live check.
