import tkinter as tk
import numpy as np
from oscillator_math import OscillatorMath

# Matplotlib 集成库
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class InputGroup(tk.Frame):
    # input group (Entry & Scale)
    def __init__(self, parent, label_text, index, callback,init_value,min_value,max_value,step_value, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callback = callback  # 数据变化时触发的回调函数（用于更新图表）
        self.index = index

        # 1. Label
        tk.Label(self, text=label_text, font=("Arial", 10, "bold")).pack(anchor="w")

        # 变量绑定
        self.var = tk.DoubleVar(value=init_value)

        # 2. Entry
        self.entry = tk.Entry(self, textvariable=self.var, width=10)
        self.entry.pack(side="left", padx=5)
        self.entry.bind('<Return>', self.on_entry_change)  # 回车确认

        # 3. Scale
        self.scale = tk.Scale(self, variable=self.var, from_=min_value, to=max_value,
                              orient="horizontal", resolution=step_value, command=self.on_scale_change)
        self.scale.pack(side="left", fill="x", expand=True, padx=5)

    def on_scale_change(self, event=None):
        self.callback()

    def on_entry_change(self, event=None):
        self.callback()

    def get_value(self):
        return self.var.get()

    def set_value(self, val):
        self.var.set(val)


class ChartWindow(tk.Toplevel):
    om = OscillatorMath()
    """
    Oscillator page
    row1 column1
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Oscillator - Visualisation")
        self.geometry("1200x900")
        self.protocol("WM_DELETE_WINDOW", self.close_window)  # 绑定关闭事件

        # === 布局划分 ===

        # bottom, control buttons
        self.bottom_panel = tk.Frame(self, height=50, bg="#e0e0e0")
        self.bottom_panel.pack(side="bottom", fill="x")

        # main area
        self.main_area = tk.Frame(self)
        self.main_area.pack(fill="both", expand=True)

        # left, graph settings
        self.left_panel = tk.Frame(self.main_area, bg="#f0f0f0", width=300)
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)
        self.left_panel.pack_propagate(False)  # fixed width

        # right, graph
        self.right_panel = tk.Frame(self.main_area)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # TODO five input groups for mass, stiffness, co, initial x and initial v
        self.init_accesses()
        # TODO one input text fot time.

        # graph
        self.update_idletasks()
        self.init_plot()

        # control buttons
        # left (Reset, Save, Input)
        btn_style = {"width": 10, "pady": 5}
        tk.Button(self.bottom_panel, text="Reset", command=self.reset_values, **btn_style).pack(side="left", padx=20,
                                                                                                pady=10)
        tk.Button(self.bottom_panel, text="Save", command=self.save_data, **btn_style).pack(side="left", padx=10,
                                                                                            pady=10)
        tk.Button(self.bottom_panel, text="Input", command=self.manual_input_trigger, **btn_style).pack(side="left",
                                                                                                        padx=10,
                                                                                                        pady=10)

        # right (Close)
        tk.Button(self.bottom_panel, text="Close", command=self.close_window, bg="#ffcccc", **btn_style).pack(
            side="right", padx=20, pady=10)
    def init_accesses(self):
        """
        for every element sent from om, generate an access group and name it with the element name.
        """
        self.inputs = []
        for index, element in enumerate(self.om.element_names()):
            if element=="mass":
                init_value, min_value, max_value,step_value = 1.0,0.1,5.0,0.1
            elif element == "stiffness":
                init_value, min_value, max_value, step_value = 1.0, 0.0, 4.0, 0.1
            elif element=="damping_coefficient":
                init_value, min_value, max_value,step_value = 0.0,0.0,4.0,0.01
            elif element=="initial_displacement":
                init_value, min_value, max_value,step_value = 1.0,-1.0,1.0,0.1
            elif element=="initial_velocity":
                init_value, min_value, max_value,step_value = 0.0,-5.0,5.0,0.1

            group = InputGroup(self.left_panel, element, index, self.update_plot,init_value,min_value,max_value,step_value)
            group.pack(fill="x", pady=10)
            self.inputs.append(group)
        return -1

    def init_plot(self):
        """初始化 Matplotlib 图表"""
        # 1. 创建 Figure
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Oscillator")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Distance")
        self.line, = self.ax.plot([], [], 'r-')  # 初始化空线条
        self.env_line, = self.ax.plot([], [], 'k--', alpha=0.5, label='Envelope')
        self.peaks = self.ax.scatter([], [], c='blue', marker='^')
        self.zeros = self.ax.scatter([], [], c='black', marker='o')
        self.valleys = self.ax.scatter([], [], c='green', marker='v')
        # 2. 嵌入到 Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        # 第一次绘制
        self.update_plot()

    def update_plot(self):
        # 获取所有滑块的值
        params = [inp.get_value() for inp in self.inputs]

        # 生成演示数据 (例如：合成正弦波)
        x = np.linspace(0, 50, 1000)
        # 使用 params[0] 控制幅度, params[1] 控制频率, 这里的逻辑可以自定义
        self.om.update_params(params)
        results = self.om.calculate()
        y = results['x']
        # 更新线条数据
        self.line.set_data(x, y)
        self.ax.set_ylim(-2, 2)
        if results['envelope'] is not None and results['crit_points'] is not None:
            envelope = results['envelope']
            crit_points = results['crit_points']
            y_env = results['envelope']
            peaks = results['crit_points'].get('peaks', [])
            zeros = results['crit_points'].get('zeros', [])
            valleys = results['crit_points'].get('valleys', [])
            t_p, x_p = zip(*peaks)
            self.peaks.set_offsets(np.c_[t_p, x_p])
            t_p, x_p = zip(*zeros)
            self.zeros.set_offsets(np.c_[t_p, x_p])
            t_p, x_p = zip(*valleys)
            self.valleys.set_offsets(np.c_[t_p, x_p])
            self.env_line.set_data(x, y_env)
            self.env_line.set_visible(True)
            self.peaks.set_visible(True)
            self.zeros.set_visible(True)
            self.valleys.set_visible(True)
        else:
            envelope = None
            crit_points = None
            self.env_line.set_visible(False)
            self.peaks.set_visible(False)
            self.zeros.set_visible(False)
            self.valleys.set_visible(False)

        self.ax.relim()  # 重新计算坐标轴限制
        self.ax.autoscale_view()  # 自动缩放
        self.update_idletasks()
        self.canvas.draw()  # 重绘

    def reset_values(self):
        """重置所有参数"""
        for index, inp in enumerate(self.inputs):
            if index == 2 or index == 4:
                inp.set_value(0.0)
            else:
                inp.set_value(1.0)
        self.update_plot()

    def save_data(self):
        print("Data Saved!")  # 此处可添加文件保存逻辑

    def manual_input_trigger(self):
        print("Input Button Clicked")  # 额外输入逻辑

    def close_window(self):
        self.destroy()


class BlankWindow(tk.Toplevel):
    """
    其他子窗口：留白
    """

    def __init__(self, parent, index):
        super().__init__(parent)
        self.title(f"Sub Window {index}")
        self.geometry("400x300")
        tk.Label(self, text=f"This is Window {index}\n(Placeholder)", font=("Arial", 14)).pack(expand=True)


class DashboardApp(tk.Tk):
    """
    主程序窗口：两侧长条按钮布局
    """

    def __init__(self):
        super().__init__()
        self.title("Dynamic System displayer")
        self.geometry("600x400")

        # 主布局：左右两列
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # 内容区
        self.grid_rowconfigure(1, weight=0)  # 底部关闭区

        # === 左侧面板 ===
        self.left_frame = tk.Frame(self, bg="#dddddd")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # === 右侧面板 ===
        self.right_frame = tk.Frame(self, bg="#cccccc")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

        # 创建按钮
        self.create_buttons()

        # === 底部关闭按钮区 ===
        # 左侧关闭
        tk.Button(self, text="Close Program", command=self.quit_app, bg="#ff9999").grid(row=1, column=0, sticky="ew",
                                                                                        padx=10, pady=10)
        # 右侧关闭
        tk.Button(self, text="Close Program", command=self.quit_app, bg="#ff9999").grid(row=1, column=1, sticky="ew",
                                                                                        padx=10, pady=10)

    def create_buttons(self):
        # 按钮通用样式
        btn_opts = {"font": ("Arial", 12), "height": 3}



        # 左侧三个按钮
        for i in range(1, 4):
            if i==1:
                btn = tk.Button(self.left_frame, text=f"Oscillator", command=lambda idx=i: self.open_window(idx),
                                **btn_opts)
                btn.pack(fill="x", padx=20, pady=10)
            else:
                btn = tk.Button(self.left_frame, text=f"Window {i}", command=lambda idx=i: self.open_window(idx),
                                **btn_opts)
                btn.pack(fill="x", padx=20, pady=10)

        # 右侧三个按钮
        for i in range(4, 7):
            btn = tk.Button(self.right_frame, text=f"Window {i}", command=lambda idx=i: self.open_window(idx),
                            **btn_opts)
            btn.pack(fill="x", padx=20, pady=10)

    def open_window(self, index):
        """窗口跳转逻辑"""
        if index == 1:
            ChartWindow(self)  # 打开配置了图表的窗口
        else:
            BlankWindow(self, index)  # 打开留白窗口

    def quit_app(self):
        """退出整个程序"""
        self.destroy()


# 用于测试运行
if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()