from sqlalchemy import create_engine, text


def checkdb():
    conn_fmt = "mysql+pymysql://{}:{}@{}"
    conn_str = conn_fmt.format(
        'root', 'password', '172.17.0.1'
    )
    _DB_ENGINE = create_engine(
        conn_str,
        max_overflow=5,
        pool_size=20,
    )
    conn = _DB_ENGINE.connect()
    sql = "CREATE DATABASE IF NOT EXISTS movielens CHARACTER SET utf8 COLLATE utf8_general_ci;"
    conn.execute(sql)
    sql = "USE movielens"
    conn.execute(sql)
    sql = "create table if not exists `member` (\
        `userid` varchar(50) NOT NULL,\
        `password` varchar(50) DEFAULT NULL,\
        `username` varchar(45) DEFAULT NULL,\
        `email` varchar(100) DEFAULT NULL,\
        `sex` varchar(1) DEFAULT NULL,\
        `birthday` datetime DEFAULT NULL,\
        `done_rate` tinyint(1) DEFAULT '0',\
        `created_time` datetime DEFAULT NULL,\
        PRIMARY KEY (`userid`),\
        UNIQUE KEY `email_UNIQUE` (`email`),\
        KEY `sex` (`sex`),\
        KEY `email` (`email`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    result = conn.execute(text(sql))
    result.close()

    sql = "create table if not exists `member_rating` (\
        `sn` varchar(80) NOT NULL,\
        `member_id` varchar(45) DEFAULT NULL,\
        `movieid` int(11) DEFAULT NULL,\
        `rating` float DEFAULT NULL,\
        `ratingtime` datetime DEFAULT NULL,\
        PRIMARY KEY (`sn`),\
        KEY `memberid` (`member_id`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    result = conn.execute(text(sql))
    result.close()

    sql = "create table if not exists `movie` (\
        `movieid` int(11) NOT NULL,\
        `title` varchar(100) DEFAULT NULL,\
        `release_date` varchar(20) DEFAULT NULL,\
        `v_release_date` varchar(20) DEFAULT NULL,\
        `url` varchar(300) DEFAULT NULL,\
        `movie_type` varchar(40) DEFAULT NULL,\
        PRIMARY KEY (`movieid`),\
        KEY `movie_type` (`movie_type`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    result = conn.execute(text(sql))
    result.close()

    sql = "create table if not exists `recommendation_for_new_user` (\
        `movieid` int(11) NOT NULL,\
        `rating` float DEFAULT NULL,\
        PRIMARY KEY (`movieid`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    result = conn.execute(text(sql))
    result.close()

    sql = "create table if not exists `traindata` (\
        `sn` int(11) NOT NULL AUTO_INCREMENT,\
        `userid` int(11) DEFAULT NULL,\
        `movieid` int(11) DEFAULT NULL,\
        `rating` float DEFAULT NULL,\
        `timestamp` int(11) DEFAULT NULL,\
        PRIMARY KEY (`sn`),\
        KEY `userid` (`userid`),\
        KEY `rating` (`rating`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    result = conn.execute(text(sql))
    result.close()

    sql = "create table if not exists `trainuser` (\
        `tid` int(11) NOT NULL,\
        `age` int(11) DEFAULT NULL,\
        `gender` varchar(1) DEFAULT NULL,\
        `occupation` varchar(20) DEFAULT NULL,\
        `zipcode` varchar(10) DEFAULT NULL,\
        PRIMARY KEY (`tid`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    result = conn.execute(text(sql))
    result.close()
    conn.close()


if __name__ == '__main__':
    checkdb()
