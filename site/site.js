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

  // Original canvas composition: elliptical constellations with spring pointer response.
  const canvas = doc.querySelector('#particle-field');
  if (canvas && !reduceMotion.matches && canvas.getContext) {
    const ctx = canvas.getContext('2d',{alpha:true});
    let width=0,height=0,dpr=1,points=[],frame=0,prev=0,running=false,visible=true;
    let pointer={x:-9999,y:-9999,active:false};
    const TAU=Math.PI*2;
    function resize() {
      const box=canvas.getBoundingClientRect();width=box.width;height=box.height;
      dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.max(1,Math.round(width*dpr));canvas.height=Math.max(1,Math.round(height*dpr));
      ctx.setTransform(dpr,0,0,dpr,0,0);
      const n=width<680?110:width<1000?170:260;
      points=Array.from({length:n},(_,i)=>{
        const t=i/n;
        const a=t*TAU*2.6 + Math.sin(i*7.1)*.18;
        const ring=.18 + .82*Math.sqrt(t);
        return {a,ring,depth:.6+(i%7)/12,phase:i*1.73,rx:0,ry:0,vx:0,vy:0,radius:Math.random()*.75+.5};
      });
    }
    function render(time) {
      if (!running || !visible || reduceMotion.matches) {frame=0;return;}
      const dt=Math.min((time-prev||16)/16.67,2);prev=time;ctx.clearRect(0,0,width,height);
      const cx=width*(width<680?.70:.76),cy=height*.49;
      const size=Math.min(width*.37,height*.54);
      const slow=time*.00012;
      points.forEach((p,i)=>{
        const theta=p.a+slow*(.22+p.depth*.2);
        const r=size*p.ring;
        const sway=Math.sin(slow*2+p.phase)*5;
        const x=cx+Math.cos(theta)*r*1.25+sway;
        const y=cy+Math.sin(theta)*r*.7+Math.cos(slow+p.phase)*5;
        const dx=x+ p.rx-pointer.x, dy=y+p.ry-pointer.y;
        const dist=Math.sqrt(dx*dx+dy*dy)||1;
        const power=pointer.active ? Math.max(0,1-dist/145)*.95 : 0;
        const tx=power*dx/dist*58,ty=power*dy/dist*58;
        p.vx+=(tx-p.rx)*.065*dt;p.vy+=(ty-p.ry)*.065*dt;
        p.vx*=Math.pow(.83,dt);p.vy*=Math.pow(.83,dt);
        p.rx+=p.vx*dt;p.ry+=p.vy*dt;
        const alpha=.23+.48*p.depth;
        ctx.beginPath();ctx.arc(x+p.rx,y+p.ry,p.radius*p.depth,0,TAU);
        ctx.fillStyle=`rgba(${root.dataset.theme==='dark'?'173,187,255':'61,80,175'},${alpha})`;ctx.fill();
        if (i%19===0){ctx.beginPath();ctx.moveTo(x+p.rx,y+p.ry);ctx.lineTo(x+p.rx+4*p.depth,y+p.ry+1);ctx.strokeStyle=`rgba(105,132,235,${alpha*.62})`;ctx.lineWidth=.7;ctx.stroke();}
      });
      frame=requestAnimationFrame(render);
    }
    function begin(){if (running)return;running=true;prev=0;frame=requestAnimationFrame(render);}
    function stop(){running=false;cancelAnimationFrame(frame);frame=0;}
    const resizeObserver=new ResizeObserver(resize);resizeObserver.observe(canvas);resize();
    const visibilityObserver=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting && !doc.hidden; if(visible)begin();else stop();});
    visibilityObserver.observe(canvas);
    const onVisibility=()=>{visible=!doc.hidden && canvas.getBoundingClientRect().bottom>0;if(visible)begin();else stop();};
    const onPointer=ev=>{const rect=canvas.getBoundingClientRect();pointer={x:ev.clientX-rect.left,y:ev.clientY-rect.top,active:true};};
    window.addEventListener('pointermove',onPointer,{passive:true});
    window.addEventListener('pointerleave',()=>pointer.active=false,{passive:true});
    doc.addEventListener('visibilitychange',onVisibility);
    const onReduce=()=>reduceMotion.matches?stop():begin();reduceMotion.addEventListener('change',onReduce);
    window.addEventListener('pagehide',()=>{stop();resizeObserver.disconnect();visibilityObserver.disconnect();window.removeEventListener('pointermove',onPointer);doc.removeEventListener('visibilitychange',onVisibility);reduceMotion.removeEventListener('change',onReduce);},{once:true});
  }
})();
