#! /usr/bin/env python3

import sys
import getopt
from extractor import extractor


def main(argv):
    video_adress = ''
    save_location = ''
    skip_frames = ''
    try:
        opts, args = getopt.getopt(argv,"hv:l:f",["video_adress=","save_location=","skip_frames="])
    except getopt.GetoptError:
        print('video_stills.py -v <video_adress> -l <save_location> -f<skip_frames>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('IDA.py --video_adress=<video_adress> --save_location=<save_location> --skip_frames=<skip_frames>')
            sys.exit()
        elif opt in ("-v", "--video_adress"):
            video_adress = arg
        elif opt in ("-l", "--save_location"):
            save_location = arg
        elif opt in ("-f", "--skip_frames"):
            skip_frames = int(arg)

    extractor(video_adress,save_location,skip_frames)

if __name__ == "__main__":
    main(sys.argv[1:])
