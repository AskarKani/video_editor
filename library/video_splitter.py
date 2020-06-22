from moviepy.editor import *
import math
from pathlib import Path


def gen_file_name(index, file_path):
    if len(file_path.split("\\")) > 1:
        file_name = str(index) + "_" + str(file_path.split("\\")[-1])
    elif len(file_path.split("/")) > 1:
        file_name = str(index) + "_" + str(file_path.split("/")[-1])
    else:
        file_name = str(index) + "_" + str(file_path)
    return file_name


def main(video_file, subclip_duration):
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
