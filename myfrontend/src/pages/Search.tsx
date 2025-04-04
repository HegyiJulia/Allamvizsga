import React, { useState } from "react";
import { searchDocuments, SearchResult } from "../api/search";
import './Search.css';

const Search = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedFileContent, setSelectedFileContent] = useState<string | null>(null);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null); 
  const [searchMode, setSearchMode] = useState<"word" | "phrase">("word"); 
  const [darkMode, setDarkMode] = useState(false); 
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    setSelectedFileContent(null); 
    setSelectedIndex(null); 
    try {
      const data = await searchDocuments(query, searchMode, startDate, endDate);
      setResults(data);
    } catch (err) {
      console.error(err);
      setError("Hiba történt a keresés során.");
    }
    setLoading(false);
  };

  const showFullContent = (content: string, index: number) => {
    setSelectedFileContent(content);
    setSelectedIndex(index);
  };

  const closeFullContent = () => {
    setSelectedFileContent(null);
    setSelectedIndex(null);
  };

    const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    
    <div className={`search-container ${darkMode ? 'dark-mode' : ''}`}>
      <h2>Dokumentum kereső</h2>

      <button onClick={toggleDarkMode} className="dark-mode-button">
        {darkMode ? "Világos mód" : "Sötét mód"}
      </button>
      <div className="date-range-container">
  <div className="date-labels">
    <label htmlFor="startDate">Dátumtól:</label>
    <label htmlFor="endDate">Dátumig:</label>
  </div>
      <div className="date-inputs">
        <input
          id="startDate"
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="date-picker"
        />
        <input
          id="endDate"
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="date-picker"
        />
      </div>
  </div>

      <div className="search-mode-container">
        <label>
          <input
            type="radio"
            name="searchMode"
            value="word"
            checked={searchMode === "word"}
            onChange={() => setSearchMode("word")}
          />
          Kulcsszavas keresés
        </label>
        <label>
          <input
            type="radio"
            name="searchMode"
            value="phrase"
            checked={searchMode === "phrase"}
            onChange={() => setSearchMode("phrase")}
          />
          Kifejezés keresés
        </label>
      </div>

      <input
        type="text"
        placeholder="Írja be a keresett szavakat../Kifejezést"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="search-input"
      />
      <button onClick={handleSearch} className="search-button">
        Keresés
      </button>

      {loading && <p>Betöltés...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div className="results-container">
        {results.length > 0 ? (
          <div className="results-list">
            {results.map((item, index) => (
              <div key={index} className="card">
                {selectedIndex === index ? (
                  <div>
                  <h3 className="title">{item.filename}</h3>
                  <p
                    dangerouslySetInnerHTML={{
                      __html: selectedFileContent ? selectedFileContent.replace(/\n/g, "<br />") : "",
                    }}
                  />
                  <button className="open-close-button" onClick={closeFullContent}>
                    Vissza
                  </button>
                </div>
                ) : (
                  <div>
                    <h3 className="title">{item.filename}</h3>
                    <p
                      className="snippet"
                      dangerouslySetInnerHTML={{
                        __html: item.snippet.replace(/<em>/g, "<strong>").replace(/<\/em>/g, "</strong>"),
                      }}
                    />
                    <button className="open-close-button" onClick={() => showFullContent(item.content, index)}>
                      Több
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          !loading && <p>Nincs találat.</p>
        )}
      </div>
    </div>
  );
};

export default Search;


