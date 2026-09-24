/* Direwolf Space Systems — site behaviour (progressive enhancement only) */
(function () {
  'use strict';

  document.documentElement.classList.add('js');
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    var closeNav = function () {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    };
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { closeNav(); toggle.focus(); }
    });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeNav); });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1020 && nav.classList.contains('is-open')) closeNav();
    });
  }

  /* ---------- Mark the current page in the nav ---------- */
  var here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  document.querySelectorAll('.nav__link').forEach(function (a) {
    var target = (a.getAttribute('href') || '').split('#')[0].toLowerCase();
    if (target === here) a.setAttribute('aria-current', 'page');
  });

  /* ---------- Reveal on scroll ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && 'IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Hero: live star layer (twinkle) + parallax ---------- */
  var hero = document.querySelector('.hero');
  var canvas = hero && hero.querySelector('.hero__stars');
  var space = hero && hero.querySelector('.hero__space');
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext('2d');
    var stars = [];
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var seed = 1337;
    var rand = function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
    var W = 0, H = 0;
    var build = function () {
      W = canvas.clientWidth; H = canvas.clientHeight;
      canvas.width = Math.floor(W * dpr); canvas.height = Math.floor(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed = 1337; stars = [];
      var count = Math.floor((W * H) / 7000);
      for (var i = 0; i < count; i++) {
        stars.push({
          x: rand() * W, y: rand() * H * 0.82, r: rand() * 1.0 + 0.25,
          a: rand() * 0.5 + 0.15, ph: rand() * Math.PI * 2, sp: 0.6 + rand() * 1.6
        });
      }
    };
    var paint = function (t) {
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        var tw = reduceMotion ? 1 : 0.65 + 0.35 * Math.sin(t * 0.001 * s.sp + s.ph);
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(214, 226, 245,' + (s.a * tw).toFixed(3) + ')';
        ctx.fill();
      }
    };
    var running = false, last = 0;
    var frame = function (t) {
      if (!running) return;
      if (t - last > 50) { paint(t); last = t; }
      requestAnimationFrame(frame);
    };
    var start = function () { if (!running) { running = true; requestAnimationFrame(frame); } };
    var stop = function () { running = false; };
    build(); paint(0);
    if (!reduceMotion) {
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (e) { e.isIntersecting ? start() : stop(); });
        }, { threshold: 0 }).observe(hero);
      } else { start(); }
      document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    }
    var rt;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { build(); paint(last); }, 120); });

    if (space && !reduceMotion) {
      var ticking = false;
      var onScroll = function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
          var y = window.scrollY || window.pageYOffset;
          var h = hero.offsetHeight || 1;
          if (y < h) {
            var p = Math.min(y, h) * 0.18;
            space.style.transform = 'translate3d(0,' + p.toFixed(1) + 'px,0) scale(1.06)';
            canvas.style.transform = 'translate3d(0,' + (p * 0.5).toFixed(1) + 'px,0)';
          }
          ticking = false;
        });
      };
      space.style.transform = 'scale(1.06)';
      window.addEventListener('scroll', onScroll, { passive: true });
    }
  }

  /* ---------- Cards: cursor spotlight ---------- */
  var cards = document.querySelectorAll('.card');
  if (cards.length && window.matchMedia && window.matchMedia('(hover: hover)').matches) {
    cards.forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* ---------- Typewriter reveal for [data-type] ---------- */
  var typeEls = document.querySelectorAll('[data-type]');
  if (typeEls.length && !reduceMotion && 'IntersectionObserver' in window) {
    typeEls.forEach(function (el) {
      var full = el.textContent.trim();
      el.textContent = '';
      var sr = document.createElement('span'); sr.className = 'visually-hidden'; sr.textContent = full;
      var vis = document.createElement('span'); vis.setAttribute('aria-hidden', 'true');
      var caret = document.createElement('span'); caret.className = 'type-caret'; caret.setAttribute('aria-hidden', 'true');
      el.appendChild(sr); el.appendChild(vis); el.appendChild(caret);
      var started = false;
      var run = function () {
        if (started) return;
        started = true;
        var i = 0;
        var step = function () {
          i += 1 + (Math.random() < 0.3 ? 1 : 0);
          vis.textContent = full.slice(0, i);
          if (i < full.length) setTimeout(step, 18 + Math.random() * 30);
          else caret.classList.add('is-done');
        };
        setTimeout(step, 250);
      };
      var obs = new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting) return;
        obs.disconnect();
        run();
      }, { threshold: 0.4 });
      obs.observe(el);
      // Safety net: never leave the block empty if the observer does not fire.
      setTimeout(function () { if (!started) { started = true; vis.textContent = full; caret.classList.add('is-done'); } }, 12000);
    });
  }

  /* ---------- Contact form: submit to the form relay without leaving the page ---------- */
  var form = document.getElementById('contact-form');
  if (form) {
    var status = document.getElementById('form-status');
    var endpoint = form.getAttribute('data-endpoint');
    var fallback = 'contact@direwolfspace.com';
    var say = function (msg) { if (status) status.textContent = msg; };
    try {
      if (new URLSearchParams(window.location.search).get('sent') === '1') {
        say('Thank you. Your inquiry has been sent, and we will reply by email.');
      }
    } catch (err) { /* ignore */ }
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !endpoint) return; /* no fetch: let the browser post the form normally */
      if (!form.checkValidity()) { e.preventDefault(); form.reportValidity(); return; }
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      var topic = data.topic || 'General inquiry';
      data._subject = '[' + topic + '] ' + (data.organization || data.name || 'Website inquiry');
      if (btn) btn.disabled = true;
      say('Sending your inquiry.');
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json().then(function (body) { return { ok: r.ok, body: body }; }); })
        .then(function (res) {
          var ok = res.ok && (res.body.success === 'true' || res.body.success === true);
          if (!ok) throw new Error(res.body && res.body.message ? res.body.message : 'Submission failed');
          form.reset();
          say('Thank you. Your inquiry has been sent, and we will reply by email.');
        })
        .catch(function () {
          say('The form could not be sent. Please email ' + fallback + ' directly.');
        })
        .then(function () { if (btn) btn.disabled = false; });
    });
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    var y = new Date().getFullYear();
    if (y > 2026) el.textContent = String(y);
  });
})();
