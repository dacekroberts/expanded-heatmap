// Run in the browser against a city's standalone heatmap (e.g. served by the
// `heatmap-static` preview at /<city_slug>/heatmap.html) via the javascript
// tool. Evaluates to a JSON string; the map is fine when `problems` is empty.
//
// Checks: every line label (the bold 14px divs inside .leaflet-marker-icon;
// the numeric cluster badges are ignored) is inside the map box, clear of the
// open legend, and not overlapping another line label; each label has a legend
// row; and the legend collapses and re-expands.
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
JSON.stringify({ labels: labels.map(l => l.text), problems, legendOpenHeight: Math.round(openH), legendClosedHeight: Math.round(closedH) });
