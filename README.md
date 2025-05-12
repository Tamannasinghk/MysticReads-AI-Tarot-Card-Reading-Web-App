# 🔮 MysticReads – AI Tarot Card Reading Web App

Welcome to **MysticReads**, an AI-powered Tarot Reading web app that gives users personalized 3-card tarot readings based on their name, birthdate, and life concerns. Users can then chat with the Tarot Bot for deeper insights!

Built with 🐍 Python, 🤖 LangChain, 🔮 Gemini (Gemini 1.5 Flash), and 🖼️ Gradio.

---

## 📌 Features

- 🌟 Personalized 3-Card Tarot Readings
- 💬 Interactive Chatbot for follow-up queries
- ♈ Zodiac Sign Detection from Date of Birth
- 🎯 Concern-based card selection (Love, Career, Health, etc.)
- 🪄 Beautiful and intuitive Gradio UI

---

## 🧠 Project Logic & Flow

### 1. **User Input**

- **Name** (e.g., Alice)
- **Date of Birth** (YYYY-MM-DD format)
- **Area of Concern** (Dropdown: Love, Career, Health, etc.)

### 2. **Zodiac Sign Detection**

- **def get_zodiac_sign(dob):**
-  Extract zodiac sign from date

### 3. Card Selection Logic
- Based on user's selected concern, the app randomly chooses 3 relevant tarot cards from a predefined list.
- Each concern category (e.g., Love, Career) has its own tarot card pool.

### 4. Prompt Generation for Tarot Reading
- **A LangChain chat prompt is constructed like:**
- **Tarot reading for:** Alice (Scorpio)
- **Concern:** Career
- **Cards:** The Chariot, Ace of Pentacles, The Emperor

### 5. Chatbot for Follow-Up Questions
- **After the initial reading, users can ask follow-up questions like:**
- "What does The Emperor mean for my career?"

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Tamannasinghk/MysticReads-AI-Tarot-Card-Reading-Web-App.git
cd MysticReads-AI-Tarot-Card-Reading-Web-App
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```
---
## Make sure to replace the following with your own key:
```python
api_key="YOUR_GOOGLE_GEMINI_API_KEY"
```

---
Thank you !
