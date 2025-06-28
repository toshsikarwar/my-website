import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import pyttsx3
import whisper
import os

def generate_voiceover(text, filename="voiceover.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

def transcribe_audio(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result["text"]

def process_video(video_path, text_option, use_transcription=False):
    try:
        if use_transcription:
            text = transcribe_audio(video_path)
        else:
            text = text_option

        generate_voiceover(text)
        video = VideoFileClip(video_path)
        audio = AudioFileClip("voiceover.mp3").set_duration(video.duration)
        video = video.set_audio(audio)

        subtitle = TextClip(text, fontsize=24, color='white', bg_color='black', size=video.size)
        subtitle = subtitle.set_duration(video.duration).set_position(("center", "bottom"))

        final = CompositeVideoClip([video, subtitle])
        final.write_videofile("edited_output.mp4", codec="libx264", audio_codec="aac")
        messagebox.showinfo("✅ Success", "Video created successfully as 'edited_output.mp4'")
    except Exception as e:
        messagebox.showerror("❌ Error", str(e))

def select_video():
    filepath = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if filepath:
        video_path_var.set(filepath)

def generate():
    video_path = video_path_var.get()
    text = text_input.get("1.0", tk.END).strip()
    use_transcribe = transcribe_var.get()

    if not video_path:
        messagebox.showwarning("⚠️ Warning", "Please select a video.")
        return

    if not use_transcribe and not text:
        messagebox.showwarning("⚠️ Warning", "Please enter voiceover text or enable transcription.")
        return

    process_video(video_path, text, use_transcribe)

app = tk.Tk()
app.title("AI Video Editor: Voiceover + Subtitles + Transcription")
app.geometry("600x400")

video_path_var = tk.StringVar()
transcribe_var = tk.BooleanVar()

tk.Label(app, text="🎞️ Select Video File:").pack(pady=5)
tk.Entry(app, textvariable=video_path_var, width=60).pack()
tk.Button(app, text="Browse", command=select_video).pack(pady=5)

tk.Checkbutton(app, text="🧠 Auto-Transcribe Voice (Whisper AI)", variable=transcribe_var).pack(pady=5)

tk.Label(app, text="📝 Or Enter Custom Voiceover Text:").pack(pady=5)
text_input = tk.Text(app, height=6, width=70)
text_input.pack(pady=5)

tk.Button(app, text="🎬 Generate Final Video", command=generate, bg="green", fg="white").pack(pady=10)

app.mainloop()
