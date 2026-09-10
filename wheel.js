/* Zodiacs wheel — rotates the ring so the selected sign sits at the top,
   updates the centre character, auto-advances every few seconds. */
(function () {
  const SIGNS = window.ZODIAC.signs;
  const STEP = 30;                 // degrees between badges
  const INTERVAL = 3200;           // ms between auto-advances

  const ring = document.getElementById('ring');
  const glyph = document.getElementById('glyph');
  const who = document.getElementById('who');
  const pill = document.getElementById('pill');
  const open = document.getElementById('open');
  const playBtn = document.getElementById('play');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');

  // Build the 12 badges. Each badge is a real link to its page.
  const badges = SIGNS.map((s, i) => {
    const a = document.createElement('a');
    a.className = 'badge';
    a.href = s.id + '.html';
    a.style.setProperty('--c', s.color);
    a.style.setProperty('--ci', s.ink);
    a.setAttribute('aria-label', s.name + ', ' + s.dates);
    a.innerHTML = '<span class="b sym">' + s.glyph + '</span><span class="a">' + s.name + '</span>';
    a.addEventListener('mouseenter', () => { show(i, false); pause(); });
    a.addEventListener('focus', () => { show(i, false); pause(); });
    ring.appendChild(a);
    return a;
  });

  // Start on today's sign, unless the URL says otherwise.
  const fromHash = SIGNS.findIndex(s => '#' + s.id === location.hash);
  let index = fromHash >= 0 ? fromHash : signForNow();
  let rotation = 0;
  let timer = null;
  let playing = true;

  function signForNow() {
    // The sign whose date range contains today. Capricorn (Dec 22) wraps across New Year.
    const d = new Date(), today = (d.getMonth() + 1) * 100 + d.getDate();
    let best = -1, bestKey = -1;
    SIGNS.forEach((s, k) => {
      const key = s.startMonth * 100 + s.startDay;
      if (key <= today && key > bestKey) { best = k; bestKey = key; }
    });
    return best >= 0 ? best : SIGNS.findIndex(s => s.id === 'capricorn');
  }

  function layout() {
    badges.forEach((b, i) => {
      const angle = -90 + i * STEP;               // Aries starts at 12 o'clock
      const rad = angle * Math.PI / 180;
      b.style.left = 'calc(50% + ' + Math.cos(rad).toFixed(4) + ' * var(--R))';
      b.style.top = 'calc(50% + ' + Math.sin(rad).toFixed(4) + ' * var(--R))';
      b.style.transform = 'rotate(' + (-rotation) + 'deg)';   // keep glyphs upright
    });
  }

  function show(i, animateText = true) {
    // shortest rotation to bring badge i to the top
    const target = -i * STEP;
    let delta = ((target - rotation) % 360 + 540) % 360 - 180;
    rotation += delta;
    index = i;
    ring.style.transform = 'rotate(' + rotation + 'deg)';
    layout();
    badges.forEach((b, k) => b.classList.toggle('is-active', k === i));

    const s = SIGNS[i];
    const paint = () => {
      glyph.textContent = s.glyph;
      who.innerHTML = s.name + '<span class="sub">' + s.symbol + '</span>';
      pill.textContent = s.dates;
      open.href = s.id + '.html';
      open.textContent = 'Read about ' + s.name;
      document.documentElement.style.setProperty('--accent', s.color);
      history.replaceState(null, '', '#' + s.id);
    };
    if (animateText && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
      glyph.classList.add('fade');
      setTimeout(() => { paint(); glyph.classList.remove('fade'); }, 180);
    } else paint();
  }

  function next() { show((index + 1) % SIGNS.length); }
  function prev() { show((index + SIGNS.length - 1) % SIGNS.length); }

  function play() {
    playing = true;
    playBtn.classList.remove('paused');
    playBtn.setAttribute('aria-label', 'Pause');
    clearInterval(timer);
    timer = setInterval(next, INTERVAL);
  }
  function pause() {
    playing = false;
    playBtn.classList.add('paused');
    playBtn.setAttribute('aria-label', 'Play');
    clearInterval(timer);
  }

  playBtn.addEventListener('click', () => (playing ? pause() : play()));
  nextBtn.addEventListener('click', () => { next(); if (playing) play(); });
  prevBtn.addEventListener('click', () => { prev(); if (playing) play(); });
  ring.addEventListener('mouseleave', () => { if (!playing && !document.activeElement.classList.contains('badge')) play(); });
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { next(); if (playing) play(); }
    if (e.key === 'ArrowLeft') { prev(); if (playing) play(); }
    if (e.key === ' ' && e.target === document.body) { e.preventDefault(); playing ? pause() : play(); }
  });
  document.addEventListener('visibilitychange', () => (document.hidden ? clearInterval(timer) : playing && play()));

  // Initial paint without animation, then start.
  ring.style.transition = 'none';
  badges.forEach(b => (b.style.transition = 'none'));
  show(index, false);
  requestAnimationFrame(() => requestAnimationFrame(() => {
    ring.style.transition = '';
    badges.forEach(b => (b.style.transition = ''));
  }));
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) play(); else pause();
})();
