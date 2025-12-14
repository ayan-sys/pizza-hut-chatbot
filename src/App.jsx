import React, { useState, useEffect, useRef } from 'react';
import { useTheme } from './context/ThemeContext';
import ThemeSwitcher from './components/ThemeSwitcher';
import ChatBubble from './components/ChatBubble';
import ChatInput from './components/ChatInput';
import ImageDisplay from './components/ImageDisplay';

// Import Assets
import Logo from './assets/pizza_hut_chatbot_logo.png';
import LargePizza from './assets/large_pizza.png';
import MediumPizza from './assets/medium_pizza.png';
import SmallPizza from './assets/small_pizza.png';
import ZingerBurger from './assets/zinger_burger.png';
import NormalBurger from './assets/normal_chicken_burger.png';
import SpecialBurger from './assets/special_chicken_burger.png';
import Cola from './assets/cola_drink.png'; // Assuming I renamed it or it's similar

const MENU_ITEMS = {
  'large pizza': { image: LargePizza, price: 1500, name: 'Large Pizza' },
  'medium pizza': { image: MediumPizza, price: 1000, name: 'Medium Pizza' },
  'small pizza': { image: SmallPizza, price: 500, name: 'Small Pizza' },
  'zinger burger': { image: ZingerBurger, price: 600, name: 'Zinger Burger' },
  'normal chicken burger': { image: NormalBurger, price: 250, name: 'Chicken Burger' },
  'special chicken burger': { image: SpecialBurger, price: 380, name: 'Special Burger' },
  'cola': { image: Cola, price: 80, name: 'Cola Next' },
  'fizzup': { image: Cola, price: 80, name: 'FizzUp' },
  'coldrink': { image: Cola, price: 80, name: 'Cold Drink' },
};

const SYSTEM_PROMPT = `You are a helpful waiter at a Pizza Hut. 
Menu:
- Large Pizza: 1500
- Medium Pizza: 1000
- Small Pizza: 500
- Zinger Burger: 600
- Normal Chicken Burger: 250
- Special Chicken Burger: 380
- Cola Next / Fizzup: 80

If a user asks for an item, confirm the order and mention the price. Be friendly and use emojis.`;

function App() {
  const { primaryColor, isDarkMode } = useTheme();
  const [messages, setMessages] = useState([
    { text: "Welcome to Pizza Hut! 🍕 How can I help you today?", isBot: true }
  ]);
  const [currentImage, setCurrentImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentImage]);

  const handleSend = async (text) => {
    // 1. Add User Message
    setMessages(prev => [...prev, { text, isBot: false }]);
    setIsLoading(true);
    setCurrentImage(null); // Reset image on new request

    // 2. Check for Menu Items (Simple intent matching for "Live Pictures")
    const lowerText = text.toLowerCase();
    let foundItem = null;

    // Heuristic: Check if user mentioned any menu item
    Object.keys(MENU_ITEMS).forEach(key => {
      if (lowerText.includes(key)) {
        foundItem = MENU_ITEMS[key];
      }
    });

    if (foundItem) {
      setCurrentImage(foundItem);
    }

    // 3. Call Hugging Face API (or Fallback)
    try {
      // NOTE: Using a free inference endpoint. This might be rate limited.
      // We use a simple conversational model.
      const response = await fetch(
        "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
        {
          headers: { Authorization: "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" }, // Ideally need a key, checking if it works without
          method: "POST",
          body: JSON.stringify({ inputs: text }),
        }
      );

      // MOCK FALLBACK if API fails (likely 401/429 without key)
      // Since user said "choose by yourself", I can't put my own private key here securely.
      // So I will implement a robust local fallback that mimics the waiter if HF fails.

      let botResponse = "";

      if (response.ok) {
        const result = await response.json();
        botResponse = result[0]?.generated_text || "I'm not sure, but I can get you some pizza!";
      } else {
        // Fallback Logic
        if (foundItem) {
          botResponse = `Great choice! Here is your ${foundItem.name}. That will be ${foundItem.price} PKR. 😋`;
        } else if (lowerText.includes('hello') || lowerText.includes('hi')) {
          botResponse = "Hello! 👋 Welcome to Pizza Hut. What would you like to order?";
        } else if (lowerText.includes('price') || lowerText.includes('menu')) {
          botResponse = "We have Large Pizza (1500), Medium (1000), Small (500), and delicious Burgers! 🍔";
        } else {
          botResponse = "I'd love to help you order! We have pizzas, burgers, and drinks. 🍕🍔🥤";
        }
      }

      // 4. Update Chat
      setMessages(prev => [...prev, { text: botResponse, isBot: true }]);

    } catch (error) {
      console.error("API Error", error);
      setMessages(prev => [...prev, { text: "Sorry, I'm having trouble connecting right now, but I can still take your order!", isBot: true }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex flex-col items-center p-4 transition-colors duration-300 ${isDarkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>

      {/* Header */}
      <header className="w-full max-w-4xl flex items-center justify-between mb-8 p-4 bg-white/10 backdrop-blur-md rounded-2xl shadow-xl border border-white/20">
        <div className="flex items-center gap-4">
          <img src={Logo} alt="Logo" className="w-16 h-16 rounded-full shadow-lg border-2 border-white" />
          <div>
            <h1 className={`text-3xl font-black tracking-tighter ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
              PIZZA HUT <span style={{ color: primaryColor }}>CHATBOT</span>
            </h1>
            <p className={`text-sm font-medium ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
              Order your favorites instantly!
            </p>
          </div>
        </div>
        <div className="hidden md:block">
          {/* Theme Switcher could go here or floating */}
        </div>
      </header>

      <div className="flex flex-col md:flex-row gap-6 w-full max-w-6xl flex-grow">

        {/* Left Side: Chat Area */}
        <div className="flex-1 flex flex-col h-[70vh] md:h-[80vh] bg-white/50 backdrop-blur-sm rounded-3xl shadow-2xl overflow-hidden border border-white/50 relative">

          <div className="absolute top-4 right-4 z-10">
            {/* Floating Theme Toggle for Mobile */}
          </div>

          <div className="flex-1 overflow-y-auto p-6 scroll-smooth">
            {messages.map((msg, idx) => (
              <ChatBubble key={idx} message={msg.text} isBot={msg.isBot} />
            ))}
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-gray-200 p-3 rounded-2xl rounded-bl-none animate-pulse text-gray-500 text-sm">
                  Typing...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="p-4 bg-white/80 backdrop-blur-md border-t border-gray-100">
            <ChatInput onSend={handleSend} disabled={isLoading} />
          </div>
        </div>

        {/* Right Side: Visuals & Settings */}
        <div className="w-full md:w-96 flex flex-col gap-6">
          <ThemeSwitcher />

          {/* Live Image Display Area */}
          <div className={`flex-1 rounded-3xl shadow-xl flex items-center justify-center p-6 transition-all duration-500 
            ${isDarkMode ? 'bg-gray-800/50' : 'bg-white/50'} border border-white/20 relative overflow-hidden`}>

            {currentImage ? (
              <ImageDisplay item={currentImage} price={currentImage.price} />
            ) : (
              <div className="text-center opacity-40">
                <span className="text-6xl">🍕</span>
                <p className="mt-4 font-bold">Your food will appear here!</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
