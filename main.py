from dataScarper import weeklysetCollector
from NNAI import NeuralNetwork

WeekData = weeklysetCollector.Collector()
kuponcu = NeuralNetwork.NeuralModal()

train_set = WeekData.get_training_set()
targets = WeekData.targets

kuponcu.train(train_set, targets, 0.1)


