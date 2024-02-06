from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import time
import concurrent.futures

class VideoProcessor:
    def __init__(self, file_path, video_output_path, audio_output_path):
        self.file_path = file_path
        self.video_output_path = video_output_path
        self.audio_output_path = audio_output_path
        self.video_clip = VideoFileClip(file_path)

    def get_video_bitrate(self):
        # Get the file size in bytes
        file_size = os.path.getsize(self.file_path)
    
        # Calculate the bitrate
        video_bitrate = (file_size * 8) / self.video_clip.duration  
    
        return video_bitrate

    def get_file_size(self, file_path):
        return os.path.getsize(file_path)

    def write_video(self):
        # Increase the bitrate to maintain video quality
        self.video_clip.write_videofile(self.video_output_path, codec="libx264", audio=False, bitrate="3000k", threads=4)

    def cut_audio(self):
        audio_clip = self.video_clip.audio
        audio_clip.write_audiofile(self.audio_output_path, codec='mp3', bitrate='192k')

    def process_video(self):
        start_time = time.time()

        # Get video bitrate of the input file
        input_video_bitrate = self.get_video_bitrate()

        # Use ThreadPoolExecutor for concurrent execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit tasks for video writing and audio cutting
            video_future = executor.submit(self.write_video)
            audio_future = executor.submit(self.cut_audio)

            # Wait for both tasks to finish
            concurrent.futures.wait([video_future, audio_future])

        # Close video clip
        self.video_clip.close()

        end_time = time.time()

        # Log input video bitrate
        print(f"Input Video Bitrate: {input_video_bitrate} kbps")

        # Log file sizes
        input_size = self.get_file_size(self.file_path)
        output_video_size = self.get_file_size(self.video_output_path)
        output_audio_size = self.get_file_size(self.audio_output_path)

        print(f"Input File Size: {input_size / (1024 * 1024):.2f} MB")
        print(f"Output Video File Size: {output_video_size / (1024 * 1024):.2f} MB")
        print(f"Output Audio File Size: {output_audio_size / (1024 * 1024):.2f} MB")

        # Log processing time
        print(f"Processing Time: {end_time - start_time:.2f} seconds")

# Update file paths as needed
file_input = os.path.join('input', 'horse.mp4')
file_video_output = os.path.join('output', 'horse_video.mp4')
file_audio_output = os.path.join('output', 'horse_audio.mp3')

processor = VideoProcessor(file_input, file_video_output, file_audio_output)
processor.process_video()
