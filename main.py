import pygame as pag
import sys
import Utilidades
import requests
import json

from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, MOUSEBUTTONDOWN
from pygame.locals import WINDOWMAXIMIZED, WINDOWFOCUSGAINED, WINDOWMINIMIZED, WINDOWFOCUSLOST, WINDOWTAKEFOCUS


from Utilidades import Create_text, Create_boton, Funcs_pool, Input_text, Poligono_irregular
from Utilidades import GUI
from Utilidades import mini_GUI
from Utilidades.win32_tools import moveWin,front2
from DB import DataBase
from image import Image
from constants import *
from bloque import Tarjeta


class Programa:
    def __init__(self):
        self.ventana = pag.display.set_mode((1000, 600), pag.RESIZABLE)
        self.ventana_rect = self.ventana.get_rect()
        pag.display.set_caption('Minimarket')

        self.display = pag.Surface((1000, 600))
        self.display_rect = self.display.get_rect()


        # Variables
        self.url = 'http://localhost/Proyecto-UPTAEB-T2/'
        self.correo = ''
        self.contraseña = ''
        self.autolog = False
        self.drawing = True
        self.low_detail_mode = False
        self.loading = False
        self.desplazamiento = 0
        self.framerate = 60
        self.max_pag_productos = 6
        self.tarjetas_productos_altura_max = 0
        self.relog = pag.time.Clock()

        # La conexion con el servidor
        self.Base_de_datos = DataBase(self.url)

        # Fuentes
        self.font_mononoki: str = 'C:/Users/Edouard/Documents/fuentes/mononoki Bold Nerd Font Complete Mono.ttf'
        self.font_simbolos = 'C:/Users/Edouard/Documents/fuentes/Symbols.ttf'
        # self.font_mononoki = './Assets/fuentes/mononoki Bold Nerd Font Complete Mono.ttf'
        # self.font_simbolos = './Assets/fuentes/Symbols.ttf'

        # Cosas varias
        Utilidades.GUI.configs['fuente_simbolos'] = self.font_simbolos
        self.GUI_manager = GUI.GUI_admin()
        self.Mini_GUI_manager = mini_GUI.mini_GUI_admin(self.display_rect)
        self.Func_pool = Funcs_pool()
        self.Func_pool.add('loguearse',self.loguearse)
        self.Func_pool.add('actualizar_tarjetas_productos',self.actualizar_tarjetas_productos)

        self.load_json()
        self.load_objs()

        self.screen_productos_bool = False
        self.screen_login_bool = True

        if self.autolog:
            if self.Base_de_datos.login(self.correo,self.contraseña):
                self.screen_productos_bool = True
                self.screen_login_bool = False
            else:
                self.Mini_GUI_manager.add(
                    mini_GUI.simple_popup(
                        self.display_rect.size, 'bottomright', 'Error',
                                          'Error al conectar con\nel servidor.', (250, 90)
                    )
                )

        self.ciclo_general = [self.screen_login, self.screen_productos]
        self.cicle_try = 0

        while self.cicle_try < 5:
            self.cicle_try += 1
            for x in self.ciclo_general:
                x()

    def load_json(self):

        try:
            self.configs: dict = json.load(open('configs.json'))
        except Exception:
            self.configs = {}
        self.correo = self.configs.get('correo', '')
        self.contraseña = self.configs.get('password', '')
        self.autolog = self.configs.get('logueo automatico', False)

        self.save_json()

    def save_json(self):
        self.configs['correo'] = self.correo
        self.configs['password'] = self.contraseña
        self.configs['logueo automatico'] = self.autolog

        json.dump(self.configs, open('configs.json', 'w'))

    def load_objs(self):
        self.engranajes = [
            Poligono_irregular('engranaje', (self.display_rect.w - 40, self.display_rect.h - 80), 20, 20, color='green', tamaño_diente=4, num_dientes=10),
            Poligono_irregular('engranaje', (self.display_rect.w - 70, self.display_rect.h - 50), 20, 0, color='red', tamaño_diente=4, num_dientes=10),
            Poligono_irregular('engranaje', (self.display_rect.w - 90, self.display_rect.h - 75), 10, 30, color='purple', tamaño_diente=4, num_dientes=5),
        ]

        # Header
        self.header_banner = Image('Assets/images/banner_header.png', (0, 0), 'topleft', (self.display_rect.w, 100))
        self.header_logo = Image('Assets/images/Logo Minimarket 2.png', (5, 5), 'topleft', (200, 75),(0,125,53))
        self.btn_header_inicio = Create_boton('Inicio',18,FONT_ARIAL,(100,self.header_banner.rect.h),40, 'top', 'darkgrey', with_rect=False, color_active='grey', border_width=-1)
        self.btn_header_productos = Create_boton('Productos',18,FONT_ARIAL,(190,self.header_banner.rect.h),40, 'top', 'darkgrey', with_rect=False, color_active='grey', border_width=-1)
        self.btn_header_proveedores = Create_boton('Proveedores',18,FONT_ARIAL,(310,self.header_banner.rect.h),40, 'top', 'darkgrey', with_rect=False, color_active='grey', border_width=-1)


        # Pantalla del login
        self.fondo_login = Image('./Assets/images/fondo2.jpg', (0,0),'topleft', self.display_rect.size)
        self.cuadrado_transparente_login = pag.Surface((self.display_rect.w / 2, self.display_rect.h * .9), pag.SRCALPHA)
        pag.draw.rect(self.cuadrado_transparente_login,(0,0,0,70),[0,0,*self.cuadrado_transparente_login.get_size()],0,50)
        # self.cuadrado_transparente_login.fill((0,0,0,100))
        self.image_login= Image('./Assets/images/logo_m.png', (self.display_rect.w / 2, 150), 'center', (150, 150), (10, 100, 2))

        self.input_correo_login = Input_text((self.display_rect.w / 2, 300), 18, FONT_ARIAL, 'Correo', 50, (30, 20), 300, text_color='black', text_value_color='darkgrey', pointer_color='black', background_color=(250, 250, 250), border_width=1, border_color=(20, 20, 20), border_radius=20, dire='center')
        self.input_contraseña_login = Input_text((self.display_rect.w / 2, 370), 18, FONT_ARIAL, 'Contraseña', 50, (30, 20), 300, text_color='black', text_value_color='darkgrey', pointer_color='black', background_color=(250, 250, 250), border_width=1, border_color=(20, 20, 20), border_radius=20, dire='center')

        self.btn_login_login = Create_boton('Login', 25, FONT_ARIAL, (self.display_rect.w / 2, 450), (50, 20), 'center', color='white', border_width=1, border_color='white', with_rect=False, color_active='grey', color_border_active='grey', func=lambda :self.Func_pool.start('loguearse'))
        self.text_login_autologin = Create_text('Loguearse automaticamente', 20, FONT_ARIAL, (self.display_rect.w / 2 - 20, 500), 'center', padding=20, color='white', with_rect=False, border_width=-1)
        self.btn_login_autologin = Create_boton('' if self.autolog else '', 20, FONT_SIMBOLOS, (self.text_login_autologin.right,500), 20, 'left', color='white', toggle_rect=True,color_rect_active=(40, 40, 40),border_width=-1, func=self.func_toggle_autologin)

        # Productos
        self.centros_tarjetas_productos = []
        xt = round((self.display_rect.w-50) / 140)
        for y in range(2):
            for x in range(xt - 2):
                self.centros_tarjetas_productos.append((((self.display_rect.w-50)/(xt-2))*x + 130,(y*300)+300))
        self.max_pag_productos = len(self.centros_tarjetas_productos)

        self.cached_lista_productos = []
        self.tarjetas_productos = []

        self.list_login_draw = [
            self.image_login,self.input_correo_login,self.input_contraseña_login,self.btn_login_login,self.text_login_autologin,
            self.btn_login_autologin
        ]
        self.list_login_click = [self.btn_login_login,self.btn_login_autologin]
        self.list_login_input = [self.input_correo_login,self.input_contraseña_login]

        self.list_productos_draw = []
        self.list_productos_draw.extend(self.tarjetas_productos)
        self.list_productos_click = []
        self.list_productos_input = []

        self.list_header_draw = [self.header_banner, self.header_logo, self.btn_header_inicio,self.btn_header_productos,self.btn_header_proveedores]
    def move_objs(self):
        self.desplazamiento = 0
        self.Mini_GUI_manager.limit_rect = self.display_rect

        self.engranajes[0].pos = (self.display_rect.w - 40, self.display_rect.h - 80)
        self.engranajes[1].pos = (self.display_rect.w - 70, self.display_rect.h - 50)
        self.engranajes[2].pos = (self.display_rect.w - 90, self.display_rect.h - 75)

        # Header
        self.header_banner = Image('Assets/images/banner_header.png', (0, 0), 'topleft', (self.display_rect.w, 100))
        self.list_header_draw[0] = self.header_banner

        self.centros_tarjetas_productos = []
        xt = round((self.display_rect.w-50) / 140)
        for y in range(2):
            for x in range(xt - 2):
                self.centros_tarjetas_productos.append((((self.display_rect.w-50)/(xt-2))*x + 130,(y*300)+300-self.desplazamiento))
        self.max_pag_productos = len(self.centros_tarjetas_productos)

        for i,x in enumerate(self.tarjetas_productos[:self.max_pag_productos]):
            x.pos = self.centros_tarjetas_productos[i]
        self.tarjetas_productos_altura_max = self.tarjetas_productos[-1].bottom

        self.image_login.pos = (self.display_rect.w / 2, 150)


    def loguearse(self):
        if self.input_correo_login.get_text() == '':
            self.Mini_GUI_manager.add(
                mini_GUI.simple_popup(self.display_rect.size, 'bottomright', 'Correo', 'Ingrese el correo', (250, 90))
            )
            return
        if self.input_contraseña_login.get_text() == '':
            self.Mini_GUI_manager.add(
                mini_GUI.simple_popup(self.display_rect.size, 'bottomright', 'Contraseña', 'Ingrese la contraseña', (250, 90))
            )
            return

        correo = self.input_correo_login.get_text()
        contraseña = self.input_contraseña_login.get_text()
        try:
            self.loading = True
            r = self.Base_de_datos.login(correo, contraseña)
            if r:
                self.correo = self.input_correo_login.get_text()
                self.contraseña = self.input_contraseña_login.get_text()
                self.Mini_GUI_manager.add(
                    mini_GUI.simple_popup(self.display_rect.size, 'bottomright', 'Exito', 'Se a logueado exitosamente', (250, 100))
                )
                self.save_json()
                self.go_to_productos()
            else:
                self.Mini_GUI_manager.add(
                    mini_GUI.simple_popup(self.display_rect.size, 'bottomright', 'Fallo', 'Usuario o contraseña incorrectos', (250, 100))
                )
        except (requests.ConnectionError,requests.ConnectTimeout,requests.ReadTimeout):
                self.Mini_GUI_manager.add(
                    mini_GUI.simple_popup(self.display_rect.size, 'bottomright', 'Error', 'Verifique su conexion a internet', (250, 100))
                )
        finally:
            self.loading = False

    def actualizar_tarjetas_productos(self):
        self.tarjetas_productos.clear()
        self.desplazamiento = 0
        self.loading = True
        lista = self.Base_de_datos.buscar(randomnautica='productos',limit=200)
        self.loading = False
        for i,x in enumerate(lista[:self.max_pag_productos]):
            self.tarjetas_productos.append(Tarjeta(self.centros_tarjetas_productos[i],(140,200+50),'center',self.Base_de_datos.download_image(x['imagen']),x['nombre'],x['stock'],(34,34,34)))
        self.tarjetas_productos_altura_max = self.tarjetas_productos[-1].bottom


    def func_toggle_autologin(self):
        self.autolog = not self.autolog
        self.btn_login_autologin.text = '' if self.autolog else ''
        self.save_json()
    def go_to_productos(self):
        self.screen_login_bool = False
        self.screen_productos_bool = True
        # self.actualizar_tarjetas_productos()
        # self.Func_pool.start('actualizar_tarjetas_productos')

    def go_to_login(self):
        self.screen_productos_bool = False
        self.screen_login_bool = True

    def eventos_en_comun(self, eventos):
        for evento in eventos:
            if evento.type == QUIT or evento.type == pag.WINDOWCLOSE:
                pag.quit()
                self.Func_pool.stop_all()
                sys.exit()
            elif evento.type == WINDOWMINIMIZED:
                self.drawing = False
                return True
            elif evento.type == WINDOWFOCUSLOST:
                self.framerate = 30 if not self.low_detail_mode else 5
                return True
            elif evento.type in [WINDOWTAKEFOCUS, WINDOWFOCUSGAINED, WINDOWMAXIMIZED]:
                self.framerate = 60 if not self.low_detail_mode else 30
                self.drawing = True
                return True
            elif evento.type in [pag.WINDOWRESIZED,pag.WINDOWMAXIMIZED,pag.WINDOWSIZECHANGED,pag.WINDOWMINIMIZED]:
                size = pag.display.get_window_size()
                self.ventana = pag.display.set_mode(size, pag.RESIZABLE)
                self.ventana_rect = self.ventana.get_rect()

                self.display = pag.Surface(self.ventana_rect.size)
                self.display_rect = self.display.get_rect()

                self.move_objs()
            elif evento.type == pag.WINDOWSHOWN or evento.type == pag.WINDOWMOVED:
                size = pag.display.get_window_size()
                self.ventana = pag.display.set_mode(size, pag.RESIZABLE)
                self.ventana_rect = self.ventana.get_rect()

                self.display = pag.Surface(self.ventana_rect.size)
                self.display_rect = self.display.get_rect()

                self.move_objs()
            return False

    def screen_login(self):
        if self.screen_login_bool:
            self.cicle_try = 0
        while self.screen_login_bool:
            self.relog.tick(self.framerate)

            mx, my = pag.mouse.get_pos()
            eventos = pag.event.get()
            self.eventos_en_comun(eventos)

            if self.loading:
                eventos.clear()

            self.GUI_manager.input_update(eventos)
            for x in self.list_login_input:
                x.eventos_teclado(eventos)
            for evento in eventos:
                if self.GUI_manager.active >= 0:
                    if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                        self.GUI_manager.pop()
                    elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                        self.GUI_manager.click((mx, my))
                elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                    self.screen_login_bool = False
                elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                    if self.Mini_GUI_manager.click(evento.pos):
                        continue
                    for x in self.list_login_click:
                        if x.click((mx, my)):
                            break
                elif evento.type == MOUSEBUTTONDOWN and evento.button == 2:
                    if self.Mini_GUI_manager.click(evento.pos):
                        continue

            self.fondo_login.draw(self.display)
            self.display.blit(self.cuadrado_transparente_login, (self.display_rect.w / 4, self.display_rect.h / 20))

            for x in self.list_login_draw:
                x.draw(self.display)

            self.Mini_GUI_manager.draw(self.display, (mx, my))

            if self.loading:
                # pag.draw.rect(self.ventana,'darkgrey',[295,180,240,230],0,20)
                # pag.draw.rect(self.ventana,'black',[295,180,240,230],3,20)
                self.engranajes[0].angle += 1
                self.engranajes[1].angle -= 1
                self.engranajes[2].angle += 2

                self.engranajes[0].draw(self.display)
                self.engranajes[1].draw(self.display)
                self.engranajes[2].draw(self.display)
            self.ventana.blit(self.display,(0,0))
            pag.display.flip()

    def screen_productos(self):
        if self.screen_productos_bool:
            self.cicle_try = 0
            self.Func_pool.start('actualizar_tarjetas_productos')
        while self.screen_productos_bool:
            self.relog.tick(self.framerate)

            mx, my = pag.mouse.get_pos()
            eventos = pag.event.get()
            self.eventos_en_comun(eventos)

            if self.loading:
                eventos.clear()

            self.GUI_manager.input_update(eventos)
            for x in self.list_productos_input:
                x.eventos_teclado(eventos)
            for evento in eventos:
                if self.GUI_manager.active >= 0:
                    if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                        self.GUI_manager.pop()
                    elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                        self.GUI_manager.click((mx, my))
                elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                    self.screen_productos_bool = False
                elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                    if self.Mini_GUI_manager.click(evento.pos):
                        continue
                    for x in self.list_productos_click:
                        if x.click((mx, my)):
                            break
                elif evento.type == MOUSEBUTTONDOWN and evento.button == 2:
                    if self.Mini_GUI_manager.click(evento.pos):
                        continue
                elif evento.type == pag.MOUSEWHEEL:
                    self.desplazamiento += evento.y*10
                    if self.tarjetas_productos_altura_max<self.ventana_rect.h-200:
                        self.desplazamiento -= evento.y*10
                    elif self.desplazamiento>0:
                        self.desplazamiento = 0
                    elif self.desplazamiento<-self.centros_tarjetas_productos[-1][1]+300:
                        self.desplazamiento = -self.centros_tarjetas_productos[-1][1]+300
                    print(self.desplazamiento,-self.centros_tarjetas_productos[-1][1])
                    # elif self.desplazamiento>self.centros_tarjetas_productos[-1][1]:
                    #     self.desplazamiento = -self.centros_tarjetas_productos[-1][1]

                    for i, x in enumerate(self.tarjetas_productos[:self.max_pag_productos]):
                        x.pos = pag.Vector2(self.centros_tarjetas_productos[i])+(0,self.desplazamiento)

            self.display.fill((20, 20, 20))

            for x in [*self.tarjetas_productos]:
                x.draw(self.display)

            pag.draw.rect(self.display, (34, 34, 34), [0, 0, self.display_rect.w, self.btn_header_inicio.bottom])
            pag.draw.line(self.display, (78, 78, 78), [0, self.btn_header_inicio.bottom], [self.display_rect.w, self.btn_header_inicio.bottom])

            for x in [*self.list_productos_draw,*self.list_header_draw]:
                x.draw(self.display)

            self.Mini_GUI_manager.draw(self.display, (mx, my))

            if self.loading:
                # pag.draw.rect(self.ventana,'darkgrey',[295,180,240,230],0,20)
                # pag.draw.rect(self.ventana,'black',[295,180,240,230],3,20)
                self.engranajes[0].angle += 1
                self.engranajes[1].angle -= 1
                self.engranajes[2].angle += 2

                self.engranajes[0].draw(self.display)
                self.engranajes[1].draw(self.display)
                self.engranajes[2].draw(self.display)

            self.ventana.blit(self.display,(0,0))
            pag.display.flip()




if __name__ == '__main__':
    print('Iniciando')
    # print(requests.post('http://localhost/Proyecto-UPTAEB-T2/Controller/funcs_ajax/login.php',
    #                     {'correo': 'nose@gmail.com', 'contraseña': 12345}
    #                     ).text)
    clase = Programa()
