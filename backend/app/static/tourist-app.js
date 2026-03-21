const travelerKpis = document.getElementById('travelerKpis');
const placesList = document.getElementById('placesList');
const alertsList = document.getElementById('alertsList');
const servicesList = document.getElementById('servicesList');

const renderCard = (title, body, badgeText, badgeClass = 'low') => `
  <div class="card">
    ${badgeText ? `<span class="badge ${badgeClass}">${badgeText}</span>` : ''}
    <h4>${title}</h4>
    <p class="muted">${body}</p>
  </div>`;

async function loginDemoTourist() {
  const response = await fetch('/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ email: 'tourist@demo.com', password: 'demo123' })
  });
  const body = await response.json();
  alert(`Logged in as ${body.display_name}`);
}

async function loadDashboard() {
  const [placesRes, alertsRes, servicesRes, sosRes, incidentRes] = await Promise.all([
    fetch('/places?city=Jaipur'),
    fetch('/alerts/feed'),
    fetch('/support-services?city=Jaipur'),
    fetch('/sos'),
    fetch('/incidents')
  ]);

  const [places, alerts, services, sos, incidents] = await Promise.all([
    placesRes.json(), alertsRes.json(), servicesRes.json(), sosRes.json(), incidentRes.json()
  ]);

  travelerKpis.innerHTML = [
    { label: 'Curated places', value: places.length },
    { label: 'Live alerts', value: alerts.length },
    { label: 'Emergency services', value: services.length },
    { label: 'Open cases', value: sos.length + incidents.length },
  ].map(item => `<div class="kpi"><span class="muted">${item.label}</span><strong>${item.value}</strong></div>`).join('');

  placesList.innerHTML = places.map(place => renderCard(
    `${place.name} • ${place.city}`,
    `${place.description} Timings: ${place.timings}. Entry fee: ₹${place.entry_fee}.`,
    `Safety ${place.safety_score}`,
    place.safety_score >= 75 ? 'low' : 'medium'
  )).join('');

  alertsList.innerHTML = alerts.map(alert => renderCard(
    alert.title,
    alert.message,
    alert.type.toUpperCase(),
    alert.type === 'critical' ? 'high' : alert.type === 'warning' ? 'medium' : 'low'
  )).join('');

  servicesList.innerHTML = services.map(service => renderCard(
    `${service.name} • ${service.service_type}`,
    `${service.address} • ${service.phone}`,
    service.is_verified ? 'Verified' : 'Unverified',
    service.is_verified ? 'low' : 'medium'
  )).join('');
}

function formToJson(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  Object.keys(data).forEach(key => {
    if (['latitude', 'longitude'].includes(key)) data[key] = Number(data[key]);
    if (['travelers', 'severity'].includes(key)) data[key] = Number(data[key]);
  });
  data.panic_mode = form.querySelector('[name="panic_mode"]')?.checked || false;
  if (data.interests) data.interests = data.interests.split(',').map(v => v.trim()).filter(Boolean);
  return data;
}

async function bindForms() {
  document.getElementById('tripForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const response = await fetch('/trips', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(formToJson(event.target))
    });
    const trip = await response.json();
    document.getElementById('tripResult').textContent = `Trip ${trip.id} saved for ${trip.city} (${trip.start_date} to ${trip.end_date}).`;
  });

  document.getElementById('locationForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const response = await fetch('/location/update', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(formToJson(event.target))
    });
    const body = await response.json();
    const safety = body.safety;
    document.getElementById('safetyResult').innerHTML = `
      <span class="badge ${safety.level === 'LOW' ? 'low' : safety.level === 'MEDIUM' ? 'medium' : 'high'}">${safety.level} risk • ${safety.score}</span>
      <p>${safety.reasons.join(' ')}</p>
      <p class="muted">${safety.advice}</p>`;
  });

  document.getElementById('sosForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const response = await fetch('/sos/trigger', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(formToJson(event.target))
    });
    const body = await response.json();
    document.getElementById('sosResult').textContent = `SOS ${body.id} is ${body.status}. Admins have been notified.`;
    await loadDashboard();
  });

  document.getElementById('incidentForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const response = await fetch('/incidents', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(formToJson(event.target))
    });
    const body = await response.json();
    document.getElementById('incidentResult').textContent = `Incident ${body.id} submitted with severity ${body.severity}.`;
    await loadDashboard();
  });
}

document.getElementById('loginBtn').addEventListener('click', loginDemoTourist);
document.getElementById('refreshBtn').addEventListener('click', loadDashboard);
loadDashboard();
bindForms();
