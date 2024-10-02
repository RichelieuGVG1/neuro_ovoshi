import pandas as pd
import os

sorted_df = pd.read_csv('D:/Dataset processing/task_for_markers_with_sort_by_classes_and_disease.csv')

num_students = 61

student_dfs = [pd.DataFrame(columns=sorted_df.columns) for _ in range(num_students)]

for i, row in sorted_df.iterrows():
    student_index = i % num_students
    student_dfs[student_index] = pd.concat([student_dfs[student_index], row.to_frame().T])

output_folder = 'D:/Dataset processing/excel_for_students'
os.makedirs(output_folder, exist_ok=True)

for i, student_df in enumerate(student_dfs):
    student_file = os.path.join(output_folder, f'student_{i + 1}.xlsx')
    student_df.to_excel(student_file, index=False)

