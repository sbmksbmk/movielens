import pymysql
import json
from flask import Response
from flask import Flask
from flask import request
from flask import session
from sqlalchemy import create_engine, text
from cf.recommendation import sbmk_train, movie_train

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
            max_overflow=10,
            pool_size=20,
        )

def _init_training():
    global TRAIN, MOVIE_INFO
    TRAIN = movie_train()
    MOVIE_INFO = {}
    global _DB_ENGINE
    if _DB_ENGINE is None:
        _init_db()

    conn = _DB_ENGINE.connect()
    sql = "select userid, movieid, rating from traindata where 1"
    result = conn.execute(
            text(sql),
            )
    training_data = {}
    res = result.fetchall()
    result.close()
    for row in res:
        try:
            training_data[row['userid']][row['movieid']] = float(row['rating'])
        except:
            training_data[row['userid']] = {row['movieid']: float(row['rating'])}
    TRAIN.load(training_data=training_data)

    sql = "select movieid, title, url from movie"
    result = conn.execute(
            text(sql),
            )
    res = result.fetchall()
    result.close()
    for row in res:
        MOVIE_INFO[row['movieid']] = {'title': row['title'], 'url': row['url'], 'movieid': row['movieid']}
    conn.close()

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
    global _DB_ENGINE, TRAIN, MOVIE_INFO
    if _DB_ENGINE is None:
        # print "_DB_ENGINE is None"
        _init_db()
        # print _DB_ENGINE
    conn = _DB_ENGINE.connect()
    ret = []
    status = 400
    # get all rating data, should be at least one record
    sql = "select movieid, rating from member_rating where member_id=:member_id"
    result = conn.execute(
            text(sql),
            member_id=member_id,
            )
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
    conn.close()
    return Response(json.dumps(ret), status=status)

@app.route('/nonrate_rec', methods=["GET"])
def nonrate_rec():
    global _DB_ENGINE, MOVIE_INFO
    if _DB_ENGINE is None:
        # print "_DB_ENGINE is None"
        _init_db()
        print _DB_ENGINE
    """
    if request.args.get('test', None) is not None:
        print request.args.get('test')
    """
    status = 400
    conn = _DB_ENGINE.connect()
    ret = []
    # get pre-process recommendation for guest and member who never rated
    sql = "select m.movieid as movieid, m.title as title, r.rating as rating, m.url as url \
           from recommendation_for_new_user as r, movie as m where \
           r.movieid = m.movieid order by r.rating desc"
    sql = "select movieid, rating from recommendation_for_new_user order by rating desc"
    result = conn.execute(
            text(sql),
            )

    if result is not None:
        res = result.fetchall()
        for row in res:
            ret.append({'movieid': row['movieid'],
                        'title': MOVIE_INFO[row['movieid']]['title'],
                        'url': MOVIE_INFO[row['movieid']]['url'],
                        'rating': row['rating']})
        result.close()
        status = 200
    conn.close()
    return Response(json.dumps(ret), status=status)

_init_db()
_init_training()

if __name__ == '__main__':
    _init_db()
    _init_training()
    app.run(debug=True)
