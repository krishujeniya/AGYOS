/* AGYOS public documentation: motion, search, navigation and code UX. No third-party runtime. */
(() => {
  'use strict';
  const doc = document;
  const root = doc.documentElement;
  const script = doc.querySelector('script[src$="site.js"]');
  const base = script ? new URL('./', script.src).pathname : '/AGYOS/';
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

  // Visual decoration removed; navigation, search, theme and copy remain functional.
})();
