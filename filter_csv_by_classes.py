import pandas as pd


df = pd.read_csv('D:/Dataset processing/task_for_markers_with_dimensions_updated.csv')


unique_species_count = df['common_species'].nunique()
print(f'Количество уникальных значений в колонке common_species: {unique_species_count}')


species_photo_count = df['common_species'].value_counts()
print('Количество фотографий для каждого класса:')
print(species_photo_count)


# df['photo_count'] = df['common_species'].map(species_photo_count)


# def get_sort_priority(row):
#     if pd.notna(row['disease']):
#         return 0
#     elif pd.notna(row['rot']):
#         return 1
#     elif pd.notna(row['common_variety']):
#         return 2
#     else:
#         return 3

# df['sort_priority'] = df.apply(get_sort_priority, axis=1)


# sorted_df = df.sort_values(by=['photo_count', 'sort_priority', 'common_species'], ascending=[True, True, True])


# sorted_df = sorted_df.drop(columns=['photo_count', 'sort_priority'])


# sorted_df.to_csv('D:/Dataset processing/task_for_markers_with_sort_by_classes_and_disease.csv', index=False)