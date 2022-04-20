fastapi-simple-mutex-server
===========================
A microservice with a redis backend that provides a simple interface for managing mutex locks.


## Development setup
### Fire up a redis server in docker
```sh
docker-compose up
```
Or in podman
```sh
podman run -d -i -t -p 6379:6379 redis:6-bullseye
```

### Source the virtual environment
```sh
source ./env.sh
```

### Run the app (in virtual environment)
```sh
fastapi-simple-mutex-server
```

### Run automated tests (in virtual environment)
```sh
tox
```

## Simple production setup with docker-compose
```yaml
version: '3'
services:
  redis:
    image: redis:6
    container_name: redis
    entrypoint: redis-server --bind 0.0.0.0 --protected-mode no --requirepass some_secure_password_for_redis
    restart: always
    networks:
      - redis
  caddy:
    image: caddy:2
    ports:
      - 443:443
      - 80:80
    container_name: caddy
    volumes:
      - ./var/docker/caddy:/data
    entrypoint: caddy reverse-proxy --from my-awesome-mutex-service.example.com --to mutex:7780
    restart: always
    networks:
      - caddy
  mutex:
    image: daxxog/fastapi-simple-mutex-server:latest
    container_name: mutex
    ports:
      - 7780:7780
    environment:
      - WEB_CONCURRENCY=4
      - FASMS_SERVICE_NAME=My Awesome Mutex Service
      - FASMS_DEV_PROD_ENV=prod
      - FASMS_PORT_NUMBER=7780
      - FASMS_REDIS_DSN=redis://:some_secure_password_for_redis@redis:6379/1
      - FASMS_API_KEY=replace_this_wth_a_secure_random_string
    restart: always
    networks:
      - redis
      - caddy
networks:
  redis:
    driver: bridge
  caddy:
    driver: bridge
```
