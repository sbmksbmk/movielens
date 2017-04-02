import json
from flask import Response
from flask import Flask
from flask import request
from sqlalchemy import create_engine, text
from cf.recommendation import movie_train
import random
import time

app = Flask(__name__)
_DB_ENGINE = None
TRAIN = None
MOVIE_INFO = None


def _init_db():
    global _DB_ENGINE
    if _DB_ENGINE is None:
        conn_fmt = "mysql+pymysql://{}:{}@{}/movielens"
        conn_str = conn_fmt.format(
            'root', 'password', 'localhost'
        )
        _DB_ENGINE = create_engine(
            conn_str,
            max_overflow=5,
            pool_size=20,
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

    sql = "select movieid, title, url from movie"
    result, conn = _db_query(sql=sql)
    res = result.fetchall()
    result.close()
    for row in res:
        try:
            MOVIE_INFO[row['movieid']] = {'title': row['title'].decode('utf-8'), 'url': row['url'], 'movieid': row['movieid']}
        except:
            MOVIE_INFO[row['movieid']] = {'title': row['title'].decode('latin-1').encode('utf-8'),
                                          'url': row['url'],
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
        return_max = request.args['return_max']
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
            return_max = request.args['return_max']
        else:
            return_max = 100
        ret = []
        rec_movies = TRAIN.get_recommendation(userdata=rating, return_max=return_max, limit=0)
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
                        'rating': row['rating']})
        result.close()
        status = 200
    try:
        conn.close()
    except:
        pass
    return Response(json.dumps(ret), status=status)

_init_db()
_init_training()

if __name__ == '__main__':
    _init_db()
    _init_training()
    app.run(debug=True)
