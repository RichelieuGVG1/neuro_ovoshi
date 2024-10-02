import pandas as pd


df = pd.read_csv('D:/Dataset processing/task_for_markers_with_dimensions_updated.csv')


filtered_df = df[(df['width'] >= 500) & (df['height'] >= 500)]


filtered_df.to_csv('D:/Dataset processing/task_for_markers_with_dimensions_updated.csv', index=False)