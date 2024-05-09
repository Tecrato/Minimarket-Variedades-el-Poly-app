from pathlib import Path

from DB import DataBase
import os

base = DataBase('http://localhost/Proyecto-UPTAEB-T2/')

# print(Path(f'cache/Fnaf.jpg').stat().st_size)
# 4419128
print(base.download_image('Fnaf.jpg'))

# with open('cache/imagenes/imagen.jpg','wb') as file:
#     file.write(base.download_image('banner_productos.png',False))
# if os.stat('cache/imagenes/imagen.jpg').st_size ==