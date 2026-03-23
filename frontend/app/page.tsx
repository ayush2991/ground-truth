"use client";

import { TextInput } from "@/components/TextInput";
import { ClaimCard } from "@/components/ClaimCard";
import { ProgressBar } from "@/components/ProgressBar";
import { useFactCheck, loadResults, clearResults } from "@/hooks/useFactCheck";
import { useState } from "react";
import { FactCheckSession } from "@/types/index";

export default function Home() {
  const { submit, claims, total, status, error, reset } = useFactCheck();
  const [historyOpen, setHistoryOpen] = useState(false);
  const [history, setHistory] = useState<FactCheckSession[]>([]);
  const [selectedHistory, setSelectedHistory] = useState<FactCheckSession | null>(null);

  const loadHistory = () => {
    setHistory(loadResults());
    setHistoryOpen(true);
  };

  const handleClearHistory = () => {
    clearResults();
    setHistory([]);
    setSelectedHistory(null);
  };

  const displayClaims = selectedHistory ? selectedHistory.claims : claims;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Ground Truth</h1>
          <p className="text-gray-600">Fact-check your text using AI-powered analysis</p>
        </header>

        {/* Main Content */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          {selectedHistory ? (
            // Viewing history
            <div>
              <button
                onClick={() => setSelectedHistory(null)}
                className="mb-4 px-3 py-1 text-sm bg-gray-200 hover:bg-gray-300 rounded text-gray-700 font-medium"
              >
                ← Back to new check
              </button>
              <div className="mb-4 pb-4 border-b">
                <h2 className="text-sm font-semibold text-gray-500 mb-1">Original text:</h2>
                <p className="text-gray-700 text-sm">{selectedHistory.text.substring(0, 200)}...</p>
                <p className="text-xs text-gray-400 mt-2">
                  Checked on {new Date(selectedHistory.timestamp).toLocaleString()}
                </p>
              </div>
            </div>
          ) : (
            // Input form
            <TextInput
              onSubmit={submit}
              disabled={status !== "idle"}
              loading={status === "extracting" || status === "checking"}
            />
          )}

          {/* Progress Bar */}
          {status === "checking" && <ProgressBar current={claims.length} total={total} />}

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4 text-sm text-red-700">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* Results */}
          {displayClaims.length > 0 && (
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Results ({displayClaims.length} claim{displayClaims.length !== 1 ? "s" : ""})
              </h2>
              {displayClaims.map((result) => (
                <ClaimCard key={`${result.index}`} result={result} />
              ))}

              {status === "done" && (
                <button
                  onClick={() => {
                    reset();
                    setSelectedHistory(null);
                  }}
                  className="mt-4 w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition"
                >
                  Check another text
                </button>
              )}
            </div>
          )}

          {/* Empty state */}
          {status === "idle" && claims.length === 0 && !selectedHistory && (
            <div className="text-center py-8">
              <p className="text-gray-500 text-sm">
                Paste text above to get started. We'll extract claims and verify them against online sources.
              </p>
            </div>
          )}
        </div>

        {/* History Panel */}
        {!selectedHistory && (
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-gray-900">
                {historyOpen ? "Recent checks" : "History"}
              </h3>
              {history.length > 0 && (
                <button
                  onClick={loadHistory}
                  className="text-xs text-blue-600 hover:underline font-medium"
                >
                  {historyOpen ? "Refresh" : "Load"}
                </button>
              )}
            </div>

            {historyOpen && history.length > 0 ? (
              <div>
                <div className="space-y-2 mb-3 max-h-60 overflow-y-auto">
                  {history.map((session) => (
                    <button
                      key={session.id}
                      onClick={() => setSelectedHistory(session)}
                      className="w-full text-left p-2 rounded hover:bg-gray-100 transition border border-transparent hover:border-gray-200"
                    >
                      <p className="text-sm text-gray-900 font-medium">
                        {session.text.substring(0, 60)}...
                      </p>
                      <p className="text-xs text-gray-500">
                        {session.claims.length} claims • {new Date(session.timestamp).toLocaleDateString()}
                      </p>
                    </button>
                  ))}
                </div>
                <button
                  onClick={handleClearHistory}
                  className="w-full text-xs text-red-600 hover:text-red-700 font-medium py-2 border-t border-gray-200"
                >
                  Clear history
                </button>
              </div>
            ) : (
              <p className="text-xs text-gray-500">
                {history.length === 0 ? "No history yet. Start by checking some text!" : ""}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
