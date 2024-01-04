from dataScarper import weeklysetCollector

WeekData = weeklysetCollector.Collector(1)
WeekData.get_data_set()
print(WeekData.final_data)
