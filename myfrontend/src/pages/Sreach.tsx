import React, { useState } from "react";
import { searchByWord } from "../api/search";
import './Search.css'; // Import the new CSS for styling the cards and scrollable list

const Search = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await searchByWord(query);
      setResults(data.results);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="search-container">
      <h2>Search Test</h2>
      <input
        type="text"
        placeholder="Enter a word..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="search-input"
      />
      <button onClick={handleSearch} className="search-button">
        Search
      </button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div className="results-container">
        {results.length > 0 ? (
          <div className="results-list">
            {results.map((item, index) => (
              <div key={index} className="card">
                <p>{item}</p>
              </div>
            ))}
          </div>
        ) : (
          !loading && <p>No results found.</p>
        )}
      </div>
    </div>
  );
};

export default Search;
