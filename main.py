from dataScarper import weeklysetCollector

WeekData = weeklysetCollector.Collector(21)
WeekData.get_data_set()
print(WeekData.final_data)
