// src/api/semantic.ts
export interface SemanticResult {
  id: string;
  content: string;
  score: number;
}

export async function semanticSearch(query: string, top_k = 5): Promise<SemanticResult[]> {
  const response = await fetch("http://localhost:8000/search/semantic-search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, top_k }),
  });

  if (!response.ok) {
    throw new Error("Szemantikus keresés sikertelen");
  }

  const data = await response.json();
  return data.results;
}
