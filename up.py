import glob
import os
import subprocess
import urllib.parse
import mimetypes


def make_html(audio: str) -> str:
    (guess_type, _) = mimetypes.guess_type(audio)
    return """<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="minimum-scale=1,initial-scale=1,width=device-width,shrink-to-fit=no">
        <title>{title}</title>
    </head>
    <body>
        <a href="{name}" target="_blank"><h1>{title}</h1></a>
        <audio controls loop autoplay>
        <source src="{name}" type="{guess_type}">
        Your browser does not support the audio element.
        </audio> 
    </body>
<html>
""".format(name=audio, guess_type=guess_type, title=os.path.splitext(audio)[0])

base_names = []

for each in glob.glob('*.mp3') + glob.glob('*.wav'):
    # print(each)
    base_name, _ = os.path.splitext(each)
    base_names.append((base_name, os.stat(each)))
    # print(base_name)

    with open(f'{base_name}.html', 'w', encoding='utf-8') as f:
        f.write(make_html(each))

subprocess.Popen([os.path.normpath(os.path.join(__file__, '..', 'up.bat'))], cwd=os.getcwd()).wait()

base_names.sort(key=lambda each: each[1])

for (base_name, _) in base_names:
    print(base_name)
    print(f'https://static.notexists.top/pronunciations/{urllib.parse.quote(base_name)}.html')
    print('')
