#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.forms.widgets import TextInput
import sqlite3
from principal.models import Game, Cluster

class NoticiaForm(forms.Form):
    key = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Curiosea'}))

class NumberInput(TextInput):
    input_type = 'number'

class GameNameForm(forms.Form):
    conn= sqlite3.connect('principal.db')
    genres = conn.execute("""select distinct genre from principal_game""")
    platforms = conn.execute("""select DISTINCT platform from principal_game""")

    #Select de generos
    l1 = []
    for k in genres:
        tupla = (k[0],k[0])
        l1.append(tupla)
    genres = tuple(l1)

    #Select de plataformas
    l2 = []
    for k in platforms:
        tupla = (k[0],k[0])
        l2.append(tupla)
    platforms = tuple(l2)

    gameName = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Nombre','id':'gameName', 'required':'True','class' : 'form-control', 'style':'background-color: #2f383d; color:white;'}))
    numeroRecomendaciones = forms.IntegerField(label='', widget=NumberInput(attrs={'placeholder':'Número de recomendaciones','required':'True','class' : 'form-control'}))
    generos = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'style':'width: 300px; float: left; margin-right:3%; color:white; background-color: #2f383d; border:#2f383d'}),
                                          choices=genres, label='')
    plataformas = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'style':'width: 300px; float:left;color:white; background-color: #2f383d; border:#2f383d'}),
                                        choices=platforms, label='')

