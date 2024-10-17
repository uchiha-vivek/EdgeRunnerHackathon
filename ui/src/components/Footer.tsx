import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-gray-300 py-6 px-4">
      <div className="container mx-auto text-center">
        <p>&copy; 2024 Finance App. All rights reserved.</p>
        <div className="mt-2 space-x-4">
          <a href="#" className="hover:text-blue-400">Privacy Policy</a>
          <a href="#" className="hover:text-blue-400">Terms of Service</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;