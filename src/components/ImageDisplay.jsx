import React from 'react';
import { useTheme } from '../context/ThemeContext';

const ImageDisplay = ({ item, price }) => {
    const { secondaryColor } = useTheme();

    if (!item) return null;

    return (
        <div className="my-4 w-full flex flex-col items-center animate-fade-in-up">
            <div className="relative group perspective-1000">
                <div
                    className="absolute -inset-1 rounded-2xl opacity-75 blur transition duration-1000 group-hover:opacity-100 group-hover:duration-200 animate-pulse"
                    style={{ backgroundColor: secondaryColor }}
                ></div>
                <div className="relative rounded-2xl overflow-hidden shadow-2xl bg-white border-4 border-white">
                    <img
                        src={item.image}
                        alt={item.name}
                        className="w-64 h-64 object-cover transform transition-transform duration-500 group-hover:scale-110"
                    />
                    <div className="absolute bottom-0 left-0 right-0 bg-black/60 backdrop-blur-sm p-3 text-white text-center">
                        <h4 className="font-bold text-lg">{item.name}</h4>
                        <p className="text-yellow-400 font-mono text-xl">{price} PKR</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ImageDisplay;
