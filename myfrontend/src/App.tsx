
import TopNavBar from './components/TopNavBar';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


import Search from './pages/Search';
import Home from './pages/Home';
import SemanticSearch from "./pages/SemanticSearch";
  
  function App() {
  
    return (
      <>
        <Router>
          <TopNavBar />
          <div style={{ padding: "20px" }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/semantic-search" element={<SemanticSearch />} />
              <Route path="/search" element={<Search />} />
            </Routes>
          </div>
        </Router>
      </>
    );
  }
  
  export default App;
  
