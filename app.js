const routes = ['overview', 'remote', 'controllers', 'sync', 'settings'];
const navItems = document.querySelectorAll('.nav-item');
const title = document.querySelector('#page-title');
const pageTitles = { overview: 'Good evening, Alex', remote: 'Remote Play', controllers: 'Controller studio', sync: 'Auto Sync', settings: 'Settings' };
const toast = document.querySelector('#toast');
let toastTimer;

function showToast(head, copy) {
  document.querySelector('#toast-title').textContent = head;
  document.querySelector('#toast-copy').textContent = copy;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}
function go(route) {
  if (!routes.includes(route)) route = 'overview';
  document.querySelectorAll('.view').forEach(v => v.classList.toggle('active', v.id === `view-${route}`));
  navItems.forEach(item => item.classList.toggle('active', item.dataset.route === route));
  title.textContent = pageTitles[route];
  history.replaceState({}, '', `#${route}`);
}
document.addEventListener('click', event => {
  const target = event.target.closest('[data-route]');
  if (target) go(target.dataset.route);
});
navItems.forEach(item => item.addEventListener('click', () => go(item.dataset.route)));

const mapDefaults = [
  ['CROSS', 'Cross / confirm', '×'], ['CIRCLE', 'Circle / cancel', '○'], ['SQUARE', 'Square / action', '□'], ['TRIANGLE', 'Triangle / menu', '△'],
  ['L1', 'Left bumper', 'L1'], ['R1', 'Right bumper', 'R1'], ['L2', 'Left trigger', 'L2'], ['R2', 'Right trigger', 'R2']
];
const mapList = document.querySelector('#map-list');
const mapOptions = ['Cross / confirm', 'Circle / cancel', 'Square / action', 'Triangle / menu', 'Left bumper', 'Right bumper', 'Left trigger', 'Right trigger', 'Unassigned'];
function renderMap() {
  const saved = JSON.parse(localStorage.getItem('zx-map') || 'null') || mapDefaults.map(row => row[1]);
  mapList.innerHTML = mapDefaults.map((row, index) => `<div class="map-row"><span class="map-key">${row[0]}</span><select data-map-index="${index}">${mapOptions.map(option => `<option ${option === saved[index] ? 'selected' : ''}>${option}</option>`).join('')}</select><span class="map-arrow">→</span></div>`).join('');
}
renderMap();
mapList.addEventListener('change', event => {
  if (!event.target.matches('select')) return;
  const values = [...mapList.querySelectorAll('select')].map(select => select.value);
  localStorage.setItem('zx-map', JSON.stringify(values));
  showToast('Mapping updated', 'Your controller profile was saved locally.');
});
document.querySelector('#reset-map').addEventListener('click', () => { localStorage.removeItem('zx-map'); renderMap(); showToast('Mapping reset', 'Profile A is back to the default layout.'); });
document.querySelector('#save-profile').addEventListener('click', () => { localStorage.setItem('zx-map', JSON.stringify([...mapList.querySelectorAll('select')].map(select => select.value))); showToast('Profile saved', 'Profile A is ready across your devices.'); });

document.querySelector('#sync-now').addEventListener('click', () => {
  const button = document.querySelector('#sync-now');
  button.disabled = true; button.innerHTML = '<span class="sync-dot"></span>SYNCING…';
  setTimeout(() => { button.disabled = false; button.innerHTML = '<span class="sync-dot"></span>SYNC NOW'; showToast('Sync complete', 'Your preferences are up to date.'); }, 900);
});
document.querySelector('#start-session').addEventListener('click', event => {
  const button = event.currentTarget;
  button.textContent = 'CONNECTING…'; button.disabled = true;
  setTimeout(() => { button.innerHTML = 'END SESSION <span>×</span>'; button.disabled = false; button.classList.add('connected'); document.querySelector('.session-status').innerHTML = '<i></i>LIVE · 12 MS'; document.querySelector('.session-status').style.color = 'var(--green)'; document.querySelector('.screen-center strong').textContent = 'STREAM ACTIVE'; document.querySelector('.screen-center span').textContent = 'DualSense input passthrough is live'; showToast('Session connected', 'Remote Play is streaming from your PS5.'); }, 1100);
});
document.querySelector('#quality-btn').addEventListener('click', () => document.querySelector('#quality').focus());
document.querySelectorAll('.toggle').forEach(toggle => toggle.addEventListener('click', () => { toggle.classList.toggle('on'); showToast(toggle.classList.contains('on') ? 'Enabled' : 'Disabled', 'Preference updated on this device.'); }));
document.querySelector('#theme-toggle').addEventListener('click', () => { document.body.classList.toggle('contrast'); showToast('Contrast updated', 'Display preference saved locally.'); });
document.querySelector('#accent-select').addEventListener('change', event => { document.body.classList.remove('accent-blue', 'accent-purple'); if (event.target.value !== 'green') document.body.classList.add(`accent-${event.target.value}`); showToast('Accent updated', `${event.target.value} signal applied.`); });

document.addEventListener('keydown', event => {
  if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
  const key = event.key.toUpperCase();
  const interesting = { 'C': 'Cross / confirm', 'X': 'Cross / confirm', 'O': 'Circle / cancel', 'S': 'Square / action', 'T': 'Triangle / menu', 'L': 'Left bumper', 'R': 'Right bumper' };
  if (interesting[key]) {
    const readout = document.querySelector('#last-input');
    if (readout) { readout.textContent = `${interesting[key]} · ${key}`; document.querySelector('#input-time').textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit', second: '2-digit'}); }
  }
  if (event.key === 'Escape') go('overview');
  if (event.key === 'F1') go('remote');
});
const hash = location.hash.replace('#', '');
if (routes.includes(hash)) go(hash);
