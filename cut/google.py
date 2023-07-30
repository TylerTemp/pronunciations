import json
import base64
import os

file_path = os.path.normpath(os.path.join(__file__, '..', 'google.json'))

with open(file_path, 'r', encoding='utf-8') as f:
    # lines = f.readlines()
    for line in f:
        try:
            content = json.loads(line)
        except json.decoder.JSONDecodeError:
            continue
        else:
            if not isinstance(content, list):
                continue
            if len(content) != 1:
                continue

            inner_content = content[0]
            if len(inner_content) < 3:
                continue

            b64_value = json.loads(inner_content[2])[0]
            print(b64_value)
            b64_dec = base64.b64decode(b64_value)
            # print(b64_dec)

            with open('google.mp3', 'wb') as f:
                f.write(b64_dec)
            break
