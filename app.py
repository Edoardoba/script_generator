import streamlit as st
import time
import io
import os
from openai import OpenAI
import re
import math

# Setup OpenAI client
client = OpenAI(api_key=st.secrets["openai_key"] )  # Replace with your actual key

# Set page title
st.set_page_config(page_title="Script Generator", layout="centered")

# UI
st.title("📝 Script Generator App")
topic = st.text_input("Topic", placeholder="Write the main topic (i.e. Space...)") #Added Default Value
title = st.text_input("Script Title", placeholder="Write the title of the script (i.e. World of Whales)")
total_word_count = st.text_input("Number of Words")  # Single-line input
words_per_section = st.text_input("Number of words per section")  # Single-line input

selected = st.selectbox("Choose type", ["", "Space", "Story", "Spirituality"])


# === INFERRED SECTION COUNT ===






if title!="" and total_word_count !="" and topic !="" and selected!="" and words_per_section!="":

          

    num_sections = int(total_word_count) // int(words_per_section)
    
    complete_prompt = f"""
    You are creating a detailed outline of {num_sections} sections for a long-form script of approximately {total_word_count} words on the followin topic:
    "{topic}""{title}".
    Structure:
    Section 1: Introduction to the topic (no summary at the end)
    Sections 2 to {num_sections - 1}: Each section must explore a specific, real, and interesting example or sub-theme related to the main topic. Avoid vague or generic overviews.
    Section {num_sections}: Final Conclusion (no intro at the start)



    Prioritize real-world cases, named examples, historic events, cultural artifacts, individual theories, singular discoveries, or concrete scientific anomalies.
    Only include philosophical, speculative, or thematic ideas if they are tied directly to something specific or real.
    Each section should sound like it could be the title of a fascinating standalone documentary segment — not a textbook chapter.
    Avoid repeating the same types of content across different scripts (e.g. “ethical implications” or “cultural perceptions”) unless it’s tailored with unique and specific content.

    Style Guide:
    Be bold, specific, and imaginative — but grounded.
    Think like a curious storyteller, not an academic summarizer.
    Surprise the audience with lesser-known facts, forgotten history, strange details, or vivid oddities.

    Output:
    Provide only the numbered section titles.

    Do not include summaries, explanations, or intros — just the titles.


    Example Use Cases
    Here’s how this prompt would naturally steer the script in the right direction for different topics:

    Topic - Example of a Better Section:

    The Strangest Stars in the Universe should be “PSR J1719–1438b: The Planet Made of Crystallized Diamond”
    Flat Earth Beliefs Through History should be “The Babylonian World Map: A Flat Earth in Cuneiform”
    Black Holes in Human Culture should be “The ‘Dark Mouth’ in Navajo Mythology and Cosmic Holes”
    The Nature of Time should be “Timekeeping on Mars: Why Sols Break Earth’s Clock”

    Output only the numbered section titles.
    """


    print(complete_prompt)

    # === STEP 1: GENERATE OUTLINE ===
    outline_prompt = complete_prompt
    
    outline_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes long, structured outlines following instructions."},
            {"role": "user", "content": outline_prompt}
        ]
    )

    outline_text = outline_response.choices[0].message.content
    print("\n=== Generated Outline ===\n")
    print(outline_text)

    # === STEP 2: PARSE SECTIONS ===
    sections = re.findall(r"^\s*\d+\.\s*(.+)", outline_text, re.MULTILINE)
    if not sections:
        sections_cleaned = [line.strip() for line in outline_text.splitlines() if line.strip()]
    


    text = st.text_area("Output", outline_text, height=400)

if st.button("Generate Full Text"):

    st.text_area("Full Script", "COMING SOON", height=400)
        
