import React from 'react';
import { useTheme } from '../context/ThemeContext';
import { Palette, Sun, Moon } from 'lucide-react';

const ThemeSwitcher = () => {
    const {
        primaryColor, setPrimaryColor,
        secondaryColor, setSecondaryColor,
        isDarkMode, setIsDarkMode
    } = useTheme();

    return (
        <div className={`p-4 rounded-xl shadow-lg border border-opacity-20 backdrop-blur-md 
      ${isDarkMode ? 'bg-gray-800 border-gray-700 text-white' : 'bg-white/80 border-gray-200 text-gray-800'}`}>

            <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold flex items-center gap-2">
                    <Palette className="w-5 h-5" /> Theme Customizer
                </h3>
                <button
                    onClick={() => setIsDarkMode(!isDarkMode)}
                    className={`p-2 rounded-full transition-colors ${isDarkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-100 hover:bg-gray-200'}`}
                >
                    {isDarkMode ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5 text-indigo-600" />}
                </button>
            </div>

            <div className="space-y-4">
                <div>
                    <label className="text-xs font-semibold uppercase tracking-wider opacity-70 mb-1 block">Primary Color</label>
                    <div className="flex gap-2 flex-wrap">
                        {['#e11d48', '#2563eb', '#16a34a', '#9333ea', '#ea580c'].map((color) => (
                            <button
                                key={color}
                                onClick={() => setPrimaryColor(color)}
                                className={`w-8 h-8 rounded-full border-2 transition-transform hover:scale-110 ${primaryColor === color ? 'border-white ring-2 ring-offset-2 ring-gray-400' : 'border-transparent'}`}
                                style={{ backgroundColor: color }}
                            />
                        ))}
                        <input
                            type="color"
                            value={primaryColor}
                            onChange={(e) => setPrimaryColor(e.target.value)}
                            className="w-8 h-8 rounded-full cursor-pointer opacity-0 absolute"
                        />
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-pink-500 to-indigo-500 flex items-center justify-center text-[10px] font-bold text-white relative pointer-events-none">
                            +
                        </div>
                    </div>
                </div>

                <div>
                    <label className="text-xs font-semibold uppercase tracking-wider opacity-70 mb-1 block">Accent Color</label>
                    <div className="flex gap-2 flex-wrap">
                        {['#fbbf24', '#f472b6', '#2dd4bf', '#a78bfa', '#fb7185'].map((color) => (
                            <button
                                key={color}
                                onClick={() => setSecondaryColor(color)}
                                className={`w-8 h-8 rounded-full border-2 transition-transform hover:scale-110 ${secondaryColor === color ? 'border-white ring-2 ring-offset-2 ring-gray-400' : 'border-transparent'}`}
                                style={{ backgroundColor: color }}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ThemeSwitcher;
