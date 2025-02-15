'use client';

import { useState } from 'react';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [evaluation, setEvaluation] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function evaluatePrompt() {
    setLoading(true);
    setEvaluation(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, response }),
      });

      const data = await res.json();
      setEvaluation(data);
    } catch (error) {
      console.error('Evaluation failed:', error);
      setEvaluation({ score: 'Error', explanation: 'Something went wrong' });
    }

    setLoading(false);
  }

  return (
    <div className="max-w-xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">LLM Evaluation Playground</h1>

      <div className="mb-4">
        <textarea
          className="w-full border rounded p-2"
          placeholder="Enter prompt here..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
      </div>

      <div className="mb-4">
        <textarea
          className="w-full border rounded p-2"
          placeholder="Enter LLM response here..."
          value={response}
          onChange={(e) => setResponse(e.target.value)}
        />
      </div>

      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={evaluatePrompt}
        disabled={loading}
      >
        {loading ? 'Evaluating...' : 'Evaluate'}
      </button>

      {evaluation && (
        <div className="mt-6 p-4 border rounded bg-gray-50">
          <p><strong>Score:</strong> {evaluation.score}</p>
          <p><strong>Explanation:</strong> {evaluation.explanation}</p>
        </div>
      )}
    </div>
  );
}
