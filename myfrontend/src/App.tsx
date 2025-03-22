import { useState } from 'react'
import { searchDocuments, SearchResult } from "./api/search";
import TopNavBar from './components/TopNavBar';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import About from './pages/About';
import Search from './pages/Search';
import Home from './pages/Home';

function App() {

  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchMode, setSearchMode] = useState<"word" | "phrase">("word");

  const handleSearch = async () => {
    setLoading(true);
    setError(null); 
    try {
      const data = await searchDocuments(query, searchMode);
      setResults(data);
    } catch (err) {
      console.error(err);
      
    }
    setLoading(false);
  };



  return (
    <>
   <Router>
      <TopNavBar />
      <div style={{ padding: "20px" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/search" element={<Search />} />
        </Routes>
      </div>
    </Router>
    
    </>
  )
}

export default App
