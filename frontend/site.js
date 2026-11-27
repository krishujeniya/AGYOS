/* AGYOS public documentation: motion, search, navigation and code UX. No third-party runtime. */
(() => {
  'use strict';
  const doc = document;
  const root = doc.documentElement;
  const script = doc.querySelector('script[src$="site.js"]');
  const base = script ? new URL('./', script.src).pathname : '/';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let theme = 'light';
  try { theme = localStorage.getItem('agyos-v2-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); } catch { /* storage disabled */ }
  root.dataset.theme = theme;
  doc.querySelectorAll('[data-theme-toggle]').forEach(button => button.addEventListener('click', () => {
    theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = theme;
    try { localStorage.setItem('agyos-v2-theme', theme); } catch { /* no storage */ }
  }));

  const menuButton = doc.querySelector('[data-menu]');
  menuButton?.addEventListener('click', () => {
    const opened = doc.body.classList.toggle('menu-open');
    menuButton.setAttribute('aria-expanded', String(opened));
    menuButton.setAttribute('aria-label', opened ? 'Close navigation' : 'Open navigation');
  });
  doc.querySelectorAll('.toplinks a').forEach(link => link.addEventListener('click', () => {
    doc.body.classList.remove('menu-open');
    menuButton?.setAttribute('aria-expanded', 'false');
  }));
  const docsMenu = doc.querySelector('[data-docs-menu]');
  const docsSide = doc.querySelector('#docs-sidebar');
  docsMenu?.addEventListener('click', () => {
    const opened = docsSide?.classList.toggle('open');
    docsMenu.setAttribute('aria-expanded', String(Boolean(opened)));
  });

  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      }
    }, { rootMargin: '0px 0px -45px 0px', threshold: .08 });
    doc.querySelectorAll('.reveal').forEach(element => observer.observe(element));
  } else {
    doc.querySelectorAll('.reveal').forEach(element => element.classList.add('is-visible'));
  }

  doc.querySelectorAll('.code-copy').forEach(button => button.addEventListener('click', async () => {
    const content = button.closest('.code-shell')?.querySelector('code')?.textContent || '';
    try {
      await navigator.clipboard.writeText(content);
      button.textContent = 'Copied';
      window.setTimeout(() => button.textContent = 'Copy', 1500);
    } catch { button.textContent = 'Unavailable'; }
  }));

  // Search is backed by generated, allowlisted Markdown content.
  const modal = doc.querySelector('#search-dialog');
  const input = doc.querySelector('#search-input');
  const results = doc.querySelector('#search-results');
  const close = doc.querySelector('#search-close');
  let index = null;
  let matches = [];
  let selection = 0;
  let previousFocus = null;
  const escape = value => String(value).replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
  const textAround = (body, term) => {
    const lowercase = body.toLowerCase();
    const found = lowercase.indexOf(term.toLowerCase());
    const start = found >= 0 ? Math.max(0, found - 75) : 0;
    const snippet = body.slice(start, start + 180).replace(/\s+/g, ' ');
    return `${start ? '…' : ''}${snippet}${start+180 < body.length ? '…' : ''}`;
  };
  const mark = (text, q) => {
    const index = text.toLowerCase().indexOf(q.toLowerCase());
    if (index === -1 || !q) return escape(text);
    return escape(text.slice(0,index))+'<mark>'+escape(text.slice(index,index+q.length))+'</mark>'+escape(text.slice(index+q.length));
  };
  async function loadIndex() {
    if (index) return;
    const resp = await fetch(new URL('search-index.json', script.src));
    if (!resp.ok) throw new Error('Search index could not be loaded');
    const data = await resp.json();
    if (!Array.isArray(data)) throw new Error('Malformed search index');
    index = data;
  }
  function updateSelected() {
    results?.querySelectorAll('.result-item').forEach((el,i) => {
      el.setAttribute('aria-selected',String(i === selection));
      if (i === selection) el.scrollIntoView({block:'nearest'});
    });
  }
  function search(term) {
    if (!results || !index) return;
    const q = term.trim().toLowerCase();
    if (!q) { results.innerHTML = '<p class="search-hint">Search project documentation, architecture, rules, and guides.</p>';matches=[];return; }
    const terms = q.split(/\s+/).filter(Boolean);
    matches = index.map(entry => {
      const title = entry.title.toLowerCase();
      const body = entry.content.toLowerCase();
      const category = entry.category.toLowerCase();
      const score = terms.reduce((n,t) => n + (title.includes(t)?10:0) + (category.includes(t)?5:0) + (body.includes(t)?1:0),0);
      return {...entry,score};
    }).filter(entry => entry.score && terms.every(term => (entry.title+' '+entry.category+' '+entry.content).toLowerCase().includes(term)))
      .sort((a,b) => b.score-a.score).slice(0,12);
    selection = 0;
    results.innerHTML = matches.length ? matches.map((entry,i) =>
      `<a class="result-item" role="option" aria-selected="${i===0}" href="${escape(entry.url)}"><strong>${mark(entry.title,terms[0])}</strong><small>${escape(entry.category)}</small><p>${mark(textAround(entry.content,terms[0]),terms[0])}</p></a>`).join('')
      : '<p class="search-hint">No matching public documentation found.</p>';
  }
  async function openSearch() {
    if (!modal || !input) return;
    previousFocus = doc.activeElement;
    modal.showModal();
    input.value = '';
    input.focus();
    results.innerHTML = '<p class="search-hint">Loading documentation index…</p>';
    try { await loadIndex();search(''); }
    catch { results.innerHTML = '<p class="search-hint">Search is temporarily unavailable. Use the documentation navigation instead.</p>'; }
  }
  doc.querySelectorAll('[data-search-open]').forEach(b => b.addEventListener('click', openSearch));
  input?.addEventListener('input', () => search(input.value));
  input?.addEventListener('keydown', ev => {
    if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
      ev.preventDefault();if (!matches.length)return;
      selection = (selection + (ev.key === 'ArrowDown' ? 1 : -1) + matches.length) % matches.length;updateSelected();
    } else if (ev.key === 'Enter' && matches[selection]) {
      window.location.href = matches[selection].url;
    }
  });
  close?.addEventListener('click', () => modal.close());
  modal?.addEventListener('close', () => previousFocus?.focus?.());
  modal?.addEventListener('click', ev => {if (ev.target === modal) modal.close();});
  doc.addEventListener('keydown', ev => {
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 'k') { ev.preventDefault();modal?.open ? modal.close() : openSearch(); }
  });

  const headings = [...doc.querySelectorAll('.prose h2[id],.prose h3[id]')];
  const tocLinks = [...doc.querySelectorAll('.docs-toc a')];
  if (headings.length && 'IntersectionObserver' in window) {
    const tocObserver = new IntersectionObserver(entries => {
      const current = entries.filter(e=>e.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top)[0];
      if (!current) return;
      tocLinks.forEach(el=>el.classList.toggle('active',el.hash === '#'+current.target.id));
    },{rootMargin:'-90px 0px -70% 0px',threshold:0});
    headings.forEach(h=>tocObserver.observe(h));
  }

  // Skills Catalog Explorer Controller
  const skillsGrid = doc.querySelector('#skills-grid');
  if (skillsGrid) {
    let catalogSkills = [];
    let catalogFilter = 'all';
    let catalogQuery = '';
    let visibleLimit = 36;
    const countEl = doc.querySelector('#skills-count');
    const searchEl = doc.querySelector('#explorer-search');
    const filterTabs = doc.querySelectorAll('.filter-tab');
    const loadMoreBtn = doc.querySelector('#load-more-skills');

    async function fetchSkillsCatalog() {
      try {
        const resp = await fetch(new URL('catalog/skills-data.json', script.src));
        if (resp.ok) {
          const data = await resp.json();
          return Array.isArray(data) ? data : (data.skills || []);
        }
      } catch { /* fallback */ }
      try {
        const resp = await fetch('skills-data.json');
        if (resp.ok) {
          const data = await resp.json();
          return Array.isArray(data) ? data : (data.skills || []);
        }
      } catch { /* unavailable */ }
      return [];
    }

    function filterSkills() {
      let filtered = catalogSkills;
      if (catalogFilter !== 'all') {
        const f = catalogFilter.toLowerCase();
        filtered = filtered.filter(s => (s.module || s.category || '').toLowerCase().includes(f));
      }
      if (catalogQuery) {
        const q = catalogQuery.toLowerCase();
        filtered = filtered.filter(s =>
          (s.name || '').toLowerCase().includes(q) ||
          (s.id || '').toLowerCase().includes(q) ||
          (s.description || '').toLowerCase().includes(q) ||
          (s.module || s.category || '').toLowerCase().includes(q)
        );
      }
      return filtered;
    }

    function renderCatalog() {
      const filtered = filterSkills();
      const visible = filtered.slice(0, visibleLimit);

      if (countEl) {
        countEl.textContent = `Showing ${visible.length} of ${filtered.length.toLocaleString()} skills`;
      }

      if (visible.length === 0) {
        skillsGrid.innerHTML = '<p class="search-hint" style="grid-column:1/-1;">No skills match your search criteria.</p>';
      } else {
        skillsGrid.innerHTML = visible.map(s => `
          <article class="skill-card">
            <div class="skill-card-header">
              <strong class="skill-name">${escape(s.id || s.name)}</strong>
              <span class="skill-tier tier-${s.tier || 2}">T${s.tier || 2}</span>
            </div>
            <p class="skill-desc">${escape(s.description || 'No description provided.')}</p>
            <span class="skill-module">${escape(s.module || s.category || 'General')}</span>
          </article>
        `).join('');
      }

      if (loadMoreBtn) {
        loadMoreBtn.style.display = filtered.length > visibleLimit ? 'inline-flex' : 'none';
      }
    }

    searchEl?.addEventListener('input', () => {
      catalogQuery = searchEl.value.trim();
      visibleLimit = 36;
      renderCatalog();
    });

    filterTabs.forEach(tab => tab.addEventListener('click', () => {
      filterTabs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      catalogFilter = tab.dataset.filter || 'all';
      visibleLimit = 36;
      renderCatalog();
    }));

    loadMoreBtn?.addEventListener('click', () => {
      visibleLimit += 36;
      renderCatalog();
    });

    fetchSkillsCatalog().then(skills => {
      catalogSkills = skills;
      renderCatalog();
    });
  }

  const topbar = doc.querySelector('.topbar');
  if (topbar) {
    let lastScrollY = Math.max(0, window.scrollY || 0);
    let isScrolled = lastScrollY > 0;
    let isHidden = false;
    let navRaf = 0;
    topbar.classList.toggle('is-scrolled', isScrolled);
    const updateNavbar = () => {
      navRaf = 0;
      const y = Math.max(0, window.scrollY || 0);
      const nextScrolled = y > 0;
      if (nextScrolled !== isScrolled) {
        isScrolled = nextScrolled;
        topbar.classList.toggle('is-scrolled', isScrolled);
      }
      if (y <= 0 || doc.body.classList.contains('menu-open')) {
        if (isHidden) {
          isHidden = false;
          topbar.classList.remove('is-hidden');
        }
        lastScrollY = y;
        return;
      }
      const delta = y - lastScrollY;
      if (delta > 5 && !isHidden) {
        isHidden = true;
        topbar.classList.add('is-hidden');
      } else if (delta < -5 && isHidden) {
        isHidden = false;
        topbar.classList.remove('is-hidden');
      }
      if (Math.abs(delta) > 5) lastScrollY = y;
    };
    const queueNavbar = () => { if (!navRaf) navRaf = requestAnimationFrame(updateNavbar); };
    window.addEventListener('scroll', queueNavbar, { passive: true });
  }

  document.querySelectorAll('.back-top').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

  const wordmarkEl = document.getElementById('footer-wordmark');
  let fRaf = 0;
  function updateFooterWordmark() {
    fRaf = 0;
    if (!wordmarkEl) return;
    const r = wordmarkEl.getBoundingClientRect();
    const vh = window.innerHeight || 800;
    wordmarkEl.classList.toggle('in-view', r.top + r.height * 0.5 <= vh);
  }
  if (wordmarkEl && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('has-motion');
    const queueFooter = () => { if (!fRaf) fRaf = requestAnimationFrame(updateFooterWordmark); };
    window.addEventListener('scroll', queueFooter, { passive: true });
    window.addEventListener('resize', queueFooter, { passive: true });
    updateFooterWordmark();
  }
})();
