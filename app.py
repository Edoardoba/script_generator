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
        if total_word_count >10000:target_words_per_section = 2000
        else:target_words_per_section = 3000
        
        num_sections = max(3, math.ceil(total_word_count / target_words_per_section))  # At least intro, 1 body, 1 conclusion
        

        
        words_per_section = total_word_count // num_sections
        


        complete_prompt = f"""
        You are creating a detailed outline for a long-form script of approximately {total_word_count} words on the followin topic:
        "{topic}""{title}".

        Structure:
        - Section 1: Introduction to the topic (no summary at end)
        - Section {num_sections}: Final Conclusion (no intro at start)
        - Sections 2 to {num_sections - 1}: Each should cover a unique and important aspect of the topic.
        Avoid overlapping content. Ensure smooth transitions between sections.
        
        Examples to understand the tone and the style:
        - The Body Knows Before the Mind Does. 
        - The Information Paradox: What Happens to Ingested Data?       
        - Philosophical, Cultural, and Ethical Implications of Black Hole Science. 
        - The Power of the Soul.
        - The Veil Between Worlds.

        List each section as a numbered item. Only output the section titles.
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
        
