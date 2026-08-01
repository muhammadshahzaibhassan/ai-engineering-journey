import Link from "next/link";

export default function NoDataState({ message = "No data loaded yet." }) {
  return (
    <div className="border border-dashed border-line rounded-xl px-8 py-16 text-center">
      <div className="text-3xl mb-3">📭</div>
      <p className="text-paper font-medium mb-1">{message}</p>
      <p className="text-muted text-sm mb-5">Upload a sales CSV to unlock this view.</p>
      <Link
        href="/"
        className="inline-block bg-signal text-ink font-medium text-sm px-4 py-2 rounded-lg hover:bg-signal2 transition-colors focus-ring"
      >
        Go to upload
      </Link>
    </div>
  );
}
