
from transformers import pipeline
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import requests, os, textwrap

# Hugging Face credentials and endpoint
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-rw-1b"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()[0]['generated_text']
    except Exception as e:
        print("⚠️ Hugging Face API error:", e)
        print("Raw response:", response.text)
        return "Sorry, the AI is sleeping. Try again in a few minutes."

# Create folders
os.makedirs("videos", exist_ok=True)
os.makedirs("audio", exist_ok=True)
os.makedirs("frames", exist_ok=True)

# 🐒 Generate story
prompt = "Write a funny 60-second jungle monkey story with a twist ending."
output = query({"inputs": prompt})
story = output.replace(prompt, "").strip()

# 🎙️ Convert to voice
tts = gTTS(text=story, lang='en')
audio_path = "audio/monkey_voice.mp3"
tts.save(audio_path)

# 🖼 Text to image
img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()
wrapped_text = textwrap.fill(story, width=30)
draw.text((40, 200), wrapped_text, font=font, fill=(255, 255, 255))
image_path = "frames/text_frame.png"
img.save(image_path)

# 🎬 Combine video
image_clip = ImageClip(image_path).set_duration(AudioFileClip(audio_path).duration)
final = image_clip.set_audio(AudioFileClip(audio_path))
final.write_videofile("videos/monkey_story.mp4", fps=24)

# ✅ Save to Google Drive (if mounted)
if os.path.exists("/content/drive"):
    os.system("cp videos/monkey_story.mp4 /content/drive/MyDrive/")
    print("✅ Video copied to your Google Drive")
