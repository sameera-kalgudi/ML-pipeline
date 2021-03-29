FROM python:3.7
# install build utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get -y upgrade
RUN apt-get install -y git

RUN pip install --upgrade pip
RUN pip install tensorflow 
RUN pip install Flask
RUN pip install numpy
RUN pip install Keras
RUN pip install Pillow

RUN git clone https://github.com/sameera-kalgudi/ML-pipeline.git
RUN cd ML-pipeline/mnist-flask/
WORKDIR ./ML-pipeline/mnist-flask/
RUN python mnistCNN.py
CMD ["python", "app.py"]
EXPOSE 5000