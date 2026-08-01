"use client";
import { useEffect, useState } from "react";
import { useSession } from "../../lib/SessionContext";
import { api } from "../../lib/api";
import Panel from "../../components/Panel";
import NoDataState from "../../components/NoDataState";
import { PageHeader, ErrorBox, LoadingBox } from "../../components/Shared";

export default function ModelPage() {
  const { sessionId, status, trainInfo, train } = useSession();
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [training, setTraining] = useState(false);

  useEffect(() => {
    if (status !== "ready" || !sessionId) return;
    api.report(sessionId).then(setReport).catch((e) => setError(e.message));
  }, [sessionId, status, trainInfo]);

  if (status !== "ready") return <NoDataState />;
  if (error) return <ErrorBox message={error} />;

  const handleTrain = async () => {
    setTraining(true);
    try {
      await train();
    } catch (e) {
      setError(e.message || String(e));
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Module 7-9 / Evaluation & Report"
        title="Model performance & report"
        desc="Confusion matrices, feature importance, and a shareable summary of everything above."
      />

      {!trainInfo && (
        <Panel title="No trained model yet">
          <p className="text-muted text-sm mb-4">
            Train the repeat-purchase model on the Prediction page, or right here.
          </p>
          <button
            onClick={handleTrain}
            disabled={training}
            className="bg-signal text-ink font-medium text-sm px-4 py-2 rounded-lg hover:bg-signal2 transition-colors focus-ring disabled:opacity-50"
          >
            {training ? "Training…" : "Train models"}
          </button>
        </Panel>
      )}

      {trainInfo && (
        <>
          <Panel
            title="Confusion matrices"
            eyebrow={`Class balance — one-time: ${trainInfo.class_balance?.["0"]}, repeat: ${trainInfo.class_balance?.["1"]}`}
          >
            <div className="grid sm:grid-cols-3 gap-4">
              {Object.entries(trainInfo.confusion_matrices || {}).map(([name, cm]) => (
                <ConfusionMatrix key={name} name={name} matrix={cm} best={name === trainInfo.best_model_name} />
              ))}
            </div>
          </Panel>

          <Panel
            title="Why Random Forest predicts what it predicts"
            eyebrow="Feature importance"
          >
            {trainInfo.feature_importance ? (
              <FeatureBars items={trainInfo.feature_importance} />
            ) : (
              <p className="text-muted text-sm">Feature importance unavailable.</p>
            )}
            <p className="text-xs text-muted mt-4 leading-relaxed">
              The bars above show which inputs move the Random Forest's prediction the most.
              Features derived from spend and purchase frequency typically dominate — customers who
              buy often and spend more are the clearest repeat-purchase signal, more so than
              geography, which usually contributes least.
            </p>
          </Panel>
        </>
      )}

      {!report && <LoadingBox />}

      {report && (
        <Panel
          title="Business report"
          eyebrow={report.filename}
          action={
            <button
              onClick={() => downloadJson(report)}
              className="text-xs text-muted hover:text-signal transition-colors focus-ring rounded px-2 py-1"
            >
              Download JSON
            </button>
          }
        >
          <div className="space-y-5 text-sm">
            {report.data_warnings?.length > 0 && (
              <div className="text-signal2 space-y-1 text-xs">
                {report.data_warnings.map((w, i) => <div key={i}>⚠ {w}</div>)}
              </div>
            )}

            <ReportRow label="Total revenue" value={fmtCurrency(report.kpis.total_revenue)} />
            <ReportRow label="Total orders" value={report.kpis.total_orders?.toLocaleString()} />
            <ReportRow label="Total customers" value={report.kpis.total_customers?.toLocaleString()} />
            <ReportRow label="Repeat customer rate" value={report.kpis.repeat_customer_rate != null ? `${(report.kpis.repeat_customer_rate * 100).toFixed(1)}%` : "—"} />

            {report.best_model && <ReportRow label="Best model" value={report.best_model} />}

            {report.top_customers?.length > 0 && (
              <div>
                <div className="text-[11px] tracking-widest uppercase text-muted mono-num mb-2">Top 5 customers</div>
                <ul className="mono-num text-xs text-muted space-y-1">
                  {report.top_customers.map((c) => (
                    <li key={c.CustomerID}>{c.CustomerID} — ${Number(c.TotalSpent).toLocaleString()} ({c.NumOrders} orders)</li>
                  ))}
                </ul>
              </div>
            )}

            {report.cleaning_log?.length > 0 && (
              <div>
                <div className="text-[11px] tracking-widest uppercase text-muted mono-num mb-2">Cleaning decisions</div>
                <ul className="text-xs text-muted space-y-1 mono-num">
                  {report.cleaning_log.map((l, i) => <li key={i}>· {l}</li>)}
                </ul>
              </div>
            )}
          </div>
        </Panel>
      )}
    </div>
  );
}

function ReportRow({ label, value }) {
  return (
    <div className="flex items-center justify-between border-b border-line/60 pb-2">
      <span className="text-muted">{label}</span>
      <span className="mono-num text-paper">{value ?? "—"}</span>
    </div>
  );
}

function ConfusionMatrix({ name, matrix, best }) {
  const [[tn, fp], [fn, tp]] = matrix;
  return (
    <div className={`border rounded-lg p-3 ${best ? "border-signal/40 bg-signal/5" : "border-line"}`}>
      <div className="text-xs text-paper font-medium mb-2 flex items-center gap-1.5">
        {best && <span className="w-1.5 h-1.5 rounded-full bg-signal" />}
        {name}
      </div>
      <div className="grid grid-cols-2 gap-1 mono-num text-center text-xs">
        <Cell label="TN" value={tn} tone="neutral" />
        <Cell label="FP" value={fp} tone="warn" />
        <Cell label="FN" value={fn} tone="warn" />
        <Cell label="TP" value={tp} tone="good" />
      </div>
    </div>
  );
}

function Cell({ label, value, tone }) {
  const tones = {
    neutral: "bg-panel2 text-paper",
    good: "bg-up/15 text-up",
    warn: "bg-down/10 text-down",
  };
  return (
    <div className={`rounded py-2 ${tones[tone]}`}>
      <div className="text-[10px] opacity-70">{label}</div>
      <div className="font-semibold">{value}</div>
    </div>
  );
}

function FeatureBars({ items }) {
  const max = Math.max(...items.map((i) => i.importance), 0.0001);
  return (
    <div className="space-y-2">
      {items.map((f) => (
        <div key={f.feature} className="flex items-center gap-3">
          <div className="text-xs text-muted w-36 truncate mono-num" title={f.feature}>
            {f.feature.replace(/^(num|cat)__/, "")}
          </div>
          <div className="flex-1 h-2 bg-panel2 rounded-full overflow-hidden">
            <div className="h-full bg-signal" style={{ width: `${(f.importance / max) * 100}%` }} />
          </div>
          <div className="text-xs mono-num text-paper w-10 text-right">{f.importance.toFixed(2)}</div>
        </div>
      ))}
    </div>
  );
}

function fmtCurrency(v) {
  if (v === null || v === undefined) return "—";
  return v.toLocaleString(undefined, { style: "currency", currency: "USD", maximumFractionDigits: 0 });
}

function downloadJson(obj) {
  const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "sales-intelligence-report.json";
  a.click();
  URL.revokeObjectURL(url);
}
