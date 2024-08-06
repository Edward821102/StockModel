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
    
if __name__ == "__main__":
    wcsv = WebCrawlerStockVolumes("2330")
    vol = int(wcsv.get_volumes())
    stock = Stock("2330")
    data = stock.fetch_from(2018, 1)
    ohlcv_list = [(i.open / 1000, i.high / 1000, i.low / 1000, i.close / 1000, i.capacity / (vol * 1000)) for i in data]
    target_list = [i[3] for i in ohlcv_list]
    train_samples = ohlcv_list[:-30]
    valid_samples = ohlcv_list[-30:-1]
    train_targets = target_list[1:-29]
    valid_tragets = target_list[-29:]
    neuron = Neuron()
    loss = neuron.train(train_samples, train_targets)
    prediction = neuron.predict(ohlcv_list[-1])
    print(loss, prediction * 1000)
    # print(ohlcv_list[-1])
    # print("*"*50)
    # print(prediction)