"use client";
import { useEffect, useState } from "react";
import { useSession } from "../../lib/SessionContext";
import { api } from "../../lib/api";
import Panel from "../../components/Panel";
import KpiTicker from "../../components/KpiTicker";
import TrendLine from "../../components/charts/TrendLine";
import RankedBar from "../../components/charts/RankedBar";
import NoDataState from "../../components/NoDataState";
import { PageHeader, ErrorBox, LoadingBox, ToggleButton } from "../../components/Shared";

export default function SalesPage() {
  const { sessionId, status } = useSession();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [productView, setProductView] = useState("by_revenue");

  useEffect(() => {
    if (status !== "ready" || !sessionId) return;
    api.salesAnalytics(sessionId).then(setData).catch((e) => setError(e.message));
  }, [sessionId, status]);

  if (status !== "ready") return <NoDataState />;
  if (error) return <ErrorBox message={error} />;
  if (!data) return <LoadingBox />;

  const countryData = data.revenue_by_country.map((c) => ({ label: c.country, value: c.revenue }));
  const productData = (data.top_products[productView] || []).map((p) => ({
    label: p.product,
    value: productView === "by_revenue" ? p.revenue : p.quantity,
  }));

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Module 3 / EDA" title="Sales performance" desc="Revenue trend, top markets, and best/worst sellers." />

      <KpiTicker kpis={data.kpis} />

      <Panel title="Monthly revenue trend">
        <TrendLine data={data.monthly_trend} />
      </Panel>

      <div className="grid md:grid-cols-2 gap-6">
        <Panel title="Revenue by country">
          <RankedBar data={countryData} valuePrefix="$" />
        </Panel>

        <Panel
          title="Top products"
          action={
            <div className="flex gap-1 text-xs">
              <ToggleButton active={productView === "by_revenue"} onClick={() => setProductView("by_revenue")}>
                Revenue
              </ToggleButton>
              <ToggleButton active={productView === "by_quantity"} onClick={() => setProductView("by_quantity")}>
                Quantity
              </ToggleButton>
            </div>
          }
        >
          <RankedBar data={productData} valuePrefix={productView === "by_revenue" ? "$" : ""} />
        </Panel>
      </div>
    </div>
  );
}
