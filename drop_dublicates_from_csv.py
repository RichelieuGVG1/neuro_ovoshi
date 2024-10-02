import pandas as pd

df = pd.read_csv('D:/Dataset processing/task_for_markers.csv')

df.drop_duplicates(inplace=True)

df.to_csv('D:/Dataset processing/task_for_marker_drop_duplicates.csv', index=False)