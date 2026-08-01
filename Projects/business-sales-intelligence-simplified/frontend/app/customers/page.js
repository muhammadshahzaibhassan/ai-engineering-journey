"use client";
import { useEffect, useState } from "react";
import { useSession } from "../../lib/SessionContext";
import { api } from "../../lib/api";
import Panel from "../../components/Panel";
import SegmentDonut from "../../components/charts/SegmentDonut";
import NoDataState from "../../components/NoDataState";
import { PageHeader, ErrorBox, LoadingBox } from "../../components/Shared";

export default function CustomersPage() {
  const { sessionId, status } = useSession();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (status !== "ready" || !sessionId) return;
    api.customerAnalytics(sessionId).then(setData).catch((e) => setError(e.message));
  }, [sessionId, status]);

  if (status !== "ready") return <NoDataState />;
  if (error) return <ErrorBox message={error} />;
  if (!data) return <LoadingBox />;

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Module 5 / Customer Analytics"
        title="Customer intelligence"
        desc="RFM segments, top accounts, and products frequently bought together."
      />

      <div className="grid md:grid-cols-2 gap-6">
        <Panel title="RFM segments" eyebrow={`${data.rfm_segments.reduce((a, s) => a + s.count, 0)} customers scored`}>
          <SegmentDonut data={data.rfm_segments} nameKey="segment" valueKey="count" />
        </Panel>

        <Panel title="Value tier breakdown">
          <SegmentDonut data={data.segment_breakdown} nameKey="segment" valueKey="count" />
        </Panel>
      </div>

      <Panel title="Top 20 customers by spend">
        <TopCustomersTable rows={data.top_customers} />
      </Panel>

      <Panel title="Frequently bought together" eyebrow="Market-basket co-occurrence, top products">
        <FBTList items={data.frequently_bought_together} />
      </Panel>
    </div>
  );
}

function TopCustomersTable({ rows }) {
  if (!rows?.length) return <p className="text-muted text-sm">No customer data available.</p>;
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-[11px] tracking-widest uppercase text-muted border-b border-line">
            <th className="pb-2 pr-4">Customer</th>
            <th className="pb-2 pr-4">Segment</th>
            <th className="pb-2 pr-4">Country</th>
            <th className="pb-2 pr-4 text-right">Orders</th>
            <th className="pb-2 text-right">Total spent</th>
          </tr>
        </thead>
        <tbody className="mono-num">
          {rows.map((r, i) => (
            <tr key={r.CustomerID ?? i} className="border-b border-line/60 last:border-0">
              <td className="py-2 pr-4 text-paper">{r.CustomerID}</td>
              <td className="py-2 pr-4">
                <SegmentPill segment={r.CustomerSegment} />
              </td>
              <td className="py-2 pr-4 text-muted">{r.Country || "—"}</td>
              <td className="py-2 pr-4 text-right text-paper">{r.NumOrders}</td>
              <td className="py-2 text-right text-signal">${Number(r.TotalSpent).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SegmentPill({ segment }) {
  const colors = {
    Gold: "text-signal border-signal/40 bg-signal/10",
    Silver: "text-paper border-line bg-panel2",
    Bronze: "text-muted border-line bg-panel2",
  };
  const cls = colors[segment] || "text-muted border-line bg-panel2";
  return <span className={`text-[11px] px-2 py-0.5 rounded border ${cls}`}>{segment || "—"}</span>;
}

function FBTList({ items }) {
  if (!items?.length) {
    return <p className="text-muted text-sm">Not enough multi-item orders to compute product pairings.</p>;
  }
  return (
    <div className="grid sm:grid-cols-2 gap-3">
      {items.slice(0, 10).map((item) => (
        <div key={item.product} className="border border-line rounded-lg p-3 bg-panel2/50">
          <div className="text-paper text-sm font-medium mb-1.5 truncate" title={item.product}>
            {item.product}
          </div>
          <div className="space-y-1">
            {item.frequently_bought_with.map((p) => (
              <div key={p.product} className="flex items-center justify-between text-xs">
                <span className="text-muted truncate pr-2">{p.product}</span>
                <span className="mono-num text-signal2 shrink-0">×{p.co_occurrences}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
