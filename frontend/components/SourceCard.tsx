"use client";

import { useState } from "react";
import { Source } from "@/types/index";
import { VerdictBadge } from "./VerdictBadge";

interface SourceCardProps {
  source: Source;
}

export function SourceCard({ source }: SourceCardProps) {
  const [expanded, setExpanded] = useState(false);
  const domain = new URL(source.url).hostname;

  return (
    <div className="border rounded-lg p-3 mb-2 bg-gray-50 hover:bg-gray-100 transition cursor-pointer">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full text-left"
      >
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1">
            <h4 className="font-semibold text-sm text-gray-900">{source.title}</h4>
            <p className="text-xs text-gray-500">{domain}</p>
          </div>
          <VerdictBadge verdict={source.nli_verdict} />
        </div>
      </button>

      {expanded && (
        <div className="mt-3 pt-3 border-t">
          <p className="text-sm text-gray-700 mb-2">{source.snippet}</p>
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500">
              Match: {Math.round(source.nli_score * 100)}%
            </span>
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-600 hover:underline"
            >
              Visit source →
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
