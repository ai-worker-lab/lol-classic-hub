(() => {
  const input = document.querySelector('#item-search');
  const cards = [...document.querySelectorAll('[data-item-search]')];
  const empty = document.querySelector('#item-search-empty');
  if (!input || !cards.length) return;
  const filter = () => {
    const query = input.value.trim().toLocaleLowerCase('ko-KR');
    let visible = 0;
    cards.forEach(card => { const show = !query || card.dataset.itemSearch.toLocaleLowerCase('ko-KR').includes(query); card.hidden = !show; if (show) visible += 1; });
    if (empty) empty.style.display = visible ? 'none' : 'block';
  };
  input.addEventListener('input', filter);
})();
