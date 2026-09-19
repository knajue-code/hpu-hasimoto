const toggle=document.querySelector('.menu-toggle');
const nav=document.querySelector('#navigation');
function closeMenu(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Menü öffnen');}
toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Menü schließen':'Menü öffnen');nav.classList.toggle('open',open);});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){closeMenu();toggle.focus();}});
nav?.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu();});
