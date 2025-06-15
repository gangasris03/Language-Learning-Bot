import streamlit as st
import boto3

# Initialize AWS clients for Translate and Polly
translate = boto3.client('translate', region_name='us-east-1') 
polly = boto3.client('polly')

# Set up Streamlit app configuration
st.set_page_config(page_title="Language Learning Bot", layout="centered")
st.title("🗣️ Language Learning Bot")

# Input text from the user
text_input = st.text_input("Enter text in English:")

# Dropdown menu for selecting target language
target_language = st.selectbox("Select target language:", {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi",
    "Tamil": "ta",
    "Japanese": "ja"
})

# When the button is clicked, perform translation and text-to-speech
if st.button("Translate & Speak") and text_input:
    try:
        # Translate the text
        result = translate.translate_text(
            Text=text_input,
            SourceLanguageCode='en',
            TargetLanguageCode=target_language
        )
        translated_text = result['TranslatedText']
        st.success(f"Translated Text ({target_language}): {translated_text}")

        # Map of language codes to Polly voice IDs
        voice_id_map = {
            "fr": "Celine", "es": "Lupe", "de": "Hans",
            "hi": "Aditi", "ta": "Aditi", "ja": "Mizuki"
        }

        # Generate speech using Polly
        tts_response = polly.synthesize_speech(
            Text=translated_text,
            OutputFormat='mp3',
            VoiceId=voice_id_map.get(target_language, 'Joanna')
        )

        # Save the audio file locally
        audio_path = "output.mp3"
        with open(audio_path, "wb") as f:
            f.write(tts_response['AudioStream'].read())

        # Play the audio in Streamlit app
        st.audio(audio_path, format='audio/mp3')

    except Exception as e:
        st.error(f"❗ An error occurred: {e}")
