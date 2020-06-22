import os, natsort
from pathlib import Path
from moviepy.editor import *





def main(input_path, out_file_name):

    video_files = os.listdir(input_path)
    current_dir = Path(os.getcwd()) / input_path
    files_sorted = natsort.natsorted(video_files)

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

    # print("The file in merged in " + str(out_file))