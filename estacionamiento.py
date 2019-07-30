#importar modulo sistema
import sys
import os
import json
import hashlib
#importar modulo tiempo
import time
#importar modulo Qr
import qrcode
#Importar para escanear qr
import zbar
import numpy as np
import cv2

from PyQt4 import QtCore, QtGui, uic

qtCreatorFile1 = "sesion.ui" # Enter file here.
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)

qtCreatorFile3 = "datachange.ui" # Enter file here.
Ui_MainWindow3, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)

qtCreatorFile2 = "estacionamiento.ui" # Nombre del archivo UI.
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)

class MyDataChange(QtGui.QMainWindow, Ui_MainWindow3):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow3.__init__(self)
        self.setupUi(self)
        #####Para que aparezcan los numeros
        with open('data/datalogin.txt', 'r') as f:
            data = json.loads(f.read())
            dinero = data["Dinero"]
            self.txtdineroph.setText(dinero)
            size = data['Size']
            self.txtsize.setText(size)
            user = data['Username']
            self.txtuser.setText(user)
            webcam = data['Webcam']
            self.comboBox.setCurrentIndex(int(webcam))

        self.comboBox.currentIndexChanged.connect(self.selector)

    def selector(self,i):
        self.changedata('Webcam',str(i))


    def warning(self, title, message, icon):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(icon)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    def changedata(self,key,value):
        with open("data/datalogin.txt", "r") as f:
            data = json.loads(f.read())
            if data[key] == value or value == "":
                return self.warning('Aviso', '{} igual a la anterior o no valida'.format(key), QtGui.QMessageBox.Warning)
            data[key] = u'{}'.format(value)
            print "{} cambiado a {}".format(key, data.get(key))

        with open("data/datalogin.txt", "w") as f:
            f.write(json.dumps(data))

        self.warning('Aviso', '{} cambiado correctamente'.format(key), QtGui.QMessageBox.Information)

    def usuario(self):
        self.usernuevo = str(self.txtuser.text())
        self.changedata('Username',self.usernuevo)
        self.txtuser.clear()

    def passw(self):
        self.passwnuevo = str(self.txtpassw.text())
        self.passwnuevo = hashlib.sha224(str(self.passwnuevo)).hexdigest()
        self.changedata('Password',self.passwnuevo)
        self.txtpassw.clear()

    def dineroph(self):
        self.dinero = str(self.txtdineroph.text())
        self.changedata('Dinero',self.dinero)

    def mas1(self):
        nactual = self.txtdineroph.text()
        self.txtdineroph.setText(str(int(nactual)+1))
    def menos1(self):
        nactual = self.txtdineroph.text()
        self.txtdineroph.setText(str(int(nactual) - 1))

    def size(self):
        self.size = str(self.txtsize.text())
        self.changedata('Size', self.size)

    def mas2(self):
        nactual = self.txtsize.text()
        self.txtsize.setText(str(int(nactual) + 1))
    def menos2(self):
        nactual = self.txtsize.text()
        self.txtsize.setText(str(int(nactual) - 1))

class Estacionamiento(QtGui.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)

        tiempo_st = time.localtime()
        self.lbltime.setText(time.asctime(tiempo_st))
        with open('data/datalogin.txt', 'r') as f:
            data = json.loads(f.read())
            self.tam_playa= data['Size']
            self.dinero_phora = data['Dinero']

        self.cant_autos=0
        self.nticket=0
        self.used_patentes=[0]
        self.patentes=[]
        self.hora_llegada=[]
        self.hora_salida=[]
        self.tickets_usados = []
        self.letras = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        #Abrir datachange.py desde menubar
        self.cambiardatos.setShortcut("Ctrl+D")
        self.cambiardatos.setStatusTip('Cambiar algunos datos')
        self.statusBar()
        self.window3 = MyDataChange()
        self.cambiardatos.triggered.connect(self.window3.show)
        #Actualizar datos
        self.actualizar.setShortcut("f5")
        self.actualizar.setStatusTip('Actualizar')
        self.statusBar()
        self.actualizar.triggered.connect(self.actualizardata)
        #Cerrar Sesion
        self.close.setShortcut("Ctrl+E")
        self.close.setStatusTip('Cerrar Sesion')
        self.statusBar()
        self.close.triggered.connect(self.closesesion)

        self.progresobar(0)

    def closesesion(self):
        window2.hide()
        window.show()
        window.txtpassw.clear()

    def actualizardata(self):
        with open('data/datalogin.txt', 'r') as f:
            data = json.loads(f.read())
            self.tam_playa= data['Size']
            self.dinero_phora = data['Dinero']
            #Actualizar reloj
            tiempo_st = time.localtime()
            self.lbltime.setText(time.asctime(tiempo_st))
            self.progresobar(0)

    def warning(self, title, message):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    def progresobar (self, n):
        self.cant_autos+=n
        if self.cant_autos == 1:
            self.lbl_cant_autos.setText('Hay ' + str(self.cant_autos) + ' auto en la playa de  ' + str(self.tam_playa))
        else:
            self.lbl_cant_autos.setText('Hay ' + str(self.cant_autos) + ' autos en la playa de  ' + str(self.tam_playa))

        self.porcentaje = (100.0*self.cant_autos)/int(self.tam_playa)
        self.barra.setValue(self.porcentaje)


    def generar(self):
        self.patente = str(self.txtpatente.text()).upper()
#########Seguridad para controlar si es una patente (nueva o vieja)
        if len(self.patente) == 6:
            for i in range(3):
                if str(self.patente[i]).lower() not in self.letras:
                    self.warning('Aviso', 'Patente no valida')
                    self.txtpatente.clear()
                    return
            for i in range(3,6):
                try:
                    x = int(self.patente[i])
                except:
                    self.warning('Aviso', 'Patente no valida')
                    self.txtpatente.clear()
                    return
        elif len(self.patente) == 7:
            for i in range(2):
                if str(self.patente[i]).lower() not in self.letras:
                    self.warning('Aviso', 'Patente no valida')
                    self.txtpatente.clear()
                    return
            for i in range(2,5):
                try:
                    x = int(self.patente[i])
                except:
                    self.warning('Aviso', 'Patente no valida')
                    self.txtpatente.clear()
                    return
            for i in range (5,7):
                if str(self.patente[i]).lower() not in self.letras:
                    self.warning('Aviso', 'Patente no valida')
                    self.txtpatente.clear()
                    return
        else:
            self.warning('Aviso', 'Patente no valida')
            return

        if self.patente in self.used_patentes:
            self.warning('Aviso', 'Patente usada')
            self.txtpatente.clear()
            return
##############################

        if (self.cant_autos + 1) > int(self.tam_playa):
            self.warning("Aviso","Playa saturada")
            return

        self.patentes.append(self.patente)

        self.progresobar(1)
        self.txtpatente.clear()
        self.hora_llegada.append(time.localtime())
        self.used_patentes.append(self.patente)
        ####Generar QR
        img = qrcode.make(self.nticket)
        f = open('Qr/'+ str(self.nticket) + '.png', 'wb')
        img.save(f)
        f.close()
        #########
        print('Ticket: {} Patente: {} entro a la playa a los {} segundos'.format(self.nticket, self.patentes[self.nticket], time.mktime(time.localtime())))
        self.nticket += 1
        self.lbl_nticket.setText(str(self.nticket))


    def escanear(self):
        #########Programa que lee qrs
        self.qr = lectorqr()
        print self.qr
##########Seguridad para controlar si el ticket es un numero, si es existente o si esta usado
        try:
            self.ticket = int(self.qr)
        except:
            self.warning('Aviso', 'Ticket no valido')
            return

        if self.ticket >= self.nticket:
            self.warning('Aviso','Ticket no valido')
            return
        elif self.ticket in self.tickets_usados:
            self.warning('Aviso', 'Ticket usado')
            return

        self.used_patentes.remove(self.patentes[self.ticket])
        self.progresobar(-1)
        self.lbl_patente.setText(str(self.patentes[self.ticket]))
        self.tiempo_ingreso = self.hora_llegada[self.ticket]
        self.lbl_ingr_date.setText(str(time.asctime(self.tiempo_ingreso)))

        self.tiempo_egreso= time.localtime()

        self.lbl_egre_date.setText(str(time.asctime(self.tiempo_egreso)))

        print 'Entrada: {} Salida: {}'.format(str(time.mktime(self.tiempo_ingreso)),str(time.mktime(self.tiempo_egreso)))

        self.tiempo_en_playa = time.mktime(self.tiempo_egreso) - time.mktime(self.tiempo_ingreso)
        self.tiempo_en_playa = time.gmtime(self.tiempo_en_playa)

        self.lbl_tplaya.setText(str(self.tiempo_en_playa.tm_yday-1) + ' Dias, ' + str(self.tiempo_en_playa.tm_hour) + ' horas y ' + str(self.tiempo_en_playa.tm_min) + ' minutos.')
        print '{} {}'.format(self.tiempo_en_playa.tm_hour, self.dinero_phora)
        ##De 00:00 a 01:00 siempre cobra la hora, de ahi cada 15 cobra te cobra la hora/4
        self.money = int(self.dinero_phora)
        horas = self.tiempo_en_playa.tm_hour
        minutos = self.tiempo_en_playa.tm_min
        while horas > 0:
            while minutos > 14:
                minutos -= 15
                self.money += int(self.dinero_phora) / 4.0
            horas -= 1
            minutos = 60

        self.lblmoney.setText('$' +  str(self.money))

        self.tickets_usados.append(self.ticket)

def lectorqr():
    #Se fija camara seleccionada
    with open("data/datalogin.txt", "r") as f:
        data = json.loads(f.read())
        webcam = data['Webcam']

    # Inicializar la camara
    capture = cv2.VideoCapture(int(webcam))
    # Cargar la fuente
    font = cv2.FONT_HERSHEY_SIMPLEX

    while 1:
        # Capturar un frame
        val, frame = capture.read()

        if val:
            # Capturar un frame con la camara y guardar sus dimensiones
            frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dimensiones = frame_gris.shape  # 'dimensiones' sera un array que contendra el alto, el ancho y los canales de la imagen en este orden.

            # Convertir la imagen de OpenCV a una imagen que la libreria ZBAR pueda entender
            imagen_zbar = zbar.Image(dimensiones[1], dimensiones[0], 'Y800', frame_gris.tobytes())

            # Construir un objeto de tipo scaner, que permitira escanear la imagen en busca de codigos QR
            escaner = zbar.ImageScanner()

            # Escanear la imagen y guardar todos los codigos QR que se encuentren
            escaner.scan(imagen_zbar)

            for codigo_qr in imagen_zbar:
                loc = codigo_qr.location  # Guardar las coordenadas de las esquinas
                dat = codigo_qr.data[:-2]  # Guardar el mensaje del codigo QR. Los ultimos dos caracteres son saltos de linea que hay que eliminar
                # Convertir las coordenadas de las cuatro esquinas a un array de numpy
                cv2.destroyAllWindows()
                return codigo_qr.data


            # Mostrar la imagen
            cv2.imshow('Imagen', frame)

        # Salir con 'ESC'
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

class MySesion(QtGui.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)

    # Usuario y Contra
    with open("data/datalogin.txt", "r") as f:
        data = json.loads(f.read())
        user = data.get("Username")
        print user
        passw = data.get("Password")
        print passw

    def iniciar(self):
        self.user_ingresado = self.txtname.text()
        self.password_ingresado = hashlib.sha224(str(self.txtpassw.text())).hexdigest()
        if self.user_ingresado == self.user and self.password_ingresado == self.passw:
            window.hide()
            window2.show()
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setWindowTitle('Atencion')
            msgBox.setText('Username o Password incorrectos')
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window3 = MyDataChange()
    window2 = Estacionamiento()
    window = MySesion()
    window.show()
    sys.exit(app.exec_())
