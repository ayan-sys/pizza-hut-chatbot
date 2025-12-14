# 🍕 Pizza Hut Chatbot

A multilingual, AI-powered chatbot for ordering pizzas and burgers! 

## Features
- **Multilingual Support**: Supports English, Urdu, Spanish, Arabic, and more.
- **AI Persona**: Integrated Hugging Face API for identifying context and replying in the user's language.
- **Dynamic Images**: Automatically shows pictures based on your order (Zinger Burger, Large Pizza, etc.).
- **Payment Integration**: Easy JazzCash details provided automatically.
- **Theme Switcher**: Dark/Light mode and custom color support.

## How to Run

### Prerequisite
You need **Python** installed.

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Enjoy!**
   The app will open in your browser at `http://localhost:8502`.

## Project Structure
- `streamlit_app.py`: Main application code.
- `src/assets/`: Images for pizzas and burgers.
