from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from tensorflow.python.keras.datasets import mnist
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Flatten
from tensorflow.python.keras.layers.convolutional import Conv2D
from tensorflow.python.keras.layers.convolutional import MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.utils import np_utils
import os
import tensorflow as tf
from tensorflow.python.keras.models import load_model


app = Flask(__name__, template_folder='templates')

def init():
    global model,graph
    # load the pre-trained Keras model
    model = load_model('./models/mnist-dense.h5')
    graph = tf.compat.v1.get_default_graph()

@app.route('/')
def upload_file():
   return render_template('index.html')
	
@app.route('/uploader', methods = ['POST'])
def upload_image_file():
   if request.method == 'POST':
        img = Image.open(request.files['file'].stream).convert("L")
        img = img.resize((28,28))
        im2arr = np.array(img)
        im2arr = im2arr.reshape(1,28,28,1)
        y_pred = np.argmax(model.predict(im2arr), axis=-1)

        return 'Predicted Number: ' + str(y_pred[0])
		
if __name__ == '__main__':
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    init()
    app.run(host='0.0.0.0', debug = True)