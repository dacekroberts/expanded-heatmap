// Run in the browser against a city's standalone heatmap (e.g. served by the
// `heatmap-static` preview at /<city_slug>/heatmap.html) via the javascript
// tool. Evaluates to a JSON string; the map is fine when `problems` is empty.
//
// Checks: every line label (the bold 14px divs inside .leaflet-marker-icon;
// the numeric cluster badges are ignored) is inside the map box, clear of the
// open legend, and not overlapping another line label; each label has a legend
// row; the legend collapses and re-expands; and the Dark Mode button is in
// view and flips and restores the theme.
await new Promise(r => setTimeout(r, 1500));
const box = document.querySelector('.folium-map').getBoundingClientRect();
const legend = document.querySelector('details');
const overlaps = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
const labels = [...document.querySelectorAll('.leaflet-marker-icon div')]
  .filter(d => d.style.fontSize === '14px' && !/^\d+$/.test(d.textContent.trim()))
  .map(d => ({ text: d.textContent.trim(), r: d.getBoundingClientRect() }));
const legendRect = legend.getBoundingClientRect();
const legendText = legend.textContent;
const problems = [];
for (const l of labels) {
  if (!(l.r.left >= box.left && l.r.right <= box.right && l.r.top >= box.top && l.r.bottom <= box.bottom)) problems.push(`out of view: ${l.text}`);
  if (overlaps(l.r, legendRect)) problems.push(`under legend: ${l.text}`);
  if (!legendText.includes(l.text)) problems.push(`no legend row: ${l.text}`);
}
for (let i = 0; i < labels.length; i++)
  for (let j = i + 1; j < labels.length; j++)
    if (overlaps(labels[i].r, labels[j].r)) problems.push(`overlap: ${labels[i].text} / ${labels[j].text}`);
const openH = legend.getBoundingClientRect().height;
legend.open = false;
const closedH = legend.getBoundingClientRect().height;
legend.open = true;
if (!(closedH < openH)) problems.push('legend does not collapse');
// Top-right buttons ("All cities" when embedded, and Dark Mode): inside the visible viewport (it is position: fixed, unlike
// Leaflet's top-right corner), not over a label, and it toggles and restores.
const toggle = document.getElementById('theme-toggle');
let darkWorks = null;
if (!toggle) problems.push('no theme toggle');
else {
  const tr = (document.getElementById('map-actions') || toggle).getBoundingClientRect();
  if (tr.left < 0 || tr.right > innerWidth || tr.top < 0) problems.push('theme toggle out of view');
  for (const l of labels) if (overlaps(l.r, tr)) problems.push(`under theme toggle: ${l.text}`);
  const was = document.body.classList.contains('dark-base');
  toggle.click();
  const flipped = document.body.classList.contains('dark-base') !== was;
  toggle.click();
  darkWorks = flipped && document.body.classList.contains('dark-base') === was;
  if (!darkWorks) problems.push('theme toggle does not flip and restore');
}
JSON.stringify({ labels: labels.map(l => l.text), problems, legendOpenHeight: Math.round(openH), legendClosedHeight: Math.round(closedH), darkToggleWorks: darkWorks });
