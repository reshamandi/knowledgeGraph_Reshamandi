from tracemalloc import start
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import os, pickle
import csv
import networkx as nx

global loading
loading = 0

def load():
    global g
    g = nx.MultiGraph()
    path = os.path.dirname(os.path.realpath(__file__)) + "/Graph1.txt"
    g = pickle.load(open(path,'rb'))

def product(filter,type,category,border,color):
    dict1={}
    row=[]
    row2=[]
    table=[]
    table2=[]
    prod=[]
    for i in type:
        for j in g[i].keys():
            var1=j.split('*')
            if var1[1] in category and var1[2] in border and var1[3] in color:
                for item in g[j].keys():
                    if item.isnumeric():
                        for item2 in g[j][item].keys():
                            if g[j][item][item2]['relation']=='SoldBy':
                                if g[j][item][item2]['w_centre'] not in dict1.keys():
                                    tup2={g[j][item][item2]['w_centre'] : {}}
                                    dict1.update(tup2)
                                if j not in prod:
                                    prod.append(j)
                                if j in dict1[g[j][item][item2]['w_centre']].keys():
                                    dict1[g[j][item][item2]['w_centre']][j]+=int(g[j][item][item2]['w_quantity'])
                                else:
                                    temp3={j : int(g[j][item][item2]['w_quantity'])}
                                    dict1[g[j][item][item2]['w_centre']].update(temp3)
                            elif g[j][item][item2]['relation']=='BoughtBy':
                                if g[j][item][item2]['r_centre'] not in dict1.keys():
                                    tup2={g[j][item][item2]['r_centre'] : {}}
                                    dict1.update(tup2)
                                if j not in prod:
                                    prod.append(j)
                                if j in dict1[g[j][item][item2]['r_centre']].keys():
                                    dict1[g[j][item][item2]['r_centre']][j]-=int(g[j][item][item2]['r_quantity'])
                                else:
                                    temp3={j : -int(g[j][item][item2]['r_quantity'])}
                                    dict1[g[item][item2]['r_centre']].update(temp3)
    head=['Type','Category','Border','Color']
    for items in dict1.keys():
        head.append(items)
    table.append(head)
    for i in range(len(prod)):
        tup={prod[i] : int(g.nodes[prod[i]]['Stock'])}
        table2.append(tup)
        var=prod[i].split('*')
        for j in range(4):
            row.append(var[j])
        for item2 in dict1.keys():
            if prod[i] in dict1[item2].keys():
                row.append(abs(dict1[item2][prod[i]]))
            else:
                row.append(0)
        row2=row.copy()
        table.append(row2)
        row.clear()
    if filter=='split':
        return table
    else:
        data = [["Type", "Category", "Border", "Color", "Stock"]]
        for i in table2:
            j = list(i.keys())[0].split("*")
            j.append(list(i.values())[0])
            data.append(j)
        return data
                            
def transactions(months, centres, ratings, wids):
    global g
    data = [0, []]
    if wids:
        for wid in wids:
            for pdt in g[wid].keys():
                for index in g[wid][pdt].keys():
                    transaction = g[wid][pdt][index].copy()
                    # print(transaction)
                    if transaction['w_month'] in months and transaction['w_centre'] in centres and transaction['w_rating'] in ratings:
                        transaction['pdt'] = pdt
                        data[1].append(transaction)
                        data[0] += 1

    else:
        for mon in months:
            for pdt in g[mon].keys():
                for index in g[mon][pdt].keys():
                    transaction = g[mon][pdt][index].copy()
                    try:
                        if transaction['w_centre'] in centres and transaction['w_rating'] in ratings:
                            transaction['pdt'] = pdt
                            data[1].append(transaction)
                            data[0] += 1
                    except:
                        pass
    return data

# //////////////////////////////////////////////
def stat(filter1, filter2, role, centres, months, years):
    head = [filter1]
    res = {}
    filter = months
    if role == 'Weaver':
        rel = 'SoldIn'
        qnty = 'w_quantity'
        month = 'w_month'
        year = 'w_year'
        centre = 'w_centre'
    else:
        rel = 'BoughtIn'
        qnty = 'r_quantity'
        month = 'r_month'
        year = 'r_year'
        centre = 'r_centre'
    if filter2 == 'Month':
        filter = months
        filter2 = month
    elif filter2 == 'Centre':
        filter = centres
        filter2 = centre
    elif filter2 == 'Year':
        filter = years
        filter2 = year
    if filter1 == 'Color':
        index = 3
    elif filter1 == 'Border':
        index = 2
    elif filter1 == 'Category':
        index = 1
    else:
        index = 0
    for i in filter:
        head.append(i)
    data = [head]
    for mon in months:
        for pdt in g[mon].keys():
            # print(g[mon][pdt],"\n\n")
            for i in g[mon][pdt].keys():
                tran = g[mon][pdt][i]
                if tran['relation'] == rel and tran[year] in years and tran[centre] in centres:
                    s = pdt.split('*')[index]
                    try:
                        res[s]
                        try:
                            res[s][tran[filter2]] += int(tran[qnty])
                        except:
                            res[s][tran[filter2]] = int(tran[qnty])
                    except:
                        if not s == 'Asilkrt ':
                            res[s] = {tran[filter2]: int(tran[qnty])}
    body = []
    for i in res.keys():
        l = []
        l.append(i)
        for j in filter:
            try:
                l.append(res[i][j])
            except:
                l.append(0)
        body.append(l)
    data.append(body)
    return data
# //////////////////////////////////////////////

def index(request):
  global loading
  if loading == 0:
      load()
      loading += 1
  formData = {
          'types': ["Accessories", "Art silk", "Bagru", "Banarasi", "Bhagalpuri", "Chanderi cotton", "Cotton linen", "Cotton tant", "Cotton voile"],
          'categories': ["AC Blanket(DOHAR)", "Beads", "Bedsheet", "Bermuda", "Bluse", "Chiffon", "Crochet Lace","Cutting Roll", "Fabric", "Fusing", "Girls Womens suit", "Shorts"],
          'borders': ["Checks", "Floral", "Golden Zari", "Lines"],
          'colors': ["Blue", "Red", "Orange", "Violet", "Green", "Yellow", "Indigo"],
          'months': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
          'centres': ["Bangalore", "Hyderabad", "Mumbai", "Agra", "Delhi", "Chennai", "Kolkata", "Ahmedabad", "Patna", "Lucknow", "Jaipur", "Ranchi"],
          'ratings': ["1", "2", "3", "4", "5"],
          'pdtSpec': ["Type","Category","Border","Color"],
          'filter': ["Month", "Centre", "Year"],
          'years': ["2010", "2011", "2012", "2013", "2014"]
      }

  if request.method == "POST":
        if request.POST.get('switch') == "product":
            filter = request.POST.get('filter')

            types = request.POST.getlist('type');
            if not types or not types[0]:
                types = formData['types']
            
            categories = request.POST.getlist('category');
            if not categories or not categories[0]:
                categories = formData['categories']
            
            colors = request.POST.getlist('color');
            if not colors or not colors[0]:
                colors = formData['colors']
            
            borders = request.POST.getlist('border');
            if not borders or not borders[0]:
                borders = formData['borders']
            data =  product(filter,types,categories,borders,colors)
            pdts =[]
            st = []
            if not filter == 'split':
                for i in data[1:]:
                    s = i[0] + "*" + i[1] + "*" + i[2] + "*" + i[3]
                    pdts.append(s)
                    st.append(int(i[4]))
            return render(request, 'first.html', {
                'headData': data[0], 
                'bodyData': data[1:] , 
                'formData': formData,
                'pdts': pdts,
                'st': st 
                }) 
    
        elif request.POST.get('switch') == "transaction": 
            months = request.POST.getlist('month')
            if not months or not months[0]:        
                months = formData['months']

            centres = request.POST.getlist('centre')
            if not centres or not centres[0]:
                centres = formData['centres']

            ratings = request.POST.getlist('rating')
            if not ratings or not ratings[0]:
                ratings = formData['ratings']

            wids = request.POST.get('wids')
            if wids:
                wids = wids.split(',')
            else:
                wids = []
            # print(months, centres, ratings, wids)
            data = transactions(months, centres, ratings, wids)
            chartMonth = []
            Wids = []
            top={}
            top_wid = {}
            top_pdt = {}
            l1 = l2 = l3 = l4 = []
            if wids:
                for wid in wids:
                    Wids.append(int(wid))
                    chart = [0,0,0,0,0,0,0,0,0,0,0,0]
                    for tran in data[1]:
                        if(tran['w_id'] == wid):
                            m = tran['w_month']
                            if m == "January":
                                chart[0] += int(tran['w_quantity'])
                            elif m == "February":
                                chart[1] += int(tran['w_quantity'])
                            elif m == "March":
                                chart[2] += int(tran['w_quantity'])
                            elif m == "April":
                                chart[3] += int(tran['w_quantity'])
                            elif m == "May":
                                chart[4] += int(tran['w_quantity'])
                            elif m == "June":
                                chart[5] += int(tran['w_quantity'])
                            elif m == "July":
                                chart[6] += int(tran['w_quantity'])
                            elif m == "August":
                                chart[7] += int(tran['w_quantity'])
                            elif m == "September":
                                chart[8] += int(tran['w_quantity'])
                            elif m == "October":
                                chart[9] += int(tran['w_quantity'])
                            elif m == "November":
                                chart[10] += int(tran['w_quantity'])
                            elif m == "December":
                                chart[11] += int(tran['w_quantity'])
                    chartMonth.append(chart);                
            else:
                for tran in data[1]:
                    try:
                        top_wid[int(tran['w_id'])] += int(tran['w_quantity'])
                    except:
                        top_wid[int(tran['w_id'])] = int(tran['w_quantity'])
                    try:
                        top_pdt[tran['pdt']] += int(tran['w_quantity'])
                    except:
                        top_pdt[tran['pdt']] = int(tran['w_quantity'])

                top_wid = {k: v for k, v in sorted(top_wid.items(), key=lambda item: item[1], reverse=True)}
                top_pdt = {k: v for k, v in sorted(top_pdt.items(), key=lambda item: item[1], reverse=True)}
                l1 =  (list(top_wid.keys()))[:10]
                l2 =  (list(top_wid.values()))[:10]
                l3 =  (list(top_pdt.keys()))[:10]
                l4 =  (list(top_pdt.values()))[:10]
                top['wids'] =  zip(l1, l2) 
                top['pdts'] =  zip(l3, l4)

            return render(request, 'first.html', {
                'count': data[0], 
                'table': data[1] , 
                'formData': formData, 
                'chartMonth': chartMonth, 
                'wids': Wids, 
                'top': top,
                'topWid': l1,
                'qtWid': l2,
                'topPdt': l3,
                'qtPdt': l4,
                }) 
        else:
            role = request.POST.get('role')
            filter1 = request.POST.get('filter1')
            if not filter1:        
                filter1 = 'Type'

            filter2 = request.POST.get('filter2')
            if not filter2:        
                filter2 = 'Month'

            centres = request.POST.getlist('centres')
            if not centres or not centres[0]:        
                centres = formData['centres']

            months = request.POST.getlist('months')
            if not months or not months[0]:        
                months = formData['months']

            years = request.POST.getlist('years')
            if not years or not years[0]:        
                years = formData['years']

            data = stat(filter1, filter2, role, centres, months, years)   
            return render(request, 'first.html', {'formData': formData, 'headData': data[0], 'bodyData': data[1]})
            

  else:
        return render(request, 'first.html', {'formData': formData}) 



