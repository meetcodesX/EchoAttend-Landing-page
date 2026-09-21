/* ==========================================================================
   ECHOATTEND — SCRIPT
   Preloader · custom cursor · scroll progress · nav behaviour · reveal
   animations · animated counters · FAQ accordion · magnetic buttons ·
   particle field · mouse parallax · typing animation · demo modal
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- footer year ---------- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- preloader ---------- */
  const preloader = document.getElementById('preloader');
  window.addEventListener('load', () => {
    setTimeout(() => preloader && preloader.classList.add('is-hidden'), 400);
  });
  // Fallback in case 'load' already fired
  setTimeout(() => preloader && preloader.classList.add('is-hidden'), 2500);

  /* ---------- custom cursor ---------- */
  const cursorDot = document.getElementById('cursorDot');
  const cursorRing = document.getElementById('cursorRing');
  const isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;

  if (!isTouch && cursorDot && cursorRing) {
    let ringX = 0, ringY = 0, targetX = 0, targetY = 0;

    window.addEventListener('mousemove', (e) => {
      targetX = e.clientX; targetY = e.clientY;
      cursorDot.style.left = `${e.clientX}px`;
      cursorDot.style.top = `${e.clientY}px`;
    });

    const animateRing = () => {
      ringX += (targetX - ringX) * 0.18;
      ringY += (targetY - ringY) * 0.18;
      cursorRing.style.left = `${ringX}px`;
      cursorRing.style.top = `${ringY}px`;
      requestAnimationFrame(animateRing);
    };
    animateRing();

    document.querySelectorAll('a, button, .faq-question').forEach((el) => {
      el.addEventListener('mouseenter', () => cursorRing.style.width = cursorRing.style.height = '54px');
      el.addEventListener('mouseleave', () => cursorRing.style.width = cursorRing.style.height = '34px');
    });
  }

  /* ---------- scroll progress + navbar state ---------- */
  const scrollProgress = document.getElementById('scrollProgress');
  const navbar = document.getElementById('navbar');
  const backToTop = document.getElementById('backToTop');

  const onScroll = () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    if (scrollProgress) scrollProgress.style.width = `${pct}%`;

    if (navbar) navbar.classList.toggle('scrolled', scrollTop > 40);
    if (backToTop) backToTop.classList.toggle('visible', scrollTop > 500);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  backToTop && backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---------- mobile nav toggle ---------- */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  navToggle && navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    navToggle.classList.toggle('active');
  });
  document.querySelectorAll('.nav-link').forEach((link) => {
    link.addEventListener('click', () => navLinks && navLinks.classList.remove('open'));
  });

  /* ---------- active nav link on scroll ---------- */
  const sections = document.querySelectorAll('main section[id], .hero[id]');
  const navAnchors = document.querySelectorAll('.nav-link');
  const navObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navAnchors.forEach((a) => a.classList.toggle('active', a.getAttribute('href') === `#${entry.target.id}`));
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  sections.forEach((s) => navObserver.observe(s));

  /* ---------- scroll reveal ---------- */
  const revealEls = document.querySelectorAll('.reveal-up');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach((el) => revealObserver.observe(el));

  /* ---------- animated counters ---------- */
  const counters = document.querySelectorAll('[data-counter]');
  const animateCounter = (el) => {
    const target = parseFloat(el.dataset.target);
    const decimals = parseInt(el.dataset.decimals || '0', 10);
    const duration = 1600;
    const start = performance.now();

    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = target * eased;
      el.firstChild.nodeType === 3
        ? (el.firstChild.textContent = value.toFixed(decimals))
        : (el.textContent = value.toFixed(decimals));
      if (progress < 1) requestAnimationFrame(step);
      else (el.firstChild && el.firstChild.nodeType === 3)
        ? (el.firstChild.textContent = target.toFixed(decimals))
        : (el.textContent = target.toFixed(decimals));
    };
    requestAnimationFrame(step);
  };

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });
  counters.forEach((c) => counterObserver.observe(c));

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll('.faq-item').forEach((item) => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach((el) => el.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });

  /* ---------- magnetic buttons ---------- */
  if (!isTouch) {
    document.querySelectorAll('.magnetic').forEach((btn) => {
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x * 0.18}px, ${y * 0.35}px)`;
      });
      btn.addEventListener('mouseleave', () => { btn.style.transform = 'translate(0,0)'; });
    });
  }

  /* ---------- hero mouse parallax ---------- */
  const heroVisual = document.getElementById('heroVisual');
  if (heroVisual && !isTouch) {
    document.querySelector('.hero').addEventListener('mousemove', (e) => {
      const rect = heroVisual.getBoundingClientRect();
      const relX = (e.clientX - rect.left - rect.width / 2) / rect.width;
      const relY = (e.clientY - rect.top - rect.height / 2) / rect.height;
      heroVisual.style.transform = `translate(${relX * 14}px, ${relY * 14}px)`;
    });
  }

  /* ---------- typing animation ---------- */
  const typedWord = document.getElementById('typedWord');
  if (typedWord) {
    const words = ['Reimagined', 'Automated', 'Effortless', 'Instant'];
    let wordIndex = 0, charIndex = words[0].length, deleting = false;

    const type = () => {
      const current = words[wordIndex];
      if (!deleting) {
        charIndex++;
        if (charIndex > current.length) { deleting = true; setTimeout(type, 1800); return; }
      } else {
        charIndex--;
        if (charIndex < 1) { deleting = false; wordIndex = (wordIndex + 1) % words.length; }
      }
      typedWord.textContent = current.slice(0, charIndex);
      setTimeout(type, deleting ? 45 : 90);
    };
    setTimeout(type, 2200);
  }

  /* ---------- demo modal ---------- */
  const demoModal = document.getElementById('demoModal');
  const watchDemoBtn = document.getElementById('watchDemoBtn');
  const demoModalClose = document.getElementById('demoModalClose');
  const demoModalBackdrop = document.getElementById('demoModalBackdrop');

  const openModal = () => demoModal && demoModal.classList.add('open');
  const closeModal = () => demoModal && demoModal.classList.remove('open');

  watchDemoBtn && watchDemoBtn.addEventListener('click', openModal);
  demoModalClose && demoModalClose.addEventListener('click', closeModal);
  demoModalBackdrop && demoModalBackdrop.addEventListener('click', closeModal);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

  /* ---------- particle field ---------- */
  const canvas = document.getElementById('particleCanvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let particles = [];
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = document.documentElement.scrollHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    const PARTICLE_COUNT = reduceMotion ? 0 : 46;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.6 + 0.4,
        vy: Math.random() * 0.25 + 0.05,
        alpha: Math.random() * 0.4 + 0.1
      });
    }

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach((p) => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(140,130,255,${p.alpha})`;
        ctx.fill();
        p.y -= p.vy;
        if (p.y < -10) p.y = canvas.height + 10;
      });
      requestAnimationFrame(draw);
    };
    if (PARTICLE_COUNT > 0) draw();
  }

  /* ---------- smooth in-page anchor scroll (offset for sticky nav) ---------- */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const id = anchor.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      const offset = 84;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

});

/* =========================
   DEMO VIDEO MODAL
========================= */

const demoDialog = document.getElementById("demoDialog");
const watchDemoBtn = document.getElementById("watchDemoBtn");
const demoClose = document.getElementById("demoClose");
const demoVideo = document.getElementById("demoVideo");

if (watchDemoBtn && demoDialog) {

    watchDemoBtn.addEventListener("click", () => {

        demoDialog.showModal();

        demoVideo.currentTime = 0;

        demoVideo.play().catch(() => {
            // User can press play manually if autoplay is blocked
        });

    });

}

if (demoClose) {

    demoClose.addEventListener("click", () => {

        demoVideo.pause();
        demoVideo.currentTime = 0;

        demoDialog.close();

    });

}

/* Close when clicking outside modal */
if (demoDialog) {

    demoDialog.addEventListener("click", (event) => {

        const rect = demoDialog.getBoundingClientRect();

        const clickedInside =
            event.clientX >= rect.left &&
            event.clientX <= rect.right &&
            event.clientY >= rect.top &&
            event.clientY <= rect.bottom;

        if (!clickedInside) {

            demoVideo.pause();
            demoVideo.currentTime = 0;

            demoDialog.close();

        }

    });

}