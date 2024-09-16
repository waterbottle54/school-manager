import json

class JsonStream:

    file_path: str

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, '+a') as file:
            file.seek(0)
            text = file.read()
            if len(text) == 0:
                return None
            return json.loads(text)

    def write(self, object):
        with open(self.file_path, 'w') as file:
            file.write(json.dumps(object))
