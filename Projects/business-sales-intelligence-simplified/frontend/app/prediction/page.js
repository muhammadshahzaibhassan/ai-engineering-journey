"use client";
import { useEffect, useState } from "react";
import { useSession } from "../../lib/SessionContext";
import { api } from "../../lib/api";
import Panel from "../../components/Panel";
import NoDataState from "../../components/NoDataState";
import { PageHeader, ErrorBox } from "../../components/Shared";

const COUNTRIES_FALLBACK = ["USA", "UK", "Germany", "France", "Canada"];
const SEGMENTS = ["Bronze", "Silver", "Gold"];

export default function PredictionPage() {
  const { sessionId, status, trainInfo, train } = useSession();
  const [training, setTraining] = useState(false);
  const [trainError, setTrainError] = useState(null);
  const [modelName, setModelName] = useState(null);
  const [form, setForm] = useState({
    Recency: 30, Frequency: 1.5, TotalSpent: 500, AvgBasketSize: 3,
    Country: "USA", CustomerSegment: "Silver",
  });
  const [result, setResult] = useState(null);
  const [predicting, setPredicting] = useState(false);
  const [predictError, setPredictError] = useState(null);

  useEffect(() => {
    if (trainInfo?.best_model_name) setModelName(trainInfo.best_model_name);
  }, [trainInfo]);

  if (status !== "ready") return <NoDataState />;

  const handleTrain = async () => {
    setTraining(true);
    setTrainError(null);
    try {
      await train();
    } catch (e) {
      setTrainError(e.message || String(e));
    } finally {
      setTraining(false);
    }
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setPredicting(true);
    setPredictError(null);
    setResult(null);
    try {
      const r = await api.predict(sessionId, modelName, form);
      setResult(r);
    } catch (err) {
      setPredictError(err.message || String(err));
    } finally {
      setPredicting(false);
    }
  };

  const update = (key, value) => setForm((f) => ({ ...f, [key]: value }));

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Module 6-7 / Machine Learning"
        title="Repeat-purchase prediction"
        desc="Train Logistic Regression, Decision Tree, and Random Forest, then score any customer profile."
      />

      {!trainInfo && (
        <Panel title="Train the model" desc="">
          <p className="text-muted text-sm mb-4">
            Builds and evaluates three classifiers on this dataset's customer features.
          </p>
          <button
            onClick={handleTrain}
            disabled={training}
            className="bg-signal text-ink font-medium text-sm px-4 py-2 rounded-lg hover:bg-signal2 transition-colors focus-ring disabled:opacity-50"
          >
            {training ? "Training…" : "Train models"}
          </button>
          {trainError && <div className="mt-3"><ErrorBox message={trainError} /></div>}
        </Panel>
      )}

      {trainInfo && (
        <>
          <Panel
            title="Model comparison"
            eyebrow={`Best: ${trainInfo.best_model_name} · train ${trainInfo.train_size} / test ${trainInfo.test_size}`}
            action={
              <button
                onClick={handleTrain}
                disabled={training}
                className="text-xs text-muted hover:text-signal transition-colors focus-ring rounded px-2 py-1"
              >
                {training ? "Retraining…" : "Retrain"}
              </button>
            }
          >
            <MetricsTable metrics={trainInfo.metrics} best={trainInfo.best_model_name} />
          </Panel>

          <div className="grid md:grid-cols-[1fr_1fr] gap-6">
            <Panel title="Customer profile">
              <form onSubmit={handlePredict} className="space-y-4">
                <NumberField label="Recency (days since last order)" value={form.Recency} onChange={(v) => update("Recency", v)} />
                <NumberField label="Frequency (orders / month)" value={form.Frequency} onChange={(v) => update("Frequency", v)} step="0.1" />
                <NumberField label="Total spent" value={form.TotalSpent} onChange={(v) => update("TotalSpent", v)} prefix="$" />
                <NumberField label="Avg basket size" value={form.AvgBasketSize} onChange={(v) => update("AvgBasketSize", v)} step="0.1" />

                <SelectField
                  label="Country"
                  value={form.Country}
                  onChange={(v) => update("Country", v)}
                  options={trainInfo.input_fields?.categorical?.includes("Country") ? COUNTRIES_FALLBACK : null}
                />
                <SelectField label="Segment" value={form.CustomerSegment} onChange={(v) => update("CustomerSegment", v)} options={SEGMENTS} />

                <SelectField
                  label="Model"
                  value={modelName || ""}
                  onChange={setModelName}
                  options={Object.keys(trainInfo.metrics?.reduce((acc, m) => ({ ...acc, [m.model]: true }), {}) || {})}
                />

                <button
                  type="submit"
                  disabled={predicting}
                  className="w-full bg-signal text-ink font-medium text-sm px-4 py-2.5 rounded-lg hover:bg-signal2 transition-colors focus-ring disabled:opacity-50"
                >
                  {predicting ? "Scoring…" : "Predict"}
                </button>
                {predictError && <ErrorBox message={predictError} />}
              </form>
            </Panel>

            <Panel title="Prediction">
              {!result && <p className="text-muted text-sm">Fill in the profile and click Predict.</p>}
              {result && <ResultCard result={result} />}
              {trainInfo.feature_importance && (
                <div className="mt-6 pt-5 border-t border-line">
                  <div className="text-[11px] tracking-widest uppercase text-muted mono-num mb-3">
                    What drives this model
                  </div>
                  <FeatureImportanceList items={trainInfo.feature_importance} />
                </div>
              )}
            </Panel>
          </div>
        </>
      )}
    </div>
  );
}

function MetricsTable({ metrics, best }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-[11px] tracking-widest uppercase text-muted border-b border-line">
            <th className="pb-2 pr-4">Model</th>
            <th className="pb-2 pr-4 text-right">Accuracy</th>
            <th className="pb-2 pr-4 text-right">Precision</th>
            <th className="pb-2 pr-4 text-right">Recall</th>
            <th className="pb-2 pr-4 text-right">F1</th>
            <th className="pb-2 text-right">ROC AUC</th>
          </tr>
        </thead>
        <tbody className="mono-num">
          {metrics.map((m) => (
            <tr key={m.model} className="border-b border-line/60 last:border-0">
              <td className="py-2 pr-4 text-paper flex items-center gap-2">
                {m.model === best && <span className="w-1.5 h-1.5 rounded-full bg-signal" />}
                {m.model}
              </td>
              <td className="py-2 pr-4 text-right">{m.accuracy}</td>
              <td className="py-2 pr-4 text-right">{m.precision}</td>
              <td className="py-2 pr-4 text-right">{m.recall}</td>
              <td className="py-2 pr-4 text-right text-signal">{m.f1}</td>
              <td className="py-2 text-right">{m.roc_auc ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ResultCard({ result }) {
  const pct = result.probability !== null ? Math.round(result.probability * 100) : null;
  const likely = result.repeat_customer_prediction;
  return (
    <div className={`rounded-xl border p-5 ${likely ? "border-up/40 bg-up/5" : "border-down/40 bg-down/5"}`}>
      <div className="text-[11px] tracking-widest uppercase text-muted mono-num mb-2">
        {result.model_used}
      </div>
      <div className={`text-2xl font-semibold mb-1 ${likely ? "text-up" : "text-down"}`}>
        {likely ? "Likely to purchase again" : "Unlikely to purchase again"}
      </div>
      {pct !== null && (
        <div className="mono-num text-sm text-muted">
          Confidence: <span className="text-paper">{pct}%</span>
        </div>
      )}
    </div>
  );
}

function FeatureImportanceList({ items }) {
  const max = Math.max(...items.map((i) => i.importance), 0.0001);
  return (
    <div className="space-y-2">
      {items.slice(0, 6).map((f) => (
        <div key={f.feature} className="flex items-center gap-3">
          <div className="text-xs text-muted w-32 truncate mono-num" title={f.feature}>
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

function NumberField({ label, value, onChange, step = "1", prefix }) {
  return (
    <label className="block">
      <span className="text-xs text-muted mb-1.5 block">{label}</span>
      <div className="relative">
        {prefix && <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted text-sm">{prefix}</span>}
        <input
          type="number"
          step={step}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className={`w-full bg-panel2 border border-line rounded-lg py-2 text-sm text-paper mono-num focus-ring outline-none ${prefix ? "pl-7 pr-3" : "px-3"}`}
        />
      </div>
    </label>
  );
}

function SelectField({ label, value, onChange, options }) {
  const opts = options?.length ? options : [value];
  return (
    <label className="block">
      <span className="text-xs text-muted mb-1.5 block">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-panel2 border border-line rounded-lg px-3 py-2 text-sm text-paper focus-ring outline-none"
      >
        {opts.map((o) => (
          <option key={o} value={o}>{o}</option>
        ))}
      </select>
    </label>
  );
}
