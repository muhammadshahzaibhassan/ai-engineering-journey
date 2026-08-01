"use client";
import { useCallback, useRef, useState } from "react";
import { useSession } from "../lib/SessionContext";

export default function UploadPanel() {
  const { uploadAndProcess, status, error, uploadInfo, processInfo, reset } = useSession();
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);

  const handleFile = useCallback(
    async (file) => {
      if (!file) return;
      if (!file.name.toLowerCase().endsWith(".csv")) {
        alert("Please upload a .csv file.");
        return;
      }
      try {
        await uploadAndProcess(file);
      } catch (_) {
        // error surfaced via context.error
      }
    },
    [uploadAndProcess]
  );

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  const busy = status === "uploading" || status === "processing";

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={`border-2 border-dashed rounded-xl px-8 py-14 text-center cursor-pointer transition-colors focus-ring ${
          dragOver ? "border-signal bg-signal/5" : "border-line hover:border-muted"
        }`}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === "Enter") inputRef.current?.click(); }}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv,text/csv"
          className="hidden"
          onChange={(e) => handleFile(e.target.files?.[0])}
        />
        <div className="text-3xl mb-3">📊</div>
        <p className="text-paper font-medium mb-1">
          {busy ? (status === "uploading" ? "Uploading…" : "Detecting columns, cleaning, building features…") : "Drop a sales CSV here, or click to browse"}
        </p>
        <p className="text-muted text-sm">
          Any retail/sales export works — we auto-detect order ID, customer ID, date, quantity, price, product, and country columns.
        </p>
      </div>

      {error && (
        <div className="border border-down/40 bg-down/10 text-down text-sm rounded-lg px-4 py-3">
          {error}
        </div>
      )}

      {uploadInfo && (
        <div className="border border-line rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-paper font-medium">{uploadInfo.filename}</span>
            <button
              onClick={reset}
              className="text-xs text-muted hover:text-down transition-colors focus-ring rounded px-2 py-1"
            >
              Clear &amp; start over
            </button>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs mono-num">
            <div>
              <div className="text-muted">ROWS</div>
              <div className="text-paper">{uploadInfo.rows?.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-muted">COLUMNS</div>
              <div className="text-paper">{uploadInfo.columns?.length}</div>
            </div>
            <div>
              <div className="text-muted">REVENUE MODE</div>
              <div className="text-paper">{uploadInfo.revenue_mode}</div>
            </div>
            <div>
              <div className="text-muted">STATUS</div>
              <div className={processInfo ? "text-up" : "text-signal"}>
                {processInfo ? "READY" : "PROCESSING"}
              </div>
            </div>
          </div>

          <div>
            <div className="text-[11px] tracking-widest uppercase text-muted mono-num mb-1.5">
              Detected schema
            </div>
            <div className="flex flex-wrap gap-1.5">
              {Object.entries(uploadInfo.detected_schema || {}).map(([role, col]) => (
                <span
                  key={role}
                  className={`text-[11px] mono-num px-2 py-1 rounded border ${
                    col ? "border-line text-paper bg-panel2" : "border-line text-muted/50"
                  }`}
                >
                  {role}: {col || "—"}
                </span>
              ))}
            </div>
          </div>

          {uploadInfo.warnings?.length > 0 && (
            <div className="text-xs text-signal2 space-y-1">
              {uploadInfo.warnings.map((w, i) => (
                <div key={i}>⚠ {w}</div>
              ))}
            </div>
          )}

          {processInfo?.cleaning_log?.length > 0 && (
            <div>
              <div className="text-[11px] tracking-widest uppercase text-muted mono-num mb-1.5">
                Cleaning log
              </div>
              <ul className="text-xs text-muted space-y-1 mono-num">
                {processInfo.cleaning_log.map((l, i) => (
                  <li key={i}>· {l}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
