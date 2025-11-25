package = 'pythonProject'

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from matplotlib.widgets import *


def oscillator_math(mass, stiffness, damping_coefficient=0):
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
line1,=ax.plot(0,0, label='Displacement x(t)')
line2,=ax.plot(0,0, label='Velocity x\'(t)', linestyle='--')

# init
plt.get_current_fig_manager().set_window_title('Oscillator')
plt.get_current_fig_manager().resize(1200,800)
plt.subplots_adjust(left=0.5,right=0.95,top=0.9, bottom=0.3)

x_init = 0.08; x_init_right=0.35; y_init = 0.9; y_space=0.05; comp_width = 0.03
slider_length=0.3; textbox_length=0.07

# sliders
axe_mass = plt.axes([x_init, y_init-1*y_space, slider_length, comp_width])
axe_stiffness = plt.axes([x_init, y_init-4*y_space, slider_length, comp_width])
axe_damping_coefficient = plt.axes([x_init, y_init-7*y_space, slider_length, comp_width])

mass_slider = Slider(axe_mass,'',valmin=0,valmax=100,valinit=10,valstep=0.01,valfmt='%.2f')
stiffness_slider = Slider(axe_stiffness,'',valmin=0.0,valmax=2.0,valinit=0.5,valstep=0.01,valfmt='%.2f')
damping_coefficient_slider = Slider(axe_damping_coefficient,'',valmin=0,valmax=2,valinit=0,valstep=0.01,valfmt='%.2f')

# textboxes
axe_mass_text = plt.axes([x_init, y_init, textbox_length, comp_width])
axe_stiffness_text = plt.axes([x_init, y_init-3*y_space, textbox_length, comp_width])
axe_damping_coefficient_text = plt.axes([x_init, y_init-6*y_space, textbox_length, comp_width])

mass_text = TextBox(axe_mass_text,'Mass')
stiffness_text = TextBox(axe_stiffness_text,'Stiffness')
damping_coefficient_text = TextBox(axe_damping_coefficient_text,'Damping-Co')

# buttons
axe_reset = plt.axes([x_init, 1-y_init, textbox_length, comp_width])
axe_input = plt.axes([x_init_right, 1-y_init, textbox_length, comp_width])
axe_save_file = plt.axes([x_init_right-0.1, 1-y_init, textbox_length, comp_width])
axe_close_window = plt.axes([0.9, 1-y_init, textbox_length, comp_width])

reset_button = Button(axe_reset, 'Reset', hovercolor='0.95')
input_button = Button(axe_input, 'Input', hovercolor='0.95')
save_button = Button(axe_save_file, 'Save', hovercolor='0.95')
close_button = Button(axe_close_window, 'Close', hovercolor='red')

# func reset button
def reset(event):
    mass_slider.reset()
    stiffness_slider.reset()
    damping_coefficient_slider.reset()
reset_button.on_clicked(reset)

# TODO func input button
# input_button.on_clicked()

# TODO func save button
# save_button.on_clicked()

# TODO func close button
# close_button.on_clicked()

# func update data
def update(val):
    mass = mass_slider.val
    stiffness = stiffness_slider.val
    damping_coefficient = damping_coefficient_slider.val
    mass_text.set_val(mass)
    stiffness_text.set_val(stiffness)
    damping_coefficient_text.set_val(damping_coefficient)
    t,x = oscillator_math(mass,stiffness,damping_coefficient)
    line1.set_data(t,x[:, 0])
    line2.set_data(t,x[:, 1])
    fig.canvas.draw_idle()

# func change text -> change slider
def update_by_text(text,target):
    target.set_val(float(text))
mass_text.on_submit(lambda text: update_by_text(text, mass_slider))
stiffness_text.on_submit(lambda text: update_by_text(text, stiffness_slider))
damping_coefficient_text.on_submit(lambda text: update_by_text(text, damping_coefficient_slider))

# func change slider -> update
mass_slider.on_changed(update)
stiffness_slider.on_changed(update)
damping_coefficient_slider.on_changed(update)

# pltshow
ax.legend()
ax.grid(True)
update(None)

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