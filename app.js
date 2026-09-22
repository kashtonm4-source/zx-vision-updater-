const routes = ['overview', 'profiles', 'shot', 'stabilizer', 'meter', 'dashboard', 'remote', 'controllers', 'sync', 'backgrounds', 'settings', 'about'];
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


const profiles = ['Competitive', 'Park / Casual', 'Remote Play', 'Practice Lab', 'Custom'];
const profileGrid = document.querySelector('#profile-grid');
if (profileGrid) {
  const active = Number(localStorage.getItem('tv-profile') || 0);
  profileGrid.innerHTML = profiles.map((name, i) => `<button class="profile-card ${i === active ? 'selected' : ''}" data-profile="${i}"><span class="profile-number">P${i + 1}</span><strong>${name}</strong><small>${i === active ? 'Active now' : 'Saved profile'}</small></button>`).join('');
  profileGrid.addEventListener('click', event => {
    const card = event.target.closest('[data-profile]'); if (!card) return;
    const index = Number(card.dataset.profile); localStorage.setItem('tv-profile', index);
    profileGrid.querySelectorAll('.profile-card').forEach(item => item.classList.toggle('selected', item === card));
    const label = document.querySelector('#active-profile-name'); if (label) label.textContent = `Profile ${index + 1} · ${profiles[index]}`;
    addLog(`Profile ${index + 1} loaded — ${profiles[index]}`); showToast('Profile loaded', `${profiles[index]} is now active.`);
  });
  document.querySelector('#active-profile-name').textContent = `Profile ${active + 1} · ${profiles[active]}`;
}
function addLog(message) {
  const lines = document.querySelector('#log-lines'); if (!lines) return;
  const row = document.createElement('div'); row.innerHTML = `<time>NOW</time><span class="log-dot"></span><p>${message}</p>`; lines.prepend(row);
}
document.querySelectorAll('[data-reset]').forEach(button => button.addEventListener('click', () => showToast('Defaults restored', `${button.dataset.reset} settings reset for the active profile.`)));
document.querySelectorAll('.step-btn').forEach(button => button.addEventListener('click', () => {
  const input = document.querySelector('#release-range'); const next = Math.max(0, Math.min(15, Number(input.value) + Number(button.dataset.delta))); input.value = next; document.querySelector('#release-value').textContent = `${next.toFixed(1)}%`; addLog(`Release Timing changed → ${next.toFixed(1)}%`);
}));
const releaseRange = document.querySelector('#release-range'); if (releaseRange) releaseRange.addEventListener('input', () => { document.querySelector('#release-value').textContent = `${Number(releaseRange.value).toFixed(1)}%`; });
document.querySelectorAll('.background-card').forEach(card => card.addEventListener('click', () => { document.querySelectorAll('.background-card').forEach(item => item.classList.remove('selected')); card.classList.add('selected'); localStorage.setItem('tv-background', card.dataset.bg); showToast('Background applied', `${card.querySelector('strong').textContent} is active.`); }));
document.querySelector('#scan-devices')?.addEventListener('click', event => { const button = event.currentTarget; button.disabled = true; button.innerHTML = 'SCANNING… <span>⌁</span>'; addLog('Device scan started — waiting for native bridge.'); setTimeout(() => { button.disabled = false; button.innerHTML = 'SCAN FOR DEVICES <span>⌁</span>'; addLog('Scan complete — no native bridge detected in browser preview.'); showToast('Scan complete', 'No native devices available in browser preview.'); }, 900); });
document.querySelector('#bridge-help')?.addEventListener('click', () => showToast('Native bridge required', 'Install the desktop companion to enumerate hardware.'));
document.querySelector('#clear-log')?.addEventListener('click', () => { const lines = document.querySelector('#log-lines'); if (lines) lines.innerHTML = ''; showToast('Log cleared', 'Computer vision results log is empty.'); });
