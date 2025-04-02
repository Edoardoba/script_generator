import streamlit as st
import time
import io


# Set page title
st.set_page_config(page_title="Script Generator", layout="centered")

# UI
st.title("📝 Script Generator App")

input1 = st.text_area("User Input", height=70)
input2 = st.text_input("Number of Words")  # Single-line input
input3 = st.text_area("Prompt", value="Write a short script about...") #Added Default Value

output_placeholder = st.empty()

if st.button("Generate"):
    with st.spinner("Generating text..."):
        time.sleep(3)  # Simulate processing
        
        generated_text = f"Coming soon!"
        
        output_placeholder.text_area("Output", generated_text, height=200)
        
        # Download Button
        output_file = io.StringIO(generated_text)
        st.download_button(
            label="Download Output",
            data=output_file.getvalue(),
            file_name="generated_text.txt",
            mime="text/plain",
        )