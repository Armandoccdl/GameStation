#encoding:utf-8

import sqlite3
from principal.models import Game, Cluster
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from principal.forms import NoticiaForm, GameNameForm
import tools.scrap as rss
import json
from django.http import HttpResponse

def index(request):
    return render_to_response('index.html')

def muestraNoticias(request):
    if request.method == 'POST':
        formulario = NoticiaForm(request.POST)
        if formulario.is_valid():
            key = formulario.cleaned_data['key']
            feedFilter = rss.search(key)
            return render_to_response('muestraNoticias.html', {'result': feedFilter, 'formulario':formulario},
                                      context_instance=RequestContext(request))
        else:
            formulario = NoticiaForm()
            feed = rss.getAllFeed()
            rss.indexar(feed)
            return render_to_response('muestraNoticias.html', {'formulario': formulario, 'result': feed},
                                      context_instance=RequestContext(request))

    else:
        formulario = NoticiaForm()
        feed = rss.getAllFeed()
        rss.indexar(feed)
        return render_to_response('muestraNoticias.html', {'formulario': formulario, 'result':feed},
                                  context_instance=RequestContext(request))


def recommendGame(request):
    conn = sqlite3.connect('principal.db')
    games = []

    if request.method == 'POST':
        formulario = GameNameForm(request.POST, auto_id=False)
        if formulario.is_valid():
            gameName = formulario.cleaned_data['gameName']
            numeroRecomendaciones = formulario.cleaned_data['numeroRecomendaciones']
            genres = formulario.cleaned_data['generos']
            platforms = formulario.cleaned_data['plataformas']

            if Game.objects.filter(name__exact=gameName):
                cluster = conn.execute('''select c.numCluster from principal_cluster c where c.game_id = (select id from principal_game where name = (?))''', (gameName,))
                for k in cluster:
                    # cluster = k[0]
                    cs = Cluster.objects.all().filter(numCluster = k[0])[0:numeroRecomendaciones]

                for k in cs:
                    if len(genres) > 0 and len(platforms) > 0 and k.game.genre in genres and k.game.platform in platforms:
                        games.append(k)
                    elif len(genres) > 0 and len(platforms) == 0 and k.game.genre in genres:
                        games.append(k)
                    elif len(genres) == 0 and len(platforms) > 0 and k.game.platform in platforms:
                        games.append(k)
                    elif len(genres) == 0 and len(platforms) == 0:
                        games.append(k)

                return render_to_response('recommendedGames.html', {'games': games})
            else:
                return render_to_response('recommendedGames.html', {'games': games})


    else:
        formulario = GameNameForm(auto_id=False)
        return render_to_response('formGame.html', {'formulario':formulario}, context_instance=RequestContext(request))

def get_name(request):
    if request.is_ajax():
        results = []
        q = request.GET.get('term', '')
        name_list = Game.objects.filter(name__startswith = q ).values('name').distinct()[:10]

        for name in name_list:
          name_json = {}
          name_json['id'] = name['name']
          name_json['label'] = name['name']
          name_json['value'] = name['name']
          results.append(name_json)
          data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

