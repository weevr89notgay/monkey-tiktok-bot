
import os
import random
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import textwrap
import urllib.request

# Monkey story lines
lines = [
    "I picked up a juicy mango and launched it like a jungle missile.",
    "Larry panicked and spun like a confused bird blender.",
    "I saw the tree was unguarded.",
    "I climbed like a ninja and snatched the banana.",
    "Sweet, glorious victory. I've never tasted anything so delicious."
]

# Make folders
os.makedirs("monkey_assets", exist_ok=True)
os.makedirs("monkey_images", exist_ok=True)

# Download 5 placeholder images once
placeholder_urls = [
    "https://i.imgur.com/odqosT0.jpg",
    "https://i.imgur.com/lkdHD7I.jpg",
    "https://i.imgur.com/sYTuA1A.jpg",
    "https://i.imgur.com/9v3P3yx.jpg",
    "https://i.imgur.com/hJWwUQn.jpg"
]

for idx, url in enumerate(placeholder_urls):
    img_path = f"monkey_images/fallback{idx}.jpg"
    if not os.path.exists(img_path):
        urllib.request.urlretrieve(url, img_path)

clips = []

for i, line in enumerate(lines):
    print(f"Using fallback image for scene {i+1}")
    img_path = f"monkey_images/fallback{i % len(placeholder_urls)}.jpg"
    img = Image.open(img_path).resize((1080, 1920))

    # Add text
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()
    wrapped = textwrap.fill(line, width=25)
    draw.text((50, 1700), wrapped, font=font, fill=(255, 255, 255))

    frame_path = f"monkey_assets/frame{i}.jpg"
    img.save(frame_path)

    # Voice
    tts = gTTS(line)
    audio_path = f"monkey_assets/line{i}.mp3"
    tts.save(audio_path)

    # Combine
    clip = ImageClip(frame_path).set_duration(4).set_audio(AudioFileClip(audio_path))
    clips.append(clip)

# Stitch together
final = concatenate_videoclips(clips, method="compose")
final.write_videofile("monkey_story.mp4", fps=24)

# Save to Drive if available
try:
    from google.colab import drive
    drive.mount('/content/drive')
    os.makedirs("/content/drive/MyDrive/MonkeyVids", exist_ok=True)
    os.system("cp monkey_story.mp4 /content/drive/MyDrive/MonkeyVids/")
    print("✅ Copied to Google Drive → MonkeyVids")
except:
    print("💾 Local video saved: monkey_story.mp4")
