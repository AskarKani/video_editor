import argparse, sys, os
import datetime


if __name__ == '__main__':
    if sys.version_info[0] < 3:
        print("!!!WARNING!!! RUN with PYTHON 3...")
        sys.exit(1)

    from library.audio_editor import audio_extract as audio_extract
    from library.audio_editor import concatenate_audio
    from library.audio_editor import audio_cutter
    from library.video_editor import add_audio_to_video
    from library.video_editor import splitter as video_splitter
    from library.video_editor import merger as video_merger

    import library.clean as clean

    des = "!........................! VIDEO EDITOR !........................!\n " \
          "\rpython run.py -s -b split duration in seconds file(split video)\n " \
          "\rpython run.py -m -i folder_path(splitted videos) - o out_file_name(merge video)\n" \
          "\rpython run.py -e -i video_file (extract audio from video)\n" \
          "\rpython run.py -a -i video_file -o audio_file(Add audio to video file)\n" \
          "\rpython run.py -audiocut -i start_second -o end_second file(Cut the Audio file)\n" \
          "\rpython run.py -ca -files (concatenate audio files)\n" \
          "python run.py -clean"
    parser = argparse.ArgumentParser(description=des, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-b', metavar='split duration in seconds', type=int)
    parser.add_argument('-s', action="store_true", default=False, help='to split')
    parser.add_argument('-m', action="store_true", default=False, help='to merge')
    parser.add_argument('-i', action="store", metavar='input_path', help='folder_path(contains split videos)')
    parser.add_argument('-o', action="store", metavar='merge_outfile_name', help='merge_file_name')
    parser.add_argument('-clean', action="store_true", default=False, help='clean the split and merge output folder')
    parser.add_argument('-e', action="store_true", default=False, help='extract audio from video file')
    parser.add_argument('-a', action="store_true", default=False, help='add audio to video file')
    parser.add_argument('-ca', action="store_true", default=False, help='concatenate audio files')
    parser.add_argument('-audiocut', action="store_true", default=False, help='cut the audio file')
    parser.add_argument('-files', nargs='+', type=str, help='pass the files as list')
    parser.add_argument('file', nargs='?')
    arg = parser.parse_args()

    # check for any functionality
    operations = [arg.e, arg.a, arg.ca, arg.s, arg.m, arg.clean, arg.audiocut]
    operation_count = [True for _ in operations if _]
    if len(operation_count) == 0 or len(operation_count) > 1:
        print("PASS valid argument".center(40, "!"))
        print(parser.print_help())
        sys.exit(1)

    print("!!.........................! VIDEO EDITOR !.........................!!")
    # clean
    if arg.clean:
        clean.clean()
        sys.exit(1)

    # extract audio from video
    if arg.e:
        if not arg.i:
            print("\nPass the input video file with -i option")
            sys.exit(1)
        if not os.path.isfile(arg.i):
            print("\n" + str(arg.i) + " is not a valid path")
            sys.exit(1)
        audio_extract(arg.i)
        sys.exit(1)

    # add audio to video
    if arg.a:
        if not arg.i:
            print("\nPass the input video file with -i option")
            sys.exit(1)
        if not os.path.isfile(arg.i):
            print("\n" + str(arg.i) + " is not a valid path")
            sys.exit(1)
        if not arg.o:
            print("\nPass the input audio file with -o option")
            sys.exit(1)
        if not os.path.isfile(arg.o):
            print("\n" + str(arg.o) + " is not a valid path")
            sys.exit(1)
        add_audio_to_video(arg.i, arg.o)
        sys.exit(1)

    # concatenate_audio
    if arg.ca:
        if not arg.files:
            print("\nPass the input audio files with -files option")
            sys.exit(1)
        concatenate_audio(arg.files)
        sys.exit(1)

    # audiocut
    if arg.audiocut:
        arguments = [arg.i, arg.o]
        pass_strs = ["start -i".split(), "end -o".split()]
        for argument, pass_str in zip(arguments, pass_strs):
            if not argument:
                print(f"\nPass the {pass_str[0]} second with {pass_str[1]} option")
                sys.exit(1)
            try:
                if "start" in pass_str:
                    start = float(argument)
                elif "end" in pass_str:
                    end = float(argument)
            except ValueError:
                print("Enter the valid " + str(pass_str[0])+ " second")
                sys.exit(1)
        if not arg.file:
            print("\nPass file for audio cutting..")
            sys.exit(1)
        if not os.path.isfile(arg.file):
            print(str(arg.file) + " is not a valid file path")
            sys.exit(1)
        print(start, end)
        audio_cutter(arg.file, arg.i, arg.o)
        sys.exit(1)

    # video splitter
    if arg.s:
        if not arg.file:
            print("\nPass video_file for splitting..")
            sys.exit(1)
        if not os.path.isfile(arg.file):
            print(str(arg.file) + " is not a valid file path")
            sys.exit(1)
        print("!!.........................! VIDEO SPLITTER !.........................!!")
        if not arg.b:
            arg.b = int(input("Enter the duration of subclip in seconds : "))
        print("\nSplittig the file " + str(arg.file) + " with duration : " + str(arg.b) + " seconds")
        video_splitter(arg.file, arg.b)

    # video merger
    if arg.m:
        print("!!.........................! VIDEO MERGER !.........................!!")
        if not arg.i:
            print("\nPass the folder path which contains the splitted videos with -i option")
            sys.exit(1)
        if not os.path.isdir(arg.i):
            print("\n" + str(arg.i) + " is not a valid folder path")
            sys.exit(1)
        if not arg.o:
            out_file_name = input("\nEnter the output file name.... ")
        else:
            out_file_name = arg.o
        print("\nMerging the files from " + str(arg.i) + " folder to " + str(out_file_name))
        video_merger(arg.i, out_file_name)