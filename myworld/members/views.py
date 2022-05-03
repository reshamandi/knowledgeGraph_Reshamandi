from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import os, pickle
import csv
import networkx as nx

def findStock(ty="",cat="",bor="",col=""):
    data = [0, []]
    g = nx.MultiGraph()
    path = os.path.dirname(os.path.realpath(__file__)) + "/Graph1.txt"
    g = pickle.load(open(path,'rb'))

    if ty=="" and cat=="" and bor=="" and col=="":
        print("Atleast one attribute/filter must be specified")
    else:        
        if ty!="":
            d = g[ty]
        elif cat!="":
            d = g[cat]
        elif bor!="":
            d = g[bor]
        else:
            d = g[col]

        for i in d.keys():
            if str(i).find(ty) != -1 and str(i).find(cat) != -1 and str(i).find(bor) != -1 and str(i).find(col) != -1:
                data[0] += g.nodes[i]['Stock']
                data[1].append(g[i])
        return data

def index(request):

  if request.method == "POST":
    data = findStock(request.POST.get("type"),request.POST.get("category"),request.POST.get("border"),request.POST.get("color"))
    # return redirect('/members')
    return render(request, 'first.html', {'stock': data[0], 'table': data[1] }) 
    


  else:
    return render(request, 'first.html', {'stock': 0, 'table': "" }) 
