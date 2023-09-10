import sqlite3

# 读取文件内容到列表
filename = "./stephen_king_adaptations.txt"
stephen_king_adaptations_list = []

try:
    with open(filename, "r") as file:
        content = file.read()
        stephen_king_adaptations_list = content.split('\n')
        
except FileNotFoundError:
    print(f"文件 '{filename}' 不存在。请确认文件名和路径是否正确。")
except IOError:
    print(f"读取文件 '{filename}' 时发生错误。")

# 建立与数据库的连接
database_name = "stephen_king_adaptations.db"
conn = sqlite3.connect(database_name)

table_name = "stephen_king_adaptations_table"
column_names = ["movieID", "movieName", "movieYear", "imdbRating"]
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_names)})"
conn.execute(create_table_query)

stephen_king_adaptations_list = [
    (1, "肖申克的救赎", 1994, 9.3),
    (2, "绿里奇迹", 1999, 8.6),
    (3, "闪灵", 1980, 8.4),
    (4, "病态", 1990, 7.8),
]
insert_data_query = f"INSERT INTO {table_name} (movieID, movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)"
conn.executemany(insert_data_query, stephen_king_adaptations_list)

def search_movie_by_name(conn, movie_name):
    query = f"SELECT * FROM stephen_king_adaptations_table WHERE movieName = '{movie_name}'"
    cursor = conn.execute(query)
    movie = cursor.fetchone()

    if movie:
        print("Movie Found:")
        print("Name:", movie[1])
        print("Year:", movie[2])
        print("Rating:", movie[3])
    else:
        print("No such movie exists in our database.")

def search_movie_by_year(conn, movie_year):
    query = f"SELECT * FROM stephen_king_adaptations_table WHERE movieYear = {movie_year}"
    cursor = conn.execute(query)
    movies = cursor.fetchall()

    if movies:
        print("Movies Found for Year", movie_year)
        for movie in movies:
            print("Name:", movie[1])
            print("Year:", movie[2])
            print("Rating:", movie[3])
    else:
        print("No movies were found for that year in our database.")

def search_movie_by_rating(conn, rating):
    query = f"SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= {rating}"
    cursor = conn.execute(query)
    movies = cursor.fetchall()

    if movies:
        print("Movies with Rating at or above", rating)
        for movie in movies:
            print("Name:", movie[1])
            print("Year:", movie[2])
            print("Rating:", movie[3])
    else:
        print("No movies at or above that rating were found in the database.")

# 建立与数据库的连接
conn = sqlite3.connect("stephen_king_adaptations.db")

choice = ""
while choice != "4":
    print("Options:")
    print("1. Search movie by name")
    print("2. Search movie by year")
    print("3. Search movie by rating")
    print("4. STOP")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        movie_name = input("Enter the movie name: ")
        search_movie_by_name(conn, movie_name)
    elif choice == "2":
        movie_year = input("Enter the movie year: ")
        search_movie_by_year(conn, movie_year)
    elif choice == "3":
        rating = input("Enter the minimum rating: ")
        search_movie_by_rating(conn, rating)
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")
# 提交更改
conn.commit()

# 关闭连接
conn.close()

