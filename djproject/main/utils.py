from math import pi, sin
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
    if d > len(temp_deys):
        time = d- len(temp_deys)
        while True:
            s = 2*(time)
            d = time
            energy = time*sum_t(30)
            toplivo = time*60
            for i in range(len(temp_deys)):
                energy += sum_t(temp_deys[i])
                r = cul_g(r, cul_k(temp_deys[i]))
                v = cul_v(60, 192+r)
                d+=1
                if s + v > dis:
                    for i in range(1, 61):
                        v = cul_v(i, 192+r)
                        if s+v > dis:
                            toplivo+=i
                            s+=v
                            break
                else:
                    toplivo+=60
                    s+=v
            if s > dis:
                break
            else:
                r = 8
                time+=1
    return [d, toplivo, energy]

def routes(data):
    sum_energy = 0
    sum_toplivo = 0
    sum_deys = 0
    routes = []
    for y in range(len(data)):
        a = data[y]
        o = res(a["SH"], a['distance'])
        sum_deys+=o[0]
        sum_toplivo += o[1]
        sum_energy += o[2]
        routes.append([o[0], o[1], o[2]])
    return [sum_deys, sum_toplivo, sum_energy, routes]
