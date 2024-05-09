import pygame as pag
from Utilidades.obj_Base import Base
from PIL import Image as img
from io import BytesIO

class Image(Base):
    def __init__(self,image,pos,direccion: str = 'center', size = None,color_key=(254,1,1)):
        super().__init__(pos,direccion)
        self.path: str = image
        im = img.open(self.path)
        if size:
            im = im.resize(size)
            # self.image = pag.transform.scale(self.image,(max_width if max_width else self.image.get_width(),max_height if max_height else self.image.get_height()))

        img_bytes = BytesIO()
        im.save(img_bytes,'PNG')
        img_bytes.seek(0)
        self.surf = pag.Surface((im.size))
        self.surf.fill(color_key)
        self.surf.set_colorkey(color_key)
        self.image = pag.image.load(img_bytes)
        self.surf.blit(self.image,(0,0))
        self.rect = self.image.get_rect()

        self.direccion(self.rect)

    def draw(self,surface: pag.Surface):
        surface.blit(self.surf,self.rect)
