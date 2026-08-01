"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSession } from "../lib/SessionContext";

const LINKS = [
  { href: "/", label: "Upload" },
  { href: "/sales", label: "Sales" },
  { href: "/customers", label: "Customers" },
  { href: "/prediction", label: "Prediction" },
  { href: "/model", label: "Model" },
];

export default function Nav() {
  const pathname = usePathname();
  const { status, uploadInfo } = useSession();

  return (
    <header className="border-b border-line bg-ink/95 backdrop-blur sticky top-0 z-20">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between gap-6">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-signal" />
          <span className="font-semibold tracking-tight text-paper text-[15px]">
            SIGNAL<span className="text-signal">/</span>DESK
          </span>
        </div>

        <nav className="flex items-center gap-1">
          {LINKS.map((link) => {
            const active = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-1.5 text-sm rounded-md transition-colors focus-ring ${
                  active
                    ? "bg-panel2 text-signal"
                    : "text-muted hover:text-paper hover:bg-panel2/60"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2 text-xs mono-num text-muted min-w-[140px] justify-end">
          {status === "ready" && (
            <>
              <span className="w-1.5 h-1.5 rounded-full bg-up pulse-dot" />
              <span className="truncate max-w-[140px]" title={uploadInfo?.filename}>
                {uploadInfo?.filename}
              </span>
            </>
          )}
          {status === "idle" && <span>NO DATA LOADED</span>}
          {(status === "uploading" || status === "processing") && (
            <>
              <span className="w-1.5 h-1.5 rounded-full bg-signal pulse-dot" />
              <span>{status === "uploading" ? "UPLOADING" : "PROCESSING"}</span>
            </>
          )}
          {status === "error" && (
            <>
              <span className="w-1.5 h-1.5 rounded-full bg-down" />
              <span>ERROR</span>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
