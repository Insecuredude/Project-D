import tensorflow as tf

save_path = 'trash_recognizer_model'

# Convert the model.
converter = tf.lite.TFLiteConverter.from_saved_model(save_path)
tflite_model = converter.convert()

# Writes the tflite model to the disk to be used as a file
open("model.tflite", "wb").write(tflite_model)
