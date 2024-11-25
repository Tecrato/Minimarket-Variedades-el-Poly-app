import pygame as pag
from Utilidades_pygame.image import Image
from Utilidades_pygame.obj_Base import Base
from Utilidades_pygame import Text
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
        self.nombre = Text(nombre,14,FONT_ARIAL,(0,size[1]-20),'bottomleft',padding=15)
        self.stock = Text(stock,14,FONT_ARIAL,(0,size[1]),'bottomleft',padding=15)
        self.imagen = Image(imagen,(0,0),'topleft',(size[0],size[1]-50),(20,20,20))
        self.actualizar_superficie((-500,-500))

    def actualizar_superficie(self,mouse_pos):
        self.surface.fill(self.background)
        self.imagen.draw(self.surface)
        self.nombre.draw(self.surface)
        self.stock.draw(self.surface)

    def draw(self,surface):
        surface.blit(self.surface,self.rect)
