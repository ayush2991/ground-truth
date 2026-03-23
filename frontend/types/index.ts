export type Verdict = "supports" | "contradicts" | "neutral";

export interface Source {
  title: string;
  url: string;
  snippet: string;
  nli_verdict: Verdict;
  nli_score: number;
}

export interface ClaimResult {
  index: number;
  claim: string;
  verdict: Verdict;
  confidence: number;
  sources: Source[];
}

export interface FactCheckSession {
  id: string;
  text: string;
  timestamp: number;
  claims: ClaimResult[];
}
