import os
import math
import struct
import wave
import subprocess
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

output_dir = os.path.abspath("brag-output")
work_dir = os.path.join(output_dir, "work")
frames_dir = os.path.join(work_dir, "frames")
os.makedirs(frames_dir, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
fps = 30
duration = 22.0
total_frames = int(fps * duration)

print(f"1. Synthesizing background soundtrack (22s)...")
audio_wav = os.path.join(work_dir, "audio.wav")
sample_rate = 44100
num_samples = int(sample_rate * duration)

# Chord progression in C Major / A Minor: C -> G -> Am -> F -> C -> G -> C
chords = [
    [261.63, 329.63, 392.00], # C (0s - 3s)
    [196.00, 246.94, 293.66], # G (3s - 6.2s)
    [220.00, 261.63, 329.63], # Am (6.2s - 9.5s)
    [174.61, 220.00, 261.63], # F (9.5s - 13.0s)
    [261.63, 329.63, 392.00], # C (13.0s - 16.5s)
    [196.00, 246.94, 293.66], # G (16.5s - 19.5s)
    [261.63, 329.63, 523.25], # C oct (19.5s - 22.0s)
]
times = [3.0, 6.2, 9.5, 13.0, 16.5, 19.5, 22.0]

with wave.open(audio_wav, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)

    frames = bytearray()
    for i in range(num_samples):
        t = i / sample_rate

        # determine chord
        cur_chord = chords[0]
        for idx, edge in enumerate(times):
            if t < edge:
                cur_chord = chords[idx]
                break

        # Warm additive synth with envelope
        val = 0.0
        for freq in cur_chord:
            val += math.sin(2 * math.pi * freq * t) * 0.2
            # Add subtle octave overtone
            val += math.sin(2 * math.pi * freq * 2.0 * t) * 0.08

        # Subtle bassline (root note)
        root = cur_chord[0] / 2.0
        val += math.sin(2 * math.pi * root * t) * 0.35

        # Master fade in and fade out
        if t < 0.5:
            val *= (t / 0.5)
        elif t > 21.0:
            val *= ((22.0 - t) / 1.0)

        sample = int(max(-1.0, min(1.0, val)) * 24000)
        frames.extend(struct.pack("<hh", sample, sample))

    wf.writeframes(frames)
print(f"Soundtrack generated at {audio_wav}")

print(f"2. Capturing {total_frames} video frames at 1920x1080 (30fps)...")
player_html = os.path.abspath(os.path.join(work_dir, "player.html")).replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto(f"file:///{player_html}")
    page.wait_for_timeout(1000)

    for frame_idx in range(total_frames):
        t = frame_idx / fps
        page.evaluate(f"window.setVideoTime({t})")
        frame_file = os.path.join(frames_dir, f"frame_{frame_idx:04d}.png")
        page.screenshot(path=frame_file)

        if frame_idx % 60 == 0 or frame_idx == total_frames - 1:
            print(f"Rendered frame {frame_idx}/{total_frames} (t={t:.2f}s)")

    browser.close()

print("3. Encoding high-definition MP4 video with FFmpeg...")
final_mp4 = os.path.join(output_dir, "brag.mp4")
poster_jpg = os.path.join(output_dir, "brag.jpg")

# Render MP4
cmd = [
    ffmpeg_exe, "-y",
    "-framerate", str(fps),
    "-i", os.path.join(frames_dir, "frame_%04d.png"),
    "-i", audio_wav,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    final_mp4
]
subprocess.run(cmd, check=True)
print(f"Video rendered successfully: {final_mp4}")

# Extract poster image (frame 0 / lobby view)
poster_frame = os.path.join(frames_dir, "frame_0100.png")
if os.path.exists(poster_frame):
    from PIL import Image
    im = Image.open(poster_frame)
    im.convert("RGB").save(poster_jpg, quality=95)
    print(f"Poster frame saved: {poster_jpg}")

print("4. Writing share-copy.txt...")
share_copy = os.path.join(output_dir, "share-copy.txt")
with open(share_copy, "w", encoding="utf-8") as f:
    f.write(
        "Built PennyWise: an open-source, local-first personal finance coach. 🏦\n\n"
        "• Instant statement analytics with Pandas\n"
        "• Grounded RAG knowledge citations with ChromaDB\n"
        "• Personalized coaching via local Llama 3.2 via Ollama\n"
        "• Total data privacy — raw transactions never leave your laptop.\n\n"
        "#BuildInPublic #LocalAI #Python #FastAPI #OpenSource\n"
    )

print("🎉 /brag launch video production complete!")
