# init system
    # copyt training data to local folder
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
