# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.cluster import KMeans
import sqlite3

def clasificaGenre():
    result = {}
    value = 0
    conn= sqlite3.connect('principal.db')
    genres = conn.execute("""select distinct genre from principal_game""")
    for row in genres:
        result[row[0]]=value
        value += 1
    conn.commit()
    conn.close()
    return result

def clasificaDeveloper():
    result = {}
    value = 0
    conn= sqlite3.connect('principal.db')
    developers = conn.execute("""select distinct developer from principal_game""")
    for row in developers:
        if row[0] == '':
            result[0]=value
        else:
            result[row[0]]=value
        value += 1
    conn.commit()
    conn.close()
    return result

def clasificaPlatform():
    result = {}
    value = 0
    conn= sqlite3.connect('principal.db')
    platforms = conn.execute("""select distinct platform from principal_game""")
    for row in platforms:
        if row[0] == '':
            result[0]=value
        else:
            result[row[0]]=value
        value += 1
    conn.commit()
    conn.close()
    return result

def clasificaPublisher():
    result = {}
    value = 0
    conn= sqlite3.connect('principal.db')
    publishers = conn.execute("""select distinct publisher from principal_game""")
    for row in publishers:
        if row[0] == 'N/A':
            result[0]=value
        else:
            result[row[0]]=value
        value += 1
    conn.commit()
    conn.close()
    return result

def clasificaRating():
    result = {}
    value = 0
    conn= sqlite3.connect('principal.db')
    ratings = conn.execute("""select distinct rating from principal_game""")
    for row in ratings:
        if row[0] == 'N/A' or row[0] == '' :
            result[0]=value
        else:
            result[row[0]]=value
        value += 1
    conn.commit()
    conn.close()
    return result

def clasificarJuegos():
    mapGenre = clasificaGenre()
    mapDeveloper = clasificaDeveloper()
    mapPublisher = clasificaPublisher()

    games = pd.read_csv('Video_Games_Sales_as_at_30_Nov_2016.csv', sep=',')
    games = games.fillna(0)

    data = pd.DataFrame()
    values_genre = []
    values_developer= []
    values_publisher = []


    for k in games.iterrows():
        genre = k[1]['genre']
        developer = k[1]['developer']
        publisher = k[1]['publisher']

        value = mapGenre[genre]
        values_genre.append(value)
        value = mapDeveloper[developer]
        values_developer.append(value)
        value = mapPublisher[publisher]
        values_publisher.append(value)

    data['genre'] = values_genre
    data['publisher'] = values_publisher
    data['critic_Score'] = games['critic_Score']
    data['user_Score'] = games['user_Score']
    data['developer'] = values_developer

    kmeans = KMeans(n_clusters=100)
    cluster = kmeans.fit_predict(data.ix[:, :-1].values)

    data['cluster'] = cluster
    data.to_csv('cluster.csv')

def main():
    clasificarJuegos()

if __name__ == "__main__":
    main()

