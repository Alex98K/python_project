import time


def fun(ha_ha):
    def nei_bu(a):
        p1 = time.time()
        ha_ha(a)
        p2 = time.time()
        print(p2-p1)
    return nei_bu


@fun
def ce_shi(i):
    for i in range(1000000000):
        pass
    print(i)


ce_shi(100)
