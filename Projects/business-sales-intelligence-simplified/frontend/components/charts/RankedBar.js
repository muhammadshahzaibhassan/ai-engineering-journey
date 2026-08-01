"use client";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { EmptyState } from "./TrendLine";

const COLORS = ["#FFB000", "#FFD066", "#39D98A", "#7A8699", "#E8ECF1"];

export default function RankedBar({ data, xKey = "value", yKey = "label", height = 280, valuePrefix = "" }) {
  if (!data?.length) return <EmptyState />;
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} layout="vertical" margin={{ top: 4, right: 24, left: 8, bottom: 4 }}>
        <CartesianGrid stroke="#242C3B" horizontal={false} />
        <XAxis type="number" stroke="#7A8699" fontSize={11} tickLine={false} axisLine={{ stroke: "#242C3B" }} />
        <YAxis
          type="category"
          dataKey={yKey}
          stroke="#7A8699"
          fontSize={11}
          tickLine={false}
          axisLine={false}
          width={110}
        />
        <Tooltip
          cursor={{ fill: "#161C28" }}
          contentStyle={{ background: "#161C28", border: "1px solid #242C3B", borderRadius: 8, fontSize: 12 }}
          formatter={(v) => [`${valuePrefix}${Number(v).toLocaleString()}`, ""]}
        />
        <Bar dataKey={xKey} radius={[0, 4, 4, 0]}>
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} fillOpacity={i === 0 ? 1 : 0.75} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
