(() => {
  const KEY = 'classic-notes-builds-v1';
  const form = document.querySelector('#build-form');
  const list = document.querySelector('#saved-builds');
  const status = document.querySelector('#save-status');
  const read = () => { try { const v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v.filter(x => x && typeof x === 'object') : []; } catch { return []; } };
  const write = builds => localStorage.setItem(KEY, JSON.stringify(builds));
  const clean = value => String(value || '').trim();
  const render = () => { const builds = read(); list.replaceChildren(); if (!builds.length) { const p = document.createElement('p'); p.className = 'small'; p.textContent = '아직 저장한 빌드가 없습니다.'; list.append(p); return; } builds.forEach(build => { const article=document.createElement('article'); const title=document.createElement('h3'); title.textContent=build.name||'이름 없는 빌드'; const detail=document.createElement('p'); detail.textContent=`챔피언: ${build.champion||'-'} / 룬: ${build.runes||'-'} / 특성: ${build.masteries||'-'} / 아이템: ${build.items||'-'}`; const remove=document.createElement('button'); remove.type='button'; remove.textContent='삭제'; remove.dataset.id=build.id; article.append(title,detail,remove); list.append(article); }); };
  form.addEventListener('submit', event => { event.preventDefault(); const data=new FormData(form); const build={id:crypto.randomUUID?crypto.randomUUID():String(Date.now()),name:clean(data.get('name')),champion:clean(data.get('champion')),runes:clean(data.get('runes')),masteries:clean(data.get('masteries')),items:clean(data.get('items')),updatedAt:new Date().toISOString()}; const builds=read(); builds.unshift(build); write(builds.slice(0,30)); form.reset(); status.textContent='이 브라우저에 저장했습니다.'; render(); });
  list.addEventListener('click', event => { const id=event.target.dataset.id; if (!id) return; write(read().filter(build => build.id !== id)); status.textContent='저장 항목을 삭제했습니다.'; render(); });
  render();
})();
