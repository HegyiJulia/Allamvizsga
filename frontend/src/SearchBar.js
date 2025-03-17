import React, { useState } from 'react';
import axios from 'axios';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  // Keresés indítása
  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:8000/search', {
        query: query,
      });
      if (response.data.results.length === 0) {
        setErrorMessage('Nincs találat');
      } else {
        setResults(response.data.results);
        setErrorMessage(''); // Ha van találat, ürítjük az error message-t
      }
    } catch (error) {
      setErrorMessage('Hiba történt a keresés során');
    }
  };

  return (
    <div>
      <h2>Szöveg keresése</h2>
      <input
        type="text"
        placeholder="Írd be a keresett szót"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Keresés</button>

      {errorMessage && <p>{errorMessage}</p>}

      <ul>
        {results.map((result, index) => (
          <li key={index}>{result}</li>
        ))}
      </ul>
    </div>
  );
};

export default SearchBar;
