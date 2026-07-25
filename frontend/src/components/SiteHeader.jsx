import { Link, NavLink } from "react-router-dom";

function SiteHeader({ theme, onToggleTheme }) {
  return (
    <header className="site-header">
      <Link to="/" className="brand-mark">
        <span className="brand-icon">F1</span>
        <span>
          <strong>Race Intelligence</strong>
          <small>Data Engineering Project</small>
        </span>
      </Link>

      <div className="header-actions">
        <nav className="site-nav" aria-label="Primary navigation">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              isActive ? "nav-link nav-link-active" : "nav-link"
            }
          >
            Seasons
          </NavLink>
        </nav>

        <button
          type="button"
          className="theme-toggle"
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
        >
          <span aria-hidden="true">{theme === "dark" ? "☀" : "☾"}</span>
          {theme === "dark" ? "Light" : "Dark"}
        </button>
      </div>
    </header>
  );
}

export default SiteHeader;
