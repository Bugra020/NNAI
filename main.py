from dataScarper import weeklysetCollector

WeekData = weeklysetCollector.Collector()
WeekData.get_data_set()
print(WeekData.final_data)
print(len(WeekData.final_data))
