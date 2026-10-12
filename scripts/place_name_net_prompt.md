You are a second net in a name review for a map's place search. Another
reader checks the same rows with more information; your job is to flag every
row whose NAME looks wrong, so a doubtful row gets a second look.

Read the one file rows.txt in the current folder. Read only that file. Do not
open any other file, do not start subagents, do not run any skill or agent,
do not fetch anything from the network, and do not write, save or create any
file, including a plan file.

rows.txt starts with a header line naming the city and its languages. Every
other line is one search-index row from OpenStreetMap, tab-separated: number,
kind (station, junction, landmark or place), name, alternate names (separated
by " | ", may be empty). You see names only: no tags, no coordinates.

The search index is meant to hold public places a visitor could look for:
stations, junctions, neighborhoods, parks, squares, museums, places of
worship, monuments, historic sites, notable public buildings. For each row
decide keep or flag. Flag a row when its name suggests one of these classes:

- home: a private residence. A house, villa, mansion, manor, apartment
  building, condominium or housing estate; a building named for a person or
  a family as their house, in any of the city's languages (for example
  "Smith House", "Casa Pérez", "Maison Dupont", "Hôtel de Dupont" as a town
  house, a name ending in 邸 or 宅, a Korean 주택, 빌라 or 아파트, a
  Japanese 団地, "Unidad Habitacional", "Sídliště"). A FAMOUS OR HISTORIC
  HOUSE IS STILL A HOME: flag "Casa Calvet" or "Maison de Victor Hugo" even
  if you recognise it as a landmark; fame, an architect's name or a heritage
  listing does not make it a keep. Keep a former home only when the name
  itself says museum or visitor attraction ("X House Museum"). The costliest
  mistake is keeping a home, so when a name could be a home, flag it.
- business: a shop, restaurant, cafe, bar, venue, hotel, company, clinic,
  office, bank branch or brand name. Exception: a historic building that
  reads as a historic site is kept even if it still carries a business's
  name.
- description: text that describes instead of naming ("open area with
  bench"), or a name that is only the object's type ("Monument",
  "Playground", "Fountain", "Parque de la iglesia", 놀이터, 祠堂, 本殿). A
  war memorial named only for its war, with no place or unit in the name
  ("First World War Memorial", "Boer War Memorial", "Památník padlých"), is
  a bare type: flag it.
- glitch: a name cut short, with stray characters or markup, a placeholder
  or note to other mappers, or plainly some other object's name. A
  dedication is a whole name, not one cut short: a monument called "A
  Francesc Viñas" or "a Pere Vila Codina" (Catalan and Spanish "to X") is
  kept. A NAME
  WRITTEN IN A SCRIPT THAT BELONGS TO NONE OF THE CITY'S LANGUAGES (the
  header lists them; English counts everywhere) is flagged as a glitch: a
  Chinese-script or Cyrillic name in Seoul, a Korean name in Montreal. A
  name that says the same thing in two of the city's languages either side
  of a separator is NOT a glitch.
- other: anything else that should not be searchable. A NAME THAT IS ONLY A
  PERSON'S NAME, with no word for a place or object ("Nachmann Mesner"); a
  museum exhibit or artwork (an aircraft, tank, cannon, locomotive, a
  painting); a family tomb or a memorial stone to a named person at their
  last home; a residence of a religious community (convent, nunnery,
  monastery, seminary, prayer house, priests' house); a station whose NAME
  says it is planned, proposed or under construction; an object whose name
  says it no longer exists. Judge from the name in front of you, never from
  what you remember about a station or a building: your memory of whether
  something is open, closed or built is often wrong.

Otherwise keep the row. Judge each row on its own. Use the alternate names as
well as the name: a row in a local script often has an English alternate.

Reply with exactly one line per row, in the file's order, every number once,
tab-separated:

number, then keep or flag, then the class (home, business, description,
glitch, other; a hyphen for keep), then a reason of at most eight words (a
hyphen for keep).

Do not skip, group or summarize rows. Print nothing before the first line and
nothing after the last except one final line: DONE followed by the count of
rows you judged. Print every line in your reply.
