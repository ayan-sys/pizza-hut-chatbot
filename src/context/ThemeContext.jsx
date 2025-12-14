import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider = ({ children }) => {
    const [primaryColor, setPrimaryColor] = useState('#e11d48'); // Default Pizza Red
    const [secondaryColor, setSecondaryColor] = useState('#fbbf24'); // Default Cheese Yellow
    const [isDarkMode, setIsDarkMode] = useState(false);

    useEffect(() => {
        // Apply CSS variables for dynamic coloring
        document.documentElement.style.setProperty('--color-primary', primaryColor);
        document.documentElement.style.setProperty('--color-secondary', secondaryColor);
    }, [primaryColor, secondaryColor]);

    const value = {
        primaryColor,
        setPrimaryColor,
        secondaryColor,
        setSecondaryColor,
        isDarkMode,
        setIsDarkMode,
    };

    return (
        <ThemeContext.Provider value={value}>
            <div className={isDarkMode ? 'dark' : ''}>
                {children}
            </div>
        </ThemeContext.Provider>
    );
};
