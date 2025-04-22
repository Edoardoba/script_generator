import streamlit as st
import re
from openai import OpenAI
import time

# CONFIGURATION

# --- Simple Password Auth ---
PASSWORD = "abcde"  # change to your real password

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Script Generator Login")
    pwd = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
        else:
            st.error("Incorrect password")
    st.stop()



spiritual_file_list = ["file-3gbyDxwpb4s7xGttZVBb7s", "file-M4c8arf7KdFLm1Tp33WrV1", "file-J7U58YcwJRif1Smo2P2RgS"]
space_file_list = ["file-SMa1t9dvuRSPMgmfESmeVR", "file-MApSfBa7y6wY1PVipm1qL3", "file-MVhqAdFiLBAi7beG9kh7gY"]
story_file_list = ["file-JTF44vJCUNXMQnuY1LYPEM", "file-HQsYc21CHAS3LgjYiRXgHW", "file-MQzDtqd5ivWdD7Ejc7wN7Y"]

base_prompt_space = (
    "Write a section titled '{title}' in approximately {word_count} words, "
    "mirroring the tone, formatting, and structure of the attached style documents. "
    "Do not reference or extract content from the attachments—use them solely for stylistic guidance. "
    "Return only the text output, with no preamble or additional commentary."
)

base_prompt_spiritual = (
    "Write a section titled '{title}' in approximately {word_count} words, "
    "mirroring the tone, formatting, and structure of the attached style documents. "
    "Do not reference or extract content from the attachments—use them solely for stylistic guidance. "
    "Return only the text output, with no preamble or additional commentary."
)

base_prompt_story = (
    "Write a section titled '{title}' in approximately {word_count} words, "
    "mirroring the tone, formatting, and structure of the attached style documents. "
    "Do not reference or extract content from the attachments—use them solely for stylistic guidance. "
    "Return only the text output, with no preamble or additional commentary."
)

def generate_text(sections, selected_list, base_prompt, word_count):
    
    attachments = []
    for fileid in selected_list:
        attachments.append({ "file_id": fileid, "tools": [{"type": "file_search"}] })

    thread = client.beta.threads.create()  # Empty thread

    section_outputs = {}

    for title in sections:

        prompt = base_prompt.format(title=title, word_count=word_count)
        # Add message to thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt,
            attachments=attachments
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_GaGtZ5ULgtzqFZPEZ4rZgW3o"
        )

    # Step 2: Wait for it to complete
        check = True
        while check == True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                messages = list(client.beta.threads.messages.list(thread_id=thread.id))
                for msg in messages[::-1]:  # Start from most recent
                    if msg.role == "assistant":
                        section_outputs[title] = msg.content[0].text.value
                        check = False

            elif run_status.status in ["failed", "cancelled", "expired"]:
                raise Exception(f"Run failed with status: {run_status.status}")
            time.sleep(1)  # avoid hammering the API

        print("Completed section", title)

    return section_outputs



# --- API Setup ---
client = OpenAI(api_key=st.secrets["openai_key"] )  # Replace with your actual key
# --- Page Setup ---
st.set_page_config(page_title="Script Generator", layout="centered")
st.title("📝 Script Generator App")

# --- Initialize Session State ---
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "final_text" not in st.session_state:
    st.session_state.final_text = ""
if "show_final_text" not in st.session_state:
    st.session_state.show_final_text = False
if "sections" not in st.session_state:
    st.session_state.sections = ""
# --- Inputs ---
with st.form(key="input_form"):
    topic = st.text_input("Topic", placeholder="Write the main topic (i.e. Space...)")
    title = st.text_input("Script Title", placeholder="Write the title of the script (i.e. World of Whales)")
    total_word_count = st.text_input("Total Number of Words", placeholder="e.g., 1200")
    words_per_section = st.text_input("Words per Section", placeholder="e.g., 200")
    selected = st.selectbox("Choose a Type", [ "Space", "Story", "Spirituality"])
    generate = st.form_submit_button("Generate Sections")

# --- First Generation ---
if generate:
    if not all([topic, title, total_word_count, words_per_section, selected]):
        st.warning("Please fill out all fields.")
    else:
        try:
            num_sections = max(1, int(total_word_count) // max(1, int(words_per_section)))

            space_prompt = f"""
            You are creating a detailed outline of {num_sections} sections for a long-form script of approximately {total_word_count} words on the following topic:
            "{topic} - {title}".

            Structure:
            Section 1: Introduction to the topic (no summary at the end)
            Sections 2 to {num_sections - 1}: Each section must explore a specific, real, and interesting example or sub-theme related to the main topic.
            Section {num_sections}: Final Conclusion (no intro at the start)

            Prioritize real-world cases, named examples, historic events, cultural artifacts, individual theories, singular discoveries, or concrete scientific anomalies.

            Style Guide:
            Be bold, specific, and imaginative — but grounded.
            Think like a curious storyteller, not an academic summarizer.

            Output: Only the numbered section titles. No summaries, intros, or extra info.
            """
            spiritual_prompt = f"""
            You are creating a detailed outline of {num_sections} sections for a long-form script of approximately {total_word_count} words on the following topic:
            "{topic} - {title}".

            Structure:
            Section 1: Introduction to the topic (no summary at the end)
            Sections 2 to {num_sections - 1}: Each section must explore a specific, real, and interesting example or sub-theme related to the main topic.
            Section {num_sections}: Final Conclusion (no intro at the start)

            Prioritize real-world cases, named examples, historic events, cultural artifacts, individual theories, singular discoveries, or concrete scientific anomalies.

            Style Guide:
            Be bold, specific, and imaginative — but grounded.
            Think like a curious storyteller, not an academic summarizer.

            Output: Only the numbered section titles. No summaries, intros, or extra info.
            """

            story_prompt = f"""
            You are creating a detailed outline of {num_sections} sections for a long-form script of approximately {total_word_count} words on the following topic:
            "{topic} - {title}".

            Structure:
            Section 1: Introduction to the topic (no summary at the end)
            Sections 2 to {num_sections - 1}: Each section must explore a specific, real, and interesting example or sub-theme related to the main topic.
            Section {num_sections}: Final Conclusion (no intro at the start)

            Prioritize real-world cases, named examples, historic events, cultural artifacts, individual theories, singular discoveries, or concrete scientific anomalies.

            Style Guide:
            Be bold, specific, and imaginative — but grounded.
            Think like a curious storyteller, not an academic summarizer.

            Output: Only the numbered section titles. No summaries, intros, or extra info.
            """

            if selected =="Space": 
                prompt = space_prompt
            elif selected =="Spiritual": 
                prompt = spiritual_prompt
            elif selected =="Story": 
                prompt = story_prompt
            else: 
                prompt = story_prompt

            
            

            with st.spinner("Generating outline..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that writes long, structured outlines."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.session_state.generated_text = response.choices[0].message.content.strip()
                

                sections = re.findall(r"^\s*\d+\.\s*(.+)", response.choices[0].message.content.strip(), re.MULTILINE)
                if not sections:
                    sections = [line.strip() for line in response.choices[0].message.content.strip().splitlines() if line.strip()]
                st.session_state.sections = sections  # Save for later use

        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- Show Generated Text Area ---
if st.session_state.generated_text:
    st.subheader("🧾 Outline (Editable)")
    edited_text = st.text_area("Edit the outline below if needed:", value=st.session_state.generated_text, height=400, key="edited_text")


    if selected =="Space": 
        selected_list = space_file_list
        base_prompt = base_prompt_space
    elif selected =="Spiritual": 
        selected_list = spiritual_file_list
        base_prompt = base_prompt_space
    elif selected =="Story": 
        selected_list = spiritual_file_list
        base_prompt = base_prompt_space
    else: 
        selected_list = spiritual_file_list
        base_prompt = base_prompt_space


    # --- Second Button to Continue ---
    if st.button("Continue"):
        sections = st.session_state.sections
        with st.spinner("Generating sections..."):
            generated_text = generate_text(sections, selected_list, base_prompt, words_per_section)
            output = ""
            for key in generated_text.keys():
                output += key + "\n" + generated_text[key] + "\n"

            st.session_state.final_text = output
            st.session_state.show_final_text = True
# --- Show Final Text Area ---
if st.session_state.show_final_text:
    st.subheader("🛠️ Final Output")
    st.text_area("Second Text Area Output", value=st.session_state.final_text, height=400, disabled=False)

        # Download Button
    st.download_button(
        label="📥 Download as .txt",
        data=str(st.session_state.final_text),
        file_name="script_output.txt",
        mime="text/plain"
    )
