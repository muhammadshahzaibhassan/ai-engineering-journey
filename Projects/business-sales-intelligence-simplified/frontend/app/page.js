"use client";
import Link from "next/link";
import { useSession } from "../lib/SessionContext";
import UploadPanel from "../components/UploadPanel";
import KpiTicker from "../components/KpiTicker";
import Panel from "../components/Panel";

export default function HomePage() {
  const { status, processInfo } = useSession();
  const ready = status === "ready" && processInfo;

  return (
    <div className="space-y-8">
      <div>
        <div className="text-[11px] tracking-widest uppercase text-signal mono-num mb-2">
          Sales Intelligence Terminal
        </div>
        <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight text-paper mb-3">
          Point it at any sales CSV.<br />Get the whole picture back.
        </h1>
        <p className="text-muted max-w-xl">
          Upload a transaction export — any columns, any retailer. We detect the schema,
          clean it, engineer customer features, and train a repeat-purchase model, live.
        </p>
      </div>

      <Panel eyebrow="Step 1 / Load data">
        <UploadPanel />
      </Panel>

      {ready && (
        <>
          <Panel eyebrow="Step 2 / Snapshot" title="Portfolio at a glance">
            <KpiTicker kpis={processInfo.kpis} />
          </Panel>

          <div className="grid sm:grid-cols-3 gap-4">
            <NextStepCard href="/sales" title="Sales" desc="Revenue trend, top products, country breakdown." />
            <NextStepCard href="/customers" title="Customers" desc="RFM segments, top accounts, cross-sell pairs." />
            <NextStepCard href="/prediction" title="Prediction" desc="Score any customer's repeat-purchase odds." />
          </div>
        </>
      )}
    </div>
  );
}

function NextStepCard({ href, title, desc }) {
  return (
    <Link
      href={href}
      className="block border border-line bg-panel rounded-xl p-5 hover:border-signal/50 hover:bg-panel2 transition-colors focus-ring group"
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-paper font-semibold">{title}</h3>
        <span className="text-signal opacity-0 group-hover:opacity-100 transition-opacity">→</span>
      </div>
      <p className="text-sm text-muted">{desc}</p>
    </Link>
  );
}
