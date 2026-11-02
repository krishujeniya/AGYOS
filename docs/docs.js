/**
 * SKILL Documentation Client-Side Engine
 * Zero backend, 100% static, fast client-side filtering across 1,500+ skills.
 */

(function () {
  'use strict';

  // State
  let allSkills = [];
  let filteredSkills = [];
  let currentModule = 'all';
  let currentRuntime = 'all';
  let searchQuery = '';
  let currentPage = 1;
  const PAGE_SIZE = 20;

  // DOM Elements
  const themeToggle = document.getElementById('theme-toggle');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const sidebar = document.getElementById('sidebar');
  const headerSearchInput = document.getElementById('header-search');
  const explorerSearchInput = document.getElementById('explorer-search');
  const moduleFilters = document.getElementById('module-filters');
  const runtimeFilters = document.getElementById('runtime-filters');
  const skillsList = document.getElementById('skills-list');
  const resultsCount = document.getElementById('results-count');
  const pagination = document.getElementById('pagination');

  // Theme Management
  function initTheme() {
    const savedTheme = localStorage.getItem('skill_docs_theme');
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
      updateThemeBtnText(savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-theme', 'dark');
      updateThemeBtnText('dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      updateThemeBtnText('light');
    }
  }

  function updateThemeBtnText(theme) {
    if (themeToggle) {
      themeToggle.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
    }
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nextTheme);
    localStorage.setItem('skill_docs_theme', nextTheme);
    updateThemeBtnText(nextTheme);
  }

  // Mobile Drawer
  function toggleMobileMenu() {
    if (sidebar) {
      sidebar.classList.toggle('open');
    }
  }

  // Load Skills Data
  async function loadSkillsData() {
    try {
      const res = await fetch('skills-data.json');
      if (!res.ok) {
        throw new Error('Failed to load skills-data.json: ' + res.status);
      }
      allSkills = await res.json();
      applyFilters();
    } catch (err) {
      console.error('Skills load error:', err);
      if (skillsList) {
        skillsList.innerHTML = '<div class="callout"><p>Failed to load skills database. Please refresh or verify skills-data.json.</p></div>';
      }
    }
  }

  // Filter Logic
  function applyFilters() {
    const q = searchQuery.toLowerCase().trim();

    filteredSkills = allSkills.filter(skill => {
      // Module check
      if (currentModule !== 'all' && skill.module !== currentModule) {
        return false;
      }

      // Runtime check
      if (currentRuntime !== 'all') {
        const runtimes = skill.runtime || [];
        const matches = runtimes.some(r => r.toLowerCase() === currentRuntime.toLowerCase());
        if (!matches) return false;
      }

      // Search query check
      if (q) {
        const matchName = (skill.name || '').toLowerCase().includes(q);
        const matchId = (skill.id || '').toLowerCase().includes(q);
        const matchDesc = (skill.description || '').toLowerCase().includes(q);
        const matchCmd = (skill.command || '').toLowerCase().includes(q);
        const matchPath = (skill.path || '').toLowerCase().includes(q);
        const matchCat = (skill.category || '').toLowerCase().includes(q);
        if (!matchName && !matchId && !matchDesc && !matchCmd && !matchPath && !matchCat) {
          return false;
        }
      }

      return true;
    });

    currentPage = 1;
    renderResults();
  }

  // Render Skill Cards
  function renderResults() {
    if (!skillsList || !resultsCount) return;

    const total = filteredSkills.length;
    resultsCount.textContent = `Showing ${total} of ${allSkills.length} skills`;

    if (total === 0) {
      skillsList.innerHTML = '<div class="callout"><p>No skills matched your search filter. Try clearing filters or using broader terms.</p></div>';
      if (pagination) pagination.innerHTML = '';
      return;
    }

    const startIndex = (currentPage - 1) * PAGE_SIZE;
    const pageItems = filteredSkills.slice(startIndex, startIndex + PAGE_SIZE);

    const html = pageItems.map(skill => {
      const runtimeBadges = (skill.runtime || []).map(r => `<span class="tag">${escapeHtml(r)}</span>`).join(' ');
      const command = skill.command || `aegis use ${skill.id}`;
      return `
        <article class="skill-row">
          <div class="skill-row-top">
            <div>
              <span class="skill-name">${escapeHtml(skill.name)}</span>
              <span class="skill-id">${escapeHtml(skill.id)}</span>
            </div>
            <span class="tag">${escapeHtml(skill.module || 'Aegis')}</span>
          </div>
          <p class="skill-desc">${escapeHtml(skill.description)}</p>
          <div class="skill-row-bottom">
            <div class="skill-meta">
              <span class="skill-command"><code>${escapeHtml(command)}</code></span>
              ${runtimeBadges}
            </div>
            <button class="copy-btn" data-copy="${escapeHtml(command)}">Copy command</button>
          </div>
        </article>
      `;
    }).join('');

    skillsList.innerHTML = html;
    renderPagination(total);
  }

  // Pagination Renderer
  function renderPagination(total) {
    if (!pagination) return;
    const totalPages = Math.ceil(total / PAGE_SIZE);
    if (totalPages <= 1) {
      pagination.innerHTML = '';
      return;
    }

    pagination.innerHTML = `
      <button class="filter-btn" id="prev-page" ${currentPage === 1 ? 'disabled style="opacity:0.4;cursor:not-allowed;"' : ''}>Previous</button>
      <span style="font-family: var(--font-mono); font-size: 0.8rem;">Page ${currentPage} of ${totalPages}</span>
      <button class="filter-btn" id="next-page" ${currentPage === totalPages ? 'disabled style="opacity:0.4;cursor:not-allowed;"' : ''}>Next</button>
    `;

    const prevBtn = document.getElementById('prev-page');
    const nextBtn = document.getElementById('next-page');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
          currentPage--;
          renderResults();
          document.getElementById('explorer')?.scrollIntoView({ behavior: 'smooth' });
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
          currentPage++;
          renderResults();
          document.getElementById('explorer')?.scrollIntoView({ behavior: 'smooth' });
        }
      });
    }
  }

  // Copy Clipboard Helper
  function initCopyButtons() {
    document.addEventListener('click', e => {
      const btn = e.target.closest('.copy-btn');
      if (!btn) return;

      const textToCopy = btn.getAttribute('data-copy');
      if (!textToCopy) return;

      navigator.clipboard.writeText(textToCopy).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Copied';
        btn.style.background = 'var(--accent-bg)';
        btn.style.color = 'var(--accent-fg)';
        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.background = '';
          btn.style.color = '';
        }, 1600);
      }).catch(err => {
        console.error('Clipboard copy failed:', err);
      });
    });
  }

  // Escape HTML helper
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Active section scroll spy
  function initScrollSpy() {
    const links = document.querySelectorAll('.sidebar-link');
    const sections = Array.from(links)
      .map(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
          return document.querySelector(href);
        }
        return null;
      })
      .filter(Boolean);

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            links.forEach(l => {
              if (l.getAttribute('href') === `#${id}`) {
                l.classList.add('active');
              } else {
                l.classList.remove('active');
              }
            });
          }
        });
      }, {
        rootMargin: '-20% 0px -70% 0px',
        threshold: 0
      });

      sections.forEach(sec => observer.observe(sec));
    }
  }

  // Event Listeners
  function initEvents() {
    // Theme toggle
    if (themeToggle) {
      themeToggle.addEventListener('click', toggleTheme);
    }

    // Mobile menu toggle
    if (mobileMenuBtn) {
      mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    }

    // Auto close mobile drawer on link click
    if (sidebar) {
      sidebar.addEventListener('click', (e) => {
        if (e.target.closest('.sidebar-link')) {
          sidebar.classList.remove('open');
        }
      });
    }

    // Header search syncs to explorer search
    if (headerSearchInput) {
      headerSearchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        if (explorerSearchInput) {
          explorerSearchInput.value = searchQuery;
        }
        applyFilters();
        if (searchQuery && window.location.hash !== '#explorer') {
          window.location.hash = '#explorer';
        }
      });
    }

    if (explorerSearchInput) {
      explorerSearchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        if (headerSearchInput) {
          headerSearchInput.value = searchQuery;
        }
        applyFilters();
      });
    }

    // Module filter buttons
    if (moduleFilters) {
      moduleFilters.addEventListener('click', (e) => {
        const btn = e.target.closest('.filter-btn');
        if (!btn) return;
        moduleFilters.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentModule = btn.getAttribute('data-module') || 'all';
        applyFilters();
      });
    }

    // Runtime filter buttons
    if (runtimeFilters) {
      runtimeFilters.addEventListener('click', (e) => {
        const btn = e.target.closest('.filter-btn');
        if (!btn) return;
        runtimeFilters.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentRuntime = btn.getAttribute('data-runtime') || 'all';
        applyFilters();
      });
    }

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
      // Focus search on '/' or Cmd/Ctrl + K
      if ((e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') ||
          ((e.metaKey || e.ctrlKey) && e.key === 'k')) {
        e.preventDefault();
        const input = explorerSearchInput || headerSearchInput;
        if (input) {
          input.focus();
          input.select();
        }
      }
      // Clear on Esc
      if (e.key === 'Escape') {
        if (document.activeElement.tagName === 'INPUT') {
          document.activeElement.blur();
        }
        if (sidebar && sidebar.classList.contains('open')) {
          sidebar.classList.remove('open');
        }
      }
    });
  }

  // Initialize
  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initEvents();
    initCopyButtons();
    initScrollSpy();
    loadSkillsData();
  });
})();
