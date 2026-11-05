/**
 * AGYOS Documentation App
 * Navigation, Search, Animations, Content, Interactions
 */

(function () {
  'use strict';

  // ============================================================
  // THEME
  // ============================================================
  const THEME_KEY = 'agyos-theme';

  function getTheme() {
    return localStorage.getItem(THEME_KEY) ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    updateThemeIcon(theme);
  }

  function updateThemeIcon(theme) {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    btn.innerHTML = theme === 'dark' ? '☀' : '☾';
  }

  function toggleTheme() {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  }

  // ============================================================
  // HEADER SCROLL EFFECT
  // ============================================================
  function initHeaderScroll() {
    const header = document.querySelector('.site-header');
    if (!header) return;
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          header.classList.toggle('scrolled', window.scrollY > 20);
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  // ============================================================
  // ACTIVE NAV LINK (scroll spy)
  // ============================================================
  function initScrollSpy() {
    const sections = Array.from(document.querySelectorAll('section[id]'));
    const navLinks = Array.from(document.querySelectorAll('.nav-link[href^="#"]'));
    if (!sections.length || !navLinks.length) return;

    const obs = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          navLinks.forEach(l => l.classList.remove('active'));
          const active = navLinks.find(l => l.getAttribute('href') === `#${entry.target.id}`);
          if (active) active.classList.add('active');
        }
      }
    }, { rootMargin: '-20% 0px -70% 0px' });

    sections.forEach(s => obs.observe(s));
  }

  // ============================================================
  // REVEAL ANIMATIONS (Intersection Observer)
  // ============================================================
  function initReveal() {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
      return;
    }

    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });

    document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
  }

  // ============================================================
  // ANIMATED COUNTER
  // ============================================================
  function animateCounter(el, target, duration = 1200) {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) { el.textContent = target; return; }

    const start = performance.now();
    const startVal = 0;
    const formatted = target.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');

    function update(ts) {
      const progress = Math.min((ts - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(startVal + (parseInt(target.toString().replace(/,/g, '')) - startVal) * eased);
      el.textContent = current.toLocaleString();
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = formatted;
    }

    requestAnimationFrame(update);
  }

  function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    if (!counters.length) return;

    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          animateCounter(el, el.dataset.count);
          obs.unobserve(el);
        }
      });
    }, { threshold: 0.4 });

    counters.forEach(el => obs.observe(el));
  }

  // ============================================================
  // COPY BUTTONS
  // ============================================================
  function initCopyButtons() {
    document.addEventListener('click', e => {
      const btn = e.target.closest('[data-copy], .copy-btn, .cli-copy');
      if (!btn) return;

      let text = '';
      if (btn.dataset.copy) {
        text = btn.dataset.copy;
      } else if (btn.closest('.code-block')) {
        const pre = btn.closest('.code-block').querySelector('pre code, pre');
        if (pre) text = pre.textContent;
      } else if (btn.closest('.cli-block')) {
        const cli = btn.closest('.cli-block').querySelector('.cli-text');
        if (cli) text = cli.textContent;
      }

      if (!text) return;

      navigator.clipboard.writeText(text.trim()).then(() => {
        const original = btn.textContent;
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
          btn.textContent = original;
          btn.classList.remove('copied');
        }, 1800);
      }).catch(() => {});
    });
  }

  // ============================================================
  // SEARCH ENGINE (client-side, full-text)
  // ============================================================
  const searchIndex = [];

  function buildSearchIndex(skillsData) {
    searchIndex.length = 0;

    // Static doc pages
    const staticPages = [
      { id: 'overview', title: 'Overview', category: 'Getting Started', excerpt: 'AGYOS is an autonomous cognitive agent operating system and physical catalog of 1,862+ modular engineering skills.' },
      { id: 'installation', title: 'Quickstart & Installation', category: 'Getting Started', excerpt: 'Install AGYOS with a single prompt. Paste the AGENTS.md content into your AI agent system prompt to activate all 1,862 skills.' },
      { id: 'architecture', title: 'System Architecture', category: 'Architecture', excerpt: 'AGYOS embeds LLM agents into a 6-layer hierarchical cognitive harness: Kernel, Memory, FastMCP, 5-Gate SOP, Agent Hierarchy, and Skills Catalog.' },
      { id: 'governance', title: '5-Gate Governance', category: 'Governance', excerpt: 'The AGYOS 5-Gate Workflow: UNDERSTAND → ANALYZE → PLAN → IMPLEMENT → VERIFY. Every multi-step task executes sequentially through 5 gates.' },
      { id: 'pods', title: '5 Corporate Pods', category: 'Architecture', excerpt: 'Five merged operational pods: pod-growth, pod-customer, pod-build, pod-gna, pod-people. Covers all 11 business functions.' },
      { id: 'decision', title: 'Decision Engine', category: 'Architecture', excerpt: 'System 1 autonomous skill discovery. Zero-slash natural language routing to the best matching skill in under 10ms.' },
      { id: 'security', title: 'Security & Dual Hooks', category: 'Security', excerpt: 'Fail-closed security hooks. Dual-hook architecture: agy_os_hook.py + authorizer.py. Zero-secret management, OWASP compliance.' },
      { id: 'vibe-faang', title: 'Vibe-to-FAANG Pipeline', category: 'Guides', excerpt: 'Transform natural language vibe prompts into FAANG-grade production code with TDD, type safety, and 80%+ test coverage.' },
      { id: 'council', title: 'Agent Council', category: 'Architecture', excerpt: 'Multi-model consensus deliberation. Convene independent model opinions and synthesize recommendations.' },
      { id: 'verification', title: 'Verification Suite', category: 'Reference', excerpt: '51-point adversarial verification suite. Run bash scripts/agyos-verify.sh to validate all checks.' },
      { id: 'skill-routing', title: 'Skill Routing', category: 'Reference', excerpt: 'Shared skill discovery and routing policy. Use bin/agyos decide or agyos_decision MCP for autonomous skill selection.' },
      { id: 'rules', title: 'Rules Catalog', category: 'Reference', excerpt: '141 modular governance rules organized by language and domain. Common rules plus language-specific extensions.' },
      { id: 'workflows', title: 'Native Workflows', category: 'Reference', excerpt: 'Deterministic multi-agent orchestration scripts. orch-review workflow for parallel code review with deduplication.' },
      { id: 'explorer', title: 'Skills Catalog Explorer', category: 'Reference', excerpt: '1,862 engineering skills across architecture, security, frontend, backend, ML, DevOps, and more.' },
      { id: 'cli', title: 'CLI Reference', category: 'Reference', excerpt: 'bin/agyos commands: init, verify, state, intent, decide, fast, council, skill.' },
      { id: 'adr-0001', title: 'ADR-0001: Skill Discovery Metadata', category: 'ADRs', excerpt: 'Architecture decision record for shared skill discovery metadata and explicit runbook delivery.' },
    ];

    staticPages.forEach(p => searchIndex.push({ ...p, type: 'page', href: `#${p.id}` }));

    // Skills from data
    if (skillsData && Array.isArray(skillsData)) {
      skillsData.slice(0, 500).forEach(skill => {
        searchIndex.push({
          id: skill.id,
          title: skill.name || skill.id,
          category: skill.module || 'Skills',
          excerpt: skill.description || '',
          type: 'skill',
          command: skill.command,
          href: '#explorer',
        });
      });
    }
  }

  function searchQuery(q) {
    if (!q || q.length < 2) return [];
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    const results = [];

    for (const item of searchIndex) {
      const haystack = `${item.title} ${item.category} ${item.excerpt} ${item.id}`.toLowerCase();
      let score = 0;
      let matched = true;

      for (const term of terms) {
        if (!haystack.includes(term)) { matched = false; break; }
        if (item.title.toLowerCase().includes(term)) score += 10;
        if (item.id.toLowerCase().includes(term)) score += 8;
        if (item.category.toLowerCase().includes(term)) score += 5;
        if (item.excerpt.toLowerCase().includes(term)) score += 2;
      }

      if (matched) results.push({ ...item, score });
    }

    return results.sort((a, b) => b.score - a.score).slice(0, 12);
  }

  function highlightTerms(text, q) {
    const terms = q.toLowerCase().split(/\s+/).filter(t => t.length > 1);
    let result = text;
    for (const term of terms) {
      const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
      result = result.replace(regex, '<mark>$1</mark>');
    }
    return result;
  }

  // ---- Search UI ----
  function initSearch() {
    const overlay = document.getElementById('search-overlay');
    const input = document.getElementById('search-modal-input');
    const resultsEl = document.getElementById('search-results');
    const triggers = document.querySelectorAll('.search-trigger, #open-search');
    if (!overlay || !input) return;

    let currentResults = [];
    let selectedIndex = -1;

    function open() {
      overlay.classList.add('open');
      input.value = '';
      selectedIndex = -1;
      renderResults([]);
      requestAnimationFrame(() => input.focus());
    }

    function close() {
      overlay.classList.remove('open');
    }

    function renderResults(results) {
      currentResults = results;
      if (!results.length) {
        const q = input.value.trim();
        resultsEl.innerHTML = q.length >= 2
          ? `<div class="search-empty">No results for "<strong>${q}</strong>"</div>`
          : '<div class="search-empty">Start typing to search documentation and skills…</div>';
        return;
      }

      resultsEl.innerHTML = results.map((r, i) => `
        <div class="search-result-item ${i === selectedIndex ? 'selected' : ''}"
             data-href="${r.href}" role="option" aria-selected="${i === selectedIndex}">
          <div class="search-result-category">${r.category}</div>
          <div class="search-result-title">${highlightTerms(r.title, input.value)}</div>
          ${r.excerpt ? `<div class="search-result-excerpt">${highlightTerms(r.excerpt.substring(0, 120), input.value)}…</div>` : ''}
          ${r.command ? `<div class="search-result-excerpt text-mono" style="margin-top:4px;">${r.command}</div>` : ''}
        </div>
      `).join('');
    }

    function navigate(item) {
      close();
      if (item.href.startsWith('#')) {
        const el = document.querySelector(item.href);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    triggers.forEach(t => t.addEventListener('click', open));

    overlay.addEventListener('click', e => {
      if (e.target === overlay) close();
    });

    input.addEventListener('input', () => {
      const q = input.value.trim();
      selectedIndex = -1;
      renderResults(q.length >= 2 ? searchQuery(q) : []);
    });

    input.addEventListener('keydown', e => {
      if (e.key === 'Escape') { close(); return; }
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIndex = Math.min(selectedIndex + 1, currentResults.length - 1);
        renderResults(currentResults);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIndex = Math.max(selectedIndex - 1, 0);
        renderResults(currentResults);
      } else if (e.key === 'Enter' && selectedIndex >= 0) {
        navigate(currentResults[selectedIndex]);
      }
    });

    resultsEl.addEventListener('click', e => {
      const item = e.target.closest('.search-result-item');
      if (!item) return;
      const href = item.dataset.href;
      const result = currentResults.find(r => r.href === href);
      if (result) navigate(result);
    });

    // Keyboard shortcut
    document.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        overlay.classList.contains('open') ? close() : open();
      }
      if (e.key === 'Escape' && overlay.classList.contains('open')) close();
    });
  }

  // ============================================================
  // SKILLS EXPLORER
  // ============================================================
  let allSkills = [];
  let activeFilter = 'all';
  let visibleCount = 36;
  let explorerQuery = '';

  function initSkillsExplorer(skillsData) {
    allSkills = skillsData || [];

    const container = document.getElementById('skills-grid');
    const countEl = document.getElementById('skills-count');
    const searchEl = document.getElementById('explorer-search');
    const filterBtns = document.querySelectorAll('.filter-tab');
    const loadMoreBtn = document.getElementById('load-more-skills');

    if (!container) return;

    function getFiltered() {
      let results = allSkills;
      if (activeFilter !== 'all') {
        results = results.filter(s => (s.module || '').includes(activeFilter));
      }
      if (explorerQuery) {
        const q = explorerQuery.toLowerCase();
        results = results.filter(s =>
          (s.name || '').toLowerCase().includes(q) ||
          (s.id || '').toLowerCase().includes(q) ||
          (s.description || '').toLowerCase().includes(q) ||
          (s.module || '').toLowerCase().includes(q)
        );
      }
      return results;
    }

    function renderSkills() {
      const filtered = getFiltered();
      const visible = filtered.slice(0, visibleCount);

      if (countEl) countEl.textContent = `Showing ${visible.length} of ${filtered.length.toLocaleString()} skills`;

      container.innerHTML = visible.map(s => `
        <div class="skill-card reveal">
          <div class="skill-card-header">
            <div class="skill-name">${s.id || s.name}</div>
            <span class="skill-tier tier-${s.tier || 2}">T${s.tier || 2}</span>
          </div>
          <p class="skill-desc">${s.description || ''}</p>
          <div class="skill-module">${s.module || s.category || ''}</div>
        </div>
      `).join('');

      // Re-trigger reveals for new cards
      requestAnimationFrame(() => {
        document.querySelectorAll('#skills-grid .reveal').forEach((el, i) => {
          setTimeout(() => el.classList.add('visible'), i * 20);
        });
      });

      if (loadMoreBtn) {
        loadMoreBtn.style.display = filtered.length > visibleCount ? 'block' : 'none';
      }
    }

    renderSkills();

    if (searchEl) {
      searchEl.addEventListener('input', () => {
        explorerQuery = searchEl.value.trim();
        visibleCount = 36;
        renderSkills();
      });
    }

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeFilter = btn.dataset.filter || 'all';
        visibleCount = 36;
        renderSkills();
      });
    });

    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', () => {
        visibleCount += 36;
        renderSkills();
      });
    }
  }

  // ============================================================
  // MOBILE NAV
  // ============================================================
  function initMobileNav() {
    const btn = document.getElementById('mobile-menu-btn');
    const drawer = document.getElementById('mobile-nav-drawer');
    const backdrop = document.getElementById('mobile-backdrop');
    const closeBtn = document.getElementById('mobile-nav-close');

    if (!btn || !drawer) return;

    function open() {
      drawer.classList.add('open');
      if (backdrop) backdrop.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }

    function close() {
      drawer.classList.remove('open');
      if (backdrop) backdrop.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }

    btn.addEventListener('click', open);
    if (closeBtn) closeBtn.addEventListener('click', close);
    if (backdrop) backdrop.addEventListener('click', close);

    drawer.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', close);
    });
  }

  // ============================================================
  // SIDEBAR ACTIVE TRACKING (docs view)
  // ============================================================
  function initSidebarSpy() {
    const links = Array.from(document.querySelectorAll('.sidebar-link[href^="#"]'));
    if (!links.length) return;

    const obs = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          links.forEach(l => l.classList.remove('active'));
          const active = links.find(l => l.getAttribute('href') === `#${entry.target.id}`);
          if (active) active.classList.add('active');
        }
      }
    }, { rootMargin: '-15% 0px -75% 0px' });

    document.querySelectorAll('section[id]').forEach(s => obs.observe(s));
  }

  // ============================================================
  // TABLE OF CONTENTS (auto-generate from headings)
  // ============================================================
  function initTOC() {
    const tocEl = document.getElementById('toc-nav');
    const content = document.getElementById('main-content');
    if (!tocEl || !content) return;

    const headings = Array.from(content.querySelectorAll('h2, h3'));
    if (!headings.length) return;

    headings.forEach(h => {
      if (!h.id) {
        h.id = h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      }
    });

    tocEl.innerHTML = headings.map(h => {
      const depth = parseInt(h.tagName[1]);
      return `<li><a href="#${h.id}" class="toc-link depth-${depth}">${h.textContent}</a></li>`;
    }).join('');

    const tocLinks = Array.from(tocEl.querySelectorAll('.toc-link'));

    const obs = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          tocLinks.forEach(l => l.classList.remove('active'));
          const active = tocLinks.find(l => l.getAttribute('href') === `#${entry.target.id}`);
          if (active) active.classList.add('active');
        }
      }
    }, { rootMargin: '-10% 0px -80% 0px' });

    headings.forEach(h => obs.observe(h));
  }

  // ============================================================
  // HOVER LINE ANIMATION for feature cards
  // ============================================================
  function initCardHover() {
    document.querySelectorAll('.feature-card, .pod-card, .skill-card').forEach(card => {
      card.addEventListener('mouseenter', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
    });
  }

  // ============================================================
  // SMOOTH HASH SCROLL
  // ============================================================
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', e => {
        const href = a.getAttribute('href');
        if (href === '#') return;
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.pushState(null, '', href);
        }
      });
    });
  }

  // ============================================================
  // VERIFY ANIMATION (checklist)
  // ============================================================
  function initVerifyAnimation() {
    const rows = document.querySelectorAll('.verify-row');
    if (!rows.length) return;

    const obs = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) return;
      rows.forEach((row, i) => {
        setTimeout(() => {
          row.style.opacity = '1';
          row.style.transform = 'translateX(0)';
        }, i * 60);
      });
      obs.disconnect();
    }, { threshold: 0.2 });

    const container = document.querySelector('.verify-list');
    if (container) {
      rows.forEach(r => {
        r.style.opacity = '0';
        r.style.transform = 'translateX(-12px)';
        r.style.transition = 'opacity 0.4s var(--ease-spring), transform 0.4s var(--ease-spring)';
      });
      obs.observe(container);
    }
  }

  // ============================================================
  // LOAD SKILLS DATA + BOOT
  // ============================================================
  async function loadData() {
    try {
      const res = await fetch('./skills-data.json');
      const data = await res.json();
      return Array.isArray(data) ? data : (data.skills || []);
    } catch {
      return [];
    }
  }

  // ============================================================
  // MAIN BOOT
  // ============================================================
  document.addEventListener('DOMContentLoaded', async () => {
    // Theme
    applyTheme(getTheme());
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    // Core UI
    initHeaderScroll();
    initScrollSpy();
    initReveal();
    initCounters();
    initCopyButtons();
    initMobileNav();
    initSidebarSpy();
    initTOC();
    initSmoothScroll();
    initVerifyAnimation();

    // Load skills data
    const skillsData = await loadData();

    // Build search index
    buildSearchIndex(skillsData);
    initSearch();

    // Skills explorer
    initSkillsExplorer(skillsData);

    // Card hover effects
    initCardHover();

    // Announce page load for screen readers
    const announcer = document.getElementById('sr-announcer');
    if (announcer) announcer.textContent = 'AGYOS documentation loaded';
  });

})();
