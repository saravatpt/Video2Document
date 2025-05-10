import whisper
from tqdm import tqdm
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
video_path=os.getenv('video_path')
def transcribe_video_with_progress(video_path, model_size="base"):
    # model = whisper.load_model(model_size)
    # print(f"🔍 Transcribing {video_path} using Whisper {model_size} model...\n")

    # result = model.transcribe(video_path, verbose=False)

    # segments = result["segments"]
    # total_segments = len(segments)

    # with open("transcript.txt", "w", encoding="utf-8") as f:
    #     f.write(f"Transcript of {video_path}\n\n")

    #     for segment in tqdm(segments, desc="📝 Writing transcript", unit="segments"):
    #         start = segment["start"]
    #         end = segment["end"]
    #         text = segment["text"].strip()
    #         f.write(f"[{start:.2f} --> {end:.2f}] {text}\n")

    # print("\n✅ Done! Transcript saved to transcript.txt")

    # Read the transcript
    transcript_content = ""
    try:
        with open("transcript.txt", "r", encoding="utf-8") as f:
            transcript_content = f.read()
    except FileNotFoundError:
        print("❌ Error: transcript.txt not found.")
        return ""

    # Send transcript to Gemini using the new method
    print("✨ Sending transcript to Gemini for document generation...")

    client = genai.Client(
        api_key=os.getenv('GEMINI_API_KEY'),
    )

    model_name = "gemini-2.5-flash-preview-04-17"
    contents = [
        types.Content(
            role="user", 
            parts=[
                types.Part.from_text(text=f"""Based on the following transcript, generate a well-structured word document:\n\n{transcript_content}"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    document_name = os.path.splitext(os.path.basename(video_path))[0]
    document_output_path = os.path.join("Output", f"{document_name}.txt")
    with open(document_output_path, "w", encoding="utf-8") as f:
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=generate_content_config,
        ):
            f.write(chunk.text)
            print(chunk.text, end="") # Optional: print to console as it streams

    print(f"\n✅ Document generated and saved to {document_output_path}")

    return ""

transcribe_video_with_progress(video_path)
