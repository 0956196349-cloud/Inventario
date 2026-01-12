
const INVENTARIO_URL = "https://inventario-qivs.onrender.com"; 
const VENTAS_URL = "https://ventas-4b2b.onrender.com";
           

async function checkHealth(baseUrl, badgeId, name) {
  const el = document.getElementById(badgeId);
  el.textContent = `${name}: verificando...`;
  el.className = "badge";

  try {
    const res = await fetch(`${baseUrl}/health`, { method: "GET" });
    if (!res.ok) throw new Error("No OK");

    el.textContent = `${name}: activo ✅`;
    el.classList.add("ok");
  } catch (e) {
    el.textContent = `${name}: caído ❌`;
    el.classList.add("fail");
    console.log("Health error:", name, e);
  }
}

window.runHealthChecks = function () {
  checkHealth(INVENTARIO_URL, "invStatus", "Inventario");
  checkHealth(VENTAS_URL, "venStatus", "Ventas");
};

window.API = { INVENTARIO_URL, VENTAS_URL };
