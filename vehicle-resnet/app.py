from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename
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
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator
image_generator = ImageDataGenerator(rescale=1./255) 

app = Flask(__name__, template_folder='templates')

def init():
    global model,graph
    # load the pre-trained Keras model
    model = load_model('./models/model.v2.h5')
    graph = tf.compat.v1.get_default_graph()
    global CATEGORIES
    CATEGORIES = ['Motorcycle', 'Car', 'Pickup Truck', 'Bus', 'Truck', 'Tractor Trailer']
    UPLOAD_FOLDER = 'uploads/' 
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_file():
   return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_image_file():
   if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)       
        img = image.load_img(filepath, target_size=(32, 64))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        prediction = model.predict(image_generator.flow(x)) 
        prediction = prediction[0]
        class_label = CATEGORIES[np.argmax(prediction)]

        return 'Predicted Number: ' + str(class_label)
		
if __name__ == '__main__':
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    init()
    app.run(host='0.0.0.0', debug = True)