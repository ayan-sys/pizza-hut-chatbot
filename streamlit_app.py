import streamlit as st
import os
import requests
import json
import base64

# --- Configuration & Theme ---
st.set_page_config(layout="wide", page_title="Pizza Hut Chatbot", page_icon="🍕")

# Heuristic for detecting local assets path
ASSETS_DIR = os.path.join(os.getcwd(), 'src', 'assets')

def get_image_path(filename):
    return os.path.join(ASSETS_DIR, filename)

# Assets Map
MENU_ITEMS = {
    'large pizza': {'image': 'large_pizza.png', 'price': 1500, 'name': 'Large Pizza', 'tags': ['large', 'pizza']},
    'medium pizza': {'image': 'medium_pizza.png', 'price': 1000, 'name': 'Medium Pizza', 'tags': ['medium', 'pizza']},
    'small pizza': {'image': 'small_pizza.png', 'price': 500, 'name': 'Small Pizza', 'tags': ['small', 'pizza']},
    'zinger burger': {'image': 'zinger_burger.png', 'price': 600, 'name': 'Zinger Burger', 'tags': ['zinger', 'burger', 'crispy']},
    'normal chicken burger': {'image': 'normal_chicken_burger.png', 'price': 250, 'name': 'Chicken Burger', 'tags': ['chicken', 'burger', 'classic', 'normal']},
    'special chicken burger': {'image': 'special_chicken_burger.png', 'price': 380, 'name': 'Special Burger', 'tags': ['special', 'burger']},
    'cola': {'image': 'cola_drink.png', 'price': 80, 'name': 'Cola Next', 'tags': ['cola', 'drink', 'soda', 'next']},
    'fizzup': {'image': 'cola_drink.png', 'price': 80, 'name': 'FizzUp', 'tags': ['fizzup', 'drink']},
}

# --- Helper: Fuzzy Match ---
def find_menu_item(text):
    text = text.lower()
    best_match = None
    max_score = 0
    
    # Simple scoring: count how many tags appear in the text
    for key, item in MENU_ITEMS.items():
        score = 0
        for tag in item['tags']:
            if tag in text:
                score += 1
        
        # Boost for exact name match
        if key in text:
            score += 2
            
        if score > max_score and score > 0:
            max_score = score
            best_match = item
            
    # Threshold: meaningful match needs at least 1 tag or partial name
    if max_score >= 1:
        # Avoid generic "burger" matching "zinger burger" if user just said "burger"
        # If user said ONLY "burger", score might be 1 (tag 'burger'), but we might want generic response
        # Heuristic: If text length is short and score is low, treat as generic?
        # For now, let's trust the score but prioritize full item names
        return best_match
    return None

# --- Helper: Hugging Face Conversational API ---
def get_ai_response(user_input, context=""):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    # Note: This is a public endpoint, might be rate limited. 
    # Using a free model that supports some instruction following.
    
    headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"} # Replace with real token if available, else standard public access might limit
    
    # Construct a prompt for the "Waiter Persona"
    prompt = f"""
You are a friendly, multilingual waiter at Pizza Hut. 
The menu has: Large Pizza (1500), Medium (1000), Small (500), Zinger Burger (600), Chicken Burger (250), Special Burger (380), Drinks (80).
Your task: Reply to the customer in the SAME LANGUAGE they used. Be helpful and polite.

Customer: {user_input}
Waiter:"""

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 100, "temperature": 0.7}
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            return None
    except:
        return None

# --- Sidebar: Theme & Language Customizer ---
st.sidebar.image(get_image_path("pizza_hut_chatbot_logo.png"), use_column_width=True)
st.sidebar.title("Settings ⚙️")

# Language Selector
selected_language = st.sidebar.selectbox(
    "Choose Language 🌍",
    ["English", "Urdu", "Spanish", "French", "Arabic", "Chinese", "Hindi", "Russian", "Portuguese", "Japanese"]
)

st.sidebar.markdown("---")
st.sidebar.title("Theme 🎨")
primary_color = st.sidebar.color_picker("Primary Color", "#e11d48")
secondary_color = st.sidebar.color_picker("Accent Color", "#fbbf24")

# Inject Custom CSS
st.markdown(f"""
    <style>
    .stApp {{
        --primary-color: {primary_color};
        --secondary-color: {secondary_color};
    }}
    .stChatInput button {{
        background-color: {primary_color} !important;
        color: white !important;
    }}
    .user-message {{
        background-color: {primary_color};
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Helper: Hugging Face Conversational API ---
def get_ai_response(user_input, context="", language="English"):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"} 
    
    # Prompt Engineering for Language + Persona
    prompt = f"""
You are a friendly waiter at Pizza Hut. 
Language: {language}
Menu: Large Pizza (1500), Medium (1000), Small (500), Zinger Burger (600), Chicken Burger (250), Drinks (80).
Task: Reply to the customer in {language}. Keep it short and helpful.

Customer: {user_input}
Waiter:"""

    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 128, "temperature": 0.7}}

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
    except:
        pass
    return None

# --- Helper: Translate Static Text ---
def translate_text(text, target_lang):
    if target_lang == "English":
        return text
    
    # Use the same AI model to "translate" or "rewrite" the static info
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    prompt = f"Translate this to {target_lang}:\n\n{text}"
    
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 128}}
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
    except:
        pass
    return text  # Fallback to English

# --- State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to Pizza Hut! 🍕 Please choose your language from the sidebar."}]
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "cart" not in st.session_state:
    st.session_state.cart = []

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item['name']} to cart! 🛒")

def calculate_total():
    return sum(item['price'] for item in st.session_state.cart)

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"Chat 💬 ({selected_language})")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask for a pizza..."):
        # 1. User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # 2. Logic: Item Detection
        lower_text = prompt.lower()
        found_item = find_menu_item(lower_text)
        
        response_text = ""
        
        # Update Image
        if found_item:
            st.session_state.current_image = found_item
        elif "burger" in lower_text:
             st.session_state.current_image = MENU_ITEMS['zinger burger']
        elif "pizza" in lower_text:
             st.session_state.current_image = MENU_ITEMS['large pizza']

        # 3. Handle Intents with Language Support
        
        # Payment Intent
        if any(w in lower_text for w in ['pay', 'bill', 'checkout', 'jazzcash', 'money']):
            base_msg = "Please check your Cart on the right side to complete your order! 👉"
            response_text = translate_text(base_msg, selected_language)
            
        # Specific Item
        elif found_item:
            base_msg = f"Here is your {found_item['name']} ({found_item['price']} PKR). You can add it to your cart on the right! 👉"
            response_text = translate_text(base_msg, selected_language)
            
        # Menu Intent
        elif any(w in lower_text for w in ['menu', 'list', 'show']):
            base_msg = "Menu: Pizzas (500-1500), Burgers (250-600), Drinks (80). What would you like?"
            response_text = translate_text(base_msg, selected_language)
            
        # General AI Chat
        else:
            ai_reply = get_ai_response(prompt, language=selected_language)
            if ai_reply:
                response_text = ai_reply
            else:
                response_text = translate_text("I am ready to take your order! Please ask for a pizza or burger.", selected_language)

        # Add Assistant Message
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.write(response_text)

with col2:
    # --- Live Picture Section ---
    st.subheader("Live Picture 📸")
    current = st.session_state.current_image
    
    if current:
        try:
            image_path = get_image_path(current['image'])
            st.image(image_path, caption=f"{current['name']} - {current['price']} PKR", use_column_width=True)
            
            # Add to Cart Button
            if st.button(f"Add {current['name']} to Cart 🛒", key="add_btn", use_container_width=True):
                add_to_cart(current)
                
        except Exception as e:
            st.error(f"Image not found")
    else:
        st.info("Ask for an item to see it here!")
        st.markdown("# 🍕")

    st.markdown("---")

    # --- Cart & Checkout Section ---
    st.subheader("Your Order 🛒")
    
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        # Display Cart Items
        for i, item in enumerate(st.session_state.cart):
            st.text(f"{i+1}. {item['name']} - {item['price']} PKR")
        
        total = calculate_total()
        st.markdown(f"**Total: {total} PKR**")
        
        if st.button("Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

        st.markdown("### Checkout 📝")
        with st.form("checkout_form"):
            name = st.text_input("Name")
            address = st.text_area("Delivery Address")
            payment_method = st.selectbox("Payment Method", ["Cash on Delivery", "JazzCash (03091331142)", "GPay"])
            
            submitted = st.form_submit_button("Place Order ✅", use_container_width=True)
            
            if submitted:
                if name and address:
                    st.success("Order Placed Successfully! 🎉")
                    st.balloons()
                    
                    # Generate Receipt
                    receipt = f"""
                    **🧾 PIZZA HUT RECEIPT**
                    --------------------------------
                    **Customer:** {name}
                    **Address:** {address}
                    **Payment:** {payment_method}
                    --------------------------------
                    **Items:**
                    """
                    for item in st.session_state.cart:
                        receipt += f"- {item['name']}: {item['price']} PKR\n"
                    
                    receipt += f"""
                    --------------------------------
                    **TOTAL AMOUNT: {total} PKR**
                    --------------------------------
                    Thnk you for ordering! 🍕
                    """
                    st.markdown(receipt)
                    
                    # Reset Cart
                    st.session_state.cart = []
                else:
                    st.error("Please fill in your Name and Address.")
