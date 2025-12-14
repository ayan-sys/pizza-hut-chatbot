import React, { useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import { Send, Sparkles } from 'lucide-react';

const ChatInput = ({ onSend, disabled }) => {
    const [input, setInput] = useState('');
    const { primaryColor } = useTheme();

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !disabled) {
            onSend(input);
            setInput('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="relative w-full">
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask for a pizza..."
                disabled={disabled}
                className="w-full h-14 pl-6 pr-14 rounded-full border-2 border-gray-200 focus:border-transparent focus:ring-2 focus:ring-offset-2 transition-all outline-none text-gray-700 bg-white shadow-lg"
                style={{ '--tw-ring-color': primaryColor }}
            />
            <button
                type="submit"
                disabled={disabled || !input.trim()}
                className="absolute right-2 top-2 h-10 w-10 flex items-center justify-center rounded-full text-white shadow-md transition-transform active:scale-95 hover:scale-105 disabled:opacity-50 disabled:scale-100"
                style={{ backgroundColor: primaryColor }}
            >
                <Send size={20} />
            </button>
        </form>
    );
};

export default ChatInput;
