import argparse, sys, os



if __name__ == '__main__':
    if sys.version_info[0] < 3:
        print("!!!WARNING!!! RUN with PYTHON 3...")
        sys.exit(1)
    import lib.video_splitter as splitter
    import lib.video_merger as merger
    import lib.clean as clean

    des = "!........................! VIDEO EDITOR !........................!\n " \
          "\rpython run.py -s -b split duration in seconds video_file\n" \
          "\rpython run.py -m  -i folder_path(splitted videos) - o out_file_name\n" \
          "python run.py -clean"
    parser = argparse.ArgumentParser(description=des, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-b', metavar='split duration in seconds', type=int)
    parser.add_argument('-s', action="store_true", default=False, help='to split')
    parser.add_argument('-m', action="store_true", default=False, help='to merge')
    parser.add_argument('-i', action="store", metavar='input_path', help='folder_path(contains split videos)')
    parser.add_argument('-o', action="store", metavar='merge_outfile_name', help='merge_file_name')
    parser.add_argument('-clean', action="store_true", default=False, help='clean the split and merge output folder')
    parser.add_argument('video_file', nargs='?')
    arg = parser.parse_args()
    if arg.clean:
        clean.clean()
        sys.exit(1)
    result = [arg.s, arg.m]
    count_s_m = [0 for _ in result if _]
    if count_s_m.count(0) == 2:
        print("pass only one argument")
        sys.exit(1)
    if count_s_m.count(0) == 0:
        print("pass any argument")
        sys.exit(1)

    if arg.s:
        if not arg.video_file:
            print("\nPass video_file for splitting..")
            sys.exit(1)
        if not os.path.isfile(arg.video_file):
            print(str(arg.video_file) + " is not a valid file path")
            sys.exit(1)
        print("!!.........................! VIDEO SPLITTER !.........................!!")
        if not arg.b:
            arg.b = int(input("Enter the duration of subclip in seconds : "))
        print("\nSplittig the file " + str(arg.video_file) + " with duration : " + str(arg.b) + " seconds")
        splitter.main(arg.video_file, arg.b)
    elif arg.m:
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
        merger.main(arg.i, out_file_name)