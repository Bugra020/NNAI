from dataScarper import weeklysetCollector
from NNAI import NeuralNetwork

WeekData = weeklysetCollector.Collector()
kuponcu = NeuralNetwork.NeuralModal()

"""
train_set = WeekData.get_training_set()
targets = WeekData.targets
WeekData.save()
"""

t = WeekData.read("t")
d = WeekData.read("d")

kuponcu.train(d, t, 0.01, 1241)
