from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import json
from pathlib import Path
from bracket.models import YtVid


class Command(BaseCommand):
    help = """refreshes the database to have all the info.json files loaded
    
            takes path containing jsons as an argument """

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str, help="path that will be searched for info jsons from the youtube-dl --write-json option and loaded to the django DB")
    
    @transaction.atomic
    def handle(self, *args, **options):
        jsonDir = Path(options['path'][0])
        print(f"got path {jsonDir} to look for info.json files downloaded with youtube-dl")
        jsons = [x for x in jsonDir.iterdir() if x.name.endswith('info.json')]
        print(f"got {len(jsons)} files to load to database")
        for cnt, j in enumerate(jsons):
            with open(j) as j:
                """
                {'dislike_count': 23,
                'duration': 566,
                'like_count': 12,
                'thumbnail': 'https://i.ytimg.com/vi_webp/-GCPUBayK7E/maxresdefault.webp',
                'title': 'painting a wand',
                'webpage_url': 'https://www.youtube.com/watch?v=-GCPUBayK7E'}
                """
                ytInfo = json.load(j)    
            keepAttrs= ['uploader_url',
                        'id',
                        'title',
                        'thumbnail',
                        'like_count',
                        'dislike_count',
                        'view_count',
                        'duration',
                        'webpage_url',
                        'upload_date',
                        ]
            mappedAttrs = {
                'uploader_url':'ytChannel',
                'id':'ytid',
            }
            mappedVals = {
                'upload_date':lambda x:x[:4] + '-' + x[4:6] + '-' + x[6:]
            }
            newDict = {}
            for k,v in ytInfo.items():
                if k not in keepAttrs:
                    continue
                key = mappedAttrs.get(k,k)
                valueMapFunc = mappedVals.get(k)
                if valueMapFunc:
                    v = valueMapFunc(v)
                else:
                    v = v
                newDict[key] = v
            ytInfo = newDict

            #ytInfo = {mappedAttrs.get(k,k):if mappedVals.get(k) else v for k,v in ytInfo.items() if k in keepAttrs}
            if cnt == 1 or cnt % 100 == 0:
                print(f"loaded {cnt} files, currently on {j.name}")
               # print(f"kwargs for YtVid = {ytInfo}")

            vid = YtVid(**ytInfo)
            vid.save()
        print(f"updated DB with {YtVid.objects.count()} new videos")