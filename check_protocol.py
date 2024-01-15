import os
from pyannote.database import registry, FileFinder

registry.load_database("database.yml")
protocol = registry.get_protocol('Primock.SpeakerDiarization.full', preprocessors={"audio": FileFinder()})
for resource in protocol.test():
    print(list(resource.keys()))
    for k in ['uri', 'database', 'subset', 'scope', 'annotated', 'annotation', 'audio']:
        print(k, resource[k])
    print(os.path.isfile(resource["audio"]))
    break