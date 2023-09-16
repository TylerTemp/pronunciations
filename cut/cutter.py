from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import glob
import subprocess

cwd = os.path.dirname(__file__)
os.chdir(cwd)

for wav in glob.glob('*.wav'):
    os.remove(wav)

for mp3 in glob.glob('*.mp3'):
    base_name, _ = os.path.splitext(mp3)
    wav = f'{base_name}.wav'
    
    subprocess.Popen(['ffmpeg', '-i', mp3, '-acodec', 'pcm_u8', '-ar', '22050', wav]).communicate()

    sound_file = AudioSegment.from_wav(wav)
    audio_chunks = split_on_silence(sound_file, 
        # must be silent for at least half a second
        min_silence_len=30,

        # consider it silent if quieter than -16 dBFS
        silence_thresh=-15
    )

    print(len(audio_chunks))

    for i, chunk in enumerate(audio_chunks):
        out_file = f"{base_name}_{i}.wav"
        print("exporting", out_file)
        chunk.export(out_file, format="wav")
