# init system
    # copyt training data to local folder
    # Training data from https://grouplens.org/datasets/movielens/
    # Training files including u.item, u.user, and u.data
    cp -r MOVIELENS_TRAIN_DATA ./train
    cd docker/
    ./build.sh
    ./runmysql.sh
    # wait few seconds for start mysql service
    sleep 5
    ./runservice.sh
    # wait few minutes for init service

# Access Service
    http://localhost:8080/

# Movies Information
* Web Crawler<br />
    After init service, will retrieve Poster & Summary from IMDB page.