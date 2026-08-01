export function PageHeader({ eyebrow, title, desc }) {
  return (
    <div>
      <div className="text-[11px] tracking-widest uppercase text-signal mono-num mb-2">{eyebrow}</div>
      <h1 className="text-2xl font-semibold text-paper mb-1">{title}</h1>
      <p className="text-muted text-sm">{desc}</p>
    </div>
  );
}

export function ErrorBox({ message }) {
  return (
    <div className="border border-down/40 bg-down/10 text-down text-sm rounded-lg px-4 py-3">
      {message}
    </div>
  );
}

export function LoadingBox() {
  return (
    <div className="flex items-center gap-2 text-muted text-sm mono-num">
      <span className="w-1.5 h-1.5 rounded-full bg-signal pulse-dot" /> Loading…
    </div>
  );
}

export function ToggleButton({ active, children, ...props }) {
  return (
    <button
      {...props}
      className={`px-2.5 py-1 rounded-md transition-colors focus-ring ${
        active ? "bg-panel2 text-signal" : "text-muted hover:text-paper"
      }`}
    >
      {children}
    </button>
  );
}
