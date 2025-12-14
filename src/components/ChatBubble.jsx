import React from 'react';
import { useTheme } from '../context/ThemeContext';
import { User, Bot } from 'lucide-react';

const ChatBubble = ({ message, isBot }) => {
    const { primaryColor, secondaryColor, isDarkMode } = useTheme();

    const bubbleStyle = isBot
        ? { backgroundColor: isDarkMode ? '#374151' : '#f3f4f6', color: isDarkMode ? '#e5e7eb' : '#1f2937' }
        : { backgroundColor: primaryColor, color: '#ffffff' };

    return (
        <div className={`flex w-full mb-4 ${isBot ? 'justify-start' : 'justify-end'}`}>
            <div className={`flex max-w-[80%] ${isBot ? 'flex-row' : 'flex-row-reverse'} items-end gap-2`}>

                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 
          ${isBot ? '' : 'bg-gray-200'}`}
                    style={{ backgroundColor: isBot ? secondaryColor : undefined }}
                >
                    {isBot ? <Bot size={18} className="text-white" /> : <User size={18} className="text-gray-600" />}
                </div>

                <div
                    className={`p-3 rounded-2xl shadow-sm text-sm md:text-base leading-relaxed break-words
            ${isBot ? 'rounded-bl-none' : 'rounded-br-none'}`}
                    style={bubbleStyle}
                >
                    {message}
                </div>
            </div>
        </div>
    );
};

export default ChatBubble;
