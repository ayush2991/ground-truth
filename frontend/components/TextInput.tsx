"use client";

import { useState } from "react";

interface TextInputProps {
  onSubmit: (text: string) => Promise<void>;
  disabled: boolean;
  loading: boolean;
}

export function TextInput({ onSubmit, disabled, loading }: TextInputProps) {
  const [text, setText] = useState("");
  const charCount = text.length;
  const isOverLimit = charCount > 5000;
  const isAtWarning = charCount > 4500;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim() || isOverLimit || disabled) return;
    await onSubmit(text);
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="mb-2">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Paste your text for fact-checking
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={disabled || loading}
          placeholder="Paste the text you want to fact-check here..."
          className="w-full h-32 p-3 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
      </div>

      <div className="flex items-center justify-between mb-2">
        <span className={`text-xs font-medium ${isOverLimit ? "text-red-600" : isAtWarning ? "text-orange-600" : "text-gray-500"}`}>
          {charCount} / 5000 characters
        </span>
        {isAtWarning && (
          <span className="text-xs text-orange-600">
            ⚠ Text length warning
          </span>
        )}
      </div>

      {isOverLimit && (
        <div className="bg-red-50 border border-red-200 rounded p-2 mb-3 text-xs text-red-700">
          Text exceeds 5000 character limit. Please reduce the length.
        </div>
      )}

      <button
        type="submit"
        disabled={!text.trim() || isOverLimit || disabled || loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-2 px-4 rounded-lg transition"
      >
        {loading ? "Checking facts..." : "Check Facts"}
      </button>
    </form>
  );
}
