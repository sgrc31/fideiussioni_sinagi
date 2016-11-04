#!/usr/bin/env python3

import sys
import time
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QCalendarWidget, QHBoxLayout, QVBoxLayout, QDialog, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import QDate
from PyQt5 import uic
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

stili = getSampleStyleSheet()
stili.add(ParagraphStyle(name='testo_standard',
                         fontName='Times-Roman',
                         fontSize=12,
                         leading=15,
                         alignment=TA_JUSTIFY
                         )
          )


def get_resized_img(path, width=10*mm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def intestazione_sinagi(lista_doc):
    acronimo = Paragraph('<para alignment=center fontsize=22 leading=30><strong>SI.NA.GI</strong></para>', stili['testo_standard'])
    titolo = Paragraph('<para alignment=center fontsize=18 leading=30><strong>Sindacato Nazionale Giornalai d\'Italia</strong></para>', stili['testo_standard'])
    segreteria = Paragraph('<para alignment=center fontsize=18 leading=20><strong>Segreteria Interprovinciale Area Marche</strong></para>', stili['testo_standard'])
    contatti1 = Paragraph('Sede via Macerata, 1 - 60128 Ancona - tel. 347 6933948 - fax 071 7200973', stili['testo_standard'])
    contatti2 = Paragraph('Sito: <a href=http://www.sinagi.it color=blue>www.sinagi.it</a> <a href=http://www.edicoleinrete.eu color=blue>www.edicoleinrete.eu</a>', stili['testo_standard'])
    contatti3 = Paragraph('Email: ancona@sinagi.it', stili['testo_standard'])
    logo = get_resized_img('logo.jpg', width=50*mm)
    logo.hAlign = 'CENTER'
    lista_doc.extend((acronimo, titolo, logo, segreteria, contatti1, contatti2, contatti3))
    return lista_doc

def explicit(lista_doc):
    firma = get_resized_img('xfirmaGS.jpeg', width=50*mm)
    firma.hAlign = 'RIGHT'
    autorita = Paragraph('Il segratario provinciale', stili['testo_standard'])
    nome_autorita = Paragraph('Sandro Guercio', stili['testo_standard'])
    data = Paragraph('Ancona, {}'.format(time.strftime("%d/%m/%Y")), stili['testo_standard'])
    lista_doc.extend((autorita, nome_autorita, firma, data))
    return lista_doc

def bolkestein(titolare='Tizio', extitolare='Caio', comune='Ancona'):
    canovaccio = []
    testo = '''
Con la presente si attesta che il comune di {} ha recepito
la direttiva Bolkestein (D.Lgs.n.59/2010) e pertanto il Sig. {} 
avvia una nuova attività di rivendita di giornali e riviste
a {} in via {}  dietro presentazione di SCIA agli Uffici
Comunali Competenti.
'''.format(titolare, extitolare, comune, comune)
    doc = SimpleDocTemplate('bolkestein.pdf',
                            pagesize=A4,
                            rightMargin=25*mm,
                            leftMargin=25*mm,
                            topMargin=25*mm,
                            bottomMargin=25*mm)
    intestazione_sinagi(canovaccio)
    canovaccio.append(Paragraph(testo, stili['testo_standard']))
    explicit(canovaccio)
    doc.build(canovaccio)

def altro_pdf():
    doc = SimpleDocTemplate('secondafunzione.pdf',
                            pagesize=A4,
                            rightMargin=25*mm,
                            leftMargin=25*mm,
                            topMargin=25*mm,
                            bottomMargin=25*mm)
    canovaccio = []
    intestazione_sinagi(canovaccio)
    doc.build(canovaccio)


#################
##      UI     ##
#################
class MyWin(QDialog):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.initUI()

    def initUI(self):
        uic.loadUi('ui.ui', self)
        self.show()


################
##  Start it  ##
################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWin()
    sys.exit(app.exec_())
