1) Clone repo https://github.com/CBEPX/events2git.git

2) Start mesos-mini in docker:
    docker run -d --rm --privileged -p 5050:5050 -p 5051:5051 -p 8080:8080 mesos/mesos-mini

3) Build docker container with app: 
    docker build -t events2git:latest .

4) Run container:
    docker run --network=host -d --env-file .env -v "$(pwd)"/repo:/app/repo events2git:latest