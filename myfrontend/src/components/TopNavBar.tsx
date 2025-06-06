import { Link } from "react-router-dom";
import './TopNavBar.css';

const TopNavBar = () => {
  return (
    <nav className="navigation-bar">
      <div className="logo">🗂️ Szenátusi határozatok</div>
      <div className="nav-links">
        <Link to="/">Kezdőlap</Link>
        <Link to="/search">Keresés</Link>
        <Link to="/semantic-search">Kontextus</Link>
        <Link to="/about">Rólunk</Link>
      </div>
  
    </nav>
  );
};

export default TopNavBar;

