function fmtCurrency(v) {
  if (v === null || v === undefined) return "—";
  return v.toLocaleString(undefined, { style: "currency", currency: "USD", maximumFractionDigits: 0 });
}
function fmtNum(v) {
  if (v === null || v === undefined) return "—";
  return v.toLocaleString();
}
function fmtPct(v) {
  if (v === null || v === undefined) return "—";
  return `${(v * 100).toFixed(1)}%`;
}

export default function KpiTicker({ kpis }) {
  const items = [
    { label: "TOTAL REVENUE", value: fmtCurrency(kpis?.total_revenue) },
    { label: "ORDERS", value: fmtNum(kpis?.total_orders) },
    { label: "CUSTOMERS", value: fmtNum(kpis?.total_customers) },
    { label: "PRODUCTS", value: fmtNum(kpis?.total_products) },
    { label: "AVG ORDER VALUE", value: fmtCurrency(kpis?.avg_order_value) },
    { label: "REPEAT RATE", value: fmtPct(kpis?.repeat_customer_rate) },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-px bg-line border border-line rounded-xl overflow-hidden">
      {items.map((item) => (
        <div key={item.label} className="bg-panel px-4 py-3.5">
          <div className="text-[10px] tracking-widest text-muted mono-num mb-1.5">{item.label}</div>
          <div className="text-xl font-semibold text-paper mono-num">{item.value}</div>
        </div>
      ))}
    </div>
  );
}
