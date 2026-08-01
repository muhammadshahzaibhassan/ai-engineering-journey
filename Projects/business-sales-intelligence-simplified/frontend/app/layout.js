import "./globals.css";
import { SessionProvider } from "../lib/SessionContext";
import Nav from "../components/Nav";

export const metadata = {
  title: "Signal/Desk — Sales Intelligence",
  description: "Upload any sales CSV and get instant revenue, customer, and repeat-purchase intelligence.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-ink text-paper">
        <SessionProvider>
          <Nav />
          <main className="max-w-6xl mx-auto px-6 py-8">{children}</main>
          <footer className="max-w-6xl mx-auto px-6 py-8 text-xs text-muted/60 mono-num">
            Signal/Desk — data processed in-memory for this session only.
          </footer>
        </SessionProvider>
      </body>
    </html>
  );
}
