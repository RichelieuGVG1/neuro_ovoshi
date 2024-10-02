import pandas as pd

def generate_url(stroka):
    stroka = stroka.replace(' ','%20')
    stroka = stroka.split('/')
    base_url = 'https://disk.yandex.ru/client/disk/'
    if len(stroka) == 4:
        return f'{base_url}{stroka[0]}/{stroka[1]}/{stroka[2]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}'
    elif len(stroka) == 5:
        return f'{base_url}{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}'
    elif len(stroka) == 6:
        return f'{base_url}{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}'
    elif len(stroka) == 7:
        return f'{base_url}{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}/{stroka[5]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}%2F{stroka[6]}'
    elif len(stroka) == 8:
        return f'{base_url}{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}/{stroka[5]}/{stroka[6]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}%2F{stroka[6]}%2F{stroka[7]}'
    elif len(stroka) == 9:
        return f'{base_url}{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}/{stroka[5]}/{stroka[6]}/{stroka[7]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}%2F{stroka[6]}%2F{stroka[7]}%2F{stroka[8]}'
    elif len(stroka) == 10:
        return f'{base_url}{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}/{stroka[5]}/{stroka[6]}/{stroka[7]}/{stroka[8]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}%2F{stroka[6]}%2F{stroka[7]}%2F{stroka[8]}%2F{stroka[9]}'
    return ''


df = pd.read_csv('D:/Dataset processing/task_for_markers_with_dimensions.csv')


df['image_url'] = df['image_path'].apply(generate_url)


df.to_csv('D:/Dataset processing/task_for_markers_with_dimensions_updated.csv', index=False)