/**
 * AGYOS Particle Animation System
 * Cinematic Canvas 2D — cursor-reactive orbital particles
 * Performance: RAF-based, DPR-aware, reduced-motion safe, offscreen pause
 */

(function () {
  'use strict';

  // ---- Configuration ----
  const CONFIG = {
    particleCount: 90,
    orbitRings: 3,
    baseRadius: [110, 185, 260],
    particlesPerRing: [18, 26, 34],
    dotSizes: [1.2, 1.8, 2.4],
    lumens: [0.9, 0.55, 0.3],
    orbitSpeeds: [0.00028, -0.00018, 0.00012],
    noiseAmplitude: 22,
    noiseFrequency: 0.0012,
    mouseInfluenceRadius: 180,
    mouseRepelStrength: 0.42,
    springBack: 0.07,
    damping: 0.82,
    colorDark: { r: 245, g: 245, b: 247 },
    colorLight: { r: 10, g: 10, b: 10 },
    fps: 60,
  };

  // ---- State ----
  let canvas, ctx, animId;
  let particles = [];
  let mouse = { x: -9999, y: -9999 };
  let center = { x: 0, y: 0 };
  let isDark = false;
  let isReduced = false;
  let time = 0;
  let lastFrame = 0;
  let isVisible = true;

  // ---- Noise helper (simple 2D smooth) ----
  function smoothNoise(x, y, t) {
    return (Math.sin(x * 1.3 + t * 0.7) * Math.cos(y * 0.9 + t * 0.5) +
            Math.sin(x * 0.7 - t * 0.4) * Math.sin(y * 1.1 + t * 0.3)) * 0.5;
  }

  // ---- Particle factory ----
  function createParticle(ringIndex, indexInRing, totalInRing) {
    const baseAngle = (indexInRing / totalInRing) * Math.PI * 2;
    return {
      ring: ringIndex,
      baseAngle,
      angle: baseAngle + Math.random() * 0.3,
      radius: CONFIG.baseRadius[ringIndex] + (Math.random() - 0.5) * 24,
      size: CONFIG.dotSizes[ringIndex] * (0.7 + Math.random() * 0.6),
      alpha: CONFIG.lumens[ringIndex] * (0.5 + Math.random() * 0.5),
      alphaBase: CONFIG.lumens[ringIndex] * (0.5 + Math.random() * 0.5),
      vx: 0,
      vy: 0,
      ox: 0,
      oy: 0,
      noiseOffsetX: Math.random() * 1000,
      noiseOffsetY: Math.random() * 1000,
      noisePhase: Math.random() * Math.PI * 2,
      pulsePhase: Math.random() * Math.PI * 2,
    };
  }

  function buildParticles() {
    particles = [];
    for (let r = 0; r < CONFIG.orbitRings; r++) {
      const count = CONFIG.particlesPerRing[r];
      for (let i = 0; i < count; i++) {
        particles.push(createParticle(r, i, count));
      }
    }
    // scatter dots (ambient field)
    for (let i = 0; i < 12; i++) {
      particles.push({
        ring: -1,
        angle: Math.random() * Math.PI * 2,
        radius: 60 + Math.random() * 320,
        size: 0.8 + Math.random() * 0.9,
        alpha: 0.08 + Math.random() * 0.14,
        alphaBase: 0.08 + Math.random() * 0.14,
        vx: 0, vy: 0, ox: 0, oy: 0,
        noiseOffsetX: Math.random() * 1000,
        noiseOffsetY: Math.random() * 1000,
        noisePhase: Math.random() * Math.PI * 2,
        pulsePhase: Math.random() * Math.PI * 2,
      });
    }
  }

  // ---- Resize ----
  function resize() {
    if (!canvas) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    center.x = rect.width / 2;
    center.y = rect.height / 2;

    // Adapt ring radii to screen
    const minDim = Math.min(rect.width, rect.height);
    CONFIG.baseRadius[0] = minDim * 0.14;
    CONFIG.baseRadius[1] = minDim * 0.235;
    CONFIG.baseRadius[2] = minDim * 0.33;
    buildParticles();
  }

  // ---- Colour helper ----
  function particleColor(alpha) {
    const c = isDark ? CONFIG.colorDark : CONFIG.colorLight;
    return `rgba(${c.r},${c.g},${c.b},${alpha})`;
  }

  // ---- Draw frame ----
  function draw(ts) {
    if (!ctx || !canvas) return;

    // Frame rate cap
    const delta = ts - lastFrame;
    if (delta < 1000 / CONFIG.fps - 1) {
      animId = requestAnimationFrame(draw);
      return;
    }
    lastFrame = ts;

    if (!isVisible || isReduced) {
      animId = requestAnimationFrame(draw);
      return;
    }

    const rect = canvas.getBoundingClientRect();
    const W = rect.width;
    const H = rect.height;
    time += delta * 0.001;

    ctx.clearRect(0, 0, W, H);

    // Draw orbital ring halos (very faint)
    for (let r = 0; r < CONFIG.orbitRings; r++) {
      ctx.beginPath();
      ctx.arc(center.x, center.y, CONFIG.baseRadius[r], 0, Math.PI * 2);
      ctx.strokeStyle = particleColor(0.04);
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // Update & draw particles
    for (const p of particles) {
      // Orbital movement
      const speed = p.ring >= 0 ? CONFIG.orbitSpeeds[p.ring] : 0.00008;
      p.angle += speed * delta;

      // Noise displacement
      const nx = smoothNoise(p.noiseOffsetX, time * 0.6, p.noisePhase);
      const ny = smoothNoise(p.noiseOffsetY, time * 0.6, p.noisePhase + 1.57);
      const noiseX = nx * CONFIG.noiseAmplitude;
      const noiseY = ny * CONFIG.noiseAmplitude;

      // Base position
      const r = p.ring >= 0 ? CONFIG.baseRadius[p.ring] : p.radius;
      const bx = center.x + Math.cos(p.angle) * r + noiseX;
      const by = center.y + Math.sin(p.angle) * r + noiseY;

      // Mouse interaction
      const dx = bx - mouse.x;
      const dy = by - mouse.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const influence = Math.max(0, 1 - dist / CONFIG.mouseInfluenceRadius);
      const repelX = influence > 0 ? (dx / dist) * influence * CONFIG.mouseRepelStrength * CONFIG.mouseInfluenceRadius * 0.3 : 0;
      const repelY = influence > 0 ? (dy / dist) * influence * CONFIG.mouseRepelStrength * CONFIG.mouseInfluenceRadius * 0.3 : 0;

      // Spring physics
      const targetX = bx + repelX;
      const targetY = by + repelY;
      p.vx += (targetX - (bx + p.ox)) * CONFIG.springBack;
      p.vy += (targetY - (by + p.oy)) * CONFIG.springBack;
      p.vx *= CONFIG.damping;
      p.vy *= CONFIG.damping;
      p.ox += p.vx;
      p.oy += p.vy;

      const px = bx + p.ox - bx;
      const py = by + p.oy - by;
      const finalX = bx + (px - bx) * 0.3;
      const finalY = by + (py - by) * 0.3;

      // Pulse alpha
      const pulse = 0.5 + 0.5 * Math.sin(time * 1.4 + p.pulsePhase);
      const alpha = p.alphaBase * (0.75 + 0.25 * pulse) * (1 + influence * 0.6);

      // Draw dot
      ctx.beginPath();
      ctx.arc(finalX, finalY, p.size, 0, Math.PI * 2);
      ctx.fillStyle = particleColor(Math.min(1, alpha));
      ctx.fill();

      // Glow halo on hover
      if (influence > 0.1) {
        ctx.beginPath();
        ctx.arc(finalX, finalY, p.size * 3, 0, Math.PI * 2);
        ctx.fillStyle = particleColor(0.06 * influence);
        ctx.fill();
      }
    }

    // Central cluster glow
    const grad = ctx.createRadialGradient(center.x, center.y, 0, center.x, center.y, 55);
    const c = isDark ? CONFIG.colorDark : CONFIG.colorLight;
    grad.addColorStop(0, `rgba(${c.r},${c.g},${c.b},0.06)`);
    grad.addColorStop(1, `rgba(${c.r},${c.g},${c.b},0)`);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    animId = requestAnimationFrame(draw);
  }

  // ---- Init ----
  function init() {
    canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    isReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    isDark = document.documentElement.dataset.theme === 'dark';

    resize();

    // Mouse tracking
    function trackMouse(e) {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    }
    function trackTouch(e) {
      if (e.touches.length > 0) {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.touches[0].clientX - rect.left;
        mouse.y = e.touches[0].clientY - rect.top;
      }
    }
    function clearMouse() {
      mouse.x = -9999;
      mouse.y = -9999;
    }

    window.addEventListener('mousemove', trackMouse, { passive: true });
    window.addEventListener('touchmove', trackTouch, { passive: true });
    window.addEventListener('mouseleave', clearMouse, { passive: true });
    window.addEventListener('touchend', clearMouse, { passive: true });

    // Resize
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(resize, 150);
    }, { passive: true });

    // Visibility
    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver(entries => {
        isVisible = entries[0].isIntersecting;
      }, { threshold: 0 });
      obs.observe(canvas);
    }

    // Theme changes
    const themeObserver = new MutationObserver(() => {
      isDark = document.documentElement.dataset.theme === 'dark';
    });
    themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    // Reduced motion
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', e => {
      isReduced = e.matches;
    });

    lastFrame = performance.now();
    animId = requestAnimationFrame(draw);
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export for cleanup if needed
  window.AGYOS_Particles = { stop: () => cancelAnimationFrame(animId) };
})();
