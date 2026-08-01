"use client";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-panel2 border border-line rounded-lg px-3 py-2 text-xs mono-num">
      <div className="text-muted mb-1">{label}</div>
      <div className="text-signal">${payload[0].value.toLocaleString()}</div>
    </div>
  );
}

export default function TrendLine({ data, xKey = "month", yKey = "revenue", height = 260 }) {
  if (!data?.length) return <EmptyState />;
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
        <CartesianGrid stroke="#242C3B" vertical={false} />
        <XAxis dataKey={xKey} stroke="#7A8699" fontSize={11} tickLine={false} axisLine={{ stroke: "#242C3B" }} />
        <YAxis stroke="#7A8699" fontSize={11} tickLine={false} axisLine={false} tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`} />
        <Tooltip content={<CustomTooltip />} />
        <Line type="monotone" dataKey={yKey} stroke="#FFB000" strokeWidth={2} dot={false} activeDot={{ r: 4, fill: "#FFB000" }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function EmptyState({ label = "No data available for this chart." }) {
  return (
    <div className="h-[200px] flex items-center justify-center text-muted text-sm border border-dashed border-line rounded-lg">
      {label}
    </div>
  );
}
