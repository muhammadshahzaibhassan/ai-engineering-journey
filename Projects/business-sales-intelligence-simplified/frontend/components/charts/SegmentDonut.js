"use client";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { EmptyState } from "./TrendLine";

const COLORS = ["#FFB000", "#39D98A", "#7A8699", "#FF5C5C", "#FFD066", "#5E9CFF"];

export default function SegmentDonut({ data, nameKey = "segment", valueKey = "count", height = 260 }) {
  if (!data?.length) return <EmptyState />;
  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie
          data={data}
          dataKey={valueKey}
          nameKey={nameKey}
          innerRadius={55}
          outerRadius={90}
          paddingAngle={2}
        >
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} stroke="#0B0E14" strokeWidth={2} />
          ))}
        </Pie>
        <Tooltip contentStyle={{ background: "#161C28", border: "1px solid #242C3B", borderRadius: 8, fontSize: 12 }} />
        <Legend
          layout="vertical"
          verticalAlign="middle"
          align="right"
          wrapperStyle={{ fontSize: 12, color: "#7A8699" }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
