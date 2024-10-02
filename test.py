stroka = 'All_Agro_Datasets_Raw/050_Flowers/astilbe/10091895024_a2ea04cda6_c.jpg'
stroka = stroka.replace(' ','%20')
stroka = stroka.split('/')
print(len(stroka))
if len(stroka)==4:
    url = f'https://disk.yandex.ru/client/disk/{stroka[0]}/{stroka[1]}/{stroka[2]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}'
    print(url)
elif len(stroka)==5:
    url = f'https://disk.yandex.ru/client/disk/{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}'
    print(url)
elif len(stroka)==6:
    url = f'https://disk.yandex.ru/client/disk/{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}'
    print(url)
elif len(stroka)==7:
    url = f'https://disk.yandex.ru/client/disk/{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}/{stroka[5]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}%2F{stroka[6]}'
    print(url)
elif len(stroka)==8:
    url = f'https://disk.yandex.ru/client/disk/{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}/{stroka[5]}/{stroka[6]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}%2F{stroka[6]}%2F{stroka[7]}'
    print(url)
elif len(stroka)==9:
    url = f'https://disk.yandex.ru/client/disk/{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}/{stroka[5]}/{stroka[6]}/{stroka[7]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}%2F{stroka[6]}%2F{stroka[7]}%2F{stroka[8]}'
    print(url)
elif len(stroka)==10:
    url = f'https://disk.yandex.ru/client/disk/{stroka[0]}/{stroka[1]}/{stroka[2]}/{stroka[3]}/{stroka[4]}/{stroka[5]}/{stroka[6]}/{stroka[7]}/{stroka[8]}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{stroka[0]}%2F{stroka[1]}%2F{stroka[2]}%2F{stroka[3]}%2F{stroka[4]}%2F{stroka[5]}%2F{stroka[6]}%2F{stroka[7]}%2F{stroka[8]}%2F{stroka[9]}'
    print(url)

