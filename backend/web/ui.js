async function json(url, options) { const response = await fetch(url, options); if (!response.ok) throw new Error(await response.text()); return response.json(); }
async function refresh() {
  try { const health = await json('/health'); document.querySelector('#health').textContent = health.status; } catch { document.querySelector('#health').textContent = 'offline'; }
  try {
    const approvals = await json('/v1/approvals');
    document.querySelector('#approvals').replaceChildren(...approvals.map(a => { const row=document.createElement('div'); row.className='card'; row.textContent=a.action+' — '+a.state; if(a.state==='pending'){ for(const pair of [['Approve','approve'],['Reject','reject']]){const b=document.createElement('button');b.textContent=pair[0];b.onclick=async()=>{await json('/v1/approvals/'+a.approval_id+'/'+pair[1],{method:'POST'});refresh();};row.appendChild(b);} } return row; }));
  } catch { document.querySelector('#approvals').textContent='unavailable'; }
  try { const runs = await json('/v1/runs?limit=20'); document.querySelector('#runs').replaceChildren(...runs.map(r=>{const row=document.createElement('div');row.className='card';row.textContent=r.run_id+' — '+r.status;return row;})); } catch { document.querySelector('#runs').textContent='unavailable'; }
}
document.querySelector('#analyze').onclick=async()=>{const task=document.querySelector('#task').value;try{document.querySelector('#analysis').textContent=JSON.stringify(await json('/v1/tasks/analyze',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({task})}),null,2);}catch(e){document.querySelector('#analysis').textContent=String(e);}};
refresh();
