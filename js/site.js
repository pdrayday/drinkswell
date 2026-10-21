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

  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();
})();
