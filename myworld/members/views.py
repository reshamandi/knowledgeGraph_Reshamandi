from nis import match
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
    g = nx.MultiGraph()
    path = os.path.dirname(os.path.realpath(__file__)) + "/Graph1.txt"
    g = pickle.load(open(path,'rb'))
    data = [0, []]
    if wids:
        print("Yess")
        for wid in wids:
            for pdt in g[wid].keys():
                for index in g[wid][pdt].keys():
                    transaction = g[wid][pdt][index].copy()
                    if transaction['month'] in months and transaction['centre'] in centres and transaction['rating'] in ratings:
                        transaction['pdt'] = pdt
                        data[1].append(transaction)
                        data[0] += 1

    else:
        print("NO")
        for mon in months:
            print(mon)
            for pdt in g[mon].keys():
                for index in g[mon][pdt].keys():
                    transaction = g[mon][pdt][index].copy()
                    if transaction['centre'] in centres and transaction['rating'] in ratings:
                        transaction['pdt'] = pdt
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
            months = request.POST.getlist('month')
            # Checking if all months was selected
            if not months[0]:        
                months = formData['months']

            centres = request.POST.getlist('centre')
            if not centres[0]:
                centres = formData['centres']

            ratings = request.POST.getlist('rating')
            if not ratings[0]:
                ratings = formData['ratings']

            wids = request.POST.get('wids')
            if wids:
                wids = wids.split(',')
            else:
                wids = []
            # print(months, centres, ratings, wids)
            data = transactions(months, centres, ratings, wids)
            chartMonth = []
            
            if wids:
                for wid in wids:
                    chart = [0,0,0,0,0,0,0,0,0,0,0,0]
                    for tran in data[1]:
                        if(tran['w_id'] == wid):
                            m = tran['month']
                            if m == "January":
                                chart[0] += int(tran['quantity'])
                            elif m == "February":
                                chart[1] += int(tran['quantity'])
                            elif m == "March":
                                chart[2] += int(tran['quantity'])
                            elif m == "April":
                                chart[3] += int(tran['quantity'])
                            elif m == "May":
                                chart[4] += int(tran['quantity'])
                            elif m == "June":
                                chart[5] += int(tran['quantity'])
                            elif m == "July":
                                chart[6] += int(tran['quantity'])
                            elif m == "August":
                                chart[7] += int(tran['quantity'])
                            elif m == "September":
                                chart[8] += int(tran['quantity'])
                            elif m == "October":
                                chart[9] += int(tran['quantity'])
                            elif m == "November":
                                chart[10] += int(tran['quantity'])
                            elif m == "December":
                                chart[11] += int(tran['quantity'])
                    chartMonth.append(chart);                
            print(type(chart[0]))
            wids = [2323133,34353534]
            return render(request, 'first.html', {'count': data[0], 'table': data[1] , 'formData': formData, 'chartMonth': chartMonth[0], 'wids': wids[0]}) 

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
        return render(request, 'first.html', {'count': 0, 'table': "" , 'formData': formData}) 
