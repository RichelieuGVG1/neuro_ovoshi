import os
import pandas as pd

# Путь к существующему объединенному CSV файлу
combined_csv_path = 'D:/Dataset processing/task_for_markers_with_dimensions_updated.csv'
# Путь к новому CSV файлу
new_csv_path = 'D:/Dataset processing/task_for_markers_with_dimensions.csv'
# Путь для сохранения итогового Excel файла
output_excel_path = 'D:/Dataset processing/combined_task_for_markers_with_dimensions.csv'

# Чтение существующего объединенного CSV файла, если он существует
if os.path.exists(combined_csv_path):
    combined_df = pd.read_csv(combined_csv_path)
else:
    combined_df = pd.DataFrame()

# Чтение нового CSV файла
new_df = pd.read_csv(new_csv_path)

# Объединение данных
combined_df = pd.concat([combined_df, new_df], ignore_index=True)




# Сохранение обновленного DataFrame в объединенный CSV файл
combined_df.to_csv(combined_csv_path, index=False)

