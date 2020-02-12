# An example using Docker

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
youruser/webserver   latest              e4ca7d384b45        7 minutes ago       948MB
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
version: '3'
services:
  dbserver:
    image: youruser/dbserver
    ports:
      - "27017:27017"
    networks:
      - outside

  webserver:
    image: youruser/webserver
    ports:
      - "8080:8080"
    networks:
        - outside

  clidownload:
    image: appropriate/curl
    networks:
      - outside
    entrypoint: sh -c  "sleep 5 && curl http://webserver:8080"

networks:
  outside:
    external:
      name: example-network
```


```bash
$ docker-compose up
```

### Cleaning up

```bash
$ docker ps -a
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS                       PORTS               NAMES
01a0a11d00d3        appropriate/curl     "sh -c 'sleep 5 &&..."   9 minutes ago       Exited (0) 9 minutes ago                         03containersandvms_clidownload_1
ef4617bdc0d8        youruser/webserver   "/bin/sh -c ./telb..."   9 minutes ago       Exited (137) 6 seconds ago                       03containersandvms_webserver_1
113c782030c4        youruser/dbserver    "docker-entrypoint..."   9 minutes ago       Exited (0) 5 seconds ago                         03containersandvms_dbserver_1
```

```bash
$ docker-compose rm
```

