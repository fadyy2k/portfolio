const menu=document.querySelector('.menu');
const navLinks=document.querySelector('.nav-links');
menu?.addEventListener('click',()=>{const open=navLinks.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
navLinks?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{navLinks.classList.remove('open');menu?.setAttribute('aria-expanded','false');}));

const reveal=new IntersectionObserver((entries)=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');reveal.unobserve(e.target);}}),{threshold:.08});
document.querySelectorAll('.reveal').forEach(el=>reveal.observe(el));

const sections=[...document.querySelectorAll('main section[id]')];
const navAnchors=[...document.querySelectorAll('.nav-links a[href^="#"]')];
const spy=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){navAnchors.forEach(a=>a.classList.toggle('active',a.getAttribute('href')===`#${e.target.id}`));}})},{rootMargin:'-35% 0px -55% 0px',threshold:0});
sections.forEach(s=>spy.observe(s));

document.querySelectorAll('.card').forEach(card=>card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();card.style.setProperty('--mx',`${e.clientX-r.left}px`);card.style.setProperty('--my',`${e.clientY-r.top}px`);}));

document.querySelector('[data-year]').textContent=new Date().getFullYear();
