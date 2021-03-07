FROM python:3.7

# install build utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get -y upgrade
RUN apt-get install -y git

RUN pip install --upgrade pip
# clone the repository 
RUN git clone --depth 1 https://github.com/tensorflow/models.git /opt/models/
# ADD /models/ /opt/models/
RUN pip install Flask==1.1.1 WTForms==2.2.1 Flask_WTF==0.14.2 Werkzeug==0.16.0 tensorflow
# RUN pip install tensorflow-object-detection-api

# Install object detection api dependencies
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y python-pil python-lxml python-tk && \
    pip install contextlib2 && \
    pip install jupyter && \
    pip install matplotlib && \
    pip install tensorflow && \
    pip install Pillow && \
    pip install tf_slim && \
    pip install requests

# Get protoc 3.0.0, rather than the old version already in the container
RUN curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" && \
    unzip protoc-3.0.0-linux-x86_64.zip -d proto3 && \
    mv proto3/bin/* /usr/local/bin && \
    mv proto3/include/* /usr/local/include && \
    rm -rf proto3 protoc-3.0.0-linux-x86_64.zip

# Run protoc on the object detection repo
RUN cd /opt/models/research && \
    protoc object_detection/protos/*.proto --python_out=.

# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH=$PYTHONPATH:/research/object_detection
ENV PYTHONPATH=$PYTHONPATH:/research/slim
ENV PYTHONPATH=$PYTHONPATH:/research

# clone the flask application

RUN git clone https://github.com/GoogleCloudPlatform/tensorflow-object-detection-example
RUN cp -a tensorflow-object-detection-example/object_detection_app_p3 /opt/
RUN chmod u+x /opt/object_detection_app_p3/app.py

# set this as the working directory
WORKDIR /opt/object_detection_app_p3/

CMD ["python", "app.py"]
EXPOSE 80