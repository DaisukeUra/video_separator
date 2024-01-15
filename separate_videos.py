import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment, silence
import math

def split_video(filename):
    audio = AudioSegment.from_file(filename)

    # 無音部を見つける
    silent_parts = silence.detect_silence(audio, min_silence_len=1000, silence_thresh=-32)
    silent_parts = [(math.ceil(start/1000), math.floor(stop/1000)) for start, stop in silent_parts] # convert to seconds

    # 分割点を見つける
    split_points = [0]
    for silent_start, silent_end in silent_parts:
        if silent_start - split_points[-1] > 1200: # 25 minutes
            split_points.append(silent_start)
    split_points.append(len(audio))

    # ビデオを分割する
    for i in range(len(split_points) - 1):
        start_time = split_points[i]
        end_time = split_points[i+1]
        ffmpeg_extract_subclip(filename, start_time, end_time, targetname=f"output{i}.mp4")

if __name__ == "__main__":
    split_video(sys.argv[1])

