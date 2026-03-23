"use client";

import { useReducer, useCallback, useRef } from "react";
import { ClaimResult, FactCheckSession } from "@/types/index";
import { saveResult } from "@/lib/storage";

export type FactCheckStatus = "idle" | "extracting" | "checking" | "done" | "error";

interface FactCheckState {
  status: FactCheckStatus;
  claims: ClaimResult[];
  total: number | null;
  error: string | null;
  sessionId: string | null;
}

type FactCheckAction =
  | { type: "RESET" }
  | { type: "START_EXTRACT" }
  | { type: "CLAIMS_FOUND"; payload: { total: number; claims: string[] } }
  | { type: "CLAIM_RESULT"; payload: ClaimResult }
  | { type: "DONE" }
  | { type: "ERROR"; payload: string }
  | { type: "SET_SESSION_ID"; payload: string };

const initialState: FactCheckState = {
  status: "idle",
  claims: [],
  total: null,
  error: null,
  sessionId: null,
};

function factCheckReducer(state: FactCheckState, action: FactCheckAction): FactCheckState {
  switch (action.type) {
    case "RESET":
      return initialState;
    case "START_EXTRACT":
      return { ...state, status: "extracting", error: null };
    case "SET_SESSION_ID":
      return { ...state, sessionId: action.payload };
    case "CLAIMS_FOUND":
      return { ...state, status: "checking", total: action.payload.total };
    case "CLAIM_RESULT":
      return { ...state, claims: [...state.claims, action.payload] };
    case "DONE":
      return { ...state, status: "done" };
    case "ERROR":
      return { ...state, status: "error", error: action.payload };
    default:
      return state;
  }
}

interface UseFactCheckReturn {
  submit: (text: string) => Promise<void>;
  claims: ClaimResult[];
  total: number | null;
  status: FactCheckStatus;
  error: string | null;
  reset: () => void;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function useFactCheck(): UseFactCheckReturn {
  const [state, dispatch] = useReducer(factCheckReducer, initialState);
  const claimsRef = useRef<ClaimResult[]>([]);

  const submit = useCallback(async (text: string) => {
    dispatch({ type: "RESET" });
    claimsRef.current = [];
    dispatch({ type: "START_EXTRACT" });

    try {
      // Step 1: Create a session
      const sessionResponse = await fetch(`${API_URL}/session`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!sessionResponse.ok) {
        throw new Error(`Failed to create session: ${sessionResponse.statusText}`);
      }

      const { session_id } = await sessionResponse.json();
      dispatch({ type: "SET_SESSION_ID", payload: session_id });

      // Step 2: Open SSE stream
      const eventSource = new EventSource(`${API_URL}/factcheck/stream?session_id=${session_id}`);

      eventSource.addEventListener("claims_found", (event: MessageEvent) => {
        const data = JSON.parse(event.data);
        dispatch({
          type: "CLAIMS_FOUND",
          payload: { total: data.total, claims: data.claims },
        });
      });

      eventSource.addEventListener("claim_result", (event: MessageEvent) => {
        const data = JSON.parse(event.data) as ClaimResult;
        claimsRef.current.push(data);
        dispatch({
          type: "CLAIM_RESULT",
          payload: data,
        });
      });

      eventSource.addEventListener("done", () => {
        eventSource.close();
        dispatch({ type: "DONE" });
        // Persist to localStorage
        const session: FactCheckSession = {
          id: session_id,
          text,
          timestamp: Date.now(),
          claims: claimsRef.current,
        };
        saveResult(session);
      });

      eventSource.addEventListener("error", (event: MessageEvent) => {
        try {
          const data = JSON.parse(event.data);
          dispatch({ type: "ERROR", payload: data.message || "Connection error" });
        } catch {
          dispatch({ type: "ERROR", payload: "Connection error" });
        }
        eventSource.close();
      });

      eventSource.onerror = () => {
        dispatch({ type: "ERROR", payload: "EventSource connection failed" });
        eventSource.close();
      };
    } catch (error) {
      dispatch({
        type: "ERROR",
        payload: error instanceof Error ? error.message : "Unknown error",
      });
    }
  }, []);

  const reset = useCallback(() => {
    dispatch({ type: "RESET" });
    claimsRef.current = [];
  }, []);

  return {
    submit,
    claims: state.claims,
    total: state.total,
    status: state.status,
    error: state.error,
    reset,
  };
}

// Re-export storage helpers
export { saveResult, loadResults, clearResults } from "@/lib/storage";
