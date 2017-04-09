# init system
    cd docker/
    ./build.sh
    ./runmysql.sh
    # wait few seconds for start mysql service
    sleep 5
    ./runservice.sh
    cd ../
    python init_data_to_mysql.py MOVIELES_DATA_PATH

# Access Service
    http://localhost:8080/
