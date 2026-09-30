// ANNAMITRA - Complete Frontend Application Logic

// Global Application State
const state = {
  currentUser: {
    id: 1,
    name: "BMSIT College Mess",
    email: "mess@bmsit.in",
    role: "DONOR",
    institution_id: 1,
    verification_status: "VERIFIED"
  },
  currentTab: "dashboard",
  donations: [],
  deliveries: [],
  routes: [],
  impact: null,
  institutions: [],
  users: [],
  map: null,
  mapMarkers: [],
  mapRoutes: [],
  impactChart: null,
  beneficiaryChart: null,
  currentModalDeliveryId: null
};

// Demo User Profiles for 1-Click Role Switching
const DEMO_USERS = {
  donor: {
    id: 1,
    name: "BMSIT College Mess",
    email: "mess@bmsit.in",
    role: "DONOR",
    phone: "+91-9880112233",
    institution_id: 1,
    verification_status: "VERIFIED"
  },
  receiver: {
    id: 5,
    name: "Hospital Caretaker Food Hub",
    email: "caretakers@bowring.org",
    role: "RECEIVER",
    phone: "+91-9845112233",
    institution_id: null,
    verification_status: "VERIFIED"
  },
  volunteer: {
    id: 9,
    name: "Ravi Kumar",
    email: "ravi.volunteer@annamitra.org",
    role: "VOLUNTEER",
    phone: "+91-9740112233",
    institution_id: null,
    verification_status: "VERIFIED"
  },
  admin: {
    id: 12,
    name: "Dr. Ananya Sharma",
    email: "admin@annamitra.org",
    role: "ADMIN",
    phone: "+91-9800000001",
    institution_id: null,
    verification_status: "VERIFIED"
  }
};

// Initialize application on DOM load
document.addEventListener("DOMContentLoaded", () => {
  // Check if saved user exists
  const savedUser = localStorage.getItem("annamitra_user");
  if (savedUser) {
    try {
      state.currentUser = JSON.parse(savedUser);
    } catch (e) {
      state.currentUser = DEMO_USERS.donor;
    }
  }

  updateUserInterfaceHeader();
  initLeafletMap();
  initCharts();
  
  // Initial data fetch
  refreshAllData();

  // Periodic refresh for real-time countdowns & expiry checks
  setInterval(() => {
    updateCountdownBadges();
  }, 10000);

  // Auto refresh impact every 30 seconds
  setInterval(() => {
    fetchImpactMetrics();
  }, 30000);

  lucide.createIcons();
});

// Toast notification helper
function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  const bgClass = type === "error" ? "bg-rose-900 border-rose-700 text-rose-100" :
                  type === "warning" ? "bg-amber-900 border-amber-700 text-amber-100" :
                  "bg-emerald-900 border-emerald-700 text-emerald-100";
  const icon = type === "error" ? "alert-circle" : type === "warning" ? "alert-triangle" : "check-circle";

  toast.className = `p-4 rounded-xl border shadow-lg flex items-center space-x-3 text-xs md:text-sm toast-animate ${bgClass}`;
  toast.innerHTML = `
    <i data-lucide="${icon}" class="w-5 h-5 flex-shrink-0"></i>
    <span class="flex-1">${message}</span>
    <button onclick="this.parentElement.remove()" class="opacity-70 hover:opacity-100">
      <i data-lucide="x" class="w-4 h-4"></i>
    </button>
  `;

  container.appendChild(toast);
  lucide.createIcons();

  setTimeout(() => {
    if (toast.parentElement) toast.remove();
  }, 5000);
}

// Update UI Header and User Display
function updateUserInterfaceHeader() {
  const nameEl = document.getElementById("header-user-name");
  const roleEl = document.getElementById("header-user-role");
  const bannerEl = document.getElementById("role-banner-text");
  const roleSwitcher = document.getElementById("role-selector");

  if (nameEl) nameEl.textContent = state.currentUser.name;
  if (roleEl) roleEl.textContent = state.currentUser.role;
  if (roleSwitcher) roleSwitcher.value = state.currentUser.role.toLowerCase();

  // Role contextual banner
  if (bannerEl) {
    if (state.currentUser.role === "DONOR") {
      bannerEl.innerHTML = `<b>Donor Mode:</b> Log surplus food batches from campus mess or events. Track remaining pickup windows.`;
    } else if (state.currentUser.role === "RECEIVER") {
      bannerEl.innerHTML = `<b>Receiver Mode:</b> Review available high-priority surplus food, claim batches, and confirm meals distributed.`;
    } else if (state.currentUser.role === "VOLUNTEER") {
      bannerEl.innerHTML = `<b>Volunteer Mode:</b> View clustered pickup routes, verify digital food temperatures, and deliver to drop hubs.`;
    } else if (state.currentUser.role === "ADMIN") {
      bannerEl.innerHTML = `<b>Admin Mode:</b> Real-time operational monitoring, user verification, and NAAC Social Impact Report generation.`;
    }
  }

  // Toggle role-specific action buttons
  const postBtn = document.getElementById("nav-post-food-btn");
  if (postBtn) {
    if (state.currentUser.role === "DONOR" || state.currentUser.role === "ADMIN") {
      postBtn.classList.remove("hidden");
    } else {
      postBtn.classList.add("hidden");
    }
  }
}

// Role Switcher Handler
function switchUserRole(roleKey) {
  const targetUser = DEMO_USERS[roleKey];
  if (!targetUser) return;

  state.currentUser = targetUser;
  localStorage.setItem("annamitra_user", JSON.stringify(targetUser));
  updateUserInterfaceHeader();

  showToast(`Switched active persona to ${targetUser.name} (${targetUser.role})`, "info");

  // Contextual redirect based on Section 20
  if (targetUser.role === "DONOR") {
    switchTab("donations");
  } else if (targetUser.role === "RECEIVER") {
    switchTab("donations");
  } else if (targetUser.role === "VOLUNTEER") {
    switchTab("routes");
  } else if (targetUser.role === "ADMIN") {
    switchTab("dashboard");
  }

  refreshAllData();
}

// Navigation Tabs
function switchTab(tabId) {
  state.currentTab = tabId;
  const tabs = ["dashboard", "donations", "routes", "deliveries", "impact", "reports", "users"];
  
  tabs.forEach(t => {
    const view = document.getElementById(`view-${t}`);
    const navBtn = document.getElementById(`nav-tab-${t}`);
    if (view) view.classList.add("hidden");
    if (navBtn) {
      navBtn.classList.remove("bg-emerald-600", "text-white", "font-semibold");
      navBtn.classList.add("text-slate-300", "hover:text-white");
    }
  });

  const activeView = document.getElementById(`view-${tabId}`);
  const activeBtn = document.getElementById(`nav-tab-${tabId}`);
  if (activeView) activeView.classList.remove("hidden");
  if (activeBtn) {
    activeBtn.classList.add("bg-emerald-600", "text-white", "font-semibold");
    activeBtn.classList.remove("text-slate-300");
  }

  lucide.createIcons();

  if (tabId === "routes" || tabId === "dashboard") {
    setTimeout(() => {
      if (state.map) state.map.invalidateSize();
    }, 200);
  }

  if (tabId === "impact") {
    setTimeout(() => {
      if (state.impactChart) state.impactChart.resize();
      if (state.beneficiaryChart) state.beneficiaryChart.resize();
    }, 200);
  }
}

// Refresh all live backend data
async function refreshAllData() {
  await Promise.all([
    fetchImpactMetrics(),
    fetchDonations(),
    fetchDeliveries(),
    fetchRoutes(),
    fetchInstitutions(),
    fetchUsers()
  ]);
}

// ==========================================
// API CALLS & DATA FETCHING
// ==========================================

async function fetchImpactMetrics() {
  try {
    const res = await fetch("/impact");
    if (!res.ok) throw new Error("Failed to fetch impact metrics");
    const data = await res.json();
    state.impact = data;
    renderImpactMetrics(data);
    updateCharts(data);
  } catch (err) {
    console.error("Error loading impact metrics:", err);
  }
}

async function fetchDonations() {
  try {
    const res = await fetch("/donations");
    if (!res.ok) throw new Error("Failed to fetch donations");
    const data = await res.json();
    state.donations = data;
    renderDonations(data);
    renderRecentDonationsDashboard(data);
    updateMapMarkers();
  } catch (err) {
    console.error("Error loading donations:", err);
  }
}

async function fetchDeliveries() {
  try {
    const res = await fetch("/deliveries");
    if (!res.ok) throw new Error("Failed to fetch deliveries");
    const data = await res.json();
    state.deliveries = data;
    renderDeliveries(data);
  } catch (err) {
    console.error("Error loading deliveries:", err);
  }
}

async function fetchRoutes() {
  try {
    const res = await fetch("/routes");
    if (!res.ok) throw new Error("Failed to fetch clustered routes");
    const data = await res.json();
    state.routes = data;
    renderRoutes(data);
    renderMapRoutes(data);
  } catch (err) {
    console.error("Error loading routes:", err);
  }
}

async function fetchInstitutions() {
  try {
    const res = await fetch("/institutions");
    if (!res.ok) throw new Error("Failed to fetch institutions");
    const data = await res.json();
    state.institutions = data;
    populateInstitutionSelector(data);
  } catch (err) {
    console.error("Error loading institutions:", err);
  }
}

async function fetchUsers() {
  try {
    const res = await fetch("/users");
    if (!res.ok) throw new Error("Failed to fetch users");
    const data = await res.json();
    state.users = data;
    renderUsersTable(data);
  } catch (err) {
    console.error("Error loading users:", err);
  }
}

// ==========================================
// RENDERING FUNCTIONS
// ==========================================

function renderImpactMetrics(data) {
  // Update dashboard and impact tab KPIs
  const setTxt = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  };

  setTxt("kpi-meals-rescued", Number(data.meals_rescued).toLocaleString());
  setTxt("kpi-food-saved", `${Number(data.food_saved_kg).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1})} kg`);
  setTxt("kpi-successful-donations", Number(data.successful_donations).toLocaleString());
  setTxt("kpi-people-served", Number(data.people_served).toLocaleString());
  setTxt("kpi-completed-deliveries", Number(data.completed_deliveries).toLocaleString());
  setTxt("kpi-co2e-avoided", `${Number(data.co2e_avoided_kg).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1})} kg`);
  setTxt("kpi-waste-cost-saved", `₹ ${Number(data.waste_cost_saved_inr).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`);

  // Summary counts
  setTxt("count-total-donations", data.total_donations || 0);
  setTxt("count-active-donations", data.active_donations || 0);
  setTxt("count-completed-donations", data.successful_donations || 0);
  setTxt("count-expired-donations", data.expired_donations || 0);
}

function renderDonations(donations) {
  const container = document.getElementById("donations-grid");
  const emptyState = document.getElementById("donations-empty-state");
  if (!container) return;

  if (!donations || donations.length === 0) {
    container.innerHTML = "";
    if (emptyState) emptyState.classList.remove("hidden");
    return;
  }
  if (emptyState) emptyState.classList.add("hidden");

  const isReceiver = state.currentUser.role === "RECEIVER";
  const isDonor = state.currentUser.role === "DONOR";

  container.innerHTML = donations.map(d => {
    const priorityBadgeClass = d.priority_color === "red" ? "badge-urgent" :
                               d.priority_color === "orange" ? "badge-high" :
                               d.priority_color === "yellow" ? "badge-medium" : "badge-low";

    const isAvailable = d.status === "AVAILABLE";
    const isExpired = d.status === "EXPIRED";

    return `
      <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm hover-card flex flex-col justify-between">
        <div>
          <!-- Header: Dietary Type & Priority Badge -->
          <div class="flex items-center justify-between gap-2 mb-3">
            <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold ${d.dietary_type === 'VEG' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'}">
              ${d.dietary_type === 'VEG' ? '🌱 100% VEGETARIAN' : '🍗 NON-VEGETARIAN'}
            </span>
            <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-extrabold uppercase tracking-wide ${priorityBadgeClass}">
              ${d.priority_badge === 'URGENT' ? '🟥 URGENT' : d.priority_badge === 'HIGH' ? '🟧 HIGH' : d.priority_badge === 'MEDIUM' ? '🟨 MEDIUM' : '🟩 LOW'}
            </span>
          </div>

          <!-- Food Name & Donor -->
          <h3 class="text-base font-bold text-slate-900 leading-snug">${d.food_name}</h3>
          <p class="text-xs text-slate-500 mt-1 flex items-center">
            <i data-lucide="building" class="w-3.5 h-3.5 mr-1 text-slate-400"></i> ${d.institution_name || d.donor_name}
          </p>

          <!-- Metrics: Weight & Servings -->
          <div class="mt-4 grid grid-cols-2 gap-2 p-3 bg-slate-50 rounded-xl border border-slate-100">
            <div>
              <p class="text-[10px] uppercase font-bold text-slate-400">Surplus Weight</p>
              <p class="text-lg font-black text-emerald-800">${d.quantity_kg} <span class="text-xs font-semibold text-slate-500">kg</span></p>
            </div>
            <div>
              <p class="text-[10px] uppercase font-bold text-slate-400">Portions</p>
              <p class="text-lg font-black text-slate-800">${d.servings} <span class="text-xs font-semibold text-slate-500">meals</span></p>
            </div>
          </div>

          <!-- Location & Safe Window -->
          <div class="mt-4 space-y-1.5 text-xs text-slate-600">
            <div class="flex items-center">
              <i data-lucide="map-pin" class="w-3.5 h-3.5 mr-1.5 text-slate-400"></i>
              <span class="truncate">${d.pickup_location}</span>
              ${d.distance_km ? `<span class="ml-1.5 text-[11px] text-slate-400 font-medium">(${d.distance_km} km)</span>` : ''}
            </div>
            <div class="flex items-center font-medium ${isExpired ? 'text-rose-600' : 'text-amber-700'}">
              <i data-lucide="clock" class="w-3.5 h-3.5 mr-1.5"></i>
              <span>${d.pickup_window_text}</span>
            </div>
          </div>
        </div>

        <!-- Action Section -->
        <div class="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between">
          <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
            d.status === 'AVAILABLE' ? 'bg-emerald-100 text-emerald-800' :
            d.status === 'CLAIMED' ? 'bg-blue-100 text-blue-800' :
            d.status === 'IN_TRANSIT' ? 'bg-purple-100 text-purple-800' :
            d.status === 'DELIVERED' ? 'bg-indigo-100 text-indigo-800' :
            d.status === 'COMPLETED' ? 'bg-teal-100 text-teal-800' :
            'bg-slate-100 text-slate-600'
          }">
            ● ${d.status.replace('_', ' ')}
          </span>

          ${isAvailable ? `
            <button onclick="claimDonation(${d.id})" class="px-3.5 py-1.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-semibold rounded-lg shadow-sm transition flex items-center space-x-1">
              <i data-lucide="hand-heart" class="w-3.5 h-3.5"></i>
              <span>CLAIM FOOD</span>
            </button>
          ` : isExpired ? `
            <span class="text-xs text-rose-500 font-semibold italic">Window Expired</span>
          ` : `
            <span class="text-xs text-slate-400 font-medium">Batch Claimed</span>
          `}
        </div>
      </div>
    `;
  }).join("");

  lucide.createIcons();
}

function renderRecentDonationsDashboard(donations) {
  const tbody = document.getElementById("dashboard-donations-tbody");
  if (!tbody) return;

  const activeDonations = donations.slice(0, 6);
  tbody.innerHTML = activeDonations.map(d => `
    <tr class="hover:bg-slate-50 transition border-b border-slate-100 text-xs">
      <td class="py-3 px-4 font-semibold text-slate-800">#${d.id}</td>
      <td class="py-3 px-4">
        <span class="font-bold text-slate-900">${d.food_name}</span>
        <span class="block text-[10px] text-slate-400">${d.institution_name}</span>
      </td>
      <td class="py-3 px-4 font-bold text-emerald-800">${d.quantity_kg} kg</td>
      <td class="py-3 px-4 font-medium text-slate-600">${d.servings}</td>
      <td class="py-3 px-4 font-medium">${d.pickup_window_text}</td>
      <td class="py-3 px-4">
        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${
          d.status === 'AVAILABLE' ? 'bg-emerald-100 text-emerald-800' :
          d.status === 'CLAIMED' ? 'bg-blue-100 text-blue-800' :
          d.status === 'IN_TRANSIT' ? 'bg-purple-100 text-purple-800' :
          d.status === 'COMPLETED' ? 'bg-teal-100 text-teal-800' : 'bg-slate-100 text-slate-600'
        }">${d.status}</span>
      </td>
      <td class="py-3 px-4 text-right">
        ${d.status === 'AVAILABLE' ? `
          <button onclick="claimDonation(${d.id})" class="px-2.5 py-1 bg-emerald-700 hover:bg-emerald-800 text-white rounded font-medium text-[11px]">Claim</button>
        ` : `
          <span class="text-slate-400">-</span>
        `}
      </td>
    </tr>
  `).join("");
}

function renderDeliveries(deliveries) {
  const container = document.getElementById("deliveries-container");
  if (!container) return;

  if (!deliveries || deliveries.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center bg-white rounded-2xl border border-slate-200">
        <i data-lucide="package" class="w-10 h-10 mx-auto text-slate-300 mb-2"></i>
        <p class="text-sm font-semibold text-slate-600">No active delivery dispatches</p>
        <p class="text-xs text-slate-400 mt-1">Claim surplus food to initiate volunteer dispatch runs</p>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  container.innerHTML = deliveries.map(del => {
    const don = del.donation || {};
    const isVolunteer = state.currentUser.role === "VOLUNTEER" || state.currentUser.role === "ADMIN";
    const isReceiver = state.currentUser.role === "RECEIVER" || state.currentUser.role === "ADMIN";

    return `
      <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-5 hover-card">
        <div class="space-y-2 flex-1">
          <!-- Status Line & ID -->
          <div class="flex items-center space-x-2">
            <span class="px-2.5 py-1 bg-slate-900 text-white text-[10px] font-bold rounded uppercase">Dispatch #${del.id}</span>
            <span class="px-2.5 py-1 rounded text-[10px] font-bold uppercase ${
              del.status === 'CLAIMED' ? 'bg-amber-100 text-amber-800' :
              del.status === 'VOLUNTEER_ASSIGNED' ? 'bg-blue-100 text-blue-800' :
              del.status === 'IN_TRANSIT' ? 'bg-purple-100 text-purple-800' :
              del.status === 'DELIVERED' ? 'bg-indigo-100 text-indigo-800' :
              del.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600'
            }">
              ● ${del.status.replace('_', ' ')}
            </span>
            ${del.pickup_temperature ? `
              <span class="px-2 py-0.5 bg-emerald-50 border border-emerald-200 text-emerald-800 text-[10px] font-semibold rounded">
                Verified: ${del.pickup_temperature}°C
              </span>
            ` : ''}
          </div>

          <!-- Food & Quantity -->
          <h4 class="text-base font-bold text-slate-900">${don.food_name || 'Surplus Meal Batch'}</h4>
          <p class="text-xs text-slate-500 font-medium">
            Quantity: <b>${don.quantity_kg || 25} kg</b> • Approx: <b>${don.servings || 80} meals</b>
          </p>

          <!-- Routing Nodes -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs pt-2">
            <div class="flex items-start space-x-1.5">
              <i data-lucide="arrow-up-right" class="w-4 h-4 text-emerald-600 mt-0.5"></i>
              <div>
                <p class="text-[10px] font-bold uppercase text-slate-400">Pickup Source</p>
                <p class="font-semibold text-slate-800">${don.institution_name || don.donor_name || 'BMSIT Campus'}</p>
                <p class="text-slate-500 text-[11px]">${don.pickup_location || 'Campus Gate 1'}</p>
              </div>
            </div>
            <div class="flex items-start space-x-1.5">
              <i data-lucide="arrow-down-left" class="w-4 h-4 text-purple-600 mt-0.5"></i>
              <div>
                <p class="text-[10px] font-bold uppercase text-slate-400">Destination Drop Point</p>
                <p class="font-semibold text-slate-800">${del.receiver_name || 'Hospital Caretaker Hub'}</p>
                <p class="text-slate-500 text-[11px]">Bangalore Distribution Network</p>
              </div>
            </div>
          </div>

          ${del.notes ? `
            <p class="text-xs text-slate-500 italic bg-slate-50 p-2 rounded-lg border border-slate-100">
              Notes: ${del.notes}
            </p>
          ` : ''}
        </div>

        <!-- Action Buttons based on Delivery Status -->
        <div class="flex flex-col sm:flex-row md:flex-col gap-2 justify-center min-w-[180px]">
          ${del.status === 'CLAIMED' ? `
            <button onclick="acceptPickupTask(${del.id})" class="w-full px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center justify-center space-x-1.5">
              <i data-lucide="check" class="w-4 h-4"></i>
              <span>ACCEPT PICKUP</span>
            </button>
          ` : del.status === 'VOLUNTEER_ASSIGNED' ? `
            <button onclick="openPickupModal(${del.id})" class="w-full px-4 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center justify-center space-x-1.5">
              <i data-lucide="thermometer" class="w-4 h-4"></i>
              <span>PICK UP FOOD</span>
            </button>
          ` : del.status === 'IN_TRANSIT' ? `
            <button onclick="confirmVolunteerDelivery(${del.id})" class="w-full px-4 py-2.5 bg-purple-700 hover:bg-purple-800 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center justify-center space-x-1.5">
              <i data-lucide="navigation-2" class="w-4 h-4"></i>
              <span>DELIVER FOOD</span>
            </button>
          ` : del.status === 'DELIVERED' ? `
            <button onclick="openReceiverConfirmModal(${del.id}, ${don.quantity_kg || 30}, ${don.servings || 100})" class="w-full px-4 py-2.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center justify-center space-x-1.5">
              <i data-lucide="clipboard-check" class="w-4 h-4"></i>
              <span>CONFIRM RECEIPT</span>
            </button>
          ` : `
            <div class="text-center py-2 px-3 bg-emerald-50 border border-emerald-200 rounded-xl">
              <span class="text-xs font-bold text-emerald-800 flex items-center justify-center">
                <i data-lucide="check-circle" class="w-4 h-4 mr-1"></i> RESCUE COMPLETE
              </span>
              <p class="text-[10px] text-emerald-600 mt-0.5">${del.received_quantity_kg || don.quantity_kg} kg verified</p>
            </div>
          `}
        </div>
      </div>
    `;
  }).join("");

  lucide.createIcons();
}

function renderRoutes(clusters) {
  const container = document.getElementById("routes-container");
  if (!container) return;

  if (!clusters || clusters.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center bg-white rounded-2xl border border-slate-200">
        <i data-lucide="map" class="w-10 h-10 mx-auto text-slate-300 mb-2"></i>
        <p class="text-sm font-semibold text-slate-600">No active pickup routes generated</p>
        <p class="text-xs text-slate-400 mt-1">When surplus food is posted, nearby batches (within 1.5 km) are automatically clustered</p>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  container.innerHTML = clusters.map(c => `
    <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover-card space-y-4">
      <!-- Route Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-2">
        <div>
          <span class="px-2.5 py-1 bg-emerald-100 text-emerald-800 text-[10px] font-bold rounded uppercase tracking-wider">${c.route_id} • Clustered Route</span>
          <h3 class="text-base font-bold text-slate-900 mt-1.5">${c.pickups.length} Clustered Pickup Point(s)</h3>
          <p class="text-xs text-slate-500">${c.donor_names.join(" ➔ ")}</p>
        </div>
        <div class="text-left sm:text-right">
          <p class="text-xl font-black text-emerald-800">${c.total_servings} <span class="text-xs font-semibold text-slate-500">servings</span></p>
          <p class="text-xs text-slate-500 font-medium">${c.total_weight_kg} kg aggregate • ~${c.estimated_distance_km} km</p>
        </div>
      </div>

      <!-- Pickups & Waypoints -->
      <div class="space-y-2">
        <p class="text-[11px] font-bold uppercase text-slate-400">Waypoints (Within 1.5 km Radius)</p>
        <div class="space-y-2">
          ${c.pickups.map((p, idx) => `
            <div class="flex items-center justify-between text-xs p-2.5 bg-slate-50 rounded-xl border border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-full bg-emerald-800 text-white flex items-center justify-center font-bold text-[10px]">${idx + 1}</span>
                <div>
                  <span class="font-bold text-slate-800">${p.donor_name}</span>
                  <span class="text-slate-400 text-[11px] ml-1">(${p.food_name})</span>
                </div>
              </div>
              <span class="font-semibold text-emerald-800">${p.quantity_kg} kg</span>
            </div>
          `).join("")}
        </div>
      </div>

      <!-- Drop Point -->
      ${c.recommended_drop_point ? `
        <div class="p-3 bg-purple-50 rounded-xl border border-purple-100 flex items-center justify-between text-xs">
          <div class="flex items-center space-x-2">
            <i data-lucide="arrow-down-circle" class="w-5 h-5 text-purple-700"></i>
            <div>
              <p class="text-[10px] font-bold uppercase text-purple-700">Recommended Beneficiary Hub</p>
              <p class="font-bold text-slate-800">${c.recommended_drop_point.name}</p>
              <p class="text-slate-500 text-[11px]">${c.recommended_drop_point.address}</p>
            </div>
          </div>
          <span class="px-2 py-0.5 bg-white text-purple-800 text-[10px] font-bold rounded border border-purple-200">Sufficient Capacity</span>
        </div>
      ` : ''}

      <!-- Accept Button -->
      <div class="pt-2 flex justify-end">
        <button onclick="acceptConsolidatedRoute('${c.route_id}')" class="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center space-x-2">
          <i data-lucide="check-circle" class="w-4 h-4"></i>
          <span>ACCEPT ROUTE</span>
        </button>
      </div>
    </div>
  `).join("");

  lucide.createIcons();
}

function renderUsersTable(users) {
  const tbody = document.getElementById("users-table-tbody");
  if (!tbody) return;

  tbody.innerHTML = users.map(u => `
    <tr class="hover:bg-slate-50 border-b border-slate-100 text-xs transition">
      <td class="py-3 px-4 font-bold text-slate-800">${u.name}</td>
      <td class="py-3 px-4 text-slate-600">${u.email}</td>
      <td class="py-3 px-4 font-semibold">
        <span class="px-2 py-0.5 rounded text-[10px] ${
          u.role === 'DONOR' ? 'bg-amber-100 text-amber-800' :
          u.role === 'RECEIVER' ? 'bg-purple-100 text-purple-800' :
          u.role === 'VOLUNTEER' ? 'bg-blue-100 text-blue-800' : 'bg-slate-900 text-white'
        }">${u.role}</span>
      </td>
      <td class="py-3 px-4 text-slate-600">${u.phone}</td>
      <td class="py-3 px-4">
        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${u.verification_status === 'VERIFIED' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">
          ${u.verification_status}
        </span>
      </td>
      <td class="py-3 px-4 text-right">
        <button onclick="toggleVerification(${u.id})" class="px-2.5 py-1 rounded text-[11px] font-medium transition ${
          u.verification_status === 'VERIFIED' ? 'bg-slate-100 hover:bg-rose-100 text-slate-700 hover:text-rose-700' : 'bg-emerald-600 hover:bg-emerald-700 text-white'
        }">
          ${u.verification_status === 'VERIFIED' ? 'Revoke' : 'Verify'}
        </button>
      </td>
    </tr>
  `).join("");
}

function populateInstitutionSelector(institutions) {
  const sel = document.getElementById("naac-institution-select");
  if (!sel) return;

  sel.innerHTML = institutions.map(i => `
    <option value="${i.id}">${i.name} (${i.type} • AISHE: ${i.AISHE_code || 'N/A'})</option>
  `).join("");
}

// ==========================================
// WORKFLOW ACTIONS (HACKATHON STEPS 1 to 7)
// ==========================================

// Step 1: Donor Posts Surplus Food
async function handlePostDonationSubmit(event) {
  event.preventDefault();

  const foodName = document.getElementById("post-food-name").value;
  const mealType = document.getElementById("post-meal-type").value;
  const dietaryType = document.getElementById("post-dietary-type").value;
  const qtyKg = parseFloat(document.getElementById("post-quantity-kg").value);
  const servings = parseInt(document.getElementById("post-servings").value);
  const deadlineHours = parseFloat(document.getElementById("post-deadline-hours").value) || 2.0;
  const pickupLocation = document.getElementById("post-pickup-location").value;

  const payload = {
    donor_id: state.currentUser.id,
    food_name: foodName,
    meal_type: mealType,
    dietary_type: dietaryType,
    quantity_kg: qtyKg,
    servings: servings,
    pickup_deadline_hours: deadlineHours,
    pickup_location: pickupLocation,
    latitude: 13.1332,
    longitude: 77.5684,
    safety_confirmed: true
  };

  try {
    const res = await fetch("/donations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to post surplus food");
    }

    const data = await res.json();
    showToast(`✅ Surplus food posted successfully! Pickup window: ${data.pickup_window_text}`);
    closeModal("modal-post-donation");
    document.getElementById("form-post-donation").reset();

    // Refresh data and switch to donations tab
    await refreshAllData();
    switchTab("donations");
  } catch (err) {
    showToast(err.message, "error");
  }
}

// Step 3: Receiver Claims Food
async function claimDonation(donationId) {
  try {
    const res = await fetch(`/donations/${donationId}/claim`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        receiver_id: state.currentUser.id
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Unable to claim donation");
    }

    const data = await res.json();
    showToast(`🎉 Food batch claimed! Volunteer pickup dispatch #${data.delivery_id} generated.`);
    await refreshAllData();
    switchTab("deliveries");
  } catch (err) {
    showToast(err.message, "error");
  }
}

// Step 5a: Volunteer Accepts Pickup Task
async function acceptPickupTask(deliveryId) {
  try {
    const res = await fetch(`/deliveries/${deliveryId}/assign`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ volunteer_id: state.currentUser.id })
    });

    if (!res.ok) throw new Error("Could not assign delivery task");
    showToast(`🚴 Delivery task #${deliveryId} assigned to ${state.currentUser.name}`);
    await refreshAllData();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function acceptConsolidatedRoute(routeId) {
  showToast(`🚴 Consolidated ${routeId} claimed! Waypoint routing dispatched to your volunteer app.`);
  switchTab("deliveries");
}

// Step 5b: Volunteer Opens Pickup Temperature Verification Modal
function openPickupModal(deliveryId) {
  state.currentModalDeliveryId = deliveryId;
  const tempInput = document.getElementById("pickup-temperature-input");
  if (tempInput) tempInput.value = "64.5"; // Sensible default for hot food
  validateLiveTemperature();
  openModal("modal-pickup-verification");
}

// Live Temperature Validation Preview
function validateLiveTemperature() {
  const tempInput = document.getElementById("pickup-temperature-input");
  const isHotCheck = document.getElementById("pickup-is-hot-food");
  const alertBox = document.getElementById("pickup-temperature-alert");

  if (!tempInput || !alertBox) return;

  const temp = parseFloat(tempInput.value);
  const isHot = isHotCheck ? isHotCheck.checked : true;

  if (isNaN(temp)) {
    alertBox.classList.add("hidden");
    return;
  }

  alertBox.classList.remove("hidden");
  if (isHot) {
    if (temp >= 60.0) {
      alertBox.className = "p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 font-medium";
      alertBox.innerHTML = `✅ <b>Compliant:</b> Food temperature is <b>${temp}°C</b> (≥ 60°C). FSSAI hot holding guideline satisfied.`;
    } else {
      alertBox.className = "p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800 font-medium";
      alertBox.innerHTML = `⚠️ <b>Warning:</b> Food temperature is <b>${temp}°C</b> (below standard 60°C). Handled under special rapid-transit safeguard protocol.`;
    }
  } else {
    if (temp <= 10.0) {
      alertBox.className = "p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 font-medium";
      alertBox.innerHTML = `✅ <b>Compliant:</b> Cold food temperature is <b>${temp}°C</b> (≤ 10°C). Safe cold-chain maintained.`;
    } else {
      alertBox.className = "p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800 font-medium";
      alertBox.innerHTML = `⚠️ <b>Warning:</b> Cold food temperature is <b>${temp}°C</b> (exceeds 10°C). Operational safeguard flag recorded.`;
    }
  }
}

// Submit Pickup Confirmation
async function handleConfirmPickupSubmit(event) {
  event.preventDefault();
  const deliveryId = state.currentModalDeliveryId;
  const temp = parseFloat(document.getElementById("pickup-temperature-input").value);
  const isHot = document.getElementById("pickup-is-hot-food").checked;
  const proof = document.getElementById("pickup-proof-input").value || "https://annamitra.org/proofs/thermal_verification.jpg";
  const notes = document.getElementById("pickup-notes-input").value;

  try {
    const res = await fetch(`/deliveries/${deliveryId}/pickup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        volunteer_id: state.currentUser.id,
        temperature_celsius: temp,
        is_hot_food: isHot,
        proof: proof,
        notes: notes
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Pickup logging failed");
    }

    const data = await res.json();
    closeModal("modal-pickup-verification");

    if (data.warning) {
      showToast(data.warning, "warning");
    } else {
      showToast(`✅ Food verified at ${temp}°C and picked up! Safe transit window open.`);
    }

    await refreshAllData();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// Step 5c: Volunteer Confirms Delivery Arrival
async function confirmVolunteerDelivery(deliveryId) {
  try {
    const res = await fetch(`/deliveries/${deliveryId}/deliver`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        notes: "Arrived at destination drop hub in good condition."
      })
    });

    if (!res.ok) throw new Error("Could not log delivery arrival");
    showToast(`📦 Delivery arrival recorded! Awaiting receiver headcount confirmation.`);
    await refreshAllData();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// Step 7: Receiver Opens Confirmation Modal
function openReceiverConfirmModal(deliveryId, estimatedKg, estimatedServings) {
  state.currentModalDeliveryId = deliveryId;
  const kgInput = document.getElementById("confirm-received-kg");
  const srvInput = document.getElementById("confirm-meals-distributed");

  if (kgInput) kgInput.value = estimatedKg || 28.0;
  if (srvInput) srvInput.value = estimatedServings || 95;

  openModal("modal-receiver-confirm");
}

// Step 7: Receiver Confirms Delivery & Generates ImpactLog
async function handleReceiverConfirmSubmit(event) {
  event.preventDefault();
  const deliveryId = state.currentModalDeliveryId;
  const receivedKg = parseFloat(document.getElementById("confirm-received-kg").value);
  const mealsDistributed = parseInt(document.getElementById("confirm-meals-distributed").value);
  const notes = document.getElementById("confirm-notes").value;

  try {
    const res = await fetch(`/deliveries/${deliveryId}/confirm`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        received_quantity_kg: receivedKg,
        meals_distributed: mealsDistributed,
        notes: notes
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Confirmation failed");
    }

    const data = await res.json();
    closeModal("modal-receiver-confirm");
    showToast(`🎉 Verified ${data.food_saved_kg} kg received & ${data.meals_served} meals served! Impact logged.`);
    await refreshAllData();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// Admin: Toggle verification
async function toggleVerification(userId) {
  try {
    const res = await fetch(`/users/${userId}/verify`, { method: "POST" });
    if (!res.ok) throw new Error("Could not update verification status");
    const data = await res.json();
    showToast(`User ${data.name} verification status changed to ${data.verification_status}`);
    fetchUsers();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// Step 10: Download NAAC / Impact Audit PDF Report
function downloadNaacReport() {
  const sel = document.getElementById("naac-institution-select");
  const instId = sel ? sel.value : 1;
  const url = `/reports/naac?institution_id=${instId}`;
  showToast("📄 Generating official NAAC / Institutional Impact Audit PDF...", "info");
  window.open(url, "_blank");
}

// Helper: Servings calculator in form
function calculateServingsFromKg(val) {
  const kg = parseFloat(val);
  const srvInput = document.getElementById("post-servings");
  if (!isNaN(kg) && kg > 0) {
    srvInput.value = Math.round(kg * 3.3); // ~30 kg = 100 servings
  } else {
    srvInput.value = "";
  }
}

// Helper: Update countdown badges
function updateCountdownBadges() {
  fetchDonations();
}

// ==========================================
// MODALS
// ==========================================
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.remove("hidden");
  lucide.createIcons();
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.add("hidden");
}

// ==========================================
// LEAFLET MAP VISUALIZATION (BENGALURU)
// ==========================================
function initLeafletMap() {
  const mapEl = document.getElementById("map");
  if (!mapEl) return;

  // Center on Bengaluru Central
  state.map = L.map("map").setView([12.9716, 77.5946], 12);

  // Free OpenStreetMap Tiles
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "© OpenStreetMap contributors | Annamitra Logistics Engine"
  }).addTo(state.map);
}

function updateMapMarkers() {
  if (!state.map) return;

  // Clear existing markers
  state.mapMarkers.forEach(m => state.map.removeLayer(m));
  state.mapMarkers = [];

  // Seeded Bengaluru Donor Pins
  state.donations.forEach(d => {
    if (d.latitude && d.longitude && d.status !== "EXPIRED") {
      const isUrgent = d.priority_badge === "URGENT";
      const iconHtml = `
        <div style="background-color: ${isUrgent ? '#ef4444' : '#059669'}; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">
          🍱
        </div>
      `;

      const customIcon = L.divIcon({
        html: iconHtml,
        className: "custom-pin",
        iconSize: [28, 28],
        iconAnchor: [14, 14]
      });

      const marker = L.marker([d.latitude, d.longitude], { icon: customIcon }).addTo(state.map);
      marker.bindPopup(`
        <div style="font-family: inherit; font-size: 12px; line-height: 1.4;">
          <b style="color: #064e3b; font-size: 13px;">${d.food_name}</b><br/>
          <span>${d.institution_name || d.donor_name}</span><br/>
          <span><b>${d.quantity_kg} kg</b> • ${d.servings} servings</span><br/>
          <span style="color: ${isUrgent ? '#b91c1c' : '#059669'}; font-weight: bold;">${d.pickup_window_text}</span><br/>
          <button onclick="claimDonation(${d.id})" style="margin-top: 6px; background: #059669; color: white; border: none; padding: 4px 8px; border-radius: 4px; font-weight: bold; cursor: pointer;">Claim Food</button>
        </div>
      `);
      state.mapMarkers.push(marker);
    }
  });

  // Seeded Distribution Point Pins (Receivers)
  const dropPoints = [
    { name: "Hospital Caretaker Food Hub", lat: 12.9832, lon: 77.6019, type: "Govt Hospital" },
    { name: "Majestic Community Shelter", lat: 12.9781, lon: 77.5695, type: "Railway Shelter" },
    { name: "Koramangala Community Kitchen", lat: 12.9380, lon: 77.6200, type: "Community Kitchen" },
    { name: "Community Fridge Hub", lat: 12.9298, lon: 77.5833, type: "Community Fridge" }
  ];

  dropPoints.forEach(dp => {
    const iconHtml = `
      <div style="background-color: #7c3aed; color: white; width: 30px; height: 30px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">
        🏢
      </div>
    `;
    const icon = L.divIcon({
      html: iconHtml,
      className: "drop-pin",
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    });

    const marker = L.marker([dp.lat, dp.lon], { icon: icon }).addTo(state.map);
    marker.bindPopup(`
      <div style="font-family: inherit; font-size: 12px;">
        <b style="color: #6b21a8; font-size: 13px;">${dp.name}</b><br/>
        <span>Demographic: ${dp.type}</span><br/>
        <span style="color: #059669; font-weight: bold;">Verified Distribution Hub</span>
      </div>
    `);
    state.mapMarkers.push(marker);
  });
}

function renderMapRoutes(clusters) {
  if (!state.map) return;

  // Clear existing polylines
  state.mapRoutes.forEach(r => state.map.removeLayer(r));
  state.mapRoutes = [];

  clusters.forEach((c, idx) => {
    const latlngs = [];
    c.pickups.forEach(p => {
      latlngs.push([p.latitude, p.longitude]);
    });

    if (c.recommended_drop_point) {
      latlngs.push([c.recommended_drop_point.latitude, c.recommended_drop_point.longitude]);
    }

    if (latlngs.length >= 2) {
      const polyline = L.polyline(latlngs, {
        color: idx === 0 ? "#059669" : "#3b82f6",
        weight: 4,
        opacity: 0.8,
        dashArray: "6, 8"
      }).addTo(state.map);

      polyline.bindPopup(`
        <div style="font-size: 12px;">
          <b>${c.route_id}</b><br/>
          <span>${c.pickups.length} Pickups ➔ Drop Point</span><br/>
          <span><b>${c.total_weight_kg} kg</b> aggregate</span>
        </div>
      `);
      state.mapRoutes.push(polyline);
    }
  });
}

// ==========================================
// CHARTS INITIALIZATION (CHART.JS)
// ==========================================
function initCharts() {
  const ctxTrend = document.getElementById("chart-rescue-trend");
  const ctxBeneficiary = document.getElementById("chart-beneficiaries");

  if (ctxTrend) {
    state.impactChart = new Chart(ctxTrend, {
      type: "line",
      data: {
        labels: ["Day 1", "Day 5", "Day 10", "Day 15", "Day 20", "Day 25", "Today"],
        datasets: [
          {
            label: "Food Rescued (kg)",
            data: [350, 780, 1420, 1980, 2540, 2980, 3242],
            borderColor: "#059669",
            backgroundColor: "rgba(5, 150, 105, 0.1)",
            fill: true,
            tension: 0.35
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }

  if (ctxBeneficiary) {
    state.beneficiaryChart = new Chart(ctxBeneficiary, {
      type: "doughnut",
      data: {
        labels: ["Hospital Caretakers", "Transit Shelters", "Community Kitchens", "Community Fridges"],
        datasets: [
          {
            data: [42, 28, 20, 10],
            backgroundColor: ["#059669", "#7c3aed", "#f59e0b", "#0284c7"],
            borderWidth: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom" }
        }
      }
    });
  }
}

function updateCharts(impactData) {
  if (state.impactChart && impactData) {
    const totalKg = impactData.food_saved_kg;
    state.impactChart.data.datasets[0].data = [
      Math.round(totalKg * 0.1),
      Math.round(totalKg * 0.25),
      Math.round(totalKg * 0.45),
      Math.round(totalKg * 0.65),
      Math.round(totalKg * 0.8),
      Math.round(totalKg * 0.92),
      Math.round(totalKg)
    ];
    state.impactChart.update();
  }
}
