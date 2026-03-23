import { ClaimResult } from "@/types/index";
import { VerdictBadge } from "./VerdictBadge";
import { SourceCard } from "./SourceCard";

interface ClaimCardProps {
  result: ClaimResult;
}

export function ClaimCard({ result }: ClaimCardProps) {
  return (
    <div className="border rounded-lg p-4 mb-4 bg-white shadow-sm hover:shadow-md transition animate-fadeIn">
      <div className="mb-3">
        <p className="text-gray-900 font-medium mb-2">{result.claim}</p>
        <div className="flex items-center justify-between">
          <VerdictBadge verdict={result.verdict} />
          <span className="text-xs text-gray-500">
            Confidence: {Math.round(result.confidence * 100)}%
          </span>
        </div>
      </div>

      {result.sources.length > 0 && (
        <div className="mt-3 pt-3 border-t">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Sources ({result.sources.length})</h4>
          {result.sources.map((source, idx) => (
            <SourceCard key={idx} source={source} />
          ))}
        </div>
      )}
    </div>
  );
}
