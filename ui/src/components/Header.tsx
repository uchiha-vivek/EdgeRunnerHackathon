import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-gray-800 text-gray-100 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">Finance App</h1>
        <button
          className="md:hidden"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
          </svg>
        </button>
        <nav className={`${isMenuOpen ? 'block' : 'hidden'} md:block absolute md:relative top-16 left-0 right-0 md:top-0 bg-gray-800 md:bg-transparent`}>
          <ul className="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-4 p-4 md:p-0">
            <li><Link to="/" className="block hover:text-blue-400" onClick={() => setIsMenuOpen(false)}>Dashboard</Link></li>
            <li><Link to="/transactions" className="block hover:text-blue-400" onClick={() => setIsMenuOpen(false)}>Transactions</Link></li>
            <li><Link to="/budget" className="block hover:text-blue-400" onClick={() => setIsMenuOpen(false)}>Budget</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;