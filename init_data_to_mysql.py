from conf import env
import os
import pymysql
import sys


def main(input):
    conn = pymysql.connect(host=env.MYSQL_SERVER,
                           port=3306,
                           user=env.MYSQL_ACCOUNT,
                           passwd=env.MYSQL_PASSWORD,
                           db='movielens')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    """
    import movielens data into mysql
    u.item: movie info
    u.user: training user info
    u.data: training data
    """

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
    """
    by training data, add some hot movies into db for new user
    rule: need 10% of total training user rated the movie with 4 or higher
          sort these avg rating and get top 200
    """
    sql = 'select count(tid) as count from trainuser where 1'
    cur.execute(sql)
    result = cur.fetchall()[0]
    limit = result.get('count', 1000) / 10
    sql = 'select movieid, avg(rating) as rating, count(*) as count FROM traindata \
           where (rating >= 4) group by movieid having count > {} \
           order by rating desc limit 200'.format(limit)
    cur.execute(sql)
    conn.commit()
    movies_for_new = cur.fetchall()
    for result in movies_for_new:
        sql = 'insert into recommendation_for_new_user (movieid, rating) values ({}, {})'
        sql = sql.format(result['movieid'], result['rating'])
        cur.execute(sql)
    conn.commit()
    """
    add other movies into db with rating = 1
    """
    sql = 'insert ignore into recommendation_for_new_user (movieid, rating) \
          (select movieid, 1 from movie)'
    cur.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()
    main(sys.argv[1])
