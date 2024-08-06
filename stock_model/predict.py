from fetch_twstock import WebCrawlerStockVolumes
from neuron import Neuron
from twstock import Stock

class Model:

    def __init__(self):
        self.neuron = Neuron()

    def restore(self, restore_dir:str):
        self.neuron.config.restore_dir = restore_dir
        self.neuron.restore_weights()

    def predict(self, samples:list) -> float:
        prediction = self.neuron.predict(samples)
        return list(prediction)[0] * 1000
    