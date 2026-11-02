/**
 * ScrollHeart — Example Output JavaScript
 * GSAP ScrollTrigger animations, audio controller, and scroll progress.
 *
 * Dependencies:
 * - GSAP 3.13+ (loaded from CDN)
 * - ScrollTrigger plugin (loaded from CDN)
 */

(function () {
  'use strict';

  // ============================================
  // 1. GSAP Setup
  // ============================================
  gsap.registerPlugin(ScrollTrigger);

  // ============================================
  // 2. Reduced Motion Detection
  // ============================================
  const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
  ).matches;

  // ============================================
  // 3. DOM References
  // ============================================
  const overlay = document.getElementById('intro-overlay');
  const beginBtn = document.getElementById('begin-btn');
  const audio = document.getElementById('bg-audio');
  const audioControls = document.getElementById('audio-controls');
  const audioToggle = document.getElementById('audio-toggle');
  const audioIcon = audioToggle.querySelector('.audio-icon');
  const progressFill = document.getElementById('progress-fill');
  const replayBtn = document.getElementById('replay-btn');
  const audioToast = document.getElementById('audio-toast');

  let isPlaying = false;

  function showAudioToast() {
    if (audioToast) {
      audioToast.classList.remove('hidden');
      setTimeout(function () {
        audioToast.classList.add('hidden');
      }, 5000);
    }
  }

  // ============================================
  // 4. Overlay & Audio Controller
  // ============================================
  beginBtn.addEventListener('click', function () {
    // Dismiss overlay
    overlay.classList.add('hidden');
    audioControls.classList.add('visible');

    // Attempt audio playback (requires user gesture)
    audio.volume = 0.5;
    audio.play()
      .then(function () {
        isPlaying = true;
        audioIcon.textContent = '🔊';
      })
      .catch(function () {
        // Audio failed — degrade gracefully
        isPlaying = false;
        audioIcon.textContent = '🔇';
        showAudioToast();
      });

    // Refresh ScrollTrigger after overlay hides
    setTimeout(function () {
      ScrollTrigger.refresh();
    }, 900);
  });

  // Audio toggle button
  audioToggle.addEventListener('click', function () {
    if (isPlaying) {
      audio.pause();
      isPlaying = false;
      audioIcon.textContent = '🔇';
    } else {
      audio.play()
        .then(function () {
          isPlaying = true;
          audioIcon.textContent = '🔊';
        })
        .catch(function () {
          audioIcon.textContent = '🔇';
          showAudioToast();
        });
    }
  });

  // ============================================
  // 5. Scroll Progress Bar
  // ============================================
  ScrollTrigger.create({
    trigger: 'main',
    start: 'top top',
    end: 'bottom bottom',
    onUpdate: function (self) {
      progressFill.style.width = (self.progress * 100) + '%';
    },
  });

  // ============================================
  // 6. Replay Button
  // ============================================
  if (replayBtn) {
    replayBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'instant' });
      // Re-enable all text animations
      setTimeout(function () {
        ScrollTrigger.refresh();
      }, 100);
    });
  }

  // ============================================
  // 7. Animations (Skip if reduced motion)
  // ============================================
  if (!prefersReducedMotion) {
    initParallaxAnimations();
    initTextAnimations();
    initSceneSpecificAnimations();
  } else {
    // Show all content immediately
    document.querySelectorAll('.scene-text, .climax-card, .signature, .replay-button').forEach(function (el) {
      el.style.opacity = '1';
    });
    if (replayBtn) {
      replayBtn.classList.add('visible');
    }
  }

  // ============================================
  // 8. Parallax Layer Animations
  // ============================================
  function initParallaxAnimations() {
    var mm = gsap.matchMedia();

    mm.add('(min-width: 1px)', function () {
      // Background layers — slowest (0.2x feel)
      gsap.utils.toArray('.bg-layer').forEach(function (layer) {
        gsap.to(layer, {
          yPercent: -15,
          ease: 'none',
          scrollTrigger: {
            trigger: layer.parentElement,
            start: 'top bottom',
            end: 'bottom top',
            scrub: true,
          },
        });
      });

      // Midground layers — moderate (0.5x feel)
      gsap.utils.toArray('.mid-layer').forEach(function (layer) {
        gsap.to(layer, {
          yPercent: -8,
          ease: 'none',
          scrollTrigger: {
            trigger: layer.parentElement,
            start: 'top bottom',
            end: 'bottom top',
            scrub: true,
          },
        });
      });

      // Foreground layers — fastest (1.5x feel)
      gsap.utils.toArray('.fg-layer').forEach(function (layer) {
        gsap.to(layer, {
          yPercent: 10,
          ease: 'none',
          scrollTrigger: {
            trigger: layer.parentElement,
            start: 'top bottom',
            end: 'bottom top',
            scrub: true,
          },
        });
      });
    });
  }

  // ============================================
  // 9. Text Entrance Animations & Accessibility
  // ============================================
  function initTextAnimations() {
    // Accessibility: Dynamically toggle aria-hidden based on scroll position
    // so screen readers pace the story exactly like sighted users.
    var allTextElements = document.querySelectorAll('.scene-text, .climax-card, .signature');
    allTextElements.forEach(function (el) {
      el.setAttribute('aria-hidden', 'true');
      ScrollTrigger.create({
        trigger: el,
        start: 'top 90%',
        end: 'bottom 10%',
        onEnter: function () { el.removeAttribute('aria-hidden'); },
        onLeave: function () { el.setAttribute('aria-hidden', 'true'); },
        onEnterBack: function () { el.removeAttribute('aria-hidden'); },
        onLeaveBack: function () { el.setAttribute('aria-hidden', 'true'); },
      });
    });

    // Scene 1 — fade up (gentle intro)
    var scene1Text = document.querySelector('#scene-1 .scene-text');
    if (scene1Text) {
      gsap.from(scene1Text, {
        y: 40,
        opacity: 0,
        duration: 2,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: scene1Text,
          start: 'top 80%',
          toggleActions: 'play none none reverse',
        },
      });
    }

    // Scene 2 — horizontal drift
    var scene2Text = document.querySelector('#scene-2 .scene-text');
    if (scene2Text) {
      gsap.from(scene2Text, {
        x: -50,
        opacity: 0,
        duration: 1.8,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: scene2Text,
          start: 'top 80%',
          toggleActions: 'play none none reverse',
        },
      });
    }

    // Scene 3 — climax card scale up
    var climaxCard = document.querySelector('.climax-card');
    if (climaxCard) {
      gsap.from(climaxCard, {
        scale: 0.85,
        opacity: 0,
        duration: 2,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: climaxCard,
          start: 'top 75%',
          toggleActions: 'play none none reverse',
        },
      });
    }

    // Scene 4 — gentle fade (no spatial movement — quiet scene)
    var scene4Text = document.querySelector('#scene-4 .scene-text');
    if (scene4Text) {
      gsap.from(scene4Text, {
        opacity: 0,
        duration: 2.5,
        ease: 'power1.inOut',
        scrollTrigger: {
          trigger: scene4Text,
          start: 'top 80%',
          toggleActions: 'play none none reverse',
        },
      });
    }

    // Scene 5 — outro text and elements
    var scene5Text = document.querySelector('#scene-5 .scene-text');
    var signature = document.querySelector('.signature');

    if (scene5Text) {
      gsap.from(scene5Text, {
        y: 20,
        opacity: 0,
        duration: 1.5,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: scene5Text,
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        },
      });
    }

    if (replayBtn) {
      gsap.from(replayBtn, {
        opacity: 0,
        duration: 1,
        delay: 0.5,
        ease: 'power1.inOut',
        scrollTrigger: {
          trigger: replayBtn,
          start: 'top 90%',
          toggleActions: 'play none none reverse',
          onEnter: function () {
            replayBtn.classList.add('visible');
          },
        },
      });
    }

    if (signature) {
      gsap.from(signature, {
        opacity: 0,
        duration: 1.5,
        delay: 1,
        ease: 'power1.inOut',
        scrollTrigger: {
          trigger: signature,
          start: 'top 90%',
          toggleActions: 'play none none reverse',
        },
      });
    }
  }

  // ============================================
  // 10. Scene-Specific Animations
  // ============================================
  function initSceneSpecificAnimations() {
    // Scene 3 — Light rays fade in
    gsap.utils.toArray('.ray').forEach(function (ray, i) {
      gsap.to(ray, {
        opacity: 0.4,
        duration: 2,
        delay: i * 0.2,
        ease: 'power1.inOut',
        scrollTrigger: {
          trigger: '#scene-3',
          start: 'top 60%',
          toggleActions: 'play none none reverse',
        },
      });
    });

    // Scene 4 — Shooting star animation (one-shot)
    var shootingStar = document.querySelector('.shooting-star');
    if (shootingStar) {
      ScrollTrigger.create({
        trigger: '#scene-4',
        start: 'top 50%',
        once: true,
        onEnter: function () {
          gsap.timeline()
            .to(shootingStar, {
              opacity: 0.8,
              x: '120vw',
              duration: 1.2,
              ease: 'power2.in',
            })
            .to(shootingStar, {
              opacity: 0,
              duration: 0.3,
            });
        },
      });
    }
  }

  // ============================================
  // 11. Cleanup
  // ============================================
  window.addEventListener('beforeunload', function () {
    ScrollTrigger.getAll().forEach(function (t) {
      t.kill();
    });
  });

})();
