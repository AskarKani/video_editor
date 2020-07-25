import os, natsort, math, sys
from pathlib import Path
from moviepy.editor import *
import mimetypes





def merger(input_path, out_file_name):
    file_type = mimetypes.MimeTypes().guess_type(input_path)[0]
    # if "video" not in file_type:
    #     print("Pass the valid video file as INPUT..")
    #     sys.exit(1)
    video_files = os.listdir(input_path)
    for file in video_files:
        file_type = mimetypes.MimeTypes().guess_type(file)[0]
        if "video" not in file_type:
            print("Pass the valid video file as INPUT..")
            sys.exit(1)
    current_dir = Path(os.getcwd()) / input_path
    files_sorted = natsort.natsorted(video_files)
    print(files_sorted)

    list_video = [VideoFileClip(str(current_dir / file)) for file in files_sorted]

    out_path = Path(os.getcwd()) / "merge_out"
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_file = out_path / out_file_name

    # To find fps
    video = VideoFileClip(str(current_dir / files_sorted[0]))
    fps = int(video.fps)

    result = concatenate_videoclips(list_video)
    result.write_videofile(str(out_file) ,fps=fps)


def gen_file_name(index, file_path):
    if len(file_path.split("\\")) > 1:
        file_name = str(index) + "_" + str(file_path.split("\\")[-1])
    elif len(file_path.split("/")) > 1:
        file_name = str(index) + "_" + str(file_path.split("/")[-1])
    else:
        file_name = str(index) + "_" + str(file_path)
    return file_name


def splitter(video_file, subclip_duration):
    file_type = mimetypes.MimeTypes().guess_type(video_file)[0]
    if "video" not in file_type:
        print("Pass the valid video file as INPUT..")
        sys.exit(1)
    video = VideoFileClip(video_file)
    fps = video.fps
    duration = int(video.duration)
    print("\nThe original duration of video : " + str(duration) + " seconds with " + str(fps) + " fps")

    number_of_subclips = math.ceil(duration / int(subclip_duration))
    print("\nTOTAL number of subclips : " + str(number_of_subclips))

    out_folder_path = Path(os.getcwd()) / "split_out"
    if not os.path.isdir(out_folder_path):
        os.mkdir(out_folder_path)

    for file_number in range(number_of_subclips):
        if not file_number:
            start = (file_number * subclip_duration)
        else:
            start = (file_number * subclip_duration)
        end = (file_number + 1) * subclip_duration
        if end > duration:
            end = duration
        file_name = gen_file_name(file_number, video_file)
        gen_file = out_folder_path / file_name
        sub_video = video.subclip(start, end)
        result = CompositeVideoClip([sub_video,])
        result.write_videofile(str(gen_file) ,fps=int(fps))


def gen_video_with_audio_name(video_path, audio_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_name =  os.path.splitext(os.path.basename(audio_path))[0]
    video_ext = os.path.splitext(video_path)[1]
    file_name = str(video_name) + "_" + str(audio_name) + str(video_ext)
    return file_name


def add_audio_to_video(video_file, audio_file):
    files ={
        "audio": audio_file,
        "video": video_file
    }
    for name, file in files.items():
        file_type = mimetypes.MimeTypes().guess_type(file)[0]
        if name not in file_type:
            print(f"Pass the valid {name} file as INPUT..")
            sys.exit(1)
    print("\nAdding audio : " + str(audio_file) + " to video : " + str(video_file))
    video = VideoFileClip(video_file)
    add_audio = AudioFileClip(audio_file)
    duration = int(video.duration)
    video = video.subclip(0,duration)
    video.audio = add_audio
    out_path = Path(os.getcwd()) / "video_out"
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    file_name = gen_video_with_audio_name(video_file, audio_file)
    out_file = out_path / file_name
    video.write_videofile(str(out_file))