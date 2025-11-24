package = 'pythonProject'

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from matplotlib.widgets import *


def oscillator_math(subplot, mass, stiffness, damping_coefficient=0):
    t = np.arange(0, 200, 1)
    b = damping_coefficient
    k = stiffness
    m = mass
    A = np.array([[0, 1], [-k / m, -b / m]])
    x0 = np.array([1.0, 0.0])
    x = np.zeros((len(t), 2))
    for i, ti in enumerate(t):
        x[i] = expm(A * ti) @ x0
    return t,x


fig = plt.figure()
ax = fig.subplots()
ax.set_xlim(0, 210)
ax.set_ylim(-1.5, 1.5)


axe_mass = plt.axes([0.25, 0.2, 0.65, 0.03])
axe_stiffness = plt.axes([0.25, 0.15, 0.65, 0.03])
axe_damping_coefficient = plt.axes([0.25, 0.1, 0.65, 0.03])

mass_slider = Slider(axe_mass,'',valmin=0,valmax=100,valinit=10,valstep=0.01,valfmt='%.2f')
stiffness_slider = Slider(axe_stiffness,'',valmin=0.0,valmax=2.0,valinit=0.5,valstep=0.01,valfmt='%.2f')
damping_coefficient_slider = Slider(axe_damping_coefficient,'',valmin=0,valmax=2,valinit=0,valstep=0.01,valfmt='%.2f')


axe_mass_text = plt.axes([0.15, 0.2, 0.07, 0.03])
axe_stiffness_text = plt.axes([0.15, 0.15, 0.07, 0.03])
axe_damping_coefficient_text = plt.axes([0.15, 0.1, 0.07, 0.03])

mass_text = TextBox(axe_mass_text,'Mass')
stiffness_text = TextBox(axe_stiffness_text,'Stiffness')
damping_coefficient_text = TextBox(axe_damping_coefficient_text,'Damping-Co')

line1,=ax.plot(0,0, label='Displacement x(t)')
line2,=ax.plot(0,0, label='Velocity x\'(t)', linestyle='--')
def update(val):
    mass = mass_slider.val
    stiffness = stiffness_slider.val
    damping_coefficient = damping_coefficient_slider.val
    mass_text.set_val(mass)
    stiffness_text.set_val(stiffness)
    damping_coefficient_text.set_val(damping_coefficient)
    t,x = oscillator_math(ax,mass,stiffness,damping_coefficient)
    line1.set_data(t,x[:, 0])
    line2.set_data(t,x[:, 1])
    fig.canvas.draw_idle()


def update_by_text(text,target):
    target.set_val(float(text))
mass_text.on_submit(lambda text: update_by_text(text, mass_slider))
stiffness_text.on_submit(lambda text: update_by_text(text, stiffness_slider))
damping_coefficient_text.on_submit(lambda text: update_by_text(text, damping_coefficient_slider))

ax.legend()
ax.grid(True)
update(None)

mass_slider.on_changed(update)
stiffness_slider.on_changed(update)
damping_coefficient_slider.on_changed(update)

resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')
def reset(event):
    mass_slider.reset()
    stiffness_slider.reset()
    damping_coefficient_slider.reset()
button.on_clicked(reset)
plt.show()
# -mx''=bx'+kx
# x'2=-b/m*x2-k/m*x1


    # def add(val):
    #     ax.plot(t, x[:, 1], label='Velocity x\'(t)', linestyle='--')
    #     # ax.plot(t,x[:, 1]/2)
    #     fig.canvas.draw()
    #     print('123123')
    # axes = plt.axes([0.81, 0.000001, 0.1, 0.075])
    # button_test=Button(axes, label='test',color='yellow')
    # button_test.on_clicked(add)


# this comment is for git testing final