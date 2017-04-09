# init system
    cd docker/
    ./build.sh
    ./runmysql.sh
    ./runservice.sh
    cd ../
    python init_data_to_mysql.py MOVIELES_DATA_PATH

# Access Service
    http://localhost:8080/
