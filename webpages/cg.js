/* CGAP Safety: sign lists with one-click add to cart, used on library and industry pages. */
(function(){
var me=document.currentScript||document.querySelector('script[src*="/webpages/cg.js"]');
var BASE=me.src.replace(/cg\.js(\?.*)?$/,'');
var LIVE='https://raw.githubusercontent.com/joepannell95/CGAP-CAST/main/webpages/d/';
function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function tag(c){c=(c||'').toUpperCase();if(c.indexOf('ISO')===0)return '<span class="tag t-ISO">ISO 7010</span>';var k=c.indexOf('SAFETY')===0?'SAFETY':c;return '<span class="tag t-'+k+'">'+esc(k==='SAFETY'?'SAFETY FIRST':c)+'</span>'}
function li(s){return '<li><input type="checkbox"'+(s[6]?'':' checked')+' data-h="'+esc(s[0])+'" aria-label="Include '+esc(s[1])+'"><div>'+tag(s[2])+'<a href="/products/'+esc(s[0])+'"><b>'+esc(s[1])+'</b></a>'+(s[4]?'<span class="req">REQUIRED BY RULE</span>':'')+(s[3]?'<p class="why">'+esc(s[3])+'</p>':'')+'</div></li>'}
function render(root,list){
 var box=root.querySelector('[data-cg-list]');if(!box)return;
 var groups=[],by={};list.forEach(function(s){var g=s[5]||'';if(!(g in by)){by[g]=[];groups.push(g)}by[g].push(s)});
 var h='';groups.forEach(function(g,i){if(g)h+='<h2>'+(i+1)+'. '+esc(g)+'</h2>';h+='<ul class="sl">'+by[g].map(li).join('')+'</ul>'});
 h+='<div class="bar"><button type="button" class="btn" data-cg-add>Add signs to cart</button><span class="note">'+esc(box.getAttribute('data-note')||'')+'</span></div>';
 box.innerHTML=h;var seo=root.querySelector('.cgl-wrap');if(seo)seo.style.display='none';bind(root);
}
function bind(root){
 var btn=root.querySelector('[data-cg-add]');
 function picked(){return Array.prototype.slice.call(root.querySelectorAll('input[data-h]:checked')).map(function(i){return i.getAttribute('data-h')})}
 function upd(){var n=picked().length;btn.textContent=n?('Add '+n+' sign'+(n>1?'s':'')+' to cart'):'Pick at least one sign';btn.disabled=!n}
 root.addEventListener('change',function(e){if(e.target.matches('input[data-h]'))upd()});upd();
 btn.addEventListener('click',async function(){
  var hs=picked();if(!hs.length)return;btn.disabled=true;btn.textContent='Adding...';var items=[];
  await Promise.all(hs.map(async function(h){try{var r=await fetch('/products/'+h+'.js');if(!r.ok)return;var p=await r.json();var v=p.variants.find(function(x){return x.available})||p.variants[0];items.push({id:v.id,quantity:1})}catch(e){}}));
  if(!items.length){btn.textContent='Could not add. Try again';btn.disabled=false;return}
  var r=await fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:items})});
  if(r.ok)location.href='/cart';else{btn.textContent='Could not add. Try again';btn.disabled=false}
 });
}
document.querySelectorAll('.cg[data-cg]').forEach(function(root){
 var f=root.getAttribute('data-cg')+'.json';
 fetch(LIVE+f).then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return fetch(BASE+'d/'+f).then(function(r){return r.json()})}).then(function(l){render(root,l)}).catch(function(){});
});
})();
