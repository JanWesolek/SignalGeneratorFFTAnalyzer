import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QLineEdit, QLayout, QComboBox, QDoubleSpinBox, QMessageBox, QAction, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem
import pyqtgraph as pg
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import pandas as pd

class Krenarator:
    def __init__(self, f, t, A, typ_generowanego_przebiegu, nazwa_pliku):
        self.f = f
        self.t = t
        self.A = A
        self.sampling = 44100
        self.typ_generowanego_przebiegu = typ_generowanego_przebiegu
        self.nazwa_pliku = nazwa_pliku
        self.time = np.linspace(0, self.t, int(self.t * self.sampling))

    def f_get(self):
        return self.f

    def t_get(self):
        return self.t

    def typ_generowanego_przebiegu_get(self):
        return self.typ_generowanego_przebiegu

    def nazwa_pliku_get(self):
        return self.nazwa_pliku

    def f_set(self, new_f):
        self.f = new_f

    def t_set(self, new_t):
        self.t = new_t

    def typ_generowanego_przebiegu_set(self, new_typ_generowanego_przebiegu):
        self.typ_generowanego_przebiegu = new_typ_generowanego_przebiegu

    def nazwa_pliku_set(self, new_nazwa_pliku):
        self.nazwa_pliku = new_nazwa_pliku

    def update_time(self):
        self.time = np.linspace(0, self.t, int(self.t * self.sampling))

    def funkcja(self):
        if self.typ_generowanego_przebiegu == "sine":
            data = self.A * np.sin(2 * np.pi * self.f * self.time)
        elif self.typ_generowanego_przebiegu == "square":
            data = self.A*np.sign(np.sin(2*np.pi * self.f * self.time))
        elif self.typ_generowanego_przebiegu == "sawtooth":
            data  = 2 * self.A / np.pi * np.arctan(np.tan(2 * np.pi * self.f * self.time))
        elif self.typ_generowanego_przebiegu == "triangle":
            data = 2 * self.A / np.pi * np.arcsin(np.sin(2 * np.pi * self.f * self.time))
        elif self.typ_generowanego_przebiegu == "whitenoise":
            data = self.A * (np.random.rand(int(self.t*self.sampling)))
        return data

    def Zapis_przebieg_czasowy(self):
        nazwa_pliku_csv = self.nazwa_pliku + "_przebieg.csv"
        dataframe = pd.DataFrame(self.funkcja())  # tworzy pandas dataframe
        dataframe.to_csv(nazwa_pliku_csv, index=False, sep="\t")

    def Zapis_plik_audio(self):
        audio_data = np.int16(self.funkcja() * 2 ** 15)
        nazwa_pliku_wav = self.nazwa_pliku + "_audio.wav"
        write(nazwa_pliku_wav, self.sampling, audio_data)

    def TranformataFouriera(self):
        N = len(self.time)
        dtime = self.time[1] - self.time[0]
        yf = 2.0 / N * np.abs(np.fft.fft(self.funkcja())[0:N // 2])
        xf = np.fft.fftfreq(N, d=dtime)[0:N // 2]
        return xf, yf

    def ZapisTranformataFouriera(self):
        N = len(self.time)
        dtime = self.time[1] - self.time[0]
        yf = 2.0 / N * np.abs(np.fft.fft(self.funkcja())[0:N // 2])
        xf = np.fft.fftfreq(N, d=dtime)[0:N // 2]
        nazwa_pliku_transformata = self.nazwa_pliku + "_transformata.csv"
        dataframe = pd.DataFrame(yf)  # tworzy pandas dataframe
        dataframe.to_csv(nazwa_pliku_transformata, index=False, sep="\t")


   

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Przebiegi Czasowe w PyQt5")
        self.f = 4
        self.t = 4
        self.A = 3
        self.typ_generowanego_przebiegu = "triangle"
        self.nazwa_pliku = "pies"
        self.tester = Krenarator(self.f, self.t, self.A, self.typ_generowanego_przebiegu, self.nazwa_pliku)
        self.sprawdzacz = 0
        
        self.tytul = QLabel()
        self.tytul.setText("Przebiegi Czasowe:")
        font = QFont("Arial", 20)  # Nazwa czcionki i rozmiar
        self.tytul.setFont(font)
        self.tytul.setAlignment(Qt.AlignCenter)
        

        #Do tworzenia przebiegów:
        self.tworzenie = QLabel()
        self.tworzenie.setText("Wybierz wszystkie dane:")
        
        #częstotliwość
        self.f_label = QLabel()
        self.f_label.setText("Częstotliwość przebiegu:")
        self.f_spin = QDoubleSpinBox()
        self.f_spin.setRange(0, 40000)  # Zakres od 0 do 100
        self.f_spin.setSingleStep(100)  # Krok zmiany wartości
        self.f_spin.setValue(0.0)

        #czas
        self.t_label = QLabel()
        self.t_label.setText("Czas przebiegu:")
        self.t_spin = QDoubleSpinBox()
        self.t_spin.setRange(0, 100)  # Zakres od 0 do 100
        self.t_spin.setSingleStep(1)  # Krok zmiany wartości
        self.t_spin.setValue(0.0)

        #czas
        self.A_label = QLabel()
        self.A_label.setText("Amplituda przebiegu:")
        self.A_spin = QDoubleSpinBox()
        self.A_spin.setRange(0, 100)  # Zakres od 0 do 100
        self.A_spin.setSingleStep(0.1)  # Krok zmiany wartości
        self.A_spin.setValue(0.0)

        #typ przebiegu
        self.typ_label = QLabel()
        self.typ_label.setText("Typ przebiegu czasowego:")
        self.typ_combo = QComboBox()
        self.typ_combo.addItem("sine")
        self.typ_combo.addItem("square")
        self.typ_combo.addItem("sawtooth")
        self.typ_combo.addItem("triangle")
        self.typ_combo.addItem("whitenoise")

        #nazwa
        self.name_label = QLabel()
        self.name_label.setText("Nazwa pliku:")
        self.name_text = QLineEdit()

        #przycisk tworzenia:
        self.tworzenie_button = QPushButton()
        self.tworzenie_button.setText("Generuj przebiegi:")
        self.tworzenie_button.clicked.connect(self.generuj)

        #Wykres przebieg
        self.tytul_wykres1 = QLabel()
        self.tytul_wykres1.setText("Wykres przebiegu czasowego:")
        self.graph1 = pg.PlotWidget()
        
        x = np.linspace(0, 360, 400)
        y = 0 * x
        self.graph1.plot(x,y)
        #y = np.sin(x / 360 * np.pi * 2)
        #pen = pg.mkPen(color=(255,128,0), width=2)
        #self.plot1 = self.graph1.plot(x, y)
        self.graph1.hide()


        #Wykres transformata fouriera
        self.tytul_wykres2 = QLabel()
        self.tytul_wykres2.setText("Wykres transformaty Fouriera:")
        self.graph2 = pg.PlotWidget()
        self.graph2.plot(x,y)
        self.graph2.hide()

        #Zapis przebiegu do wav
        self.zapis_wav = QPushButton()
        self.zapis_wav.setText("Zapisz do .wav")
        self.zapis_wav.clicked.connect(self.funkcja_zapis_wav)

        #Zapis do pliku csv
        self.zapis_csv = QPushButton()
        self.zapis_csv.setText("Zapisz przebieg do .csv")
        self.zapis_csv.clicked.connect(self.funkcja_zapis_csv)

        #Zapis do pliku csv
        self.zapis_transformata_csv = QPushButton()
        self.zapis_transformata_csv.setText("Zapisz transformatę do .csv")
        self.zapis_transformata_csv.clicked.connect(self.funkcja_zapis_transformata_csv)
        
        #Tabela z danymi
        self.table = QTableWidget()
        self.table.setRowCount(2)
        self.table.setColumnCount(2)
        self.table.setItem(0, 0, QTableWidgetItem("Dziedzina"))
        self.table.setItem(0, 1, QTableWidgetItem("Zbiór wartości"))
        

        #ustawienie nowych danych
        #x = np.linspace(0, 360, 20)
        #y = np.cos(x /360 * np.pi * 2 + 0.15 * np.random.rand(len(x)))
        #self.plot.setData(x,y)

        #Informacje:
        self.info_label = QLabel()
        self.info_label.setText("Tutaj będę wyświetlały się ewentualne błędy.")


        #layouty
        layout = QGridLayout()
        layout1 = QGridLayout()
        layout2 = QVBoxLayout()
        
        layout1.addWidget(self.tworzenie, 1, 0, 1, 2)
        layout2.addWidget(self.tytul_wykres1)
        layout1.addWidget(self.f_label, 2, 0, 1, 1)
        layout1.addWidget(self.f_spin, 2, 1, 1, 2)
        layout2.addWidget(self.graph1)
        layout1.addWidget(self.t_label, 3, 0, 1, 1)
        layout1.addWidget(self.t_spin, 3, 1, 1, 2)
        layout1.addWidget(self.A_label, 4, 0, 1, 1)
        layout1.addWidget(self.A_spin, 4, 1, 1, 2)
        layout1.addWidget(self.typ_label, 5, 0, 1, 1)
        layout1.addWidget(self.typ_combo, 5, 1, 1, 2)
        layout1.addWidget(self.name_label, 6, 0, 1, 1)
        layout1.addWidget(self.name_text, 6, 1, 1, 2)
        layout1.addWidget(self.tworzenie_button, 7, 0, 1, 3)
        layout2.addWidget(self.tytul_wykres2)
        layout2.addWidget(self.graph2)
        layout1.addWidget(self.zapis_wav, 8, 0, 1, 1)
        layout1.addWidget(self.zapis_csv, 8, 1, 1, 1)
        layout1.addWidget(self.zapis_transformata_csv, 8, 2, 1, 1)
        layout1.addWidget(self.info_label, 9, 0, 1, 4)
        layout1.addWidget(self.table, 10, 0, 1, 4)

        layout.addWidget(self.tytul, 0, 0, 1, 2)
        layout.addLayout(layout1, 1, 0, 1, 1)
        layout.addLayout(layout2, 1, 1, 1, 1)
        
        self.setLayout(layout)

        self.show()        
    
    def generuj(self):
        tester = 0
        if self.f_spin.value() > 0:
            if self.t_spin.value().is_integer():
                if self.t_spin.value() > 0:
                    if self.A_spin.value() > 0:
                        if self.name_text.text().strip(): # Sprawdzanie, czy nazwa jest niepusta
                            self.f = self.f_spin.value()
                            self.t = self.t_spin.value()
                            self.A = self.A_spin.value()
                            self.typ_generowanego_przebiegu = self.typ_combo.currentText()
                            self.nazwa_pliku = self.name_text.text()

                            self.tester = Krenarator(self.f, self.f, self.A, self.typ_generowanego_przebiegu, self.nazwa_pliku)
                            self.x = self.tester.time
                            self.y = self.tester.funkcja()

                            # Wyczyszczenie istniejącego wykresu
                            self.graph1.clear()
                            self.graph2.clear()



                            self.graph1.plot(self.x, self.y, pen='g')
                            self.graph1.setRange(xRange=(0, min(0.1, self.x[-1])), yRange=(-1.2 * self.A, 1.2 * self.A))
                            self.graph1.showGrid(x=True, y=True, alpha=0.5)
                            self.graph1.getPlotItem().layout.setContentsMargins(10, 10, 10, 10)
                            self.graph1.setFixedSize(600, 300)
                            self.graph1.setLabel('left', 'Amplituda', units='V')  # Etykieta osi Y
                            self.graph1.setLabel('bottom', 'Czas', units='s')    # Etykieta osi X

                            
                            if self.typ_combo.currentText() == "whitenoise":
                                self.table.setItem(1, 1, QTableWidgetItem(f"[0,{self.A}]"))
                            else:
                                self.table.setItem(1, 1, QTableWidgetItem(f"[-{self.A},{self.A}]"))
                            self.table.setItem(1, 0, QTableWidgetItem(f"[0;{self.t}]"))
                            
                            
                            

                            xf, yf = self.tester.TranformataFouriera()
                            self.graph2.plot(xf, yf, pen='b')
                            self.graph2.showGrid(x=True, y=True, alpha=0.5)
                            self.graph2.getPlotItem().layout.setContentsMargins(10, 10, 10, 10)
                            self.graph2.setFixedSize(600, 300)
                            self.graph2.setLabel('left', 'Amplituda', units='')  # Etykieta osi Y
                            self.graph2.setLabel('bottom', 'Częstotliwość', units='Hz')  # Etykieta osi X

                             #dodać, żeby renderowało się w czasie od 0 do 0.1
                            self.graph1.show()
                            self.graph2.show()

                            #zrobić resztę instrukcji i wyświetlanie rzeczy w oknie informacji

                            self.sprawdzacz = 1
                            tester = 1
        if tester == 0:
            self.info_label.setText("Wpisz poprawne wartości, żeby stworzyć przebieg i jego transformatę.")
        elif tester == 1:
            self.info_label.setText("Utworzono przebieg i transformatę Fouriera.")

    
    def funkcja_zapis_wav(self):
        if self.sprawdzacz == 1:
            self.tester.Zapis_plik_audio()
            self.info_label.setText("Utworzono plik audio z przebiegiem funkcji.")
            print("działa wav")
        else:
            self.info_label.setText("Zanim zapiszesz, musisz najpier stworzyć przebieg.")

    def funkcja_zapis_csv(self):
        if self.sprawdzacz == 1:
            self.tester.Zapis_przebieg_czasowy()
            print("działa csv")
            self.info_label.setText("Utworzono plik csv z przebiegiem funkcji.")
        else:
            self.info_label.setText("Zanim zapiszesz, musisz najpierw stworzyć przebieg.")
    
    def funkcja_zapis_transformata_csv(self):
        if self.sprawdzacz == 1:
            self.tester.ZapisTranformataFouriera()
            print("działa transformata csv")
            self.info_label.setText("Utworzono plik csv z transformatą fouriera przebiegu.")
        else:
            self.info_label.setText("Zanim zapiszesz, musisz najpierw stworzyć przebieg.")
    
app = QApplication(sys.argv)
ex = App()
app.exec_()