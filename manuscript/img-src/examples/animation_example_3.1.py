import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
#plt.rcParams['text.usetex'] = True
plt.rc('font', size=20)
fig, ax = plt.subplots(1, figsize=(6.40,2.40),dpi=100)

x = [0, .8, 1, .6, .1, .4, .2, .1, .6, .3, 1, .7, .4, 0, .6, 1]
n = len(x)


lines = [ax.plot(range(n), x, 'bs-')[0], ax.text(0.32, -0.2, "Initialization", transform=ax.transAxes)]

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
plt.tight_layout()
#plt.ylim(top=3)

plt.draw()

#ax.grid()

def animate(iteration):
    global x,n
    if (0==iteration):
        return lines

#    for z in range(0, 10):
    x = [ x[0] ] + [ (x[i-1]+x[i+1])/2. for i in range(1, len(x)-1) ] + [ x[-1] ]
#        for i in range(1, len(x)-1):
#            x[i] = (x[i-1]+x[i+1])/2.
#        x[-1] = x[-2]

    print(iteration)

    lines[0].set_data(range(n), x)  # update the data.
    if (0==iteration):
        lines[1].set_text("Initialization")
    else:
        lines[1].set_text("Iteration #" + str(iteration))
    plt.draw()
    ax.relim()
    ax.autoscale_view(False,True,False)
#    ax.autoscale_view(True,True,True)
    return lines

ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 501), interval=100, blit=False, save_count=50)
if (1):
    ani.save('animation.gif', dpi=100, writer='imagemagick')
else:
    from matplotlib.animation import FFMpegWriter
    writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save("animation.mp4", writer=writer)

#plt.show()
