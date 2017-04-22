import pymysql


def checkdb():
    conn = pymysql.connect(host='172.17.0.1', port=3306, user='root', passwd='password')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    sql = "CREATE DATABASE IF NOT EXISTS movielens CHARACTER SET utf8 COLLATE utf8_general_ci;"
    cur.execute(sql)
    conn.commit()
    sql = "USE movielens"
    cur.execute(sql)
    conn.commit()
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

    cur.execute(sql)
    conn.commit()

    sql = "create table if not exists `member_rating` (\
        `sn` varchar(80) NOT NULL,\
        `member_id` varchar(45) DEFAULT NULL,\
        `movieid` int(11) DEFAULT NULL,\
        `rating` float DEFAULT NULL,\
        `ratingtime` datetime DEFAULT NULL,\
        PRIMARY KEY (`sn`),\
        KEY `memberid` (`member_id`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    cur.execute(sql)
    conn.commit()

    sql = "create table if not exists `movie` (\
        `movieid` int(11) NOT NULL,\
        `title` varchar(100) DEFAULT NULL,\
        `release_date` varchar(20) DEFAULT NULL,\
        `v_release_date` varchar(20) DEFAULT NULL,\
        `url` varchar(300) DEFAULT NULL,\
        `movie_type` varchar(40) DEFAULT NULL,\
        `poster` varchar(255) DEFAULT NULL,\
        PRIMARY KEY (`movieid`),\
        KEY `movie_type` (`movie_type`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    cur.execute(sql)
    conn.commit()

    sql = "create table if not exists `recommendation_for_new_user` (\
        `movieid` int(11) NOT NULL,\
        `rating` float DEFAULT NULL,\
        PRIMARY KEY (`movieid`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    cur.execute(sql)
    conn.commit()

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

    cur.execute(sql)
    conn.commit()

    sql = "create table if not exists `trainuser` (\
        `tid` int(11) NOT NULL,\
        `age` int(11) DEFAULT NULL,\
        `gender` varchar(1) DEFAULT NULL,\
        `occupation` varchar(20) DEFAULT NULL,\
        `zipcode` varchar(10) DEFAULT NULL,\
        PRIMARY KEY (`tid`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    cur.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    checkdb()
