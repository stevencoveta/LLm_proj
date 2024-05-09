import streamlit as st
import openai

# Sidebar for API key input
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

def generate_response(input_text):
    # Checking if API key is valid format
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter a valid OpenAI API key!', icon='⚠️')
        return

    # Configure the API key for the OpenAI library
    openai.api_key = openai_api_key

    # Generating response using the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Updated to use the latest available model
            messages=[
                {"role": "user", "content": input_text}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return

# Main form interface
with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        response = generate_response(text)
        if response:
            st.info(response)

