# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import feedparser
from whoosh.fields import *
from whoosh.qparser import QueryParser
import whoosh.index as index
import os, os.path

def get_feed():
    titles = []
    links = []
    pictures = []
    summaries = []
    dates = []
    feed = feedparser.parse('https://www.gamereactor.es/rss/rss.php?texttype=4')
    for entry in feed['entries']:
        dates.append(entry['published'])
        titles.append(entry['title'])
        description = BeautifulSoup(entry['summary'], 'html.parser')
        pictures.append(description.img['src'])
        summaries.append(description.p.string)
        links.append(entry['links'][0]['href'])

    return zip(titles,links,pictures,summaries,dates)

def getAllFeed():
    titles = []
    links = []
    pictures = []
    summaries = []
    dates = []
    feed = feedparser.parse('https://www.gamereactor.es/rss/allnewcontent.php')
    for entry in feed['entries']:
        dates.append(entry['published'])
        titles.append(entry['title'])
        pictures.append(entry['links'][1]['href'])
        summaries.append(entry['summary'])
        links.append(entry['links'][0]['href'])

    return zip(titles, links, pictures, summaries, dates)

def indexar(news):
    schema = Schema(title=TEXT(stored=True), summary=TEXT(stored=True),
                    date=TEXT(stored=True),link=ID(stored=True), picture=ID(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    ix = index.create_in("indexdir", schema)
    writer = ix.writer()
    for n in news:
        writer.add_document(title=n[0], summary=n[3],
                            date=n[4], link=n[1], picture=n[2])
    writer.commit()

def search(word):
    ix = index.open_dir("indexdir")
    with ix.searcher() as searcher:
        toSearch = word
        query = QueryParser("title", ix.schema).parse(toSearch)
        results = searcher.search(query, terms=True)
        if results.is_empty():
            query = QueryParser("summary", ix.schema).parse(toSearch)
            results = searcher.search(query, terms=True)
        results = buildSearch(results)

    return results

def buildSearch(news):
    titles = []
    links = []
    pictures = []
    summaries = []
    dates = []
    if news.has_matched_terms():
        for hit in news:
            titles.append(hit.get('title'))
            links.append(hit.get('link'))
            pictures.append(hit.get('picture'))
            summaries.append(hit.get('summary'))
            dates.append(hit.get('date'))

    return zip(titles, links, pictures, summaries, dates)

