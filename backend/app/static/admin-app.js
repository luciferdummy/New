const adminKpis = document.getElementById('adminKpis');
const zonesList = document.getElementById('zonesList');
const adminSosList = document.getElementById('adminSosList');
const adminIncidentsList = document.getElementById('adminIncidentsList');

const renderAdminCard = (title, body, badgeText, badgeClass = 'low') => `
  <div class="card">
    ${badgeText ? `<span class="badge ${badgeClass}">${badgeText}</span>` : ''}
    <h4>${title}</h4>
    <p class="muted">${body}</p>
  </div>`;

async function loginDemoAdmin() {
  const response = await fetch('/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ email: 'admin@demo.com', password: 'admin123' })
  });
  const body = await response.json();
  alert(`Logged in as ${body.display_name}`);
}

async function loadAdmin() {
  const [summaryRes, zonesRes, sosRes, incidentsRes] = await Promise.all([
    fetch('/admin/dashboard/summary'),
    fetch('/admin/unsafe-zones'),
    fetch('/admin/sos'),
    fetch('/admin/incidents')
  ]);

  const [summary, zones, sos, incidents] = await Promise.all([
    summaryRes.json(), zonesRes.json(), sosRes.json(), incidentsRes.json()
  ]);

  adminKpis.innerHTML = Object.entries(summary).map(([label, value]) => `
    <div class="kpi"><span class="muted">${label.replaceAll('_', ' ')}</span><strong>${value}</strong></div>`).join('');

  zonesList.innerHTML = zones.map(zone => renderAdminCard(
    `${zone.title} • ${zone.city}`,
    `${zone.advice} Radius: ${zone.radius_km} km.`,
    `Severity ${zone.severity}`,
    zone.severity >= 4 ? 'high' : 'medium'
  )).join('');

  adminSosList.innerHTML = sos.length ? sos.map(alert => renderAdminCard(
    `${alert.traveler_name} • ${alert.city}`,
    `${alert.message} Trigger: ${alert.trigger_method}.`,
    alert.status.toUpperCase(),
    alert.status === 'active' ? 'high' : 'medium'
  )).join('') : '<p class="muted">No active SOS alerts.</p>';

  adminIncidentsList.innerHTML = incidents.length ? incidents.map(incident => renderAdminCard(
    `${incident.category} • ${incident.traveler_name}`,
    incident.description,
    `Severity ${incident.severity}`,
    incident.severity >= 4 ? 'high' : 'medium'
  )).join('') : '<p class="muted">No incidents reported.</p>';
}

function formToJson(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  ['severity', 'latitude', 'longitude', 'radius_km'].forEach(key => data[key] = Number(data[key]));
  data.active_from = new Date(data.active_from).toISOString();
  data.active_until = new Date(data.active_until).toISOString();
  return data;
}

async function bindAdminForms() {
  const zoneForm = document.getElementById('zoneForm');
  const now = new Date();
  const later = new Date(now.getTime() + 6 * 60 * 60 * 1000);
  zoneForm.active_from.value = now.toISOString().slice(0, 16);
  zoneForm.active_until.value = later.toISOString().slice(0, 16);

  zoneForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const response = await fetch('/admin/unsafe-zones', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(formToJson(event.target)),
    });
    const body = await response.json();
    document.getElementById('zoneResult').textContent = `Zone ${body.id} published for ${body.city}.`;
    await loadAdmin();
  });
}

document.getElementById('adminLoginBtn').addEventListener('click', loginDemoAdmin);
document.getElementById('adminRefreshBtn').addEventListener('click', loadAdmin);
loadAdmin();
bindAdminForms();
