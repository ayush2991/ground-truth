import { Verdict } from "@/types/index";

interface VerdictBadgeProps {
  verdict: Verdict;
}

export function VerdictBadge({ verdict }: VerdictBadgeProps) {
  const colors: Record<Verdict, string> = {
    supports: "bg-green-100 text-green-800",
    contradicts: "bg-red-100 text-red-800",
    neutral: "bg-gray-100 text-gray-800",
  };

  const labels: Record<Verdict, string> = {
    supports: "✓ Supports",
    contradicts: "✗ Contradicts",
    neutral: "◇ Neutral",
  };

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${colors[verdict]}`}>
      {labels[verdict]}
    </span>
  );
}
