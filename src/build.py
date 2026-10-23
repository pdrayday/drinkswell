"""Builds the SWELL Vending site from shared partials. Run: python3 src/build.py"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
SITE_URL = 'https://pdrayday.github.io/drinkswell/'
read = lambda n: open(os.path.join(SRC, n)).read()
LOGO_D = read('logo_path.txt')
MACHINE = read('machine.svg')
DIMS = read('dims.svg')

SPRITE = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="swell-logo" viewBox="0 0 2496 954"><path fill-rule="evenodd" d="{LOGO_D}"/></symbol></svg>'
LOGO = '<svg class="logo" viewBox="0 0 2496 954" aria-hidden="true"><use href="#swell-logo"/></svg>'

SHAKES = [
    ('vanilla', 'Vanilla', 'Vanilla bean, the one that goes with everything'),
    ('chocolate', 'Chocolate', 'Dark cocoa, thick like a drive-thru shake'),
    ('cookies-cream', 'Cookies & Cream', 'Cookie crumble in sweet cream'),
]
SMOOTHIES = [
    ('mango', 'Mango', 'Ripe mango, bright and creamy'),
    ('berry-bliss', 'Berry Bliss', 'Strawberry, raspberry, blueberry and blackberry'),
    ('pina-colada', 'Pina Colada', 'Pineapple and coconut'),
]

SOCIAL = [
    ('Instagram', 'https://www.instagram.com/drinkswell', '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/>'),
    ('TikTok', 'https://www.tiktok.com/@drinkswell', '<path d="M14.5 3v11.2a3.6 3.6 0 1 1-3.6-3.6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M14.5 3c.4 2.6 2.2 4.4 5 4.6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>'),
    ('YouTube', 'https://www.youtube.com/@drinkswell', '<rect x="2.5" y="5.5" width="19" height="13" rx="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10.2 9.2v5.6l4.8-2.8z" fill="currentColor"/>'),
    ('Facebook', 'https://www.facebook.com/drinkswell', '<path d="M13.6 21v-7.6h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5H17V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H8.2v3h2.6V21z" fill="currentColor"/>'),
    ('X', 'https://x.com/drinkswell', '<path d="M4 4l16 16M20 4L4 20" stroke="currentColor" stroke-width="2.3" stroke-linecap="round"/>'),
]
SOCIAL_HTML = '<ul class="social" aria-label="Swell on social media">' + ''.join(
    f'<li><a href="{u}" target="_blank" rel="noopener" aria-label="Swell on {n}"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">{p}</svg></a></li>' for n, u, p in SOCIAL) + '</ul>'

NAV = [('machine.html', 'The machine'), ('menu.html', 'Menu'), ('locations.html', 'Locations'), ('about.html', 'About'), ('faq.html', 'FAQ')]


def head(title, desc, path):
    return f'''<!doctype html>
<html lang="en" data-line="shakes">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE_URL}{'' if path == 'index.html' else path}">
<meta name="theme-color" content="#f8e7eb">
<meta name="color-scheme" content="light dark">
<meta property="og:type" content="website"><meta property="og:site_name" content="SWELL Vending"><meta property="og:title" content="{title}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{SITE_URL}img/menu/shakes.webp">
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="img/icons/favicon-32.png"><link rel="apple-touch-icon" href="img/icons/apple-touch-icon.png">
<link rel="preload" href="fonts/source-serif-4.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/instrument-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/playfair-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
<script>try{{var l=localStorage.getItem("swell-line");if(l==="smoothies"||l==="shakes")document.documentElement.setAttribute("data-line",l)}}catch(e){{}}</script>
</head>
<body>
{SPRITE}
'''


def header(active):
    links = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<a class="sr" href="#main">Skip to content</a>
<div class="announce"><div class="wrap"><p>Now placing SWELL machines in Utah County gyms, schools and hotels. <a href="machine.html#request">Get one</a></p></div></div>
<header class="top"><div class="wrap">
  <a class="brand" href="index.html" aria-label="SWELL Vending home">{LOGO}<span class="tag">Vending</span></a>
  <div class="linetog" role="group" aria-label="Show shakes or smoothies"><button type="button" data-line-btn="shakes" aria-pressed="true">Shakes</button><button type="button" data-line-btn="smoothies" aria-pressed="false">Smoothies</button></div>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn" href="machine.html#request">Get a machine</a></nav>
</div></header>
<main id="main">
'''


FOOT = f'''</main>
<footer class="site-foot"><div class="wrap">
  <div class="cols">
    <div class="foot-brand">
      <a href="index.html" aria-label="Swell home">{LOGO}</a>
      <p class="small">Protein shakes and smoothies, blended fresh. Made in Utah County.</p>
    </div>
    <div><h4>Machines</h4><ul><li><a href="machine.html">The machine</a></li><li><a href="machine.html#programs">Host, own or lease</a></li><li><a href="machine.html#estimate">Earnings estimate</a></li><li><a href="machine.html#request">Request a site survey</a></li></ul></div>
    <div><h4>Swell</h4><ul><li><a href="menu.html">Menu</a></li><li><a href="locations.html">Find a machine</a></li><li><a href="about.html">About</a></li></ul></div>
    <div><h4>Help</h4><ul><li><a href="faq.html">FAQ</a></li><li><a href="machine.html#request">Host a machine</a></li><li><a href="refer.html">Refer a location</a></li></ul></div>
  </div>
  <div class="fsocial">{SOCIAL_HTML}<p>Tag <b>@drinkswell</b> and use <b>#drinkswell</b> to get featured.</p></div>
  <div class="fine">
    <p>*These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease. Contains milk.</p>
    <p>Prices, program terms, nutrition and machine locations shown are placeholders until launch.</p>
    <p>© <span id="yr">2026</span> Swell.</p>
  </div>
</div></footer>
<nav class="mbar-nav" aria-label="Find a Swell machine"><a class="mbar pre" id="mbar" href="index.html#find"><i><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/></svg></i><span class="p"><b>Find a machine</b><span id="mb-s">9 in Utah County</span></span><span class="go" aria-hidden="true">Map <span>→</span></span></a></nav>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="js/site.js"></script>
</body>
</html>
'''


def cup_li(key, name, note, kind, with_note=True):
    n = f'<span>{html.escape(note)}</span>' if with_note else ''
    w, h = (557, 941) if kind == 'shake' else (512, 864)
    return f'<li><div class="photo"><img src="img/menu/{key}.webp" alt="Swell {html.escape(name)} protein {kind} in a cup" width="{w}" height="{h}"></div><b>{html.escape(name)}</b>{n}</li>'


def cups_block(id_, with_notes=False):
    sh = ''.join(cup_li(*c, 'shake', with_note=with_notes) for c in SHAKES)
    sm = ''.join(cup_li(*c, 'smoothie', with_note=with_notes) for c in SMOOTHIES)
    return f'''<div id="{id_}" class="menu-lines">
  <div class="line" data-line-group="shakes"><div class="cups-label"><h3>Protein shakes</h3><span>Milkshake flavors</span></div><ul class="cups">{sh}</ul></div>
  <div class="line" data-line-group="smoothies"><div class="cups-label"><h3>Protein smoothies</h3><span>Fruit flavors</span></div><ul class="cups">{sm}</ul></div>
  <p class="small sizes-note">Every flavor comes as a SWELL with 30g of protein or a SWOLL with 50g.</p>
</div>'''


HOW_PHOTOS = '''<div class="how-photos">
  <figure><img src="img/photos/grab-a-cup.webp" alt="A student takes a frozen Berry Bliss cup from a pink SWELL machine at school" width="900" height="1599" loading="lazy"><figcaption>Grab a frozen cup from the freezer.</figcaption></figure>
  <figure><img src="img/photos/scan-to-blend.webp" alt="A frozen SWELL Berry Bliss cup with a Scan to blend QR code in front of the machine" width="900" height="1599" loading="lazy"><figcaption>Scan the code on the cup, then blend.</figcaption></figure>
</div>'''

PHOTO_BAND = '''<section class="photo-band" aria-label="Swell shakes and smoothies"><div class="wrap">
  <a class="photo-link" href="menu.html"><span class="photo-cta">See the <span class="sw">menu</span> →</span>
  <img data-line-show="shakes" src="img/menu/shakes.webp" alt="Swell Vanilla, Chocolate and Cookies &amp; Cream protein shakes" width="1672" height="941">
  <img data-line-show="smoothies" src="img/menu/smoothies.webp" alt="Swell Mango, Berry Bliss and Pina Colada protein smoothies" width="1536" height="1024"></a>
</div></section>'''


def hero_stage():
    return '''<div class="hero-stage">
  <img class="hero-machine" src="img/photos/machine.webp" alt="A pink SWELL vending machine with a glass freezer door full of frozen shake and smoothie cups, a touchscreen and a blending window" width="900" height="1599">
</div>'''


STEPS = '''<ol class="steps">
  <li><h3>Grab a cup</h3><p class="small">Open the freezer door and pick a frozen SWELL shake or smoothie cup.</p></li>
  <li><h3>Scan it</h3><p class="small">Scan the QR code on the cup at the screen, then tap a card or phone to pay.</p></li>
  <li><h3>Blend</h3><p class="small">Peel the lid, set the cup in the blending window and the machine blends it fresh.</p></li>
  <li><h3>Sip</h3><p class="small">Take it out cold and thick, with a straw, and go.</p></li>
</ol>'''

SIZES = '''<div class="sizes">
  <article class="size">
    <div class="txt">
      <svg class="logo mark-swell" viewBox="0 0 2496 954" role="img" aria-label="SWELL"><use href="#swell-logo"/></svg>
      <p class="big">30g<small>PROTEIN</small></p>
      <ul><li>16 oz cup</li><li>Every shake and smoothie flavor</li><li>Collagen, colostrum and iron in every cup*</li><li>$7.99 at the machine</li></ul>
    </div>
  </article>
  <article class="size is-swoll">
    <div class="txt">
      <p class="mark-swoll">SWOLL</p>
      <p class="big">50g<small>PROTEIN</small></p>
      <ul><li>24 oz cup</li><li>The same flavors, bigger</li><li>Built for after a hard lift</li><li>$9.99 at the machine</li></ul>
    </div>
  </article>
</div>'''

SPECS = '''<dl class="specs">
  <div><dt>Footprint</dt><dd>16.9 in wide × 34.3 in deep (428 × 872 mm). Fits through a standard doorway.</dd></div>
  <div><dt>Height</dt><dd>76.2 in (1,935 mm) on casters with leveling feet</dd></div>
  <div><dt>Freezer</dt><dd>Glass-door freezer stocked with frozen SWELL shake and smoothie cups</dd></div>
  <div><dt>Ordering</dt><dd>Touchscreen with QR scan, bottom edge at 51.5 in</dd></div>
  <div><dt>Cup window</dt><dd>36.4 in from the floor</dd></div>
  <div><dt>Payment</dt><dd>Tap-to-pay reader for cards and phone wallets at 30.6 in</dd></div>
  <div><dt>Service</dt><dd>Locking freezer door for restocking and cleaning</dd></div>
  <div><dt>Wrap</dt><dd>SWELL and SWOLL graphics, or co-branded with your gym or school</dd></div>
  <div><dt>Power &amp; water</dt><dd>Confirmed at your free site survey before install</dd></div>
</dl>'''

PROGRAMS = '''<div class="programs">
  <article class="prog">
    <p class="who">Gyms, hotels, offices</p>
    <h3>Host it</h3>
    <ul><li>We install the machine at no cost to you</li><li>We stock, clean and service it on a schedule</li><li>You get a share of every cup sold</li><li>Monthly sales report</li></ul>
    <p class="pay"><b>Free to host</b>Revenue share, set per location</p>
  </article>
  <article class="prog feature">
    <p class="who">Operators and owners</p>
    <h3>Own it</h3>
    <ul><li>Buy the machine and keep the sales</li><li>We supply frozen SWELL cups, lids and straws</li><li>Install, training and a service checklist</li><li>Remote sales and stock alerts</li></ul>
    <p class="pay"><b>One-time purchase</b>Quoted by location and volume</p>
  </article>
  <article class="prog">
    <p class="who">Schools and rec centers</p>
    <h3>Lease it</h3>
    <ul><li>Low monthly payment, no large purchase</li><li>Keep the sales after the lease</li><li>We supply SWELL cups and handle repairs</li><li>Option to buy at the end</li></ul>
    <p class="pay"><b>Monthly lease</b>Quoted by term</p>
  </article>
</div>'''

PLACES = ['Gyms', 'High schools', 'Colleges', 'Hotels', 'Offices', 'Hospitals', 'Rec centers', 'CrossFit boxes', 'Pilates & yoga studios', 'Resorts', 'Apartment clubhouses', 'Sports complexes']
PLACES_HTML = '<ul class="places">' + ''.join(f'<li{" class=\"hl\"" if i < 3 else ""}>{p}</li>' for i, p in enumerate(PLACES)) + '</ul>'

ESTIMATOR = '''<div class="est" id="est">
  <form onsubmit="return false" aria-label="Earnings estimate">
    <div class="range"><label for="est-cups">Cups sold per day <output id="est-cups-o" for="est-cups">30</output></label><input id="est-cups" type="range" min="5" max="120" step="1" value="30"></div>
    <div class="range"><label for="est-price">Average price per cup <output id="est-price-o" for="est-price">$8.50</output></label><input id="est-price" type="range" min="5.99" max="11.99" step="0.25" value="8.49"></div>
    <div class="range"><label for="est-days">Days open per month <output id="est-days-o" for="est-days">26</output></label><input id="est-days" type="range" min="10" max="31" step="1" value="26"></div>
    <div class="range"><label for="est-share">Your share of sales <output id="est-share-o" for="est-share">15%</output></label><input id="est-share" type="range" min="5" max="100" step="5" value="15"></div>
    <p class="small">Hosts earn a revenue share. Owners keep 100% of sales, minus SWELL cubes and cups.</p>
  </form>
  <div class="est-out" aria-live="polite">
    <p class="k">Monthly sales at the machine</p>
    <p class="v" id="est-month">$6,630</p>
    <div class="row"><span>Cups per month</span><b id="est-cupsmo">780 cups</b></div>
    <div class="row"><span>Your share</span><b id="est-host">$995 / mo</b></div>
    <div class="row"><span>Your share per year</span><b id="est-year">$11,934 / yr</b></div>
    <p class="small" style="margin-top:8px;color:#d7a9b6">An illustration from the numbers you choose, not a forecast.</p>
  </div>
</div>'''

TYPES = ['Gym', 'High school', 'College', 'Hotel', 'Office', 'Hospital', 'Rec center', 'CrossFit box', 'Pilates or yoga studio', 'Resort', 'Apartment community', 'Other']


def request_block(heading='Get a SWELL machine', sub='Tell us about your spot. We will set up a free site survey, check power and space, and send terms for hosting, owning or leasing.'):
    opts = ''.join(f'<option>{t}</option>' for t in TYPES)
    return f'''<section class="band-ink" id="request"><div class="wrap req">
  <div class="sec-head">
    <p class="eyebrow">Request a site survey</p>
    <h2>Get a <span class="sw">Swell</span> machine</h2>
    <p class="lead">{sub}</p>
    <ul class="small" style="margin:6px 0 0;padding-left:18px;display:grid;gap:6px">
      <li>Survey and quote within one week</li>
      <li>Most installs take a single morning</li>
      <li>Serving Utah County first, then the rest of Utah</li>
    </ul>
  </div>
  <div>
    <form class="form" data-lead="req-thanks" novalidate>
      <div class="field"><label for="f-name">Your name *</label><input id="f-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="f-email">Work email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="f-org">Business or school *</label><input id="f-org" name="org" autocomplete="organization" required></div>
      <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="f-type">Type of location *</label><select id="f-type" name="type" required><option value="">Choose one</option>{opts}</select></div>
      <div class="field"><label for="f-city">City</label><input id="f-city" name="city" autocomplete="address-level2"></div>
      <div class="field"><label for="f-traffic">People through each day</label><select id="f-traffic" name="traffic"><option>Under 100</option><option selected>100 to 300</option><option>300 to 1,000</option><option>1,000+</option></select></div>
      <div class="field"><label for="f-prog">Interested in</label><select id="f-prog" name="program"><option>Not sure yet</option><option>Hosting (free)</option><option>Owning</option><option>Leasing</option></select></div>
      <div class="field full"><label for="f-msg">Anything else</label><textarea id="f-msg" name="msg" placeholder="Where would it go? Hours, nearby outlet, who to talk to."></textarea></div>
      <p class="err" role="alert" hidden></p>
      <button class="btn" type="submit">Request a site survey</button>
      <p class="note">Demo form: it shows a confirmation but is not connected to an inbox yet.</p>
    </form>
    <div class="thanks" id="req-thanks" tabindex="-1" hidden>
      <p class="eyebrow">Request received</p>
      <h3>Thanks, <span data-name>there</span>.</h3>
      <p class="small">We will reach out within two business days to set up your site survey.</p>
    </div>
  </div>
</div></section>'''


MDATA = [
    {"id": "provo", "city": "Provo", "type": "shopping", "address": "1200 Towne Centre Blvd", "csz": "Provo, UT 84601", "lat": 40.2173, "lng": -111.6646, "venue": "Shopping center"},
    {"id": "orem", "city": "Orem", "type": "shopping", "address": "575 E University Pkwy", "csz": "Orem, UT 84097", "lat": 40.2767, "lng": -111.6829, "venue": "Shopping center"},
    {"id": "lehi", "city": "Lehi", "type": "gym", "address": "1230 E Main St", "csz": "Lehi, UT 84043", "lat": 40.3887, "lng": -111.8279, "venue": "Gym"},
    {"id": "af", "city": "American Fork", "type": "gym", "address": "51 E 100 N", "csz": "American Fork, UT 84003", "lat": 40.3786, "lng": -111.7946, "venue": "Gym"},
    {"id": "pg", "city": "Pleasant Grove", "type": "school", "address": "Address coming soon", "csz": "Pleasant Grove, UT 84062", "lat": 40.364, "lng": -111.738, "venue": "High school"},
    {"id": "em", "city": "Eagle Mountain", "type": "gym", "address": "Address coming soon", "csz": "Eagle Mountain, UT 84005", "lat": 40.3141, "lng": -112.0069, "venue": "Gym"},
    {"id": "ss", "city": "Saratoga Springs", "type": "gym", "address": "Address coming soon", "csz": "Saratoga Springs, UT 84045", "lat": 40.3492, "lng": -111.9047, "venue": "Gym"},
    {"id": "sv", "city": "Springville", "type": "school", "address": "Address coming soon", "csz": "Springville, UT 84663", "lat": 40.1652, "lng": -111.6107, "venue": "High school"},
    {"id": "sf", "city": "Spanish Fork", "type": "hotel", "address": "Address coming soon", "csz": "Spanish Fork, UT 84660", "lat": 40.115, "lng": -111.655, "venue": "Hotel"},
]
for _m in MDATA: _m["photo"] = "img/machine_thumb.webp"
CHEV = '<svg class="chev" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def finder_section(pad_top='10px'):
    import json
    cards = ''.join(
        f'<button type="button" class="mloc" data-id="{m["id"]}" data-type="{m["type"]}" data-q="{html.escape((m["city"] + " " + m["address"] + " " + m["csz"] + " " + m["venue"]).lower())}">'
        f'<img src="{m["photo"]}" alt="Swell vending machine in {html.escape(m["city"])}" width="112" height="140" loading="lazy">'
        f'<span class="mt"><b>{html.escape(m["city"])}</b><span class="dist" data-venue="{m["venue"]}">{m["venue"]}</span><span class="addr">{html.escape(m["address"])}<br>{html.escape(m["csz"])}</span></span>{CHEV}</button>'
        for m in MDATA)
    return f'''<section style="padding-top:{pad_top}" id="find" class="find-sec"><div class="wrap">
<link rel="stylesheet" href="vendor/maplibre-gl.css">
<div class="finder2">
  <div class="fside">
    <div class="fhead"><h2>Find a <span class="sw">Swell</span></h2><p>Utah County · <span id="fcount">{len(MDATA)}</span> machines</p></div>
    <div class="ffilters filters" role="group" aria-label="Location type"><button type="button" class="press" aria-pressed="true" data-mf="all">All</button><button type="button" class="press" aria-pressed="false" data-mf="gym">Gyms</button><button type="button" class="press" aria-pressed="false" data-mf="school">Schools</button><button type="button" class="press" aria-pressed="false" data-mf="hotel">Hotels</button><button type="button" class="press" aria-pressed="false" data-mf="shopping">Shopping</button></div>
    <button type="button" class="btn sm alt flocate" id="flocate2"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="currentColor"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="12" r="7.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>Sort by distance from me</button>
    <div class="flist" id="flist">{cards}</div>
    <p class="small fnote">Sample locations for layout. Replace with live machine data before launch.</p>
  </div>
  <div class="fmapwrap">
    <div id="fmap" data-lib="vendor/maplibre-gl.js" role="region" aria-label="Map of Swell vending machines in Utah County"></div>
    <form class="fsearch" id="fsearch" role="search"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>
      <label class="sr" for="fq">Search by city, address or ZIP</label><input id="fq" type="search" placeholder="Search city, address or ZIP" autocomplete="off"><button type="button" id="fclear" aria-label="Clear search">×</button></form>
    <div class="fctl"><button type="button" id="fzin" aria-label="Zoom in">+</button><button type="button" id="fzout" aria-label="Zoom out">−</button></div>
    <button type="button" class="fctl fme" id="flocate" aria-label="Show my location"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="12" cy="12" r="3.5" fill="currentColor"/><circle cx="12" cy="12" r="7.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 1.5v3.5M12 19v3.5M1.5 12H5M19 12h3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    <p class="fnotiles" hidden>The map couldn't load here. The list still works, and Directions opens Google Maps.</p>
  </div>
</div>
<script type="application/json" id="mdata">{json.dumps(MDATA)}</script>
</div></section>'''


LOCS = [
    ('Provo', 'shopping', 'Shopping center', '1200 Towne Centre Blvd', 'Provo, UT 84601'),
    ('Orem', 'shopping', 'Shopping center', '575 E University Pkwy', 'Orem, UT 84097'),
    ('Lehi', 'gym', 'Gym', '1230 E Main St', 'Lehi, UT 84043'),
    ('American Fork', 'gym', 'Gym', '51 E 100 N', 'American Fork, UT 84003'),
    ('Pleasant Grove', 'school', 'High school', None, 'Pleasant Grove, UT 84062'),
    ('Eagle Mountain', 'gym', 'Gym', None, 'Eagle Mountain, UT 84005'),
    ('Saratoga Springs', 'gym', 'Gym', None, 'Saratoga Springs, UT 84045'),
    ('Springville', 'school', 'High school', None, 'Springville, UT 84663'),
    ('Spanish Fork', 'hotel', 'Hotel', None, 'Spanish Fork, UT 84660'),
]


def loc_li(l):
    city, t, tl, street, cz = l
    if street:
        q = (street + ', ' + cz).replace(' ', '+')
        return f'<li class="loc" data-type="{t}"><p class="type">{tl}</p><h3>{city}</h3><address>{street}<br>{cz}</address><a href="https://www.google.com/maps/dir/?api=1&amp;destination={q}" target="_blank" rel="noopener">Directions</a></li>'
    return f'<li class="loc soon" data-type="{t}"><p class="type">{tl} · coming soon</p><h3>{city}</h3><address>Address coming soon<br>{cz}</address></li>'


def page(name, title, desc, body):
    out = head(title, desc, name) + header(name) + body + FOOT
    open(os.path.join(ROOT, name), 'w').write(out)
    return out


# ---------------- pages ----------------
index = page('index.html', 'SWELL Vending', 'SWELL vending machines blend fresh protein smoothies and shakes to order: 30g protein in a SWELL, 50g in a SWOLL. Host, own or lease one for your gym, school or hotel.', f'''
<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <p class="eyebrow">SWELL vending · Utah County</p>
    <h1>Protein smoothies, <em>blended by the machine.</em></h1>
    <p class="lead">SWELL machines make protein smoothies and shakes to order: 30g of protein in a SWELL, 50g in a SWOLL. Put a real smoothie bar in your gym, school or hotel in a footprint 17 inches wide.</p>
    <div class="btn-row"><a class="btn arrow" href="machine.html#request">Get a SWELL machine</a><a class="btn ghost" href="menu.html">See the menu</a></div>
    <div class="facts">
      <div><b>17 in</b><span>wide footprint</span></div>
      <div><b>30g · 50g</b><span>protein per cup</span></div>
      <div><b>6</b><span>shakes and smoothies</span></div>
      <div><b>Tap</b><span>to pay</span></div>
    </div>
  </div>
  {hero_stage()}
</div></section>

{PHOTO_BAND}

<section class="band-card" id="how"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">How it works</p><h2>Grab it. Scan it. <em>Blend it.</em></h2><p class="lead">Every SWELL machine is a freezer full of frozen shake and smoothie cups with a blender built in. Grab a cup, scan it, and it comes out fresh and cold.</p></div>
  {HOW_PHOTOS}
  {STEPS}
</div></section>

<section class="band-ink" id="machine"><div class="wrap mach">
  <div class="mach-fig">{DIMS}</div>
  <div>
    <p class="eyebrow">The machine</p>
    <h2 style="margin-top:14px">Fits where a smoothie bar <em>never could.</em></h2>
    <p class="lead" style="margin-top:16px">The customer side is under 17 inches wide, so it fits beside a front desk, in a hallway or by the lockers. It rolls in on casters and plugs in near a wall.</p>
    {SPECS}
    <div class="btn-row" style="margin-top:26px"><a class="btn arrow" href="machine.html">Full machine details</a></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Built for busy places</p><h2>Anywhere people work out, <em>study or travel.</em></h2><p class="lead">Our first machines went into high schools, gyms and hotels around Utah County. These are the spots that sell the most cups.</p></div>
  {PLACES_HTML}
</div></section>

<section class="band-card" id="programs"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Ways to get one</p><h2>Host it, own it <em>or lease it.</em></h2><p class="lead">Pick the setup that fits your building. Every option includes install, frozen SWELL cups and our help keeping it running.</p></div>
  {PROGRAMS}
  <p class="note-chip" style="margin-top:18px">Terms are set per location. Ask for a quote.</p>
</div></section>

<section id="estimate"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Earnings estimate</p><h2>What a machine could do <em>at your spot.</em></h2><p class="lead">Move the sliders to match your foot traffic.</p></div>
  {ESTIMATOR}
</div></section>

<section class="mach-intro" id="machines"><div class="wrap"><div class="sec-head"><p class="eyebrow">Already blending</p><h2>Find a <span class="sw">Swell</span> machine</h2><p class="lead">You'll find SWELL machines in gyms, high schools, hotels and shopping centers around Utah County, blending shakes and smoothies to order.</p></div></div></section>
{finder_section()}

<section class="drinkswell"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">#drinkswell</p><h2>Post your <span class="sw">Swell.</span></h2><p class="lead">Gym bags, school hallways, the line at the machine. Tag <b>@drinkswell</b> and use <b>#drinkswell</b>, and your post could end up here.</p></div>
  {SOCIAL_HTML}
</div></section>

{request_block()}
''')

page('machine.html', 'The SWELL Machine', 'Specs, dimensions and programs for the SWELL protein smoothie vending machine: 16.9 in wide, 34.3 in deep, 76.2 in tall, with touchscreen ordering and tap to pay.', f'''
<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <p class="eyebrow">The SWELL machine</p>
    <h1>A smoothie bar <em>on casters.</em></h1>
    <p class="lead">A glass-door freezer full of frozen SWELL cups and a blender in one machine. Grab a cup, scan it, and it blends fresh. We bring it in, set it up and keep it stocked.</p>
    <div class="btn-row"><a class="btn arrow" href="#request">Request a site survey</a><a class="btn ghost" href="#programs">Compare programs</a></div>
  </div>
  {hero_stage()}
</div></section>

<section class="band-ink" id="specs"><div class="wrap mach">
  <div class="mach-fig">{DIMS}</div>
  <div>
    <p class="eyebrow">Specs</p>
    <h2 style="margin-top:14px">Measured for <em>tight spaces.</em></h2>
    {SPECS}
  </div>
</div></section>

<section class="band-card"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">What comes with it</p><h2>Everything <em>a cup needs.</em></h2></div>
  <div class="boosts">
    <div><b>Install</b><p class="small">Delivery, setup and a test run. Most installs take a single morning.</p></div>
    <div><b>Frozen SWELL cups</b><p class="small">Pre-filled, frozen shake and smoothie cups for all six flavors, each with its own scan-to-blend code, plus straws.</p></div>
    <div><b>Cashless payments</b><p class="small">Cards and phone wallets through the tap-to-pay reader. Sales post daily.</p></div>
    <div><b>Your wrap</b><p class="small">Standard SWELL and SWOLL graphics, or a co-branded wrap with your logo and colors.</p></div>
  </div>
</div></section>

<section id="programs"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Programs</p><h2>Host it, own it <em>or lease it.</em></h2></div>
  {PROGRAMS}
  <div class="tbl-wrap" style="margin-top:28px">
    <table>
      <caption class="sr">Program comparison</caption>
      <thead><tr><th scope="col"></th><th scope="col">Host</th><th scope="col">Own</th><th scope="col">Lease</th></tr></thead>
      <tbody>
        <tr><th scope="row">Upfront cost</th><td>None</td><td>Machine purchase</td><td>None or small deposit</td></tr>
        <tr><th scope="row">Who keeps sales</th><td>SWELL, you get a share</td><td>You</td><td>You</td></tr>
        <tr><th scope="row">Restocking</th><td>Our team</td><td>You, with our cube supply</td><td>You, with our cube supply</td></tr>
        <tr><th scope="row">Repairs</th><td>Included</td><td>Warranty, then service plan</td><td>Included during lease</td></tr>
        <tr><th scope="row">Best for</th><td>Gyms and hotels that want zero work</td><td>Operators with several sites</td><td>Schools and rec centers on a budget</td></tr>
      </tbody>
    </table>
  </div>
  <p class="note-chip" style="margin-top:18px">Sample program terms for layout. Final terms are quoted per location.</p>
</div></section>

<section class="band-blush" id="estimate"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Earnings estimate</p><h2>Run <em>your numbers.</em></h2></div>
  {ESTIMATOR}
</div></section>

{request_block()}
''')

page('menu.html', 'SWELL Menu', 'Protein shakes and smoothies blended fresh in SWELL vending machines, in a 30g SWELL or a 50g SWOLL cup.', f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Menu</p>
  <h1>Dessert flavors, <em>real protein.</em></h1>
  <p class="lead">Every cup is packed frozen with real fruit and protein, then blended fresh in the machine when you scan it. Choose a 16 oz SWELL with 30g of protein or a 24 oz SWOLL with 50g.</p>
</div></section>

<section style="padding-top:0"><div class="wrap">
  {cups_block('menu-cups', with_notes=True)}
</div></section>

<section class="band-blush" id="sizes"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Sizes</p><h2><span class="sw">Swell</span> or <span class="swoll-word">SWOLL</span>.</h2></div>
  {SIZES}
</div></section>

<section><div class="wrap">
  <div class="sec-head"><p class="eyebrow">In every cup</p><h2>More than <em>protein.</em></h2><p class="lead">Every SWELL and SWOLL, shakes and smoothies, also has collagen peptides, colostrum and iron.</p></div>
  <div class="boosts">
    <div><b>30g or 50g protein</b><p class="small">30g in a SWELL and 50g in a SWOLL, enough for a post-workout shake or a light meal.</p></div>
    <div><b>Collagen peptides</b><p class="small">Hydrolyzed collagen that supports healthy skin, hair, nails and joints.* No taste, no grit.</p></div>
    <div><b>Colostrum</b><p class="small">Naturally rich in immunoglobulins that support gut health and immune function.*</p></div>
    <div><b>Iron</b><p class="small">Helps your blood carry oxygen to working muscles, for steady energy and endurance.*</p></div>
  </div>
  <p class="small" style="margin-top:22px">Contains milk. Full nutrition facts for each flavor will be posted after lab testing.</p>
</div></section>

<section class="band-ink cta-band"><div class="wrap">
  <h2>Want this menu <em>in your building?</em></h2>
  <div class="btn-row"><a class="btn arrow" href="machine.html#request">Get a SWELL machine</a><a class="btn ghost" href="locations.html">Find a machine</a></div>
</div></section>
''')

page('locations.html', 'Find a SWELL Machine', 'SWELL protein smoothie vending machines in gyms, schools, hotels and shopping centers around Utah County, Utah.', f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Locations</p>
  <h1>Find a <span class="sw">Swell</span> machine.</h1>
  <p class="lead">Machines in gyms, high schools, hotels and shopping centers around Utah County, with more on the way.</p>
</div></section>

{finder_section('0')}

<section class="band-ink cta-band"><div class="wrap">
  <h2>Don't see one <em>near you?</em></h2>
  <div class="btn-row"><a class="btn arrow" href="machine.html#request">Request a machine</a><a class="btn ghost" href="refer.html">Refer a location</a></div>
</div></section>
''')

page('about.html', 'About SWELL', 'SWELL started selling frozen smoothie cubes from its own vending machines in Utah County high schools, gyms and hotels. Now the machine blends them fresh.', f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">About</p>
  <h1>We started <em>in a vending machine.</em></h1>
</div></section>

<section style="padding-top:0"><div class="wrap split">
  <div class="prose">
    <p>SWELL began as frozen smoothie cubes, sold out of our own vending machines in high schools, gyms and hotels around Utah County.</p>
    <p>The machines taught us a lot. People bought the dessert flavors first. They wanted real protein in them. And nobody wanted to blend anything themselves between classes or on the way out of the gym.</p>
    <p>So we built a machine that does the blending. It takes the order, takes the payment and blends a frozen SWELL cup into a fresh protein smoothie or shake in front of you. SWOLL is the big one, with 50 grams of protein for after a hard lift.</p>
    <p>Today we place, sell and lease SWELL machines to the places that asked for them first: gyms, schools, hotels and offices.</p>
  </div>
  <ol class="timeline">
    <li><b>Cubes</b><p class="small">Frozen SWELL smoothie cubes in our own vending machines.</p></li>
    <li><b>Flavors</b><p class="small">Dessert shakes and candy-shop smoothies, all with real protein.</p></li>
    <li><b>SWOLL</b><p class="small">A 50g version for lifters and athletes.</p></li>
    <li><b>The machine</b><p class="small">A slim blender machine that makes every cup fresh.</p></li>
  </ol>
</div></section>

<section class="band-blush"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Who it's for</p><h2>Built for people with a protein goal <em>and a sweet tooth.</em></h2></div>
  <div class="boosts">
    <div><b>Before the gym</b><p class="small">A light, cold cup with protein, ready before the warm-up.</p></div>
    <div><b>After the gym</b><p class="small">A 50g SWOLL on the way out the door.</p></div>
    <div><b>Between meals</b><p class="small">Fills the gap without a drive-thru stop.</p></div>
    <div><b>Dessert cravings</b><p class="small">Milkshake flavors that still count toward your protein.</p></div>
  </div>
</div></section>

<section class="band-ink cta-band"><div class="wrap">
  <h2>Bring <span class="sw">Swell</span> to your building.</h2>
  <div class="btn-row"><a class="btn arrow" href="machine.html#request">Get a SWELL machine</a></div>
</div></section>
''')

FAQ_HOST = [
    ('How much space does a SWELL machine need?', 'The front is 16.9 inches wide and the machine is 34.3 inches deep and 76.2 inches tall. Leave room on the side for the service doors to open. It rolls in on casters and fits through a standard doorway.'),
    ('What does it need for power and water?', 'We confirm power and water at a free site survey before anything is installed, so there are no surprises on install day.'),
    ('Who stocks and cleans it?', 'On the Host program our team restocks frozen SWELL cups, lids and straws and cleans the machine on a set schedule. Owners and lessees restock themselves with our cube supply and service checklist.'),
    ('How do we get paid?', 'Hosts receive a share of sales each month with a sales report. Owners and lessees keep their sales, which are deposited from the tap-to-pay reader.'),
    ('Can I buy a machine outright?', 'Yes. The Own program is a one-time purchase quoted by location and volume. We supply cubes and help with install and training.'),
    ('Can the machine carry our logo?', 'Yes. Machines ship with SWELL and SWOLL graphics, or we can print a co-branded wrap for your gym, school or company.'),
    ('Do you install outside Utah County?', 'We are starting in Utah County and expanding through Utah next. Send a request either way and we will tell you when we reach your area.'),
]
FAQ_DRINK = [
    ('What is the difference between SWELL and SWOLL?', 'SWELL is a 16 oz cup with 30g of protein. SWOLL is a 24 oz cup with 50g. Both come in every flavor and have collagen, colostrum and iron.'),
    ('Is it really blended fresh?', 'Yes. Each cup sits frozen in the machine until you scan it. Then the machine blends it in front of you, so nothing sits pre-made.'),
    ('How do I pay?', 'Tap a card or phone wallet on the reader. The machine does not take cash.'),
    ('Is there dairy?', 'Yes. SWELL shakes and smoothies contain milk.'),
    ('Is SWELL a good fit if I am on a GLP-1?', 'Many people eating less still have a protein goal, and one cup gives you 30g or 50g without a full meal. SWELL is not a medical product, so check with your doctor about your own needs.'),
]


def faq_items(items):
    return ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in items)


page('faq.html', 'SWELL FAQ', 'Answers about hosting, buying and leasing a SWELL protein smoothie vending machine, and about SWELL and SWOLL cups.', f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">FAQ</p>
  <h1>Questions, <em>answered.</em></h1>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="faq-group mt-0"><h3>For gyms, schools and businesses</h3><div class="faq">{faq_items(FAQ_HOST)}</div></div>
  <div class="faq-group"><h3>About the drinks</h3><div class="faq">{faq_items(FAQ_DRINK)}</div></div>
</div></section>
<section class="band-ink cta-band"><div class="wrap">
  <h2>Still have <em>a question?</em></h2>
  <div class="btn-row"><a class="btn arrow" href="machine.html#request">Ask us</a></div>
</div></section>
''')

ref_opts = ''.join(f'<option>{t}</option>' for t in TYPES)
page('refer.html', 'Refer a SWELL Location', 'Know a gym, school or hotel that should have a SWELL machine? Refer it and get paid when the machine goes live.', f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Referral program</p>
  <h1>Know a spot that needs <em>a Swell?</em></h1>
  <p class="lead">Coaches, students, members and front-desk staff know which buildings need a protein option. Tell us where, and we pay you when the machine goes live.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <ol class="steps">
    <li><h3>Send it</h3><p class="small">Tell us the gym, school or business and who to talk to, if you know.</p></li>
    <li><h3>We pitch</h3><p class="small">We reach out, run the site survey and handle the details.</p></li>
    <li><h3>It goes live</h3><p class="small">The machine is installed and selling cups.</p></li>
    <li><h3>You get paid</h3><p class="small">$250 per machine that goes live, plus a free SWOLL on us.</p></li>
  </ol>
  <p class="note-chip" style="margin-top:18px">Sample referral reward for layout. Final terms set before launch.</p>
</div></section>
<section class="band-ink" id="refer"><div class="wrap req">
  <div class="sec-head"><p class="eyebrow">Refer a location</p><h2>Send us <em>a spot.</em></h2><p class="lead">It takes a minute. You do not need to know the owner.</p></div>
  <div>
    <form class="form" data-lead="ref-thanks" novalidate>
      <div class="field"><label for="r-name">Your name *</label><input id="r-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="r-email">Your email *</label><input id="r-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="r-place">Location name *</label><input id="r-place" name="place" required></div>
      <div class="field"><label for="r-city">City *</label><input id="r-city" name="city" required></div>
      <div class="field"><label for="r-type">Type of location</label><select id="r-type" name="type">{ref_opts}</select></div>
      <div class="field"><label for="r-contact">Contact there</label><input id="r-contact" name="contact" placeholder="Name, email or phone"></div>
      <p class="err" role="alert" hidden></p>
      <button class="btn" type="submit">Send referral</button>
      <p class="note">Demo form: it shows a confirmation but is not connected to an inbox yet.</p>
    </form>
    <div class="thanks" id="ref-thanks" tabindex="-1" hidden><p class="eyebrow">Referral received</p><h3>Thanks, <span data-name>there</span>.</h3><p class="small">We will email you when we reach out and again when the machine goes live.</p></div>
  </div>
</div></section>
''')

# ---- supporting files
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n')
urls = ['', 'machine.html', 'menu.html', 'locations.html', 'about.html', 'faq.html', 'refer.html']
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE_URL}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(ROOT, 'llms.txt'), 'w').write(f'''# SWELL Vending

> SWELL makes vending machines that blend fresh protein smoothies and shakes to order. A SWELL cup is 16 oz with 30g protein; a SWOLL cup is 24 oz with 50g protein. Machines are placed in gyms, high schools, colleges, hotels and offices, starting in Utah County, Utah.

## Key facts
- Machine size: 16.9 in wide x 34.3 in deep x 76.2 in tall (428 x 872 x 1935 mm), on casters
- Ordering by touchscreen, tap-to-pay for cards and phone wallets, cup window at 36.4 in
- Programs: Host (free placement, revenue share), Own (purchase), Lease (monthly)
- Shake flavors: {', '.join(n for _, n, _ in SHAKES)}
- Smoothie flavors: {', '.join(n for _, n, _ in SMOOTHIES)}
- Every cup has collagen peptides, colostrum and iron. Contains milk.

## Pages
''' + ''.join(f'- [{t}]({SITE_URL}{u})\n' for u, t in [('', 'Home'), ('machine.html', 'The machine'), ('menu.html', 'Menu'), ('locations.html', 'Locations'), ('about.html', 'About'), ('faq.html', 'FAQ'), ('refer.html', 'Refer a location')]))
open(os.path.join(ROOT, 'README.md'), 'w').write('''# SWELL Vending

Site for SWELL protein smoothie and shake vending machines (SWELL 30g / SWOLL 50g).
Separate from the SWELL bottle site (pdrayday.github.io/swell), which it only borrows the brand from.

## Edit
Pages are generated from `src/build.py` (shared header, footer, menu, forms). Edit there, then run:

    python3 src/build.py

## Before launch
- Connect the two forms (site survey, referral) to an inbox or CRM. They only show a thank-you today.
- Replace sample prices, program terms, referral reward and machine locations.
- Swap the cup photos for your own product shots (the current cups are a rebranded stock-style photo).
- Confirm power and water specs for the machine.
- Update `SITE_URL` in `src/build.py` if the domain changes.
''')

# artifact entry: page body without the document wrapper (the host adds its own)
m = re.search(r'<head>(.*)</head>\s*<body>(.*)</body>', index, re.S)
headin = m.group(1)
keep = '\n'.join(l for l in headin.splitlines() if l.startswith(('<title', '<meta name="claude', '<link rel="stylesheet', '<link rel="preload')))
open(os.path.join(ROOT, 'artifact-home.html'), 'w').write(keep + '\n' + m.group(2))
print('built')
