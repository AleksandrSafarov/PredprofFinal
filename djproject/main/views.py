from django.urls.base import reverse_lazy
from django.views.generic import *
from django.http import HttpResponse, JsonResponse
from math import pi, sin, ceil
import requests
import json

from .models import *
from .utils import *

def cul_v(w, m):
    return 2*(w/80)*(200/m)

def cul_g(g, k):
    return g + g*k

def cul_k(t):
    return sin((-pi/2) + (pi*(t + 30))/40)

def sum_t(t):
    return sum([i for i in range(t)])

def mass(sh):
    m = 8
    tem = []
    while True:
        if m*2 <= sh+8:
            m = m*2
            tem.append(10)
        else:
            p = 30
            k = 1
            for i in range(0, 31):
                if cul_g(m, cul_k(i)) > sh+8:
                    if cul_k(i) < k:
                        k = cul_k(i)
                        p = i
            if p == 30:
                return tem
            else:
                tem.append(p)
            return tem

def res(sh, dis):
    s = 0
    r = 8
    d = 0
    while s < dis:
        d += 1
        s += cul_v(60, 192 + r)
    temp_deys = mass(sh)
    toplivo = 0
    energy = 0
    pt_d = 1
    if d > len(temp_deys):
        time = d- len(temp_deys)
        while True:
            s = 2*(time)
            d = time
            energy = time*sum_t(30)
            toplivo = time*60
            for i in range(len(temp_deys)):
                energy += sum_t(temp_deys[i])
                r = ceil(cul_g(r, cul_k(temp_deys[i])))
                v = cul_v(60, 192+r)
                d+=1
                if s + v > dis:
                    for y in range(1, 61):
                        v = cul_v(y, 192+r)
                        if s+v > dis:
                            toplivo+=y
                            s+=v
                            pt_d = (time*60 + y)/(time+1)
                            break
                else:
                    toplivo+=60
                    s+=v
            if s > dis:
                break
            else:
                r = 8
                time+=1
    return [d, toplivo+ceil(energy/11), energy, r, r*60, round(pt_d, 2), round(energy/d/11)]


url = 'https://dt.miet.ru/ppo_it_final'
headers = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': 'jtbx8tpu'
}


def getData():
    response = requests.get(url=url, headers=headers)

    routes = list()
    arr = json.loads(response.text)['message']
    for i in arr:
        routes.append(i['points'])

    return routes

data = getData()

def credit(top, ox):
    cr = ox*7
    cr += top*10
    return cr

def routes(data, id):
    sum_energy = 0
    sum_toplivo = 0
    sum_deys = 0
    routes = []
    sum_oxugen = 0
    for y in range(len(data)):
        a = data[y]
        o = res(a['SH'], a['distance'])
        o.append(y+1)
        sum_deys+=o[0]
        sum_toplivo += o[1]
        sum_energy += o[2]
        sum_oxugen += o[4]
        routes.append(o)
    cr = credit(sum_toplivo, sum_oxugen)
    return [sum_deys, sum_toplivo, sum_energy, routes, sum_oxugen, cr, id]


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        global r
        r=[]
        print(data)
        for i in range(len(data)):
            r.append(routes(data[i], i+1))
        print(r)
        self.extra_context = {
            'allroutes': r
        }
        return super().get_context_data(**kwargs)
        
    def get_success_url(self):
        return reverse_lazy('index')