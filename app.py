#################### Importing needed libraries ##################### 

import gradio as gr
import random
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os

#################### Pre-define Zodiac based on DOB ##################### 
def get_zodiac_sign(dob):
    dob = datetime.strptime(dob, "%Y-%m-%d")
    zodiac_dates = [
        ("Capricorn", (datetime(dob.year, 12, 22), datetime(dob.year, 12, 31))),
        ("Aquarius", (datetime(dob.year, 1, 20), datetime(dob.year, 2, 18))),
        ("Pisces", (datetime(dob.year, 2, 19), datetime(dob.year, 3, 20))),
        ("Aries", (datetime(dob.year, 3, 21), datetime(dob.year, 4, 19))),
        ("Taurus", (datetime(dob.year, 4, 20), datetime(dob.year, 5, 20))),
        ("Gemini", (datetime(dob.year, 5, 21), datetime(dob.year, 6, 20))),
        ("Cancer", (datetime(dob.year, 6, 21), datetime(dob.year, 7, 22))),
        ("Leo", (datetime(dob.year, 7, 23), datetime(dob.year, 8, 22))),
        ("Virgo", (datetime(dob.year, 8, 23), datetime(dob.year, 9, 22))),
        ("Libra", (datetime(dob.year, 9, 23), datetime(dob.year, 10, 22))),
        ("Scorpio", (datetime(dob.year, 10, 23), datetime(dob.year, 11, 21))),
        ("Sagittarius", (datetime(dob.year, 11, 22), datetime(dob.year, 12, 21)))
    ]
    for zodiac, (start_date, end_date) in zodiac_dates:
        if start_date <= dob <= end_date:
            return zodiac
    return "Invalid date"

#################### Define All Tarot Cards Based on Concerns ##################### 
concern_cards = {
    "Love": ["The Lovers", "Two of Cups", "The Empress", "The Moon", "Three of Swords", "The Star", "The High Priestess", "The Sun", "Ten of Cups", "Ace of Cups", "Knight of Cups", "Queen of Cups", "King of Cups", "Page of Cups", "Six of Cups", "Four of Wands", "Five of Pentacles"],
    "Career": ["The Emperor", "The Chariot", "The Hierophant", "Strength", "The World", "Three of Pentacles", "Eight of Pentacles", "Knight of Pentacles", "King of Pentacles", "Queen of Pentacles", "Ace of Pentacles", "Six of Pentacles", "Page of Pentacles", "Ten of Pentacles", "The Devil", "The Fool", "Two of Wands"],
    "Health": ["The Star", "The Empress", "The Moon", "The Sun", "Temperance", "The Hermit", "Death", "Four of Swords", "Nine of Swords", "Ace of Swords", "Six of Swords", "Queen of Cups", "King of Cups", "The Lovers", "The High Priestess", "Two of Cups"],
    "Family": ["The Empress", "The Lovers", "Ten of Pentacles", "The Hierophant", "The Chariot", "Four of Wands", "The Star", "The Moon", "King of Pentacles", "Queen of Pentacles", "Six of Cups", "Two of Cups", "The Sun", "Three of Cups", "The Fool", "The Magician"],
    "Finance": ["The Emperor", "The Devil", "Ace of Pentacles", "Ten of Pentacles", "Four of Pentacles", "Nine of Pentacles", "King of Pentacles", "Queen of Pentacles", "Eight of Pentacles", "Two of Pentacles", "Six of Pentacles", "Three of Pentacles", "Five of Pentacles", "The Fool", "Seven of Pentacles", "The Tower"],
    "Personal Growth": ["The Fool", "The Hermit", "The High Priestess", "The Chariot", "Strength", "Judgement", "The Magician", "The Star", "Temperance", "The Emperor", "The Lovers", "The Sun", "The World", "Ace of Swords", "Eight of Pentacles", "Two of Wands"],
    "Others/General": ["The Fool", "The Magician", "The Empress", "The Lovers", "The Chariot", "The Hermit", "The Sun", "The Star", "The Moon", "The High Priestess", "Justice", "Death", "The Tower", "The Devil", "The Emperor", "The World", "Ace of Cups", "Ace of Pentacles", "Ten of Swords", "Seven of Cups", "Nine of Cups", "Two of Wands", "Three of Swords"]
}
#################### Creating model ##################### 
api_key = os.environ.get("GEMINI_API_KEY")
model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        api_key=api_key,  # replace with HF secret key
        temperature=0.2
    )

#################### Prompt for model ##################### 
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a Tarot card reading assistant. Which gives the short and accurate point to point reading of the tarot cards . ( Please keep the reading short and accurate .) , Please tell the user his/her zodiac , each card that is drone for user , each card meaning for user ."),
    ("user", "{query}")
])
parser = StrOutputParser()

#################### Generate Readings ##################### 
def generate_tarot_reading(name, dob, concern):
    try:
        
        zodiac = get_zodiac_sign(dob)
        selected_cards = random.sample(concern_cards[concern], 3)
        prompt = (
            f"Tarot reading for {name} ({zodiac}):\n"
            f"Concern: {concern}\n"
            f"Cards: {', '.join(selected_cards)}\n"
            "Provide a detailed, mystical, and personalized interpretation."
        )
        chain = chat_template | model | parser
        result = chain.invoke({"query": prompt})
        return result, selected_cards, zodiac
    except Exception as e:
        return f"Error: {e}", [], ""

#################### Chat with AI ##################### 
def chat_with_tarot(history, user_input, name, concern, zodiac_sign, tarot_cards):
    try:
        
        system = f"You are a Tarot chatbot. User is {name}, zodiac sign is {zodiac_sign}, concern is {concern}, and the tarot cards drawn were: {', '.join(tarot_cards)}. Keep the answer short and to the point accurate which should be easy to understand ."
        messages = [SystemMessage(content=system)]
        for msg in history:
            messages.append(HumanMessage(content=msg[0]))
            messages.append(AIMessage(content=msg[1]))
        messages.append(HumanMessage(content=user_input))
        response = model.invoke(messages)
        history.append((user_input, response.content))
        return history, "", name, concern, zodiac_sign, tarot_cards
    except Exception as e:
        history.append((user_input, f"Error: {e}"))
        return history, "", name, concern, zodiac_sign, tarot_cards

#################### Interface for user interaction ##################### 
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔮 MysticReads - Tarot Reading & Chat")
    gr.Markdown("Get a mystical tarot reading and chat about it with our AI Tarot guide.")

    with gr.Row():
        name_input = gr.Text(label="Your Name")
        dob_input = gr.Textbox(label="Date of Birth (YYYY-MM-DD)", placeholder="e.g., 1997-11-02")

    concern_input = gr.Dropdown(label="Area of Concern", choices=list(concern_cards.keys()), value="Career")

    output_text = gr.Textbox(label="Your Tarot Reading", lines=10, interactive=False)
    submit_button = gr.Button("Get Tarot Reading ✨")

    tarot_cards_state = gr.State([])
    zodiac_state = gr.State("")
    name_state = gr.State("")
    concern_state = gr.State("")

    chatbot = gr.Chatbot(label="Mystic Chat")
    msg = gr.Textbox(label="Ask more about your reading", placeholder="Type a follow-up...")
    send_btn = gr.Button("Send")

    submit_button.click(
        fn=generate_tarot_reading,
        inputs=[name_input, dob_input, concern_input],
        outputs=[output_text, tarot_cards_state, zodiac_state]
    ).then(
        fn=lambda name, concern: ([], "", name, concern),
        inputs=[name_input, concern_input],
        outputs=[chatbot, msg, name_state, concern_state]
    )

    send_btn.click(
        fn=chat_with_tarot,
        inputs=[chatbot, msg, name_state, concern_state, zodiac_state, tarot_cards_state],
        outputs=[chatbot, msg, name_state, concern_state, zodiac_state, tarot_cards_state]
    )

demo.launch(share = True)
