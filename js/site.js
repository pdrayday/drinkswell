(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // mobile nav
  var mb = $('.menu-btn'), nav = $('#nav');
  if (mb && nav) {
    mb.addEventListener('click', function () {
      var open = mb.getAttribute('aria-expanded') !== 'true';
      mb.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('open', open);
    });
    $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { mb.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }); });
  }

  // SWELL / SWOLL size toggle on the menu
  $$('[data-size-toggle]').forEach(function (seg) {
    var scope = document.getElementById(seg.getAttribute('data-size-toggle')) || document;
    $$('button', seg).forEach(function (b) {
      b.addEventListener('click', function () {
        var size = b.getAttribute('data-size');
        $$('button', seg).forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        $$('img[data-cup]', scope).forEach(function (img) {
          img.src = 'img/cups/' + size + '_' + img.getAttribute('data-cup') + '_sm.webp';
          img.alt = img.alt.replace(/^(SWELL|SWOLL)/, size.toUpperCase());
        });
        $$('[data-protein]', scope).forEach(function (el) { el.textContent = size === 'swoll' ? '50g protein · 24 oz' : '30g protein · 16 oz'; });
      });
    });
  });

  // earnings estimator
  var est = $('#est');
  if (est) {
    var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
    var calc = function () {
      var cups = +$('#est-cups').value, price = +$('#est-price').value, days = +$('#est-days').value, share = +$('#est-share').value;
      $('#est-cups-o').textContent = cups;
      $('#est-price-o').textContent = '$' + price.toFixed(2);
      $('#est-days-o').textContent = days;
      $('#est-share-o').textContent = share + '%';
      var month = cups * price * days;
      $('#est-month').textContent = money(month);
      $('#est-cupsmo').textContent = (cups * days).toLocaleString('en-US') + ' cups';
      $('#est-host').textContent = money(month * share / 100) + ' / mo';
      $('#est-year').textContent = money(month * share / 100 * 12) + ' / yr';
    };
    $$('input', est).forEach(function (i) { i.addEventListener('input', calc); });
    calc();
  }

  // locations
  var locList = $('#locs');
  if (locList) {
    var filter = 'all', q = '';
    var render = function () {
      var shown = 0;
      $$('.loc', locList).forEach(function (li) {
        var ok = (filter === 'all' || li.getAttribute('data-type') === filter) && (!q || li.textContent.toLowerCase().indexOf(q) > -1);
        li.hidden = !ok; if (ok) shown++;
      });
      $('#loc-empty').hidden = shown > 0;
      $('#loc-count').textContent = shown;
    };
    $$('#loc-chips button').forEach(function (b) {
      b.addEventListener('click', function () {
        filter = b.getAttribute('data-f');
        $$('#loc-chips button').forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        render();
      });
    });
    var inp = $('#loc-q');
    inp.addEventListener('input', function () { q = inp.value.trim().toLowerCase(); render(); });
    render();
  }

  // forms: no backend yet, so validate and show a thank-you state
  $$('form[data-lead]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = $('.err', f);
      var bad = $$('[required]', f).filter(function (el) { return !el.value.trim() || (el.type === 'email' && !/^\S+@\S+\.\S+$/.test(el.value)); });
      if (bad.length) {
        err.hidden = false;
        err.textContent = 'Fill in ' + bad.map(function (el) { return $('label[for="' + el.id + '"]', f).textContent.replace(' *', '').toLowerCase(); }).join(', ') + ' so we can reach you.';
        bad[0].focus();
        return;
      }
      err.hidden = true;
      var name = (f.elements.name && f.elements.name.value.trim().split(' ')[0]) || 'there';
      var t = document.getElementById(f.getAttribute('data-lead'));
      $('[data-name]', t).textContent = name;
      f.hidden = true; t.hidden = false; t.focus();
    });
  });

  // prefill the form's location type from ?type= links on the page
  $$('[data-pick-type]').forEach(function (a) {
    a.addEventListener('click', function () {
      var s = $('#f-type'); if (s) s.value = a.getAttribute('data-pick-type');
    });
  });

  // Shakes / Smoothies line toggle (switches the theme like the main Swell site)
  var root = document.documentElement;
  var setLine = function (l, save) {
    root.setAttribute('data-line', l);
    $$('[data-line-btn]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-line-btn') === l)); });
    var tc = document.querySelector('meta[name="theme-color"]'); if (tc) tc.setAttribute('content', l === 'smoothies' ? '#fbf0cf' : '#f8e7eb');
    if (save) { try { localStorage.setItem('swell-line', l); } catch (e) {} }
  };
  setLine(root.getAttribute('data-line') || 'shakes', false);
  $$('[data-line-btn]').forEach(function (b) { b.addEventListener('click', function () { setLine(b.getAttribute('data-line-btn'), true); }); });

  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();
})();

/* ---- Machine finder + Find a machine bar, ported from the main Swell site ---- */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var toastEl = $('toast'), tt;
  function toast(h) { if (!toastEl) return; toastEl.innerHTML = h; toastEl.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { toastEl.classList.remove('on'); }, 2600); }
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var MACHS = [
    { id: 'provo', city: 'Provo', venue: 'Shopping center' }, { id: 'orem', city: 'Orem', venue: 'Shopping center' },
    { id: 'lehi', city: 'Lehi', venue: 'Gym' }, { id: 'af', city: 'American Fork', venue: 'Gym' },
    { id: 'pg', city: 'Pleasant Grove', venue: 'High school' }, { id: 'em', city: 'Eagle Mountain', venue: 'Gym' },
    { id: 'ss', city: 'Saratoga Springs', venue: 'Gym' }, { id: 'sv', city: 'Springville', venue: 'High school' },
    { id: 'sf', city: 'Spanish Fork', venue: 'Hotel' }
  ];
  function homeMach() { var h = store.get('swell-home'); return MACHS.filter(function (m) { return m.id === h; })[0]; }

  // ---------- Find a machine bar: tucks away while the machine finder itself is on screen ----------
  var mbar = $('mbar'), mtop = $('find'), mend = $('find');
  function mbarState() { if (!mbar || !mtop) return; var a = mtop.getBoundingClientRect().top, b = (mend || mtop).getBoundingClientRect().bottom, H = window.innerHeight;
    mbar.classList.toggle('hide', a < H * .85 && b > H * .15); }
  function paintMbar() { var t = $('mb-s'); if (!t) return; var h = homeMach();
    t.textContent = h ? 'Your go-to: ' + h.venue + ' · ' + h.city : MACHS.length + ' in Utah County'; }
  if (mbar) {
    if (mtop) mbar.setAttribute('href', '#find');
    if (mtop && /^#(machines|find)$/.test(location.hash)) mbar.classList.add('hide');
    mbarState(); paintMbar();
    var mraf = 0; window.addEventListener('scroll', function () { if (!mraf) mraf = requestAnimationFrame(function () { mraf = 0; mbarState(); }); }, { passive: true });
    window.addEventListener('resize', mbarState);
    setTimeout(function () { mbarState(); mbar.classList.remove('pre'); }, 700);
  }

  // go-to machine (kept on this device)
  document.addEventListener('click', function (e) { var t = e.target.closest && e.target.closest('[data-sethome]'); if (!t) return;
    store.set('swell-home', t.dataset.sethome); paintMbar();
    var h = homeMach(); if (h) toast(h.city + ' is your go-to machine'); });

  // ---------- machine finder (MapLibre) ----------
  var fmapEl = $('fmap'), mdataEl = $('mdata');
  if (fmapEl && mdataEl) (function () {
    var M = JSON.parse(mdataEl.textContent), P = '';
    var cards = {}; document.querySelectorAll('.mloc').forEach(function (c) { cards[c.dataset.id] = c; });
    var you = null, markers = {}, map = null, current = null, filter = 'all';
    function miles(a, b) { var R = 3958.8, r = Math.PI / 180, dl = (b.lat - a.lat) * r, dg = (b.lng - a.lng) * r;
      var h = Math.sin(dl / 2) * Math.sin(dl / 2) + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dg / 2) * Math.sin(dg / 2); return 2 * R * Math.asin(Math.sqrt(h)); }
    function dirUrl(m) { return 'https://www.google.com/maps/dir/?api=1&destination=' + m.lat + ',' + m.lng; }
    function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function popupHtml(m) {
      var d = you ? '<p class="pv">' + miles(you, m).toFixed(1) + ' mi away · ' + esc(m.venue) + '</p>' : '<p class="pv">' + esc(m.venue) + ' · Shakes and smoothies</p>';
      return '<div class="pc"><img src="' + m.photo + '" alt=""><div><h3><svg class="wm" viewBox="0 0 2496 954" role="img" aria-label="Swell"><use href="#swell-logo"/></svg> Vending, ' + esc(m.city) + '</h3><p class="pa">' + esc(m.address) + '<br>' + esc(m.csz) + '</p>' + d +
        '<button type="button" class="sethome" data-sethome="' + m.id + '">Make this my go-to machine</button>' +
        '<a class="dir" href="' + dirUrl(m) + '" target="_blank" rel="noopener">Directions <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg></a></div></div>';
    }
    function select(id, fly, fromPin) {
      var m = M.filter(function (x) { return x.id === id; })[0]; if (!m) return; current = id;
      Object.keys(cards).forEach(function (k) { cards[k].classList.toggle('sel', k === id); });
      if (map) {
        Object.keys(markers).forEach(function (k) { markers[k].getElement().classList.toggle('sel', k === id); });
        if (fly !== false) map.flyTo({ center: [m.lng, m.lat], zoom: Math.max(map.getZoom(), 12.5), duration: 700, offset: [0, 80] });
        Object.keys(markers).forEach(function (k) { var pp = markers[k].getPopup(); if (k !== id && pp.isOpen()) pp.remove(); });
        if (!fromPin && !markers[id].getPopup().isOpen()) markers[id].togglePopup();
      }
    }
    function applyFilter() {
      var q = ($('fq').value || '').trim().toLowerCase(), n = 0;
      M.forEach(function (m) {
        var c = cards[m.id], ok = (filter === 'all' || m.type === filter) && (!q || c.dataset.q.indexOf(q) > -1);
        c.hidden = !ok; if (ok) n++;
        if (map) { if (ok) markers[m.id].addTo(map); else { markers[m.id].getPopup().remove(); markers[m.id].remove(); } }
      });
      $('fcount').textContent = n;
      return n;
    }
    function sortByDistance() {
      var list = $('flist');
      M.slice().sort(function (a, b) { return miles(you, a) - miles(you, b); }).forEach(function (m) {
        var c = cards[m.id]; c.querySelector('.dist').textContent = miles(you, m).toFixed(1) + ' mi · ' + m.venue; list.appendChild(c);
      });
      if (map) Object.keys(markers).forEach(function (k) { var m = M.filter(function (x) { return x.id === k; })[0]; markers[k].getPopup().setHTML(popupHtml(m)); });
    }
    function locate() {
      if (!navigator.geolocation) { toast("Location isn't available in this browser"); return; }
      toast('Finding machines near you…');
      navigator.geolocation.getCurrentPosition(function (pos) {
        you = { lat: pos.coords.latitude, lng: pos.coords.longitude }; sortByDistance();
        var near = M.slice().sort(function (a, b) { return miles(you, a) - miles(you, b); })[0];
        if (map) {
          if (!locate.dot) { var d = document.createElement('div'); d.className = 'youdot'; locate.dot = new window.maplibregl.Marker({ element: d }).setLngLat([you.lng, you.lat]).addTo(map); }
          else locate.dot.setLngLat([you.lng, you.lat]);
          map.fitBounds([[Math.min(you.lng, near.lng), Math.min(you.lat, near.lat)], [Math.max(you.lng, near.lng), Math.max(you.lat, near.lat)]], { padding: { top: 140, left: 60, right: 110, bottom: 60 }, maxZoom: 13 });
        }
        select(near.id, false); toast('Closest machine: ' + near.city + ', ' + miles(you, near).toFixed(1) + ' mi');
      }, function () { toast("Couldn't get your location. Search by city instead."); }, { enableHighAccuracy: false, timeout: 9000, maximumAge: 300000 });
    }
    function initMap() {
      var ML = window.maplibregl;
      if (ML) try {
        var b = M.reduce(function (a, m) { return [[Math.min(a[0][0], m.lng), Math.min(a[0][1], m.lat)], [Math.max(a[1][0], m.lng), Math.max(a[1][1], m.lat)]]; }, [[180, 90], [-180, -90]]);
        map = new ML.Map({ container: fmapEl, style: 'https://tiles.openfreemap.org/styles/liberty', bounds: b,
          fitBoundsOptions: { padding: { top: 100, left: 110, right: 200, bottom: 40 } }, scrollZoom: false, dragRotate: false, pitchWithRotate: false,
          attributionControl: { compact: true } });
        map.touchZoomRotate.disableRotation();
        var loaded = false, note = document.querySelector('.fnotiles'); window.swellMap = map;
        map.on('load', function () { loaded = true; note.hidden = true;
          map.getStyle().layers.forEach(function (l) {
            if (l.type === 'symbol' && l['source-layer'] === 'place') map.setLayoutProperty(l.id, 'visibility', 'none');
            if (l.type === 'fill' && l['source-layer'] === 'water') map.setPaintProperty(l.id, 'fill-color', '#a9d5f5');
          }); });
        var watch = function () { if (document.visibilityState !== 'visible') return document.addEventListener('visibilitychange', watch, { once: true });
          setTimeout(function () { if (!loaded) note.hidden = false; }, 9000); }; watch();
        fmapEl.addEventListener('click', function () { map.scrollZoom.enable(); });
        M.forEach(function (m) {
          var el = document.createElement('button'); el.type = 'button'; el.className = 'spin'; el.setAttribute('aria-label', 'Swell machine in ' + m.city);
          el.innerHTML = '<span class="pinb"><img src="' + P + 'img/s_mark.png" alt=""></span><span class="plbl' + (m.id === 'lehi' ? ' left' : '') + '">' + esc(m.city) + '</span>';
          var pop = new ML.Popup({ className: 'spop', offset: [0, -52], maxWidth: '340px', focusAfterOpen: false }).setHTML(popupHtml(m));
          var mk = new ML.Marker({ element: el, anchor: 'bottom' }).setLngLat([m.lng, m.lat]).setPopup(pop).addTo(map);
          el.dataset.id = m.id;
          el.addEventListener('click', function () { select(m.id, false, true); });
          pop.on('close', function () { if (current === m.id) { el.classList.remove('sel'); if (cards[m.id]) cards[m.id].classList.remove('sel'); current = null; } });
          markers[m.id] = mk;
        });
        var lz = function () { fmapEl.classList.toggle('lowzoom', map.getZoom() < 10.4 && fmapEl.offsetWidth < 600); }; map.on('zoomend', lz); map.on('load', lz); lz();
        $('fzin').addEventListener('click', function () { map.zoomIn(); });
        $('fzout').addEventListener('click', function () { map.zoomOut(); });
      } catch (e) { map = null; document.querySelector('.fnotiles').hidden = false; }
      else { document.querySelector('.fnotiles').hidden = false; }
    }
    if (window.maplibregl) initMap();
    else {
      var started = false, loadLib = function () { if (started) return; started = true;
        var sc = document.createElement('script'); sc.src = fmapEl.dataset.lib; sc.onload = initMap;
        sc.onerror = function () { document.querySelector('.fnotiles').hidden = false; }; document.body.appendChild(sc); };
      if (window.IntersectionObserver) new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { o.disconnect(); loadLib(); } }, { rootMargin: '900px 0px' }).observe(fmapEl);
      else loadLib();
    }
    Object.keys(cards).forEach(function (k) { cards[k].addEventListener('click', function () {
      select(k); if (window.matchMedia('(max-width: 900px)').matches) fmapEl.scrollIntoView({ behavior: 'smooth', block: 'center' }); }); });
    document.querySelectorAll('[data-mf]').forEach(function (b) { b.addEventListener('click', function () {
      document.querySelectorAll('[data-mf]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); filter = b.dataset.mf; applyFilter(); }); });
    $('fq').addEventListener('input', applyFilter);
    $('fclear').addEventListener('click', function () { $('fq').value = ''; applyFilter(); $('fq').focus(); });
    $('fsearch').addEventListener('submit', function (e) { e.preventDefault(); if (!applyFilter()) { toast('No machines match that yet'); return; }
      var first = M.filter(function (m) { return !cards[m.id].hidden; })[0]; select(first.id); });
    $('flocate').addEventListener('click', locate); $('flocate2').addEventListener('click', locate);
  })();
})();
