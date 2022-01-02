import random as rand

ff = open('mat.txt', 'w')

ff.write('M = [\n')
for i in range(6000):
    ff.write('[\n')
    for j in range(100):
        ff.write(str(rand.randint(1, 50)) + ',\n')
    ff.write('],\n')
ff.write(']\n')
ff.close()