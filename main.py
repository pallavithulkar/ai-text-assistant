
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

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Check whether API key exists
if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)


# ==========================================
# STEP 3: Session State Initialization
# ==========================================

# Store previous AI responses during the session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================
# STEP 4: Create Helper Functions
# ==========================================

# Function to create a prompt based on user selections
def build_prompt(task, tone, output_length, user_text):

    # Task instructions
    task_instructions = {
        "Summarize": "Summarize the given text.",
        "Rewrite": "Rewrite the given text in clear and natural English.",
        "Explain": "Explain the given text in simple language with examples."
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

    # Combine all instructions into one prompt
    final_prompt = f"""
    Task: {task_instructions[task]}

    Tone: {tone_instructions[tone]}

    Output Length: {length_instructions[output_length]}

    Text: {user_text}
    """

    return final_prompt


# Function to send prompt to Gemini
def generate_response(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ==========================================
# STEP 5: Application UI
# ==========================================

# Application title
st.title("AI Text Assistant")

# Application description
st.write("Your personal AI assistant for text summarization, rewriting and explanation.")


# STEP 6: Task Selection
task = st.selectbox(
    "Choose an AI Task",
    ["Summarize", "Rewrite", "Explain"]
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

# Display character count
st.caption(f"Characters: {len(user_text)} / 5000")


# ==========================================
# STEP 10: Generate Button
# ==========================================

if st.button("Generate", type="primary"):

    # Validate empty input
    if not user_text.strip():
        st.warning("Please enter some text.")

    # Validate minimum input length
    elif len(user_text.strip()) < 10:
        st.warning("Please enter at least 10 characters.")

    else:

        try:

            # Build the final prompt
            final_prompt = build_prompt(
                task,
                tone,
                output_length,
                user_text
            )

            # Show loading spinner while Gemini generates response
            with st.spinner("Generating your response..."):

                generated_text = generate_response(final_prompt)

            # Check whether Gemini returned a response
            if not generated_text:
                st.warning("Gemini returned an empty response.")

            else:

                # Save generated response in session history
                st.session_state.chat_history.append({
                    "task": task,
                    "tone": tone,
                    "length": output_length,
                    "input": user_text,
                    "output": generated_text
                })

                # Display generated result
                st.subheader("AI Generated Result")

                st.code(
                    generated_text,
                    language=None
                )

                st.success("Response generated successfully!")

        except Exception as e:

            # Handle different API errors
            error_message = str(e).lower()

            if "429" in error_message or "resource_exhausted" in error_message:
                st.error("API quota exceeded. Please wait and try again.")

            elif "api key" in error_message or "401" in error_message or "403" in error_message:
                st.error("API authentication failed. Check your Gemini API key.")

            elif "connection" in error_message or "network" in error_message:
                st.error("Network error. Please check your internet connection.")

            else:
                st.error(f"Something went wrong: {e}")


# ==========================================
# STEP 11: Chat History
# ==========================================

st.divider()

st.subheader("Generation History")

# Check whether history contains any responses
if st.session_state.chat_history:

    # Clear history button
    if st.button("Clear History"):

        st.session_state.chat_history.clear()
        st.rerun()

    # Display previous responses
    for index, item in enumerate(
        reversed(st.session_state.chat_history),
        start=1
    ):

        with st.expander(f"{item['task']} | {item['tone']} | {item['length']}"):

            st.write("**Original Input:**")
            st.write(item["input"])

            st.write("**AI Generated Output:**")
            st.code(item["output"], language=None)

else:

    st.info("No generation history yet. Generate your first response!")
