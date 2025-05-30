import azure.cognitiveservices.speech as speechsdk
import os
# Replace with your Azure Speech resource info
speech_key = os.getenv("azure_speech_key")  
service_region = os.getenv("azure_speech_region")
service_endpoint = os.getenv("azure_speech_endpoint")

def from_microphone():
    # Set up the config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Optional: improve recognition
    speech_config.speech_recognition_language = "en-US"
    speech_config.enable_dictation()

    # Use default mic
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create recognizer
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone (Ctrl+C to stop)...")

    # Recognize continuously
    def handle_final_result(evt):
        print(f"\n[Result] {evt.result.text}")

    def handle_intermediate(evt):
        print(f"\r[Partial] {evt.result.text}", end='')

    speech_recognizer.recognizing.connect(handle_intermediate)
    speech_recognizer.recognized.connect(handle_final_result)

    # Start continuous recognition
    speech_recognizer.start_continuous_recognition()

    try:
        while True:
            pass  # Keep the app running
    except KeyboardInterrupt:
        print("\nStopping...")
        speech_recognizer.stop_continuous_recognition()

from_microphone()
