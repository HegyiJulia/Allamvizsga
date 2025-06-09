import { NavLink } from "react-router-dom";
import './TopNavBar.css';

const TopNavBar = () => {
  return (
    <nav className="navigation-bar">
      <div className="logo">🗂️ Szenátusi határozatok</div>
      <div className="nav-links">
        <NavLink
          to="/"
          className={({ isActive }) => (isActive ? "active-link" : "")}
        >
          Böngészés
        </NavLink>
        <NavLink
          to="/search"
          className={({ isActive }) => (isActive ? "active-link" : "")}
        >
          Keresés
        </NavLink>
        <NavLink
          to="/semantic-search"
          className={({ isActive }) => (isActive ? "active-link" : "")}
        >
          Szemantikus keresés
        </NavLink>
      </div>
    </nav>
  );
};

export default TopNavBar;


