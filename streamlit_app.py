import streamlit as st
import os
import requests
import json
import pandas as pd
from database import init_db, get_menu, create_order, get_orders, update_order_status, get_orders_by_name

# --- Init DB ---
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

# --- Configuration ---
st.set_page_config(layout="wide", page_title="Pizza Hut System", page_icon="🍕")
ASSETS_DIR = os.path.join(os.getcwd(), 'src', 'assets')

def get_image_path(filename):
    return os.path.join(ASSETS_DIR, filename)

# Load Menu from DB
db_menu = get_menu()
# Create a fallback/lookup dict for fuzzy matching
MENU_ITEMS = {item['name'].lower(): item for item in db_menu}

# --- Shared Helpers ---
TRANSLATIONS = {
    "English": {
        "chat_header": "Customer Chat",
        "welcome": "Welcome! 🍕 Check menu, order food, or track your order!",
        "ask_placeholder": "Ask for pizza, or say 'Track Order <your name>'...",
        "track_hint": "To track, please type: 'Track Order [Your Name]'",
        "cancel_hint": "To cancel an order, please provide your Order ID. OR contact support.",
        "menu_header": "**Menu:**\n",
        "cart_check": "Please check your Cart on the right to place the order! 👉",
        "general_help": "I can help you Order, Track Status, or Browse Menu. What would you like?",
        "live_pic": "Live Picture 📸",
        "add_btn": "Add",
        "cart_header": "Your Cart 🛒",
        "clear_cart": "Clear Cart",
        "checkout_header": "Checkout Details",
        "place_order": "Place Order ✅",
        "name_lbl": "Full Name",
        "addr_lbl": "Delivery Address",
        "pay_lbl": "Payment Method",
        "empty_cart": "Cart is empty.",
        "success_order": "Order Placed! 🎉",
        "track_info": "You can track it by typing 'Track Order <Name>'"
    },
    "Urdu": {
        "chat_header": "کسٹمر چیٹ",
        "welcome": "خوش آمدید! 🍕 مینو چیک کریں، کھانا آرڈر کریں، یا اپنا آرڈر ٹریک کریں!",
        "ask_placeholder": "پیزا مانگیں، یا کہیں 'ٹریک آرڈر <نام>'...",
        "track_hint": "ٹریک کرنے کے لیے لکھیں: 'Track Order [اپنا نام]'",
        "cancel_hint": "آرڈر منسوخ کرنے کے لیے آرڈر آئی ڈی فراہم کریں۔ یا سپورٹ سے رابطہ کریں۔",
        "menu_header": "**مینو:**\n",
        "cart_check": "براہ کرم آرڈر کرنے کے لیے دائیں طرف اپنی ٹوکری چیک کریں! 👉",
        "general_help": "میں آرڈر، ٹریکنگ یا مینو میں مدد کر سکتا ہوں۔ آپ کیا پسند کریں گے؟",
        "live_pic": "لائیو تصویر 📸",
        "add_btn": "شامل کریں",
        "cart_header": "آپ کی ٹوکری 🛒",
        "clear_cart": "ٹوکری خالی کریں",
        "checkout_header": "چیک آؤٹ کی تفصیلات",
        "place_order": "آرڈر کریں ✅",
        "name_lbl": "پورا نام",
        "addr_lbl": "پتہ",
        "pay_lbl": "ادائیگی کا طریقہ",
        "empty_cart": "ٹوکری خالی ہے۔",
        "success_order": "آرڈر کر دیا گیا! 🎉",
        "track_info": "آپ 'Track Order <نام>' لکھ کر ٹریک کر سکتے ہیں"
    }
    # Add other languages as needed or fallback to English
}

def t(key, lang):
    # Fallback to English if key/lang missing
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, TRANSLATIONS["English"][key])

def find_menu_item(text):
    text = text.lower()
    best_match = None
    max_score = 0
    for item in db_menu:
        score = 0
        for tag in item['tags']:
            if tag in text: score += 1
        if item['name'].lower() in text: score += 3
        
        if score > max_score and score > 0:
            max_score = score
            best_match = item
    if max_score >= 1: return best_match
    return None

def get_orders_df():
    orders = get_orders()
    if not orders: return pd.DataFrame()
    df = pd.DataFrame(orders, columns=['ID', 'Name', 'Address', 'Items', 'Total', 'Status', 'Payment', 'Time'])
    return df

# --- SIDEBAR NAV ---
st.sidebar.image(get_image_path("pizza_hut_chatbot_logo.png"), use_column_width=True)
app_mode = st.sidebar.radio("Navigation 🧭", ["Chatbot 🤖", "Dashboard 📊"])

# ==========================================
# PAGE 1: CHATBOT
# ==========================================
if app_mode == "Chatbot 🤖":
    st.sidebar.markdown("---")
    st.sidebar.title("Settings ⚙️")
    selected_language = st.sidebar.selectbox("Language 🌍", ["English", "Urdu", "Spanish", "Arabic"])
    
    # State
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t("welcome", selected_language)}]
    if "current_image" not in st.session_state:
        st.session_state.current_image = None
    if "cart" not in st.session_state:
        st.session_state.cart = []

    col1, col2 = st.columns([2, 1])

    with col1:
        st.header(f"{t('chat_header', selected_language)} ({selected_language})")
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input(t("ask_placeholder", selected_language)):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)

            lower_text = prompt.lower()
            response_text = ""
            
            # 1. TRACK ORDER Intent
            if "track" in lower_text or "status" in lower_text:
                name_query = prompt.replace("track", "").replace("order", "").strip()
                if len(name_query) > 2:
                    orders = get_orders_by_name(name_query)
                    if orders:
                        last_order = orders[0]
                        response_text = f"Found your order #{last_order[0]}! \n**Status:** {last_order[5]} 🕒\nTotal: {last_order[4]} PKR\nItems: {last_order[3]}"
                    else:
                        response_text = f"No order found for '{name_query}'."
                else:
                    response_text = t("track_hint", selected_language)
            
            # 2. CANCEL ORDER Intent
            elif "cancel" in lower_text:
                 response_text = t("cancel_hint", selected_language)

            # 3. MENU / ORDER Intent
            else:
                found_item = find_menu_item(lower_text)
                if found_item:
                    st.session_state.current_image = found_item
                    response_text = f"**{found_item['name']}** ({found_item['price']} PKR). {t('add_btn', selected_language)}? 👉"
                elif "menu" in lower_text:
                    response_text = t("menu_header", selected_language) + "\n".join([f"- {m['name']} ({m['price']} PKR)" for m in db_menu])
                elif "pay" in lower_text or "checkout" in lower_text:
                    response_text = t("cart_check", selected_language)
                else:
                     # Fallback / General
                     response_text = t("general_help", selected_language)

            st.session_state.messages.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"): st.write(response_text)

    with col2:
        st.subheader(t("live_pic", selected_language))
        curr = st.session_state.current_image
        if curr:
            st.image(get_image_path(curr['image']), caption=curr['name'])
            if st.button(f"{t('add_btn', selected_language)} {curr['name']} ➕", key="add"):
                st.session_state.cart.append(curr)
                st.toast("Added!")
        else:
            st.info("Choose food to see here!")

        st.markdown("---")
        st.subheader(t("cart_header", selected_language))
        if st.session_state.cart:
            total = 0
            for i, it in enumerate(st.session_state.cart):
                st.text(f"{i+1}. {it['name']} ({it['price']})")
                total += it['price']
            
            st.markdown(f"**Total: {total} PKR**")
            
            if st.button(t("clear_cart", selected_language)): 
                st.session_state.cart = []
                st.rerun()
            
            with st.form("checkout"):
                st.markdown(f"### {t('checkout_header', selected_language)}")
                name = st.text_input(t("name_lbl", selected_language))
                addr = st.text_input(t("addr_lbl", selected_language))
                pay = st.selectbox(t("pay_lbl", selected_language), ["Cash on Delivery", "JazzCash (03091331142)", "GPay"])
                
                if st.form_submit_button(t("place_order", selected_language), use_container_width=True):
                    if name and addr:
                        items_summary = ", ".join([i['name'] for i in st.session_state.cart])
                        oid = create_order(name, addr, items_summary, total, pay)
                        
                        st.balloons()
                        st.success(f"{t('success_order', selected_language)} (ID: {oid})")
                        st.info(f"{t('track_info', selected_language).replace('<Name>', name)}")
                        st.session_state.cart = []
                    else:
                        st.error("Name and Address required")
        else:
            st.write(t("empty_cart", selected_language))

# ==========================================
# PAGE 2: DASHBOARD
# ==========================================
elif app_mode == "Dashboard 📊":
    st.title("Restaurant Admin Dashboard 📈")
    # ... (Dashboard logic remains mostly the same, usually admin is English)
    # ... But let's leave the rest of the file intact by ending edit here 
    # and relying on existing code for dashboard
    
    st.markdown("Manage orders, view sales, and analytics.")
    
    df = get_orders_df()
    
    if df.empty:
        st.info("No orders yet. Go to Chatbot and place some!")
    else:
        # Metrics
        total_sales = df['Total'].sum()
        total_orders = len(df)
        pending_orders = len(df[df['Status'] == 'Pending'])
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"{total_sales} PKR", delta="Today")
        m2.metric("Total Orders", total_orders)
        m3.metric("Pending Orders", pending_orders, delta_color="inverse")
        
        st.divider()
        
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("Sales by Status")
            status_counts = df['Status'].value_counts()
            st.bar_chart(status_counts)
            
        with c2:
            st.subheader("Recent Activity")
            st.dataframe(df[['Name', 'Total', 'Status']].head(5), hide_index=True)

        st.divider()
        st.subheader("Order Management")
        
        # Display as editable table or list
        for index, row in df.iterrows():
            with st.expander(f"Order #{row['ID']} - {row['Name']} ({row['Total']} PKR)"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Items:** {row['Items']}")
                    st.write(f"**Address:** {row['Address']}")
                    st.write(f"**Payment:** {row['Payment']}")
                with col_b:
                    st.write(f"**Current Status:** {row['Status']}")
                    st.write(f"**Time:** {row['Time']}")
                    
                    # Update Status
                    new_status = st.selectbox("Update Status", ["Pending", "Cooking", "Delivered", "Cancelled"], key=f"status_{row['ID']}", index=["Pending", "Cooking", "Delivered", "Cancelled"].index(row['Status']) if row['Status'] in ["Pending", "Cooking", "Delivered", "Cancelled"] else 0)
                    if st.button(f"Update Order #{row['ID']}", key=f"btn_{row['ID']}"):
                        update_order_status(row['ID'], new_status)
                        st.success("Updated!")
                        st.rerun()
