from django.shortcuts import render
from django.http import HttpResponse
from corphub_app import forms
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
# Create your views here.

links = []
agent = UserAgent()
header = {'user-agent': agent.chrome}
query = ""

def index(request):
    global links
    global query
    if request.method == "POST":
        form = forms.SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['search']
            links = []
            queries = []
            queries.append(query)
            queries.append("\"{}\"".format(query))

            for new_query in queries:
                links = search_web(links, new_query, False)
                links = search_web(links, new_query, True)

    else:
        form = forms.SearchForm()
        query = ""

    midpoint = len(links) // 2
    return render(request, "corphub_app/index.html", context={"form": form, "links1": links[:20], "links2": links[20:40]})

def search_web(links, query, news):
    if news:
        page = requests.get("https://news.google.com/search?q=" + query + "&hl=en-US&gl=US&ceid=US%3Aen", headers=header)
        soup = BeautifulSoup(page.content)
        for i in soup.find_all('a', href=True):
            if str(i['href']).startswith("./articles/"):
                link = "https://news.google.com" + i['href'][1:]
                links.append(link)
    else:
        page = requests.get("https://www.google.dz/search?q=see")
        soup = BeautifulSoup(page.content)
        for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            new_link = re.split(":(?=http)",link["href"].replace("/url?q=",""))
            links.append(new_link[0])

    return list(set(links))

def viewall(request):
    global query
    links = []
    queries = []
    queries.append(query)
    # queries.append(query + " news")
    # queries.append(query + " speculations")
    # queries.append(query + " stock")
    # queries.append(query + " startup")
    # queries.append(query + " development")
    # queries.append(query + " founder")
    # queries.append(query + " funding")
    # queries.append(query + " products")
    # queries.append(query + " market")
    # queries.append(query + " evaluation")
    # queries.append(query + " launches")
    # queries.append("\"{}\"".format(query))
    # queries.append("\"{} CEO\"".format(query))

    for new_query in queries:
        links = search_web(links, new_query, False)
        links = search_web(links, new_query, True)

    midpoint = len(links) // 2
    return render(request, "corphub_app/viewall.html", context={"links1": links[:midpoint], "links2": links[midpoint:-1]})
