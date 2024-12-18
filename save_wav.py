import subprocess
from datetime import timedelta

def extract_audio_by_milliseconds(input_video, start_ms, end_ms, output_audio):
  """Extracts audio from a video within a specified millisecond range.

  Args:
    input_video: Path to the input video file.
    start_ms: Start time in milliseconds.
    end_ms: End time in milliseconds.
    output_audio: Path to the output audio file.
  """

  # Convert milliseconds to HH:MM:SS.mmm format
  start_time = str(timedelta(milliseconds=start_ms))
  end_time = str(timedelta(milliseconds=end_ms))

  command = f"ffmpeg -i {input_video} -ss {start_time} -t {end_time} -ar 16000 {output_audio} "
  subprocess.call(command, shell=True)

# extract_audio_by_milliseconds(video_file, start_millisecond, end_millisecond, audio_file)