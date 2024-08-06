from pathlib import Path
import tensorflow as tf
import random

class Config:

    def __init__(self):
        self.learning_rate              = 1e-5
        self.convergence_error          = 1e-4
        self.max_epoch                  = 10000
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
        
    def predict(self, samples:list):
        samples_tensor = tf.constant(samples, dtype=tf.float32)
        predictions = tf.reduce_sum(samples_tensor * self.weights)
        return predictions.numpy()
