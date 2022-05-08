from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import os, pickle
import csv
import networkx as nx

def load():
    global g
    g = nx.MultiGraph()
    path = os.path.dirname(os.path.realpath(__file__)) + "/Graph1.txt"
    g = pickle.load(open(path,'rb'))

def transactions(months, centres, ratings, wids):
    data = [0, []]
    if wids:
        print("Yess")
        for wid in wids:
            for pdt in g[wid].keys():
                for index in g[wid][pdt].keys():
                    transaction = g[wid][pdt][index]
                    if transaction['month'] in months and transaction['centre'] in centres and transaction['rating'] in ratings:
                        data[1].append(transaction)
                        data[0] += 1

    else:
        print("NO")
        for mon in months:
            print(mon)
            for pdt in g[mon].keys():
                for index in g[mon][pdt].keys():
                    transaction = g[mon][pdt][index]
                    if transaction['centre'] in centres and transaction['rating'] in ratings:
                        data[1].append(transaction)
                        data[0] += 1
    return data

def findStock(ty="",cat="",bor="",col=""):
    data = [0, []]
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
  formData = {
          'types': ["Accessories", "Art-silk", "Bagru", "Banarasi", "Bhagalpuri", "Chanderi-cotton", "Cotton-linen", "Cotton-tant", "Cotton-voile"],
          'categories': ["AC Blanket(DOHAR)", "Beads", "Bedsheet", "Bermuda", "Bluse", "Chiffon", "Crochet Lace","Cutting Roll", "Fabric", "Fusing", "Girls-Womens Suit", "Shorts"],
          'borders': ["Checks", "Floral", "Golden-Zari", "Lines"],
          'colors': ["Blue", "Red", "Orange", "Violet", "Green", "Yellow", "Indigo"],
          'months': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
          'centres': ["Bangalore", "Hyderabad", "Mumbai"],
          'ratings': ["1s", "2s", "3s", "4s", "5s"]
      }

  if request.method == "POST":

        if request.POST.get('switch') == "product":
            print("pdt")
    
        else: 
            print("Trans")
            months = request.POST.getlist('month')
            centres = request.POST.getlist('centre')
            ratings = request.POST.getlist('rating')
            data = transactions(months, centres, ratings, [])
            return render(request, 'first.html', {'count': data[0], 'table': data[1] , 'formData': formData}) 
            print(months, centres, ratings)

    #   types = request.POST.getlist('type')
    #   category = request.POST.getlist('category')
    # #   print(type(request.POST.getlist('type')))
    #   print(types)
    #   print(category)
    #   print(request.POST.get('wids'))
    #     data = findStock(request.POST.get("type"),request.POST.get("category"),request.POST.get("border"),request.POST.get("color"))
        return redirect('/members')
      
    #     return render(request, 'first.html', {'stock': data[0], 'table': data[1] , 'formData': formData}) 

    


  else:
        load()
        return render(request, 'first.html', {'stock': 0, 'table': "" , 'formData': formData}) 
