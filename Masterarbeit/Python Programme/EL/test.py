import random
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import matplotlib.animation as animation

plt.rcParams['animation.ffmpeg_path'] = 'C:/Program Files/ffmpeg-n4.4.1-2-gcc33e73618-win64-gpl-4.4/bin/ffmpeg'
fps = 30
nSeconds = 1
snapshots = [ np.random.rand(5,5) for _ in range( nSeconds * fps ) ]

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure( figsize=(8,8) )

a = snapshots[0]
im = plt.imshow(a, interpolation='none', aspect='auto', vmin=0, vmax=1)

def animate_func(i):
    if i % fps == 0:
        print( '.', end ='' )
    print(i)
    im.set_array(snapshots[i])
    return [im]

anim = animation.FuncAnimation(
                               fig,
                               animate_func,
                               frames = nSeconds * fps,
                               interval = 1000 / fps, # in ms
                               )

FFwriter = animation.FFMpegWriter(fps=fps, extra_args=['-vcodec', 'libx264'])
anim.save('basic_animation.mp4', writer=FFwriter)

# plt.show()  # Not required, it seems!