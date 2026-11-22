/* CGAP Sign Tracker: team accounts panel. Loaded on /pages/sign-tracker after the tracker config. */
(function () {
  var cfgEl = document.getElementById('tk-cfg'); if (!cfgEl) return;
  var C; try { C = JSON.parse(cfgEl.textContent); } catch (e) { return; }
  var main = document.getElementById('tk-main'); if (!main) return;
  var box = document.createElement('div'); box.className = 'tk-card'; box.id = 'tk-team'; box.style.marginBottom = '1.6rem';
  main.parentNode.insertBefore(box, main);
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  async function api(body) {
    var r = await fetch(C.api, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(Object.assign({}, C.auth, body)) });
    var d = await r.json().catch(function () { return {}; });
    if (!r.ok || !d.ok) throw new Error(d.error || 'Something went wrong');
    return d;
  }
  var btn = 'class="tk-btn tk-btn--ghost" type="button"', obtn = 'class="tk-btn tk-btn--o" type="button"';
  function draw(team) {
    if (!team) {
      box.innerHTML = '<h3 style="margin-top:0">Share this list with your team</h3>' +
        '<p style="font-size:1.4rem;color:var(--mut);margin:.4rem 0 1rem">Safety managers, maintenance leads and site supervisors can all work from one list, across every building and site. Each person signs in with their own account.</p>' +
        '<div class="tk-row"><button ' + obtn + ' data-t="new">Start a team</button><button ' + btn + ' data-t="join">I have a team code</button></div><div id="tkt-f"></div>';
      return;
    }
    var owner = team.role === 'owner';
    box.innerHTML = '<div class="tk-row" style="justify-content:space-between;align-items:center"><h3 style="margin:0">Team: ' + esc(team.name) + '</h3><span style="font-size:1.3rem;color:var(--mut)">' + team.members.length + ' ' + (team.members.length === 1 ? 'person' : 'people') + '</span></div>' +
      '<p style="font-size:1.4rem;margin:.8rem 0">Team code: <b style="font-size:1.7rem;letter-spacing:.12em">' + esc(team.code) + '</b> <button ' + btn + ' data-t="copy">Copy invite</button></p>' +
      '<p style="font-size:1.3rem;color:var(--mut);margin:0 0 .8rem">To add someone, send them the invite. They create a free account, open the Sign Tracker and enter the code. Tip: start each location with the site name, like "Plant 2 / Boiler room", to keep facilities separate.</p>' +
      '<details><summary style="cursor:pointer;font-weight:600">People and settings</summary><ul style="list-style:none;padding:0;margin:.8rem 0">' +
      team.members.map(function (m) { return '<li style="display:flex;justify-content:space-between;gap:1rem;padding:.4rem 0;border-bottom:1px solid #eee"><span>' + esc(m.label) + (m.you ? ' (you)' : '') + (m.role === 'owner' ? ' <small style="color:var(--mut)">owner</small>' : '') + '</span>' + (owner && !m.you ? '<button class="tk-ic" type="button" data-rm="' + esc(m.id) + '">Remove</button>' : '') + '</li>'; }).join('') +
      '</ul><div class="tk-row">' + (owner ? '<button ' + btn + ' data-t="rename">Rename team</button><button ' + btn + ' data-t="code">New code</button>' : '') + '<button ' + btn + ' data-t="label">Change my name</button><button ' + btn + ' data-t="leave">' + (owner ? 'Close team' : 'Leave team') + '</button></div></details><div id="tkt-f"></div>';
    box._team = team;
  }
  function form(html) { var f = box.querySelector('#tkt-f'); f.innerHTML = '<div style="margin-top:1.2rem">' + html + '<div class="tk-err" id="tkt-err"></div></div>'; return f; }
  async function act(body, reload) {
    try { var d = await api(body); if (reload) { location.reload(); return; } draw(d.team); }
    catch (e) { var er = box.querySelector('#tkt-err'); if (er) er.textContent = e.message; else alert(e.message); }
  }
  box.addEventListener('click', function (e) {
    var rm = e.target.closest('[data-rm]'); if (rm) { if (confirm('Remove this person from the team? Signs they added stay on the team list.')) act({ action: 'team_remove', member: rm.getAttribute('data-rm') }); return; }
    var t = e.target.closest('[data-t]'); if (!t) return; t = t.getAttribute('data-t');
    if (t === 'new') {
      form('<label class="tk-f"><span>Team name (usually your company)</span><input id="tkt-n" maxlength="120"></label><label class="tk-f"><span>Your name</span><input id="tkt-l" maxlength="80" value="' + esc(C.name || '') + '"></label><p style="font-size:1.3rem;color:var(--mut)">Signs already on your list move to the team list.</p><button ' + obtn + ' id="tkt-go">Create team</button>');
      box.querySelector('#tkt-go').addEventListener('click', function () { act({ action: 'team_create', name: box.querySelector('#tkt-n').value, label: box.querySelector('#tkt-l').value, move: true }, true); });
    }
    if (t === 'join') {
      form('<label class="tk-f"><span>Team code</span><input id="tkt-c" maxlength="12" style="text-transform:uppercase;letter-spacing:.12em"></label><label class="tk-f"><span>Your name</span><input id="tkt-l" maxlength="80" value="' + esc(C.name || '') + '"></label><label style="display:flex;gap:.6rem;align-items:center;font-size:1.4rem;margin:.6rem 0"><input type="checkbox" id="tkt-m"> Move the signs already on my list into the team list</label><button ' + obtn + ' id="tkt-go">Join team</button>');
      box.querySelector('#tkt-go').addEventListener('click', function () { act({ action: 'team_join', code: box.querySelector('#tkt-c').value, label: box.querySelector('#tkt-l').value, move: box.querySelector('#tkt-m').checked }, true); });
    }
    if (t === 'copy') {
      var tm = box._team, msg = 'Join our safety sign list on CGAP Safety. Create a free account, open ' + location.origin + '/pages/sign-tracker and enter team code ' + tm.code + '.';
      (navigator.clipboard ? navigator.clipboard.writeText(msg) : Promise.reject()).then(function () { alert('Invite copied. Paste it into an email or text.'); }, function () { prompt('Copy this invite:', msg); });
    }
    if (t === 'rename') { var n = prompt('New team name:', box._team.name); if (n) act({ action: 'team_rename', name: n }); }
    if (t === 'code') { if (confirm('Make a new team code? The old code stops working. People already on the team stay.')) act({ action: 'team_code' }); }
    if (t === 'label') { var l = prompt('Your name as your team sees it:'); if (l) act({ action: 'team_label', label: l }); }
    if (t === 'leave') {
      var own = box._team.role === 'owner';
      if (confirm(own ? 'Close this team? Everyone loses access to the shared list, and each sign goes back to the person who added it.' : 'Leave this team? Signs you added stay with the team.')) act({ action: 'team_leave' }, true);
    }
  });
  api({ action: 'list' }).then(function (d) { draw(d.team); }).catch(function () { box.remove(); });
})();
