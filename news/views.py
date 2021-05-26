import json
import logging
import random
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from django.http.response import HttpResponseNotFound


class HomeView(View):
    def get(self, request):
        return redirect('/news/')

# this makes each article its own random number, that is not already defined
def link_func():
    number = random.randint(5, 100000)
    with open('hypernews/news.json', "r") as json_file:
        data = json.load(json_file)
    if number not in data:
        return number
    else:
        link_func()


class NewsView(View):
    def get(self, request):
        search_param = request.GET.get('q')

        with open('hypernews/news.json', "r") as json_file:
            data = json.load(json_file)

        # If not search has been made this stays empty
        search_header = ''

        # Checks that the search is not empty, before filtering the list
        if search_param is not 'none' and search_param is not '' and search_param is not None:
            data = [x for x in data if str(search_param).lower() in str(x['title']).lower()]
            search_header = f'Found {len(data)} items!'

        return render(request, 'news/news.html', context={'data': data, 'search_header': search_header})


class ArticleView(View):
    def get(self, request, article_id):
        with open('hypernews/news.json', "r") as json_file:
            data = json.load(json_file)
        article = list(filter(lambda x: x['link'] == int(article_id), data))
        if not article:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        return render(request, 'news/article.html', context={'article': article[0]})


class CreateView(View):
    def get(self, request):
        return render(request, 'news/create.html')

    def post(self, request):
        article_dict = {
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'link': link_func(),
            'title': request.POST.get('title'),
            'text': request.POST.get('text')
        }

        with open('hypernews/news.json', "r") as json_file:
            data = json.load(json_file)

        if type(data) == list:
            data.append(article_dict)
            json_string = json.dumps(data)
        else:
            a_list = [data, article_dict]
            json_string = json.dumps(a_list)

        json_file = open("hypernews/news.json", "w")
        json_file.write(json_string)
        json_file.close()

        return redirect('/news/')

