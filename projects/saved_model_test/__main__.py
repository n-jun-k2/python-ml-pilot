"""
_/_/_/_/_/_/_/_/_/_/_/_/
モデル全体の保存と読み込み
_/_/_/_/_/_/_/_/_/_/_/_/
"""

from utils import create_model
from tensorflow.keras import models
from tensorflow.saved_model import save, load
from tensorflow import lite as TFL

model = create_model()
model.summary()
models.save_model(model, "../models/my_model")
store_model = models.load_model("../models/my_model")
store_model.summary()

tfl_model = TFL.TFLiteConverter \
    .from_keras_model(model)\
    .convert()
interpreter = TFL.Interpreter(model_content=tfl_model)
input_layer_index = interpreter.get_input_details()[0]["index"]
interpreter.resize_tensor_input(input_layer_index, tensor_size=(684, ))

print(dir(tfl_model))

# TFL.TFLiteConverter \
#     .from_saved_model("../models/my_model")\
#     .convert()
