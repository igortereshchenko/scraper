import json
import copy


class FileWriter:

    def __init__(self, filepath):
        self.filepath = filepath


    def write(self, dictionary):
        with open(self.filepath, mode='a+') as file:
            for url in dictionary:
                # TODO delete shallow copy
                data = copy.copy(dictionary[url])

                data['date'] = data['date'].strftime("%d/%m/%Y %H:%M:%S")

                json.dump(data, file)

                file.write("\n")

            file.flush()
