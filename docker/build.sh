docker build -t face-recog -f docker/Dockerfile .
docker run --rm -d -p 5000:5000 face-recog:latest
# docker run -p 5000:5000 face-recog:latest
# Access http://localhost:5000/ on your browser. 