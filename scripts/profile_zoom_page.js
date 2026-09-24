// Page half of scripts/profile_zoom.mjs, which evaluates it into a loaded map.
// Not a standalone check. __prof.begin() starts recording; the driver then
// sends TRUSTED input over CDP; __prof.end() resolves once the map has been
// quiet for `quiet` ms. It wraps map.fire, so every map event's handlers are
// timed - that is how zoomend (markercluster) and moveend (Leaflet.heat) costs
// were separated.
(function () {
  var name = Object.keys(window).find(function (k) {
    return k.indexOf('map_') === 0 && window[k] && window[k].getZoom;
  });
  var m = window[name];
  var P = window.__prof = {map: m};
  var rec = null;

  // Time every event dispatch on the map (handlers run synchronously inside fire).
  var origFire = m.fire;
  m.fire = function (type) {
    var t0 = performance.now();
    var r = origFire.apply(this, arguments);
    var dt = performance.now() - t0;
    if (rec) {
      var e = rec.events[type] || (rec.events[type] = {n: 0, ms: 0, max: 0});
      e.n++; e.ms += dt; if (dt > e.max) e.max = dt;
      if (type === 'zoomend') rec.zooms.push(+m.getZoom().toFixed(2));
      if (type === 'zoomstart' && rec.firstZoomStart == null) rec.firstZoomStart = t0 - rec.t0;
      rec.lastEventEnd = performance.now();
    }
    return r;
  };

  m.eachLayer(function (l) {
    if (L.HeatLayer && l instanceof L.HeatLayer) {
      var o = l._redraw;
      l._redraw = function () {
        var t0 = performance.now();
        var r = o.apply(this, arguments);
        if (rec) { rec.heat.n++; rec.heat.ms += performance.now() - t0; }
        return r;
      };
    }
  });

  try {
    new PerformanceObserver(function (list) {
      list.getEntries().forEach(function (e) {
        if (rec) rec.longtasks.push(Math.round(e.duration));
      });
    }).observe({entryTypes: ['longtask']});
  } catch (e) {}

  // Wheel events actually delivered to the map (trusted ones from CDP).
  m.getContainer().addEventListener('wheel', function (e) {
    if (rec) { rec.wheels++; rec.wheelDy.push(e.deltaY); }
  }, {capture: true, passive: true});

  P.begin = function () {
    rec = {events: {}, zooms: [], heat: {n: 0, ms: 0}, longtasks: [], frames: [],
           wheels: 0, wheelDy: [], t0: performance.now(), firstZoomStart: null,
           z0: m.getZoom()};
    rec.lastEventEnd = rec.t0;
    var last = rec.t0, R = rec;
    (function f(t) {
      if (rec !== R) return;
      rec.frames.push(t - last); last = t;
      requestAnimationFrame(f);
    })(performance.now());
    return true;
  };

  P.end = function (quiet) {
    quiet = quiet || 800;
    return new Promise(function (res) {
      var start = performance.now();
      (function poll() {
        var now = performance.now();
        if ((now - rec.lastEventEnd > quiet && !m._animatingZoom) || now - start > 20000) return res();
        setTimeout(poll, 50);
      })();
    }).then(function () {
      var r = rec; rec = null;
      var fr = r.frames.slice(2);
      var ev = {};
      Object.keys(r.events).forEach(function (k) {
        ev[k] = [r.events[k].n, Math.round(r.events[k].ms), Math.round(r.events[k].max)];
      });
      var sum = function (a) { return a.reduce(function (x, y) { return x + y; }, 0); };
      return {z0: r.z0, z1: m.getZoom(), zooms: r.zooms, wheels: r.wheels,
              wheelDy: r.wheelDy.slice(0, 3),
              firstZoomStartMs: r.firstZoomStart == null ? null : Math.round(r.firstZoomStart),
              settledMs: Math.round(r.lastEventEnd - r.t0),
              heat: [r.heat.n, Math.round(r.heat.ms)],
              longtasks: r.longtasks, longSum: sum(r.longtasks),
              maxFrame: Math.round(Math.max.apply(null, fr.concat([0]))),
              framesOver50: fr.filter(function (g) { return g > 50; }).length,
              frames: fr.length,
              events: ev};
    });
  };

  // Everything the driver needs to aim its clicks.
  P.targets = function () {
    var rect = function (el) {
      if (!el) return null;
      var b = el.getBoundingClientRect();
      return {x: b.left + b.width / 2, y: b.top + b.height / 2, w: b.width, h: b.height};
    };
    var c = m.getContainer().getBoundingClientRect();
    // Clusters fully inside the map, biggest first, away from the controls.
    var clusters = Array.prototype.slice.call(document.querySelectorAll('.business-cluster-icon'))
      .map(function (el) { var r = rect(el); r.n = +el.textContent; r.el = el; return r; })
      .filter(function (r) {
        // Topmost at its centre: the three category groups stack clusters on
        // one spot, and a click on a buried one lands on whatever is on top.
        var hit = document.elementFromPoint(r.x, r.y);
        return r.x > c.left + 80 && r.x < c.right - 80 && r.y > c.top + 80 && r.y < c.bottom - 80
          && hit && (hit === r.el || r.el.contains(hit));
      })
      .map(function (r) { delete r.el; return r; })
      .sort(function (a, b) { return b.n - a.n; });
    return {center: {x: c.left + c.width / 2, y: c.top + c.height / 2},
            zoomIn: rect(document.querySelector('.leaflet-control-zoom-in')),
            zoomOut: rect(document.querySelector('.leaflet-control-zoom-out')),
            clusters: clusters.slice(0, 5), zoom: m.getZoom(),
            view: window.__HEATMAP_VIEW && {touched: window.__HEATMAP_VIEW.touched,
                                            corrections: window.__HEATMAP_VIEW.corrections}};
  };
  P.ready = true;
})();
