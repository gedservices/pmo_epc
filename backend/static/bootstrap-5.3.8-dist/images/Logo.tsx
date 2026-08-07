
import React from 'react';

const Logo: React.FC = () => {
  return (
    <div className="flex items-center space-x-4 text-4xl sm:text-5xl md:text-6xl font-sans select-none">
      <div className="flex-shrink-0 flex items-center justify-center bg-white rounded-xl w-16 h-16 sm:w-20 sm:h-20 shadow-2xl transform hover:scale-105 transition-transform duration-300">
        <span className="text-blue-700 font-black text-5xl sm:text-6xl">M</span>
      </div>
      <div className="flex flex-col justify-center">
        <span className="text-white font-extrabold tracking-wide leading-none">PLAN</span>
        <span className="text-blue-300 font-light text-2xl sm:text-3xl tracking-widest leading-none mt-1">
          TOOL
        </span>
      </div>
    </div>
  );
};

export default Logo;
