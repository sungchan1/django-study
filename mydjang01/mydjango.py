# mydjango.py
import sqlite3
import sys
import django
import requests
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.db.models import Q

# from django.db import connection
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path

settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "melon-20230906.sqlite3",

        },
    },
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
        }
    ],
)
django.setup()


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    가수 = models.CharField(max_length=100)
    곡명 = models.CharField(max_length=200)
    곡일련번호 = models.IntegerField()
    순위 = models.IntegerField()
    앨범 = models.CharField(max_length=200)
    좋아요 = models.IntegerField()
    커버이미지_주소 = models.URLField()

    class Meta:
        db_table = "songs"
        app_label = "melon"


def index(request: HttpRequest):
    query = request.GET.get("query", "").strip()
    # song_list = get_song_list(query)

    song_list = Song.objects.all()
    if query:
        song_list = song_list.filter(
            Q(곡명__icontains=query) | Q(가수__icontains=query)  # 포함이 되었다면
        )
    return render(request, "index.html", {"song_list": song_list, "query": query})


# def get_song_list(query: str):
#     # connection = sqlite3.connect('melon-20230906.sqlite3')
#     cursor = connection.cursor()
#     # connection.set_trace_callback(print)
#
#     if query:
#         param = '%' + query + '%'
#         sql = f"SELECT * FROM songs WHERE 가수 LIKE '{param}' OR 곡명 LIKE '{param}'"
#         cursor.execute(sql)
#     else:
#         cursor.execute("SELECT * FROM songs")
#
#
#     column_names = [desc[0] for desc in cursor.description]
#
#     print("list size :", len(column_names))
#     song_list = [dict(zip(column_names, song_tuple))
#                  for song_tuple in cursor.fetchall()]
#
#     # connection.close()
#
#     return song_list


urlpatterns = [
    path("", index),
]

execute_from_command_line(sys.argv)
