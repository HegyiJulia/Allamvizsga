
import TopNavBar from './components/TopNavBar';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import About from './pages/About';
import Search from './pages/Search';
import Home from './pages/Home';
  
  function App() {
  
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
    );
  }
  
  export default App;
  
