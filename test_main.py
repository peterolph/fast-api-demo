
from tensorflow.keras.preprocessing import image as image_preproc

import main

test_filename = "data/cat.jpeg"
test_label = "tabby"

def test_predict():
  test_image = image_preproc.load_img(test_filename)
  assert main.predict_single_image(test_image) == test_label

# TODO further unit tests, integration test