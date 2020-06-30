from pathlib import Path
from moviepy.editor import *
import mimetypes



def audio_cutter(file, start_time, end_time):
    if end_time <= start_time:
        print("Start time should be lesser than end time")
        sys.exit(1)
    file_type = mimetypes.MimeTypes().guess_type(file)[0]
    out_path = Path(os.getcwd()) / "audio_out"
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    if "video" in file_type:
        print(f"\nCutting the video file: {file} from {str(start_time)} to {str(end_time)} seconds")
        video = VideoFileClip(file)
        audio = video.audio.subclip(start_time, end_time)
        cut_audio = "cut" + os.path.splitext(os.path.basename(file))[0] + ".mp3"
    elif "audio" in file_type:
        print(f"\nCutting the audio file: {file} from {str(start_time)} to {str(end_time)} seconds")
        audio = AudioFileClip(file).subclip(start_time, end_time)
        cut_audio = "cut" + os.path.basename(file)
    out_file = out_path / cut_audio
    audio.write_audiofile(out_file)


def concatenate_audio(audio_files):
    print("\nConcatenating the audio files....")
    if len(audio_files) < 2:
        print("Pass atleast two files....\n")
        sys.exit(1)
    add_audio = [AudioFileClip(file) for file in audio_files]
    out_path = Path(os.getcwd()) / "audio_out"
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_file = out_path / "concatenate_audio.mp3"
    result = concatenate_audioclips(add_audio)
    result.write_audiofile(str(out_file))


def audio_extract(video_file):
    print("\nExtracting audio from the video " + str(video_file))
    audio_name = os.path.splitext(os.path.basename(video_file))[0] + ".mp3"
    video = VideoFileClip(video_file)
    audio = video.audio
    out_path = Path(os.getcwd()) / "audio_out"
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_file = out_path / audio_name
    audio.write_audiofile(str(out_file))