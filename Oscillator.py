package = 'pythonProject'

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from matplotlib.widgets import *
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from oscillator_math import OscillatorMath

def oscillator_math_old(mass, stiffness, damping_coefficient=0):
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

# renew math: notes for equation.
# 阻尼、刚度和质量，
# 有阻尼比zeta=阻尼/（2*sqrt（刚度*质量）），当阻尼比=1时无过冲，最快回到初始位置；<1时过冲，震荡；>1时无过冲但恢复慢
# 有固有频率w_n=sqrt(k/m)

# 在阻尼情况下，有阻尼频率w_d=w_n*sqrt(1-zeta**2)
# 有积分常数A、B，用于确定初始位置和速度
# 其中e^(-zeta*w_n*t)为衰减项（控制幅度的衰减），(A*cos(w_d*t)+B*sin(w_d*t))是由欧拉公式得出的基本往复
# 当 欠阻尼 时A=x0初始位置，,B=(v0+zeta*w_n*x0)/w_d以消除由指数衰减产生的负速度分量
# 位移有通解x(t)=e^(-zeta*w_n*t)*(A*cos(w_d*t)+B*sin(w_d*t))
# 当 临界阻尼 时A=x0,B=v0+w_n*x0
# x=(A+B*t)*e^(-w_n*t)
# 当 过阻尼 时(两个不同实根r1r2)B=(v0-r1*x0)/(r2-r1),A=x0-B
# x=A*e^(r1*t)+B*e^(r2*t)
def oscillator_math(mass,stiffness,damping_coefficient=0,x0=1,v0=0,t=None):
    if t is None:
        t = np.linspace(0, 10, 1000)
    c=damping_coefficient
    m=mass
    k=stiffness
    zeta = c/(2*np.sqrt(k*m))
    # damping ratio
    w_n = np.sqrt(k / m)
    # natural frequency
    if zeta < 1.0:
        # underdamped
        w_d = w_n * np.sqrt(1 - zeta ** 2)
        # damped natural frequency
        A = x0
        B = (v0+zeta*w_n*x0)/w_d
        x = np.exp(-zeta * w_n * t) * (A * np.cos(w_d * t) + B * np.sin(w_d * t))
    elif np.isclose(zeta, 1.0):
        # critically damped
        A = x0
        B = v0 + w_n * x0
        x = (A + B * t) * np.exp(-w_n * t)
    elif zeta > 1.0:
        # overdamped
        r1 = -w_n*(zeta-np.sqrt(zeta**2-1))
        r2 = -w_n*(zeta+np.sqrt(zeta**2-1))
        '''
        r=(-b+-sqrt(b^2-4ac))/2a
         =(-c+-sqrt(c^2-4mk))/2m
         =(-zeta*(2*sqrt(mk)) +- sqrt(zeta^2-1)*(2*sqrt(mk))) / 2m
         =sqrt(k/m) * (-zeta+-sqrt(zeta^2-1))
         =w_n*(-zeta+-sqrt(zeta^2-1))
         =-w_n*(zeta-+sqrt(zeta^2-1))
        '''
        B = (v0-r1*x0)/(r2-r1)
        A = x0-B
        x = A * np.exp(r1*t)+B * np.exp(r2*t)
    return x

# init
om=OscillatorMath()

fig = plt.figure()
ax = fig.subplots()
ax.set_xlim(0, 210)
ax.set_ylim(-1.5, 1.5)
line1,=ax.plot(0,0, label='Displacement x(t)')
line2,=ax.plot(0,0, label='Envelope(underdamped)', linestyle='--')
peaks=ax.scatter([],[],color='red',marker='o',label='Peaks')
valleys=ax.scatter([],[],color='blue',marker='o',label='Valleys')
zeros=ax.scatter([],[],color='black',marker='o',label='Zeros')



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

# func save button
def save(val):
    root = Tk()
    root.withdraw()
    filename = asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*"),
        ],
    )
    root.destroy()
    plt.savefig(filename)
save_button.on_clicked(save)

# func close button
def close(val):
    plt.close()
close_button.on_clicked(close)

# func update data
def update(val):
    mass = mass_slider.val
    stiffness = stiffness_slider.val
    damping_coefficient = damping_coefficient_slider.val
    mass_text.set_val(mass)
    stiffness_text.set_val(stiffness)
    damping_coefficient_text.set_val(damping_coefficient)
    t = np.linspace(0, 200, 1000)

    om.update_value('mass',mass)
    om.update_value('stiffness',stiffness)
    om.update_value('damping_coefficient',damping_coefficient)
    om.update_value('t',t)


    results = om.calculate()
    x=results['x']
    if results['envelope'] is not None and results['crit_points'] is not None:
        envelope = results['envelope']
        crit_points = results['crit_points']
        line2.set_data(t,envelope)
        p_t,p_x = zip(*crit_points['peaks'])
        v_t,v_x = zip(*crit_points['valleys'])
        z_t,z_x = zip(*crit_points['zeros'])
        ps = np.column_stack((p_t, p_x))
        vs = np.column_stack((v_t, v_x))
        zs = np.column_stack((z_t, z_x))
        peaks.set_offsets(ps)
        valleys.set_offsets(vs)
        zeros.set_offsets(zs)


    line1.set_data(t,x)
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