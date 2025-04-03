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
topic = st.text_input("Script Topic", placeholder="Write the main topic") #Added Default Value
title = st.text_input("Script Title", placeholder="Write the title of the script")
total_word_count = st.text_input("Number of Words")  # Single-line input



output_placeholder = st.empty()

if st.button("Generate"):
    with st.spinner("Generating text..."):
    
        # === INFERRED SECTION COUNT ===
        total_word_count = int(total_word_count)
        if total_word_count >10000:target_words_per_section = 3000
        elif 5000>total_word_count >10000:target_words_per_section = 3000
        elif 3000>total_word_count >5000:target_words_per_section = 2000
        elif 1500>total_word_count >3000:target_words_per_section = 1000
        else:target_words_per_section = 500
        
        num_sections = max(3, math.ceil(total_word_count / target_words_per_section))  # At least intro, 1 body, 1 conclusion
                
        words_per_section = total_word_count // num_sections

        complete_prompt = f"""
        You are creating a detailed outline for a long-form script of approximately {total_word_count} words on the followin topic:
        "{topic}""{title}".
        Structure:
        Section 1: Introduction to the topic (no summary at the end)
        Section {num_sections}: Final Conclusion (no intro at the start)
        Sections 2 to {num_sections - 1}: Each section must explore a specific, real, and interesting example or sub-theme related to the main topic.
        Rules for Sections 2 to {num_sections - 1}:
        Avoid vague or generic overviews.
        
        
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
        
        
        🔁 Example Use Cases
        Here’s how this prompt would naturally steer the script in the right direction for different topics:
        
        Topic - Example of a Better Section:
        
        The Strangest Stars in the Universe should be “PSR J1719–1438b: The Planet Made of Crystallized Diamond”
        Flat Earth Beliefs Through History should be “The Babylonian World Map: A Flat Earth in Cuneiform”
        Black Holes in Human Culture should be “The ‘Dark Mouth’ in Navajo Mythology and Cosmic Holes”
        The Nature of Time should be “Timekeeping on Mars: Why Sols Break Earth’s Clock”
        
        Output only the numbered section titles.
        """


        words_per_section = total_word_count // num_sections

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
            

        
        output_placeholder.text_area("Output", outline_text, height=400)
        
        # Download Button
        #output_file = io.StringIO(sections)
        #st.download_button(
        #    label="Download Output",
        #    data=output_file.getvalue(),
        #    file_name="generated_text.txt",
        #    mime="text/plain",
        #)
        
