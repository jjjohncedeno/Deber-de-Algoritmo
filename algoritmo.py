# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tabulate import tabulate
import sys

class Equipo():
    def __init__(self,nombre):
        self.nombre=nombre
        self.totalPuntos=0
        self.Jugados=0
        self.Ganados=0
        self.Empatados=0
        self.Perdidos=0
        self.GolesDiferencia=0
        self.GolesHecho=0
        self.GolesRecibidos=0

    def setDiferencia(self):
        self.GolesDiferencia=self.GolesHecho-self.GolesRecibidos

    def setPuntos(self,num):
        if (num==1):
            self.totalPuntos+=3
            self.Ganados+=1
        elif (num==2):
            self.totalPuntos+=1
            self.Empatados+=1
        else:
            self.Perdidos+=1

        self.Jugados+=1

    def setGoles(self,golH,golR):
        self.GolesHecho+=golH
        self.GolesRecibidos+=golR
        self.setDiferencia()

    def __str__(self):
        return self.nombre + " " + str(self.totalPuntos) + "p, " + str(self.Jugados) + "g (" + str(self.Ganados) + \
               "-" + str(self.Empatados) + "-" + str(self.Perdidos) + "), " + str(self.GolesDiferencia) + "gd (" + \
               str(self.GolesHecho) + "-" + str(self.GolesRecibidos) + ")"

class Partido():
    def __init__(self, E1,G1,G2,E2):
        self.Equipo1=E1
        self.Equipo2=E2
        self.Gol1=int(G1)
        self.Gol2=int(G2)
        self.Iniciar()

    def Iniciar(self):
        if (self.Gol1>self.Gol2):
            self.Equipo1.setPuntos(1)
            self.Equipo2.setPuntos(3)
            self.Equipo1.setGoles(self.Gol1,self.Gol2)
            self.Equipo2.setGoles(self.Gol2,self.Gol1)
        elif (self.Gol1==self.Gol2):
            self.Equipo1.setPuntos(2)
            self.Equipo2.setPuntos(2)
            self.Equipo1.setGoles(self.Gol1,self.Gol2)
            self.Equipo2.setGoles(self.Gol2,self.Gol1)
        else:
            self.Equipo1.setPuntos(3)
            self.Equipo2.setPuntos(1)
            self.Equipo1.setGoles(self.Gol1,self.Gol2)
            self.Equipo2.setGoles(self.Gol2,self.Gol1)


class Torneo():
    def __init__(self, nombre):
        self.Nombre=nombre
        self.Equipos=[]

    def NuevoEquipo(self, Equipo):
        self.Equipos.append(Equipo)

    def setPartido(self,E1,G1,G2,E2):
        P = Partido(E1,G1,G2,E2)

    def __str__(self):
        s = self.Nombre + "\n\n"
        for i in self.Equipos:
            s += str(i) + "\n"
        return s

    def ordenarPorPuntos(self):
        self.heapsort(self.Equipos)

    def ordenarPorDiferencia(self):
        self.quicksort(self.Equipos,0,len(self.Equipos)-1)

    def ordenarPorGoles(self):
        self.radixsort(self.Equipos)

    def buscarEquipo(self,nombre):
        for i in self.Equipos:
            if (nombre == i.nombre):
                return i
        return 0

    def heapsort(self,s):
        sl = len(s)

        def swap(pi, ci):
            if s[pi].totalPuntos > s[ci].totalPuntos:
                s[pi], s[ci] = s[ci], s[pi]

        def sift(pi, unsorted):
            i_gt = lambda a, b: a if s[a].totalPuntos < s[b].totalPuntos else b
            while pi*2+2 < unsorted:
                gtci = i_gt(pi*2+1, pi*2+2)
                swap(pi, gtci)
                pi = gtci
        # heapify
        for i in range(int(sl/2)-1, -1, -1):
            sift(i, sl)
        # sort
        for i in range(sl-1, 0, -1):
            swap(i, 0)
            sift(0, i)
        return s

    def quicksort(L, first, last):
        i = first
        j = last
        pivote = (L[i] + L[j]) / 2

        while i < j:
            while L[i] < pivote:
                i+=1
            while L[j] > pivote:
                j-=1
            if (i <= j):
                x = L[j]
                L[j] = L[i]
                L[i] = x
                i+=1
                j-=1

        if first < j:
            L = quicksort(L, first, j)
        if last > i:
            L = quicksort(L, i, last)

        return L

    def radixsort( aList ):
      RADIX = 10
      maxLength = False
      tmp , placement = -1, 1

      while not maxLength:
        maxLength = True
        # declare and initialize buckets
        buckets = [list() for _ in range( RADIX )]

        # split aList between lists
        for  i in aList:
          tmp = i / placement
          buckets[int(tmp % RADIX)].append( i )
          if maxLength and tmp > 0:
            maxLength = False

        # empty lists into aList array
        a = 0
        for b in range( RADIX ):
          buck = buckets[b]
          for i in buck:
            aList[a] = i
            a += 1

        # move to next digit
        placement *= RADIX
        return aList

def LlenarPartidos(T,soup):
    cont=0
    for i in soup[24:]:
        if (cont == 0):
            list=[]
            list.append(T.buscarEquipo(i.string.replace(" ", "")))
            cont +=1
        elif (cont<3):
            list.append(i.string)
            cont +=1
        else:
            list.append(T.buscarEquipo(i.string.replace(" ", "")))
            T.setPartido(list[0],list[1],list[2],list[3])
            list=[]
            cont=0

def LlenarEquipos(T,soup):
    for i in soup[:12]:
        T.NuevoEquipo(Equipo(i.string.replace(' ', '')))

url="http://www.eluniverso.com/files/widgetseu/campeonato/html/2015/nacional/serie_a/fase_1/nw_html_tablasposicionesHTML.html?r=90728021731"
soup = BeautifulSoup(urlopen(url), 'html.parser')
SoupPart = soup.findAll("span", { "class" : "field-content" })
T = Torneo("Campeonato Ecuatoriano")
LlenarEquipos(T,SoupPart)
LlenarPartidos(T,SoupPart)
print (T)
T.ordenarPorPuntos()
print (T)
