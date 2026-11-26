
# ==========================================
# AI TEXT ASSISTANT
# ==========================================

# STEP 1: Import required libraries
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai


# ==========================================
# STEP 2: Application Configuration
# ==========================================

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Check whether API key exists
if not api_key:
    st.error(
        "Gemini API key not found. Configure GEMINI_API_KEY "
        "in your .env file or Streamlit Cloud Secrets."
    )
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)


# ==========================================
# STEP 3: Session State Initialization
# ==========================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================
# STEP 4: Helper Functions
# ==========================================

def build_prompt(task, tone, output_length, user_text):

    # Task instructions
    task_instructions = {
        "Summarize": "Summarize the given text.",
        "Rewrite": "Rewrite the given text in clear and natural English.",
        "Explain": "Explain the given text in simple language with examples.",

        "Translate to Hinglish": """
Translate the given text into natural, clear Hinglish.

Rules:
1. Use Hindi and English naturally in Roman script.
2. Preserve the exact meaning and intent of the original text.
3. Do not add greetings, opinions, jokes, questions or extra information.
4. Do not remove or summarize any information.
5. Keep technical terms in English.
6. Maintain the original tone: formal text must remain formal,
   and casual text must remain casual.
7. Avoid unnecessary filler words.
8. Use grammatically correct and natural Hinglish.
9. STRICT SCRIPT RULE: Write the entire output ONLY
   using English/Roman alphabets (A-Z, a-z).
   NEVER use Hindi Devanagari characters.
   Even Hindi words must be written in Roman script.
   Example: Write "kaam karna", NOT "काम करना".
"""
    }

    # Tone instructions
    tone_instructions = {
        "Professional": "Use professional language.",
        "Casual": "Use casual and conversational language.",
        "Friendly": "Use warm and friendly language."
    }

    # Output length instructions
    length_instructions = {
        "Short": "Keep the response to 2-3 sentences.",
        "Medium": "Give a balanced response in one short paragraph.",
        "Detailed": "Provide a detailed response with key points and examples."
    }

    # Special prompt for Hinglish translation
    if task == "Translate to Hinglish":

        final_prompt = f"""
        Task: {task_instructions[task]}

        Important: Translate the complete text.
        Do not shorten, summarize or add extra information.

        Original Text:
        {user_text}
        """

    else:

        final_prompt = f"""
        Task: {task_instructions[task]}

        Tone: {tone_instructions[tone]}

        Output Length: {length_instructions[output_length]}

        Text: {user_text}
        """

    return final_prompt


# Function to generate AI response
def generate_response(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ==========================================
# STEP 5: Application UI
# ==========================================

st.title("AI Text Assistant")

st.write(
    "Your personal AI assistant for text summarization, "
    "rewriting, explanation and Hinglish translation."
)


# STEP 6: Task Selection
task = st.selectbox(
    "Choose an AI Task",
    [
        "Summarize",
        "Rewrite",
        "Explain",
        "Translate to Hinglish"
    ]
)


# STEP 7: Tone Selection
tone = st.selectbox(
    "Choose Response Tone",
    ["Professional", "Casual", "Friendly"]
)


# STEP 8: Output Length Selection
output_length = st.selectbox(
    "Choose Output Length",
    ["Short", "Medium", "Detailed"]
)


# STEP 9: User Text Input
user_text = st.text_area(
    "Enter your text here:",
    height=200,
    max_chars=5000,
    placeholder="Paste your text here..."
)

st.caption(f"Characters: {len(user_text)} / 5000")


# ==========================================
# STEP 10: Generate Button
# ==========================================

if st.button("Generate", type="primary"):

    if not user_text.strip():
        st.warning("Please enter some text.")

    elif len(user_text.strip()) < 10:
        st.warning("Please enter at least 10 characters.")

    else:

        try:

            final_prompt = build_prompt(
                task,
                tone,
                output_length,
                user_text
            )

            with st.spinner("Generating your response..."):

                generated_text = generate_response(final_prompt)

            if not generated_text:
                st.warning("Gemini returned an empty response.")

            else:

                # Save response in history
                st.session_state.chat_history.append({
                    "task": task,
                    "tone": tone,
                    "length": output_length,
                    "input": user_text,
                    "output": generated_text
                })

                # Keep only the latest 10 responses
                if len(st.session_state.chat_history) > 10:
                    st.session_state.chat_history.pop(0)

                # Display result
                st.subheader("AI Generated Result")

                st.code(
                    generated_text,
                    language=None
                )

                st.success("Response generated successfully!")

        except Exception as e:

            error_message = str(e).lower()

            if "429" in error_message or "resource_exhausted" in error_message:
                st.error("API quota exceeded. Please wait and try again.")

            elif "api key" in error_message or "401" in error_message or "403" in error_message:
                st.error("API authentication failed. Check your Gemini API key.")

            elif "connection" in error_message or "network" in error_message:
                st.error("Network error. Please check your internet connection.")

            else:
                st.error("An unexpected error occurred. Please try again.")
                print(f"Unexpected error: {e}")


# ==========================================
# STEP 11: Chat History
# ==========================================

st.divider()

st.subheader("Generation History")

if st.session_state.chat_history:

    if st.button("Clear History"):

        st.session_state.chat_history.clear()
        st.rerun()

    for index, item in enumerate(
        reversed(st.session_state.chat_history),
        start=1
    ):

        with st.expander(
            f"{item['task']} | {item['tone']} | {item['length']}"
        ):

            st.write("**Original Input:**")
            st.write(item["input"])

            st.write("**AI Generated Output:**")
            st.code(item["output"], language=None)

else:

    st.info("No generation history yet. Generate your first response!")
