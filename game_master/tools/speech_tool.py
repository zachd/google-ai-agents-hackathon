import os
import tempfile
import time
from google.adk.tools import ToolContext
from google.cloud import texttospeech_v1beta1 as texttospeech # Using v1beta1 for more advanced voice options
from google.cloud import aiplatform
from google.api_core.exceptions import ResourceExhausted

# Initialize Vertex AI (assuming project ID and location are set in environment or gcloud config)
aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location="us-central1")

# Define a mapping of agent names to voice configurations
AGENT_VOICES = {
    "quest_master": texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-D",  # Vertex AI Neural2 voice
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    ),
    "user_persona": texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-E",  # Vertex AI Neural2 voice
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    ),
    # Add more agents and their desired voices here
}

def process_speech_input(tool_context: ToolContext, speech_text: str) -> str:
    """
    Processes speech input from the user using Vertex AI Speech-to-Text (conceptual).
    In a real scenario, this would be the output of a Vertex AI Speech-to-Text API.
    """
    tool_context.update_state({"last_speech_input": speech_text})
    return f"Understood via Vertex AI STT: '{speech_text}'. How can I assist further?"

def generate_speech_output(tool_context: ToolContext, response_text: str, agent_name: str = "default") -> str:
    """
    Generates speech output for the user using Vertex AI Text-to-Speech.
    The voice used depends on the provided agent_name.
    Returns the path to the generated audio file.
    """
    # Vertex AI Text-to-Speech uses the same client as Google Cloud Text-to-Speech, but with specific models
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=response_text)

    # Select voice based on agent_name, default to a neutral Vertex AI Neural2 voice if not found
    voice = AGENT_VOICES.get(agent_name, texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Neural2-A", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    ))

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        time.sleep(1) # Introduce a small delay to mitigate quota issues
    except ResourceExhausted as e:
        return f"Error: Quota exceeded for Vertex AI Text-to-Speech API. Please check your Google Cloud project quotas. Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred during Vertex AI speech synthesis: {e}"

    # The response's audio_content is binary. Save it to a temporary file.
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as out_file:
        out_file.write(response.audio_content)
        audio_file_path = out_file.name

    tool_context.update_state({"last_speech_output_file": audio_file_path})
    return f"Audio generated for {agent_name} via Vertex AI and saved to: {audio_file_path}"
