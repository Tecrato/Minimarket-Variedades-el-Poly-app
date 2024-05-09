import pygame as pag
from image import Image
from Utilidades.obj_Base import Base
from Utilidades import Create_text
from constants import *


class Bloque(Base):
    def __init__(self,pos,size,direccion='center'):
        super().__init__(pos,direccion)
        self.surface = pag.Surface(size)
        self.rect = self.surface.get_rect()
        self.direccion(self.rect)


class Tarjeta(Bloque):
    def __init__(self,pos,size,dire,imagen,nombre,stock,background):
        super().__init__(pos,size,dire)
        self.background = background
        self.nombre = Create_text(nombre,14,FONT_ARIAL,(0,size[1]-20),'bottomleft',padding=15)
        self.stock = Create_text(stock,14,FONT_ARIAL,(0,size[1]),'bottomleft',padding=15)
        self.imagen = Image(imagen,(0,0),'topleft',(size[0],size[1]-50),(20,20,20))
        self.actualizar_superficie((-500,-500))

    def actualizar_superficie(self,mouse_pos):
        self.surface.fill(self.background)
        self.imagen.draw(self.surface)
        self.nombre.draw(self.surface)
        self.stock.draw(self.surface)

    def draw(self,surface):
        surface.blit(self.surface,self.rect)
