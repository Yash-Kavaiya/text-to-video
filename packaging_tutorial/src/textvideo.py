import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import textwrap
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips

class VideoCreator:
    def __init__(self, file_path, font_path, image_size=(1920, 1080), background_color=(238, 164, 127),
                 font_color=(1, 83, 157), font_size=90, line_spacing=10, margin=80, fps=24):
        self.file_path = file_path
        self.font_path = font_path
        self.image_size = image_size
        self.background_color = background_color
        self.font_color = font_color
        self.font_size = font_size
        self.line_spacing = line_spacing
        self.margin = margin
        self.fps = fps

        # Initialize data_frame and data_list
        self.data_frame = pd.read_csv(file_path)
        self.data_list = self.data_frame.values.tolist()

    def create_image(self, data, idx):
        image = Image.new("RGB", self.image_size, self.background_color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, self.font_size)
        y_position = self.margin
        text_to_speak = ""

        for text in data:
            print("Type of 'text':", type(text))
            print("Content of 'text':", text)

            wrapped_text = textwrap.fill(str(text), width=40)  # Convert to string
            print("Type of 'wrapped_text':", type(wrapped_text))
            print("Content of 'wrapped_text':", wrapped_text)

            lines = wrapped_text.split('\n')

            for line in lines:
                draw.text((self.margin, y_position), line, font=font, fill=self.font_color)
                y_position += self.font_size + self.line_spacing
                text_to_speak += line + "\n"

            y_position += self.line_spacing

        image.save(f"Gyan_Dariyo_image_{idx + 1}.png")
        return image, text_to_speak

    def create_audio(self, text_to_speak, idx):
        tts = gTTS(text=text_to_speak, lang='gu')
        audio_file_path = f"Gyan_Dariyo_audio_{idx + 1}.mp3"
        tts.save(audio_file_path)
        return audio_file_path

    def create_video(self, audio_file_path, image_path, idx):
        audio_clip = AudioFileClip(audio_file_path)
        audio_duration = audio_clip.duration
        image_clip = ImageClip(image_path)
        video_clip = image_clip.set_audio(audio_clip)
        video_clip = video_clip.set_duration(audio_duration)
        video_clip = video_clip.set_fps(self.fps)
        video_file_path = f"Gyan_Dariyo_video_{idx + 1}.mp4"
        video_clip.write_videofile(video_file_path, codec="libx264", audio_codec="aac")
        print(f"Video {idx + 1} created: {video_file_path}")
        return video_file_path

    def create_final_video(self):
        video_list = []

        for idx, data in enumerate(self.data_list):
            image, text_to_speak = self.create_image(data, idx)
            audio_file_path = self.create_audio(text_to_speak, idx)
            video_file_path = self.create_video(audio_file_path, f"Gyan_Dariyo_image_{idx + 1}.png", idx)
            video_list.append(video_file_path)

        clips = [VideoFileClip(video) for video in video_list]
        final_video = concatenate_videoclips(clips)
        final_video_file_path = "Gyan_Dariyo_final_video.mp4"
        final_video.write_videofile(final_video_file_path, codec="libx264", audio_codec="aac")
        print(f"Final video created: {final_video_file_path}")

# Usage
file_path = '/content/તલાટી અને જુનિયર કલાર્ક મોડેલ પેપર -3.csv'
font_path = "/content/HindVadodara-SemiBold.ttf"

gyan_dariyo_creator = VideoCreator(file_path, font_path)
gyan_dariyo_creator.create_final_video()