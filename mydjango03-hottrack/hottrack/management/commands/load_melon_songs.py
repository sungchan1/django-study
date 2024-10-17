import json
from urllib.request import urlopen

from django.core.management import BaseCommand

from ...models import Song


class Command(BaseCommand):
    help = "Load songs from melon chart"

    def handle(self, *args, **options):
        melon_chart_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230910.json"
        json_string = urlopen(melon_chart_url).read().decode("utf-8")

        song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]
        print(f"loaded song_list : {len(song_list)}")

        Song.objects.bulk_create(song_list, batch_size=100, ignore_conflicts=True)

        total = Song.objects.all().count()
        print(f"saved song_list : {total}")
