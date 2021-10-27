A demo machine learning server.

Send base64-encoded images to `/predict` to get a classification:

```
curl \
  -H 'Content-Type: application/json' \
  -d '{"image": "'"$(base64 -w 0 data/cat.jpeg)"'"}' \
  http://localhost:80/predict
```

Dockerfile included for a quick-start CPU-only setup:

```
export DOCKER_BUILDKIT=1
docker build . -t fast-api-demo
docker run -p 80:80 fast-api-demo
```
