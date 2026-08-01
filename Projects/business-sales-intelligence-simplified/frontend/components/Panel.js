export default function Panel({ title, eyebrow, action, children, className = "" }) {
  return (
    <section className={`bg-panel border border-line rounded-xl p-5 ${className}`}>
      {(title || eyebrow) && (
        <div className="flex items-center justify-between mb-4">
          <div>
            {eyebrow && (
              <div className="text-[11px] tracking-widest uppercase text-muted mb-1 mono-num">
                {eyebrow}
              </div>
            )}
            {title && <h2 className="text-paper font-semibold text-[15px]">{title}</h2>}
          </div>
          {action}
        </div>
      )}
      {children}
    </section>
  );
}
