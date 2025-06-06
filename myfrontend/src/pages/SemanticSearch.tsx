// src/pages/SemanticSearch.tsx
import { useState } from "react";
import { semanticSearch, SemanticResult } from "../api/semantic";
import { Input, Spin } from "antd";
import "./Search.css"; // használd a meglévő stílust

const { Search: AntSearch } = Input;

const SemanticSearch = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SemanticResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await semanticSearch(query);
      setResults(data);
    } catch (err) {
      setError("Hiba történt a szemantikus keresés során.");
    }
    setLoading(false);
  };

  return (
    <div className="search-container">
      <div className="search-controls">
        <AntSearch
          placeholder="Add meg a keresett fogalmat (pl. klímastratégia)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onSearch={handleSearch}
          enterButton="Keresés"
          size="large"
        />
      </div>

      {loading && <Spin tip="Keresés..." />}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div className="results-container">
        {results.map((item) => (
          <div key={item.id} className="card">
            <p className="snippet">{item.content}</p>
            <p className="score">Hasonlóság: {(item.score * 100).toFixed(2)}%</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SemanticSearch;
