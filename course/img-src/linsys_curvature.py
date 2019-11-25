import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
#plt.rcParams['text.usetex'] = True
plt.rc('font', size=20)
fig, ax = plt.subplots(1, figsize=(6.40,2.40),dpi=100)

x = [0.] * 32
x[0] = x[31] = 1.
x[18] = 2.

n = len(x)


lines = [ax.plot(range(n), x, 'bs-')[0], ax.text(0.32, -0.2, "Iteration #0", transform=ax.transAxes)]

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

    c = 23./32**2 # the curvature to prescribe
    for i in range(0, len(x)):
        if i in [0,18,31]: continue
        x[i] = (x[i-1]+x[i+1]+c)/2.

    print(iteration)

    lines[0].set_data(range(n), x)  # update the data.
    lines[1].set_text("Iteration #" + str(iteration))
    plt.draw()
    ax.relim()
    ax.autoscale_view(True,True,True)
    return lines

ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 150), interval=100, blit=False, save_count=50)
#ani.save('linsys_curvature.gif', dpi=100, writer='imagemagick')

# To save the animation, use e.g.
#
#ani.save("movie.mp4")
#
# or
#
from matplotlib.animation import FFMpegWriter
writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
ani.save("linsys_curvature.mp4", writer=writer)

#plt.show()
