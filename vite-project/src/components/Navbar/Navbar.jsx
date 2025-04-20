// src/components/Navbar/Navbar.jsx
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-white shadow-md py-4 px-8 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-blue-600">Logo</h1>
      <ul className="flex space-x-6 text-lg">
        <li><Link to="/" className="hover:text-blue-600">Home</Link></li>
        <li><Link to="/about" className="hover:text-blue-600">About</Link></li>
        <li><Link to="/services" className="hover:text-blue-600">Services</Link></li>
        <li><Link to="/contact" className="hover:text-blue-600">Contact</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;


