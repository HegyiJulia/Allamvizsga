import { useState } from "react";  
import { searchDocuments, SearchResult } from "../api/search";
import './Search.css';
import { DatePicker, Input, Segmented } from "antd";
import 'antd/dist/reset.css';

const Search = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedFileContent, setSelectedFileContent] = useState<string | null>(null);
  const [searchMode, setSearchMode] = useState<"word" | "phrase">("word");
  const [darkMode] = useState(false);
  const [startDate, setStartDate] = useState<string>(""); 
  const [endDate, setEndDate] = useState<string>(""); 
  const [hasSearched, setHasSearched] = useState(false);

  const { RangePicker,  } = DatePicker;
  const { Search: AntSearch } = Input;

  const handleSearch = async () => {
    if (query.trim() === "") {
      setError("Kérlek, adj meg egy keresési kifejezést!");
      setResults([]); 
      return;
    }

    setLoading(true);
    setError(null);
    setSelectedFileContent(null);
    setHasSearched(true);

    try {
      const data = await searchDocuments(query, searchMode, startDate, endDate);
      setResults(data);
    } catch (err) {
      console.error(err);
      setError("Hiba történt a keresés során.");
    }

    setLoading(false);
  };



  const showFullContent = (content: string) => {
    const highlightQuery = (text: string) => {
      if (!query) return text;

      const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // escape regex
      const regex = searchMode === 'phrase'
        ? new RegExp(escapedQuery, 'gi')
        : new RegExp(`\\b(${escapedQuery.split(' ').join('|')})\\b`, 'gi');

      return text.replace(regex, (match) => `<strong>${match}</strong>`);
    };

    setSelectedFileContent(highlightQuery(content));

  };

  return (
    <div className={`search-container ${darkMode ? 'dark-mode' : ''}`}>
      <div className="left-site">
        <div className="search-controls">
          <Segmented
            options={[{ label: 'Kulcsszavak', value: 'word' }, { label: 'Kifejezés', value: 'phrase' }] }
            value={searchMode}
            onChange={(val) => setSearchMode(val as 'word' | 'phrase')}
            size="large"
          />
          <AntSearch
            placeholder="Írja be a keresett szavakat../Kifejezést"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onSearch={handleSearch}
            enterButton="Keresés"
            allowClear
            size="large"
          />
          <RangePicker
            style={{ width: '100%', borderRadius: 8 }}
             picker="month"
            format="YYYY-MM"
            allowClear
            onChange={(_, dateStrings) => {
              setStartDate(dateStrings[0]);  
              setEndDate(dateStrings[1]);
            }}
          />
        </div>

        {loading && <p>Betöltés...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>

      <div className={selectedFileContent ? "results-split-view" : "results-container"}>
        {results.length > 0 ? (
          <>
            <div className="results-list">
              {results.map((item, index) => (
                <div key={index} className="card">
                  <h3 className="title">{item.filename}</h3>
                  <p
                    className="snippet"
                    dangerouslySetInnerHTML={{
                      __html: item.snippet.replace(/<em>/g, "<strong>").replace(/<\/em>/g, "</strong>"),
                    }}
                  />
                  <button
                    className="open-close-button"
                    onClick={() => showFullContent(item.content)}
                  >
                    Több
                  </button>
                </div>
              ))}
            </div>

            {selectedFileContent && (
              <div className="full-content-panel">
                <div
                  dangerouslySetInnerHTML={{
                    __html: selectedFileContent.replace(/\n/g, "<br />"),
                  }}
                />
              </div>
            )}
          </>
        ) : (
          hasSearched && !loading && results.length === 0 && <p>Nincs találat.</p>
        )}
      </div>
    </div>
  );
};

export default Search;
