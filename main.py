package = 'pythonProject'
import pandas as pd
import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
import Oscillator
from main_window import DashboardApp
import tkinter as tk

from matplotlib.widgets import *

if __name__ == '__main__':
    app = DashboardApp()
    app.mainloop()
    # Oscillator

    # print(matplotlib.__version__)
    # print(matplotlib.get_backend())


    # axes = plt.axes([0.81, 0.000001, 0.1, 0.075])
    # button_test=Button(axes, label='test',color='yellow')
    # button_test.on_clicked(Oscillator.oscillator_math(10,2))
    # plt.show()


