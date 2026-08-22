import { NavLink } from "react-router-dom";

function Navbar() {
  const links = [
    { name: "Dashboard", path: "/" },
    { name: "Emails", path: "/emails" },
    { name: "Invoices", path: "/invoices" },
    { name: "Tasks", path: "/tasks" },
    { name: "Disputes", path: "/disputes" },
    { name: "Audit", path: "/audit" },
  ];

  return (
    <nav className="navbar">
      <div className="brand">
        <span className="brand-icon">🤖</span>
        <span>Autonomous Email Agent</span>
      </div>

      <div className="nav-links">
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            {link.name}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}

export default Navbar;