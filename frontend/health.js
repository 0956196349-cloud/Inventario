window.API = {
  INVENTARIO_URL: "https://inventario-qivs.onrender.com",
  VENTAS_URL: "https://ventas-4b2b.onrender.com"
};

async function runHealthChecks(){
  const inv = document.getElementById("invStatus");
  const ven = document.getElementById("venStatus");

  // Inventario
  try{
    const r1 = await fetch(`${window.API.INVENTARIO_URL}/health`);
    const ok = r1.ok;
    inv.textContent = ok ? "Inventario: OK" : "Inventario: CAÍDO";
    inv.className = ok ? "badge ok" : "badge fail";
  }catch{
    inv.textContent = "Inventario: CAÍDO";
    inv.className = "badge fail";
  }

  // Ventas
  try{
    const r2 = await fetch(`${window.API.VENTAS_URL}/health`);
    const ok = r2.ok;
    ven.textContent = ok ? "Ventas: OK" : "Ventas: CAÍDO";
    ven.className = ok ? "badge ok" : "badge fail";
  }catch{
    ven.textContent = "Ventas: CAÍDO";
    ven.className = "badge fail";
  }
}
