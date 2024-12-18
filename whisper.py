import subprocess

def save_subt():
    s = subprocess.run("main -m ggml-model-whisper-small.en.bin -t 4 -osrt -f test.wav")