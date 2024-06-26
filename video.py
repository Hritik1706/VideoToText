import os
import streamlit as st
import assemblyai as aai
import subprocess
from tempfile import NamedTemporaryFile

st.title("Video_To_Transcribe")

# File uploader
video_file = st.file_uploader("Upload Video", type=["mp4", "mkv", "avi"])

aai.settings.api_key = "your api key"
st.text("Model Loaded")

# Audio file path
audio_file_path = "audio_file_path.wav"

def convert_video_to_mp3(input_file, audio_file_path):
    # Saving file to a temporary location
    with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(input_file.read())
        temp_video_file_path = temp_video_file.name

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", temp_video_file_path,
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        "-y", audio_file_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    os.remove(temp_video_file_path)

    return audio_file_path

if st.sidebar.button("Transcribe"):
    if video_file is not None:
        # Convert the video to audio
        audio_file_path = convert_video_to_mp3(video_file, audio_file_path)

        # Transcribe the audio
        transcriber = aai.Transcriber()
        transcription = transcriber.transcribe(audio_file_path)

        # Access the transcribed text using .text attribute
        transcribed_text = transcription.text
        st.sidebar.success("Transcribing complete")
        st.markdown(transcribed_text)
    else:
        st.sidebar.error("Please upload a video file")

if os.path.exists(audio_file_path):
    try:
        os.remove(audio_file_path)
    except OSError:
        pass

st.sidebar.header("Play Original Video File")
st.sidebar.video(video_file)
