import matplotlib.pyplot as plt
import numpy as np

moresamples = False
logistic = True
samples = [[0.47,1],[0.24,1],[0.75,1],[0.00,1],[-0.80,1],[-0.59,1],[1.09,1],[1.34,1],
           [1.01,1],[-1.02,1],[0.50,1],[0.64,1],[-1.15,1],[-1.68,1],[-2.21,1],[-0.52,1],
           [3.93,1],[4.21,1],[5.18,1],[4.20,1],[4.57,1],[2.63,1],[4.52,1],[3.31,1],
           [6.75,1],[3.47,1],[4.32,1],[3.08,1],[4.10,1],[4.00,1],[2.99,1],[3.83,1]]
n = len(samples)
m = len(samples[0])
labels = [0]*(n//2) + [1]*(n//2)

if moresamples:
    samples += [[16.2,1],[15.7,1],[15.0,1],[16.0,1],[15.4,1],[17.3,1],[15.6,1],[15.8,1],[12.8,1],[16.2,1],[14.8,1],[17.0,1],[16.1,1],[16.0,1],[16.9,1],[15.9,1]]
    n = len(samples)
    labels  += [1]*(n-len(labels))

xmin = np.min([x for x,_ in samples])
xmax = np.max([x for x,_ in samples])
print(xmax-xmin)

if logistic:
    U = np.matrix([[1],[0]])
    for _ in range(5):
        JR = np.matrix(np.zeros((n, 2)))
        R  = np.matrix(np.zeros((n, 1)))
        for i in range(n):
            ei = np.exp(-U[1,0] - samples[i][0]*U[0,0])
            R[i,0] = -1/(1+ei) + labels[i]
            for j in range(3):
                JR[i, 0] = samples[i][0]*ei/(1+ei)**2
                JR[i, 1] = ei/(1+ei)**2
        U = U + np.linalg.inv(JR.T*JR)*JR.T*R
    a,b = U.T.tolist()[0]
    sep = -b/a
    xred = np.linspace(xmin, sep, 100)
    yred = [1/(1+np.exp(-x*U[0,0] - U[1,0])) for x in xred]
    xgrn = np.linspace(sep, xmax, 100)
    ygrn = [1/(1+np.exp(-x*U[0,0] - U[1,0])) for x in xgrn]
else:
    A = np.matrix(np.zeros((n,m)))
    b = np.matrix(np.zeros((n,1)))
    for i in range(n):
        A[i,:] = samples[i]
        b[i,0] = labels[i]

    X = np.linalg.inv(A.transpose()*A)*A.transpose()*b
    k,m = X.transpose().tolist()[0]

    sep = (.5-m)/k
    xred = np.linspace(xmin, sep, 500)
    yred = k*xred + m
    xgrn = np.linspace(sep, xmax, 500)
    ygrn = k*xgrn + m

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=20)


if moresamples:
    fig, ax = plt.subplots(1, figsize=(6.40*2,2.40),dpi=150)
else:
    fig, ax = plt.subplots(1, figsize=(6.40,2.40),dpi=150)


plt.axvline(sep, ymin=-0.25, ymax=1.25, color='black', linestyle='--', linewidth=3)
plt.plot(xred, yred, '-r', linewidth=2)
plt.plot(xgrn, ygrn, '-g', linewidth=2)

for sample, label in zip(samples,labels):
    c = 'g'
    if (label<.5): c = 'r'
    plt.scatter(sample[0], label, color=c, edgecolors='black')

plt.tight_layout()
plt.savefig("a.png", bbox_inches='tight')
plt.show()
