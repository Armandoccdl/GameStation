# -*- coding: utf-8 -*-

import sqlite3

def populateJuego():
    tmp = 0
    conn = sqlite3.connect('principal.db')
    conn.execute("""DELETE FROM principal_game""")
    conn.text_factory = str
    games = open('tools/Video_Games_Sales_as_at_30_Nov_2016.csv', 'r')
    for row in games:
        if tmp == 0:
            tmp += 1
        else:
            game = row.split(',')
            conn.execute("""INSERT INTO principal_game (name,platform,year_of_Release,genre,publisher,na_Sales,eu_Sales,jp_Sales,other_Sales,global_Sales,critic_Score,user_Score,developer,rating) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                         (game[1],game[2],game[3],game[4],game[5],game[6],game[7],game[8],game[9],game[10],game[11],game[12],game[13],game[14]))
    conn.commit()
    conn.close()

def populateCluster():
    tmp = 0
    conn = sqlite3.connect('principal.db')
    conn.execute("""DELETE FROM principal_cluster""")
    conn.text_factory = str
    clusters = open('tools/cluster.csv', 'r')
    for row in clusters:
        if tmp == 0:
            tmp += 1
        else:
            game = row.split(',')
            numCluster = int(game[0])+1
            conn.execute("""INSERT INTO principal_cluster (numCluster,game_id) VALUES (?,?)""",
                         (game[3], numCluster))
    conn.commit()
    conn.close()

def main():
    populateJuego()
    populateCluster()

if __name__ == "__main__":
    main()