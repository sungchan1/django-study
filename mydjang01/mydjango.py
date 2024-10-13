# mydjango.py
import sqlite3
import sys
import django
import requests
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path

settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
        }
    ],
)
django.setup()


def index(request: HttpRequest):
    query = request.GET.get("query", "").strip()
    song_list = get_song_list(query)


    return render(request, "index.html", {"song_list": song_list, "query": query})


def get_song_list(query: str):
    connection = sqlite3.connect('melon-20230906.sqlite3')
    cursor = connection.cursor()
    connection.set_trace_callback(print)

    if query:
        param = '%' + query + '%'
        sql = f"SELECT * FROM songs WHERE 가수 LIKE '{param}' OR 곡명 LIKE '{param}'"
        cursor.execute(sql)
    else:
        cursor.execute("SELECT * FROM songs")


    column_names = [desc[0] for desc in cursor.description]

    print("list size :", len(column_names))
    song_list = [dict(zip(column_names, song_tuple))
                 for song_tuple in cursor.fetchall()]

    connection.close()

    return song_list


urlpatterns = [
    path("", index),
]

execute_from_command_line(sys.argv)
