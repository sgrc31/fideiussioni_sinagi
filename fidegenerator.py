#!/usr/bin/env python3

import sys
import time
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMessageBox
from PyQt5 import uic
from reportlab.lib import utils
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

stili = getSampleStyleSheet()
stili.add(ParagraphStyle(name='testo_standard',
                         fontName='Times-Roman',
                         fontSize=12,
                         leading=19,
                         alignment=TA_JUSTIFY
                         )
          )


def get_resized_img(path, width=10*mm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def nome_titolare_to_file(titolare):
    return titolare.strip().lower().replace('\'', '').replace(' ', '')

def intestazione_sinagi(lista_doc):
    acronimo = Paragraph('<para alignment=center fontsize=22 spacea=15><strong>SI.NA.G.I</strong></para>', stili['testo_standard'])
    titolo = Paragraph('<para alignment=center fontsize=16 spacea=15><strong>Sindacato Nazionale Giornalai d\'Italia</strong></para>', stili['testo_standard'])
    segreteria = Paragraph('<para alignment=center fontsize=14 spaceb=10 spacea=1><strong>Segreteria Interprovinciale Area Marche</strong></para>', stili['testo_standard'])
    contatti1 = Paragraph('<para leftindent=30>Sede via Macerata, 1 - 60128 Ancona - tel. 347 6933948 - fax 071 7200973</para>', stili['testo_standard'])
    contatti2 = Paragraph('<para leftindent=30><i>Sito</i>: <a href=http://www.sinagi.it color=blue>www.sinagi.it</a></para>', stili['testo_standard'])
    contatti3 = Paragraph('<para leftindent=30 spacea=20><i>Email</i>: <a href=mailto:ancona@sinagi.it>ancona@sinagi.it</a>', stili['testo_standard'])
    logo = get_resized_img('logo.jpg', width=50*mm)
    logo.hAlign = 'CENTER'
    lista_doc.extend((acronimo, titolo, logo, segreteria, contatti1, contatti2, contatti3))
    return lista_doc

def explicit(lista_doc, data_firma):
    firma = get_resized_img('xfirmaGS.jpeg', width=50*mm)
    firma.hAlign = 'RIGHT'
    autorita = Paragraph('<para align=right>Il segratario provinciale</para>', stili['testo_standard'])
    nome_autorita = Paragraph('<para align=right><strong>Sandro Guercio</strong></para>', stili['testo_standard'])
    data = Paragraph('Ancona, {}'.format(data_firma), stili['testo_standard'])
    lista_doc.extend((data, autorita, nome_autorita, firma))
    return lista_doc

def bolkestein(comune, indirizzo, titolare, sesso_titolare, data_firma):
    canovaccio = []
    testo = '''
<para spacea=35>Con la presente si attesta che il comune di {} ha recepito
la direttiva Bolkestein (D.Lgs.n.59/2010) e pertanto {} {} 
avvia una nuova attività di rivendita di giornali e riviste
a {} in via {}, dietro presentazione di SCIA agli Uffici
Comunali Competenti.</para>
'''.format(comune, 'il Sig.' if sesso_titolare == 'm' else 'la Sig.ra', titolare, comune, indirizzo)
    doc = SimpleDocTemplate('{}_bolkestein.pdf'.format(nome_titolare_to_file(titolare)),
                            pagesize=A4,
                            rightMargin=25*mm,
                            leftMargin=25*mm,
                            topMargin=25*mm,
                            bottomMargin=25*mm)
    intestazione_sinagi(canovaccio)
    canovaccio.append(Paragraph('<para align=right>Allegato A</para>', stili['testo_standard']))
    canovaccio.append(Paragraph('<para align=center spacea=20><strong>DICHIARAZIONE</strong></para>', stili['testo_standard']))
    canovaccio.append(Paragraph(testo, stili['testo_standard']))
    explicit(canovaccio, data_firma)
    doc.build(canovaccio)

def iscrizione(comune, indirizzo, titolare, sesso_titolare, data_firma):
    canovaccio = []
    testo = '''
<para spacea=35>Con la presente si attesta che {}, gestore della rivendita di quotidiani
e periodici sita a {}, in {} è iscritt{} alla struttura territoriale di
Ancona di questo Sindacato.</para>
'''.format(titolare, comune, indirizzo, 'o' if sesso_titolare == 'm' else 'a')
    doc = SimpleDocTemplate('{}_iscrizione.pdf'.format(nome_titolare_to_file(titolare)),
                            pagesize=A4,
                            rightMargin=25*mm,
                            leftMargin=25*mm,
                            topMargin=25*mm,
                            bottomMargin=25*mm)
    intestazione_sinagi(canovaccio)
    canovaccio.append(Paragraph('<para align=center spacea=20><strong>DICHIARAZIONE</strong></para>', stili['testo_standard']))
    canovaccio.append(Paragraph(testo, stili['testo_standard']))
    explicit(canovaccio, data_firma)
    doc.build(canovaccio)

def modello_a(comune, indirizzo, titolare, extitolare, n_vecchia_autorizzazione, data_vecchia_autorizzazione, stato_procedura, data_firma):
    canovaccio = []
    testo = '''
Con la presente si attesta che il comune di {} ha recepito la
direttiva Bolkestein (D.Lgs.n.59/2010) e che, per quanto a nostra conoscenza,
nulla osta al subentro di {} nella titolarità dell'autorizzazione n. {} del {}
per la vendita di quotidiani e periodici già rilasciata a {} relativa al punto
vendita a carattere permanente, ubicato a {} in {}.
'''.format(comune, titolare, n_vecchia_autorizzazione, data_vecchia_autorizzazione, extitolare, comune, indirizzo)
    testo_procedura_perfezionata = '''
Si attesta inoltre che la suddetta procedura deve intendersi perfezionata
con l'avvenuto subentro senza rilascio da parte del Comune di una nuova
autorizzazione/licenza intestata al subentrante.
'''
    testo_procedura_da_perfezionare = '''
Si attesta inoltre che la suddetta procedura sarà perfezionata previo rilascio
da parte del Comune, nei tempi da esso previsti, di una nuova autorizzazione/licenza
intestata al subentrante
'''
    testo2 = '''
<para spacea=35>Il sottoscritto si impegna a comunicare tempestivamente
eventuali dinieghi al subentro da parte delle preposte autorità comunali.</para>
'''
    doc = SimpleDocTemplate('{}_modello_a.pdf'.format(nome_titolare_to_file(titolare)),
                            pagesize=A4,
                            rightMargin=25*mm,
                            leftMargin=25*mm,
                            topMargin=25*mm,
                            bottomMargin=25*mm)
    intestazione_sinagi(canovaccio)
    canovaccio.append(Paragraph('<para align=right>Allegato A</para>', stili['testo_standard']))
    canovaccio.append(Paragraph('<para align=center spacea=20><strong>DICHIARAZIONE</strong></para>', stili['testo_standard']))
    canovaccio.append(Paragraph(testo, stili['testo_standard']))
    canovaccio.append(Paragraph(testo_procedura_perfezionata if stato_procedura == 1 else testo_procedura_da_perfezionare, stili['testo_standard']))
    canovaccio.append(Paragraph(testo2, stili['testo_standard']))
    explicit(canovaccio, data_firma)
    doc.build(canovaccio)

def permanente(comune, indirizzo, titolare, data_firma):
    canovaccio = []
    testo = '''
<para spacea=35>Con la presente si attesta che la rivendita di quotidiani e periodici sita
a {} in {}, gestita da {} è a carattere permanente.</para>
'''.format(comune, indirizzo, titolare)
    doc = SimpleDocTemplate('{}_permanente.pdf'.format(nome_titolare_to_file(titolare)),
                            pagesize=A4,
                            rightMargin=25*mm,
                            leftMargin=25*mm,
                            topMargin=25*mm,
                            bottomMargin=25*mm)
    intestazione_sinagi(canovaccio)
    canovaccio.append(Paragraph('<para align=center spacea=20><strong>DICHIARAZIONE</strong></para>', stili['testo_standard']))
    canovaccio.append(Paragraph(testo, stili['testo_standard']))
    explicit(canovaccio, data_firma)
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
        self.pushButton.clicked.connect(self.raccogli_variabili)
        self.date_vecchialicenza.setDateTime(QDateTime.currentDateTime())
        self.date_firma.setDateTime(QDateTime.currentDateTime())
        self.setWindowTitle('SINAGI - genera fideiussioni')
        self.show()

    def warning_campo_vuoto(self):
        self.warning = QMessageBox()
        self.warning.setText('Accertarsi di aver compilato tutti i campi')
        self.warning.setWindowTitle('Warning')
        self.warning.setStandardButtons(QMessageBox.Ok)
        self.warning.exec_()

    def warning_stesse_date(self):
        self.warning2 = QMessageBox()
        self.warning2.setText('Le date non possono coincidere, accertarsi di aver inserito le date corrette')
        self.warning2.setWindowTitle('Attenzione')
        self.warning2.setStandardButtons(QMessageBox.Ok)
        self.warning2.exec_()

    def raccogli_variabili(self):
        if all((self.line_comune.text(),
                self.line_extitolare.text(),
                self.line_indirizzo.text(),
                self.line_nlicenza.text(),
                self.line_titolare.text()
                )):
            self.titolare = self.line_titolare.text()
            self.comune = self.line_comune.text()
            self.indirizzo = self.line_indirizzo.text()
            self.ex_titolare = self.line_extitolare.text()
            self.n_licenza = self.line_nlicenza.text()
        else:
            return self.warning_campo_vuoto()
        if self.date_vecchialicenza.date() == self.date_firma.date():
            return self.warning_stesse_date()
        else:
            self.data_licenza = self.date_vecchialicenza.date().toString('dd/MM/yy')
            self.data_firma = self.date_firma.date().toString('dd/MM/yyyy')
        if self.radio_sessom.isChecked():
            self.sesso_titolare = 'm'
        else:
            self.sesso_titolare = 'f'
        if self.radio_perfezionata.isChecked():
            self.stato_procedura = 1
        else:
            self.stato_procedura = 0
        self.genera_documenti()

    def genera_documenti(self):
        bolkestein(self.comune,
                   self.indirizzo,
                   self.titolare,
                   self.sesso_titolare,
                   self.data_firma
                   )
        self.progressBar.setValue(25)
        iscrizione(self.comune,
                   self.indirizzo,
                   self.titolare,
                   self.sesso_titolare,
                   self.data_firma
                   )
        self.progressBar.setValue(50)
        permanente(self.comune,
                   self.indirizzo,
                   self.titolare,
                   self.data_firma
                   )
        self.progressBar.setValue(75)
        modello_a(self.comune,
                  self.indirizzo,
                  self.titolare,
                  self.ex_titolare,
                  self.n_licenza,
                  self.data_licenza,
                  self.stato_procedura,
                  self.data_firma
                  )
        self.progressBar.setValue(100)


################
##  Start it  ##
################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWin()
    sys.exit(app.exec_())
