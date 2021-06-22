docker rm logfile
docker run -it -v "$(pwd)/data":/myvol --name logfile test:logstash
# -v crea un volume 