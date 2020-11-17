x = [100,100,97,93 ...  23,21,19] # 2d closed polyline
y = [0,25,27,28,30 ...  11,6,4,1]
n = len(x)                        # number of points
cx = [x[i] - (x[(i-1+n)%n]+x[(i+1)%n])/2 for i in range(n)] #precompute the
cy = [y[i] - (y[(i-1+n)%n]+y[(i+1)%n])/2 for i in range(n)] #discrete curvature
for _ in range(1000): # Gauss-Seidel iterations
    for i in range(n):
        x[i] = (x[(i-1+n)%n]+x[(i+1)%n])/2 + cx[i]*1.9
        y[i] = (y[(i-1+n)%n]+y[(i+1)%n])/2 + cy[i]*1.9
