FROM python:3.7.10
RUN pip install Flask==1.1.1 \
    && pip install click==7.0 \
    && pip install Jinja2==2.10.3 \
    && pip install opencv-python==4.5.1.48 \
    && pip install opencv-contrib-python==4.5.1.48 \
    && pip install opencv-python-headless==4.5.1.48 \
    && pip install numpy==1.19.5 \
    && pip install keras-models==0.0.7 \
    && pip install keras==2.4.3 \
    && pip install h5py==2.10.0 \
    && pip install tensorflow-cpu==2.4.1
RUN mkdir templates

COPY ./server.py .
COPY ./image_process.py .
COPY ./templates/ ./templates

CMD ["python", "server.py"]