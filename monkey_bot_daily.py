import os
import requests
import time
import random
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import textwrap

# 1. Generate funny monkey story with multiple lines
lines = [
    "I picked up a juicy mango and launched it like a jungle missile.",
    "Larry panicked and spun like a confused bird blender.",
    "I saw the tree was unguarded.",
    "I climbed like a ninja and snatched the banana.",
    "Sweet, glorious victory. I've never tasted anything so delicious."
]

# 2. Create directory
if not os.path.exists("monkey_assets"):
    os.makedirs("monkey_assets")

clips = []

# 3. Loop through lines and generate image + audio
for i, line in enumerate(lines):
    print(f"Generating scene {i+1}")

    # Get image from Craiyon
    prompt = line + " cartoon style"
    response = requests.post(
        "https://backend.craiyon.com/generate",
        json={"prompt": prompt}
    )
    if response.status_code != 200:
        print("Image failed, using fallback")
        img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    else:
        try:
            img_url = response.json()["images"][0]
            img_data = requests.get(f"https://img.craiyon.com/{img_url}").content
            with open(f"monkey_assets/scene{i}.jpg", "wb") as f:
                f.write(img_data)
            img = Image.open(f"monkey_assets/scene{i}.jpg")
        except:
            img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))

    # Draw text
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()
    wrapped = textwrap.fill(line, width=25)
    draw.text((50, 1700), wrapped, font=font, fill=(255, 255, 255))

    img_path = f"monkey_assets/frame{i}.jpg"
    img.save(img_path)

    # Text to speech
    tts = gTTS(line)
    audio_path = f"monkey_assets/line{i}.mp3"
    tts.save(audio_path)

    # Make clip
    clip = ImageClip(img_path).set_duration(4).set_audio(AudioFileClip(audio_path))
    clips.append(clip)

# 4. Combine clips
final = concatenate_videoclips(clips, method="compose")
final.write_videofile("monkey_story.mp4", fps=24)

# 5. Copy to Drive (if on Colab)
try:
    from google.colab import drive
    drive.mount('/content/drive')
    os.makedirs("/content/drive/MyDrive/MonkeyVids", exist_ok=True)
    os.system("cp monkey_story.mp4 /content/drive/MyDrive/MonkeyVids/")
    print("✅ Video copied to your Google Drive folder: MonkeyVids")
except:
    print("💾 Local video saved: monkey_story.mp4")
