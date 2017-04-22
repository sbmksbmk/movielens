# -*- coding: utf-8 -*-
from cf.recommendation import movie_train
from imdb_parser import get_movie_extra_infomation as EXTRA_INFO

from flask import Response
from flask import Flask
from flask import request
import json
import random
from sqlalchemy import create_engine, text
import sys
import time
import threading

app = Flask(__name__)
_DB_ENGINE = None
TRAIN = None
MOVIE_INFO = None
POSTER_THREAD = None

reload(sys)
sys.setdefaultencoding('utf8')


def _init_db():
    global _DB_ENGINE
    if _DB_ENGINE is None:
        conn_fmt = "mysql+pymysql://{}:{}@{}/movielens"
        conn_str = conn_fmt.format(
            'root', 'password', '172.17.0.1'
        )
        _DB_ENGINE = create_engine(
            conn_str,
            max_overflow=5,
            pool_size=20,
            pool_timeout=10,
            pool_recycle=5
        )


def _db_query(sql, keys={}):
    global _DB_ENGINE
    if _DB_ENGINE is None:
        _init_db()
    conn = _DB_ENGINE.connect()
    db_retry = 5
    retry_count = 0
    result = None
    while retry_count < db_retry:
        try:
            result = conn.execute(
                text(sql),
                **keys)
            break
        except Exception as e:
            print e
            time.sleep(random.random() / 2)
            retry_count += 1
    return result, conn


def _init_training():
    global TRAIN, MOVIE_INFO
    TRAIN = movie_train()
    MOVIE_INFO = {}
    sql = "select userid, movieid, rating from traindata where 1"
    result, conn = _db_query(sql=sql)
    training_data = {}
    res = result.fetchall()
    result.close()
    for row in res:
        try:
            training_data[row['userid']][row['movieid']] = float(row['rating'])
        except:
            training_data[row['userid']] = {row['movieid']: float(row['rating'])}
    TRAIN.load(training_data=training_data)
    try:
        conn.close()
    except:
        pass

    sql = "select movieid, title, url, poster, description, movie_type from movie"
    result, conn = _db_query(sql=sql)
    res = result.fetchall()
    result.close()
    for row in res:
        poster = '/img/image_not_found.png'
        description = 'No information or still in retrieving...'
        movie_type = _movie_types(row['movie_type'].strip())
        if row['poster'] is not None:
            poster = row['poster']
        if row['description'] is not None:
            description = row['description']
        try:
            MOVIE_INFO[row['movieid']] = {'title': row['title'].decode('utf-8'),
                                          'url': row['url'],
                                          'poster': poster,
                                          'description': description,
                                          'movie_type': movie_type,
                                          'movieid': row['movieid']}
        except:
            MOVIE_INFO[row['movieid']] = {'title': row['title'].decode('latin-1').encode('utf-8'),
                                          'url': row['url'],
                                          'poster': poster,
                                          'description': description,
                                          'movie_type': movie_type,
                                          'movieid': row['movieid']}
    try:
        conn.close()
    except:
        pass


@app.errorhandler(404)
def not_found(error):
    return Response(json.dumps({'error': 'Not found'}), 404)


@app.route('/')
def index():
    msg = {'msg': 'test index message'}
    return Response(json.dumps(msg), status=200)


@app.route('/rating_rec/<member_id>', methods=["GET"])
def rating_rec(member_id):
    # need user account
    global TRAIN, MOVIE_INFO
    ret = []
    status = 400
    # get all rating data, should be at least one record
    sql = "select movieid, rating from member_rating where member_id=:member_id"
    keys = {"member_id": member_id}
    result, conn = _db_query(sql=sql, keys=keys)
    if request.args.get('return_max', None) is not None:
        return_max = int(request.args['return_max'])
    else:
        return_max = 100
    rating = {}
    if result is not None:
        res = result.fetchall()
        for row in res:
            rating[row['movieid']] = float(row['rating'])
        result.close()
        rec_movies = TRAIN.get_recommendation(userdata=rating, return_max=return_max, limit=0.3)
        for movieid, rec_rating in rec_movies:
            movie = MOVIE_INFO[movieid]
            movie['rating'] = rec_rating
            ret.append(movie)
        status = 200
    try:
        conn.close()
    except:
        pass
    return Response(json.dumps(ret), status=status)


@app.route('/rating_rec_guest', methods=["POST"])
def rating_rec_guest():
    # need user account
    global TRAIN, MOVIE_INFO
    rating = {}
    for k, v in request.form.items():
        rating[int(k)] = float(v)
    if len(rating) == 0:
        return nonrate_rec()
    else:
        if request.args.get('return_max', None) is not None:
            return_max = int(request.args['return_max'])
        else:
            return_max = 100
        ret = []
        rec_movies = TRAIN.get_recommendation(userdata=rating, return_max=return_max, limit=0)
        # print rec_movies
        for movieid, rec_rating in rec_movies:
            movie = MOVIE_INFO[movieid]
            movie['rating'] = rec_rating
            ret.append(movie)
        return Response(json.dumps(ret), status=200)


@app.route('/nonrate_rec', methods=["GET"])
def nonrate_rec():
    global MOVIE_INFO
    status = 400
    ret = []
    # get pre-process recommendation for guest and member who never rated
    sql = "select movieid, rating from recommendation_for_new_user order by rating desc"
    result, conn = _db_query(sql=sql)
    if result is not None:
        res = result.fetchall()
        for row in res:
            ret.append({'movieid': row['movieid'],
                        'title': MOVIE_INFO[row['movieid']]['title'],
                        'url': MOVIE_INFO[row['movieid']]['url'],
                        'poster': MOVIE_INFO[row['movieid']]['poster'],
                        'description': MOVIE_INFO[row['movieid']]['description'],
                        'movie_type': MOVIE_INFO[row['movieid']]['movie_type'],
                        'rating': row['rating']})
        result.close()
        status = 200
    try:
        conn.close()
    except:
        pass
    return Response(json.dumps(ret), status=status)


@app.route('/update_poster', methods=["POST"])
def update_poster():
    # not to block init service, update poster info in thread
    global POSTER_THREAD
    try:
        if POSTER_THREAD is None or POSTER_THREAD.is_alive() is False:
            POSTER_THREAD = threading.Thread(target=_movie_poster_retrieve)
            POSTER_THREAD.start()
    except:
        pass


def _movie_poster_retrieve():
    global MOVIE_INFO
    sql = "select movieid, url from movie where poster is NULL"
    movies, movies_conn = _db_query(sql=sql)
    if movies is not None:
        movie_list = movies.fetchall()
        # could get poster in multi-thread to enhance performance
        # but it may be banned if do it in multi-trhead
        for movie in movie_list:
            url = movie['url']
            movieid = movie['movieid']
            poster, description = EXTRA_INFO(url)
            MOVIE_INFO[movieid]['poster'] = poster
            MOVIE_INFO[movieid]['description'] = description
            sql = "update movie set poster=:poster, description=:description where movieid={}".format(movieid)
            keys = {"poster": poster, "description": description}
            result, conn = _db_query(sql=sql, keys=keys)
            try:
                conn.close()
            except:
                pass
    try:
        movies_conn.close()
    except:
        pass
    return Response("Done", status=200)


def _movie_types(movie_type=None):
    all_types =['Action',
                'Adventure',
                'Animation',
                'Children\'s',
                'Comedy',
                'Crime',
                'Documentary',
                'Drama',
                'Fantasy',
                'Film-Noir',
                'Horror',
                'Musical',
                'Mystery',
                'Romance',
                'Sci-Fi',
                'Thriller',
                'War',
                'Western',
                '(no genres listed)']
    if movie_type is None or movie_type == "":
        return all_types[-1]
    sp = movie_type.split('|')
    TYPE = ""
    for i in range(len(sp)):
        try:
            if sp[i] == '1':
                TYPE += all_types[i] + ", "
        except:
            break
    if len(TYPE) == 0:
        return all_types[-1]
    else:
        # remove tail ", "
        return TYPE[:-2]

_init_db()
_init_training()
update_poster()

if __name__ == '__main__':
    _init_db()
    _init_training()
    app.run(debug=True)
