import pymysql
import sys
import os


def main(input):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='password', db='movielens')
    cur = conn.cursor()

    path = os.path.join(input, "u.item")
    with open(path, 'r') as fn:
        moives = fn.readlines()
        for m in moives:
            sql = "insert into movie (movieid, title, release_date, v_release_date, url, movie_type) \
                   values (%s, %s, %s, %s, %s, %s)"
            minfo = m.split('|', 5)
            cur.execute(sql, minfo)
            conn.commit()

    path = os.path.join(input, "u.user")
    with open(path, 'r') as fn:
        moives = fn.readlines()
        count = 0
        for m in moives:
            sql = "insert into trainuser (tid, age, gender, occupation, zipcode) \
                   values (%s, %s, %s, %s, %s)"
            tinfo = m.split('|')
            cur.execute(sql, tinfo)
            conn.commit()

    path = os.path.join(input, "u.data")
    with open(path, 'r') as fn:
        moives = fn.readlines()
        count = 0
        for m in moives:
            sql = "insert into traindata (userid, movieid, rating, timestamp) \
                   values (%s, %s, %s, %s)"
            dinfo = m.split('\t')
            cur.execute(sql, dinfo)
            count += 1
            if count % 100 == 0:
                conn.commit()
        conn.commit()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()
    main(sys.argv[1])
