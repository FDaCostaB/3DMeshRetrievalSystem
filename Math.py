# Previously used to compute area and compute the moment test with area weighted coefficient

def dist(a, b=None):
    if b is None:
        b = [0, 0, 0]
    x = 0
    y = 1
    z = 2
    return ((b[x] - a[x])**2 + (b[y] - a[y])**2 + (b[z] - a[z])**2)**0.5

def triArea(a,b,c):
    ab = dist(a,b)
    bc = dist(b,c)
    ac = dist(a,c)
    s = (ab+bc+ac) / 2
    area = (s*(s-ab)*(s-bc)*(s-ac))**0.5
    return area