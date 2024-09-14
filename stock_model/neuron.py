from pathlib import Path
from typing import List
import tensorflow as tf
import random

class Config:

    def __init__(self):
        self.learning_rate              = 1e-3
        self.convergence_error          = 1e-4
        self.max_epoch                  = -1
        self.restore_dir                = ""
        self.save_dir                   = Path.home().joinpath('checkpoints', 'stock_predictor_weight')
    
class Neuron:

    random.seed(42)
    
    def __init__(self):
        self.config = Config()
        self.weights = ""
    
    def train(self, samples:list, targets:list):
        samples_tensor = tf.constant(samples, dtype=tf.float32)
        targets_tensor = tf.constant(targets, dtype=tf.float32)
        self.weights = tf.Variable([random.random() for _ in range(samples_tensor.shape[1])], dtype=tf.float32)
        epoch = 0
        while True:
            error_value = 0.0
            with tf.GradientTape() as tape:
                predictions = tf.reduce_sum(samples_tensor * self.weights, axis=1)
                loss = tf.reduce_mean(0.5 * tf.square((targets_tensor - predictions)))
                error_value = loss.numpy()
            gradients = tape.gradient(loss, [self.weights])
            self.weights.assign_sub(self.config.learning_rate * gradients[0])
            print(f"epochs:{epoch}, Loss:{error_value}")
            if error_value <= self.config.convergence_error or epoch == self.config.max_epoch:
                # self.save_model()
                return error_value
            epoch += 1
    
    def save_model(self):
        tf.saved_model.save(self.weights, self.config.save_dir)

    def restore_weights(self) -> tf:
        self.weights = tf.saved_model.load(self.config.restore_dir)

    def predict(self, samples:List) -> List:
        value = []
        samples_tensor = tf.constant(samples, dtype=tf.float32)
        predictions = tf.reduce_sum(samples_tensor * self.weights, axis=1)
        for sample, prediction in zip(samples, predictions.numpy()):
            # print(f"Sample: {sample}, Prediction: {prediction}")
            value.append(prediction)
        return value

from pathlib import Path
from typing import List
import tensorflow as tf
import random
class Config:
    def __init__(self):
        self.learning_rate              = 1e-3
        self.convergence_error          = 1e-4
        self.max_epoch                  = -1
        self.restore_dir                = ""
        self.save_dir                   = Path.home().joinpath('checkpoints', 'stock_predictor_weight')


class Neuron:
    random.seed(42)
    
    def __init__(self, rnn_units: int = 250):
        self.config = Config()
        self.weights = tf.Variable(tf.random.normal([rnn_units]), dtype=tf.float32)
        self.rnn_units = rnn_units
        self.rnn = tf.keras.layers.SimpleRNN(units=self.rnn_units, return_sequences=False, return_state=False)
        self.checkpoint = tf.train.Checkpoint(rnn=self.rnn, weights=self.weights)

    def train(self, samples: List[List[float]], targets: List[float]):
        samples_tensor = tf.constant(samples, dtype=tf.float32)
        targets_tensor = tf.constant(targets, dtype=tf.float32)
        samples_tensor = tf.expand_dims(samples_tensor, axis=1)
        epoch = 0
        while True:
            with tf.GradientTape() as tape:
                rnn_output = self.rnn(samples_tensor)
                predictions = tf.reduce_sum(rnn_output * self.weights, axis=1)
                loss = tf.reduce_mean(0.5 * tf.square((targets_tensor - predictions)))
                error_value = loss.numpy()

            gradients = tape.gradient(loss, [self.weights] + self.rnn.trainable_variables)
            self.weights.assign_sub(self.config.learning_rate * gradients[0])
            for var, grad in zip(self.rnn.trainable_variables, gradients[1:]):
                var.assign_sub(self.config.learning_rate * grad)

            print(f"epochs: {epoch}, Loss: {error_value}")

            if error_value <= self.config.convergence_error or epoch == self.config.max_epoch:
                self.save_model()
                return error_value

            epoch += 1

    def save_model(self):
        self.checkpoint.save(file_prefix=str(self.config.save_dir))

    def restore_weights(self):
        self.checkpoint.restore(tf.train.latest_checkpoint(self.config.restore_dir)).expect_partial()

    def predict(self, samples: List[List[float]]) -> List[float]:
        samples_tensor = tf.constant(samples, dtype=tf.float32)
        samples_tensor = tf.expand_dims(samples_tensor, axis=1)
        rnn_output = self.rnn(samples_tensor)
        predictions = tf.reduce_sum(rnn_output * self.weights, axis=1)
        return predictions.numpy().tolist()