import sqlite3

query = "악뮤"

print("검색어", query)

connection = sqlite3.connect('melon-20230906.sqlite3')
cursor = connection.cursor()
connection.set_trace_callback(print)


param = '%' + query + '%'
sql = f"SELECT * FROM songs WHERE 가수 LIKE '{param}' OR 곡명 LIKE '{param}'"
cursor.execute(sql)


# cursor.execute("SELECT * FROM songs")

column_names = [desc[0] for desc in cursor.description]

print("list size :", len(column_names))




song_list = cursor.fetchall()



for song_tuple in song_list:
    song_dict = dict(zip(column_names, song_tuple))
    print("{곡명} {가수}".format(**song_dict))


connection.close()





