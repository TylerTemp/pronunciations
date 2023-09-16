import glob
import os
import subprocess
import urllib.parse
import mimetypes
import sys


def make_html(audio: str) -> str:
    (guess_type, _) = mimetypes.guess_type(audio)
    return """<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="minimum-scale=1,initial-scale=1,width=device-width,shrink-to-fit=no">
        <title>{title}</title>
        <style>
            html, body {{
                font-family: sans-serif;
            }}
        </style>
    </head>
    <body>
        <a href="{name}" target="_blank"><h1>{title}</h1></a>
        <audio controls autoplay>
        <source src="{name}" type="{guess_type}">
        Your browser does not support the audio element.
        </audio>

        <textarea></textarea>
    </body>
<html>
""".format(name=audio, guess_type=guess_type, title=os.path.splitext(audio)[0])

base_names = []

for each in glob.glob('*.mp3') + glob.glob('*.wav') + glob.glob('*.ogg'):
    # print(each)
    base_name, _ = os.path.splitext(each)
    base_names.append((base_name, os.stat(each)))
    # print(base_name)

    with open(f'{base_name}.html', 'w', encoding='utf-8') as f:
        f.write(make_html(each))

# subprocess.Popen([os.path.normpath(os.path.join(__file__, '..', 'up.bat'))], cwd=os.getcwd()).wait()
subprocess.Popen(['rsync'] + sys.argv[1:] + ['--progress', '*', 'tyler@notexists.top:static/pronunciations/'], cwd=os.getcwd(), shell=True).wait()
# subprocess.Popen('rsync --progress * tyler@notexists.top:static/pronunciations/', cwd=os.getcwd(), shell=True).wait()
subprocess.Popen(['ssh', 'tyler@notexists.top', 'bash', '~/static/pronunciations/permission.sh'], cwd=os.getcwd()).wait()

base_names.sort(key=lambda each: each[1])

history_file = '.history.txt'
open_mode = 'a+'
if not os.path.exists(history_file):
    open_mode = 'w+'


with open(history_file, open_mode, encoding='utf-8') as f:
    f.seek(0)
    old_contents = set(each.strip() for each in f.readlines())


    for (base_name, _) in base_names:
        if base_name in old_contents:
            continue

        old_contents.add(base_name)
        f.write(f'{base_name}\n')

        print(base_name)
        print(f'https://static.notexists.top/pronunciations/{urllib.parse.quote(base_name)}.html')
        print('')
