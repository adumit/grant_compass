import { useNavigate } from "react-router-dom";
import './css/Header.css';

const Header = () => {
  const navigate = useNavigate();
  return (
    <header className="header">
      <a className="header-title" href="" onClick={() => navigate({ pathname: "/" })}>Grant Compass</a>
      <nav className="header-nav">
        <a href="#what-is-grant-compass">What is Grant Compass?</a>
        <a href="#about-us">About Us</a>
        <a href="#contact">Contact</a>
      </nav>
    </header>
  );
};

export default Header;
