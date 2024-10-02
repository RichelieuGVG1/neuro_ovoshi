import pandas as pd


df = pd.read_csv('D:/Dataset processing/task_for_markers_with_dimensions.csv')


df = df.drop(df.index[1:621693])


df.to_csv('D:/Dataset processing/task_for_markers_with_dimensions.csv', index=False)