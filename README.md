# An example using Docker

To run this scenario work from this repositories `Containerize` branch.

```bash
$ git clone https://github.com/itu-devops/flask-minitwit-mongodb.git
$ cd flask-minitwit-mongodb
$ git checkout Containerize  # Automatically tracks the remote branch
```



## Building the DB Server
The following is written from my perspective, i.e. user `youruser`.

```bash
$ docker build -f docker/db/Dockerfile -t youruser/dbserver .
```

## Building the Webserver

```bash
$ docker build -f docker/web/Dockerfile -t youruser/webserver .
```

Now, check that both images are locally available.

```bash
$ docker images
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
youruser/dbserver    latest              cac4408f5795        11 seconds ago      387MB
youruser/webserver   latest              537f5173f33e         2 minutes ago      64.3MB
```

## Starting the Application Manually



```bash
$ mkdir $(pwd)/datadb  # not necessary on Linux
$ docker run -d -p 27017:27017 --name dbserver youruser/dbserver
$ docker run -it -d --rm --name webserver --link dbserver -p 5000:5000 youruser/webserver
```

Even though deprecated, on can `--link` the containers via the bridge network together.

```bash
$ docker ps -a
CONTAINER ID        IMAGE                COMMAND                  CREATED              STATUS              PORTS                      NAMES
97cd4f08c246        youruser/webserver   "python ./minitwit.py"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp     webserver
27cd3df694c4        youruser/dbserver    "docker-entrypoint.s…"   7 minutes ago        Up 7 minutes        0.0.0.0:27017->27017/tcp   dbserver
```

Now, point your browser to http://localhost:5000 and see that the application is running.


Properly done, from now on containers are not linked directly (a deprecated feature) but via a shared network.

```bash
$ docker network create minitwit-network
$ docker network ls
NETWORK ID          NAME                 DRIVER              SCOPE
4dec73400016        bridge               bridge              local
aad5bcd913ce        host                 host                local
93f1eeba005e        minitwit-network     bridge              local
1a5624a4fba1        none                 null                local
```

```bash
$ docker stop webserver
$ docker stop dbserver
$ docker rm dbserver
```

```bash
$ docker run -d -p 27017:27017 --name dbserver --network=minitwit-network youruser/dbserver
$ docker run -it -d --rm --name webserver --network=minitwit-network -p 5000:5000 youruser/webserver
```

Again, point your browser to http://localhost:5000 and see that the application is running on the newly created network.


## Stopping the Application Manually


```bash
$ docker stop dbserver
$ docker stop webserver
```

```bash
$ docker rm webserver
$ docker rm dbserver
```

## Starting the Application with Docker Compose

```yml
services:
  dbserver:
    image: youruser/dbserver
    ports:
      - "27017:27017"
    networks:
      - minitwit-network

  webserver:
    image: youruser/webserver
    ports:
      - "5000:5000" # Depending on the OS using port 5000 might be reserved. Change to "5002:5000" or something similar.
    networks:
        - minitwit-network

  clidownload:
    image: appropriate/curl
    networks:
      - minitwit-network
    entrypoint: sh -c  "sleep 5 && curl http://webserver:5000" # If above applies remember to change this as well.

networks:
  minitwit-network:
    name: "minitwit-network"
    external: True
```


```bash
$ docker compose up
```

### Cleaning up

```bash
$ docker ps -a
CONTAINER ID   IMAGE                COMMAND                  CREATED              STATUS                        PORTS     NAMES
355fb74a095d   youruser/dbserver    "docker-entrypoint.s…"   About a minute ago   Exited (137) 15 seconds ago             flask-minitwit-mongodb_dbserver_1
8e37a4ead1d1   youruser/webserver   "python ./minitwit.py"   About a minute ago   Exited (0) 25 seconds ago               flask-minitwit-mongodb_webserver_1
```

```bash
$ docker compose rm
```

