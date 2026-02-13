import numpy as np


class OscillatorMath:
    mass:float=1.0
    stiffness:float=1.0
    damping_coefficient:float=0.0
    initial_displacement:float=0.0
    initial_velocity:float=0.0
    t :np.ndarray | None = None

    def __init__(self):
        self.mass = 1.0
        self.stiffness = 1.0
        self.damping_coefficient = 0.0
        self.initial_displacement = 0.0
        self.initial_velocity = 0.0

    def element_names(self):
        return tuple(self.__dict__.keys())

    def update_value(self, key:str, value):
        if hasattr(self, key):
            current_attr = getattr(self, key)
            if current_attr is None:
                if key == 't' and isinstance(value, np.ndarray):
                    setattr(self, key, value)
                    return 0
        else:
            return -1
        if isinstance(value, type(current_attr)):
            setattr(self, key, value)
            return 0
        else:
            return -1

    def update_params(self, params):
        param_list = ['mass', 'stiffness', 'damping_coefficient', 'initial_displacement', 'initial_velocity']
        for i in range(len(params)):
            setattr(self, param_list[i], params[i])


    def calculate(self):
        def cal_underdamped():
            w_d = w_n * np.sqrt(1 - zeta ** 2)
            # damped natural frequency
            A = x0
            B = (v0 + zeta * w_n * x0) / w_d
            decay = np.exp(-zeta * w_n * t)
            x = decay * (A * np.cos(w_d * t) + B * np.sin(w_d * t))

            # envelope
            combined_amp = np.sqrt(A ** 2 + B ** 2)
            upper_envelope = combined_amp * decay
            return x, upper_envelope
        def cal_critically_damped():
            A = x0
            B = v0 + w_n * x0
            x = (A + B * t) * np.exp(-w_n * t)
            return x
        def cal_overdamped():
            r1 = -w_n * (zeta - np.sqrt(zeta ** 2 - 1))
            r2 = -w_n * (zeta + np.sqrt(zeta ** 2 - 1))
            """
            r=(-b+-sqrt(b^2-4ac))/2a
             =(-c+-sqrt(c^2-4mk))/2m
             =(-zeta*(2*sqrt(mk)) +- sqrt(zeta^2-1)*(2*sqrt(mk))) / 2m
             =sqrt(k/m) * (-zeta+-sqrt(zeta^2-1))
             =w_n*(-zeta+-sqrt(zeta^2-1))
             =-w_n*(zeta-+sqrt(zeta^2-1))
            """
            B = (v0 - r1 * x0) / (r2 - r1)
            A = x0 - B
            x = A * np.exp(r1 * t) + B * np.exp(r2 * t)
            return x

        def cal_critical_points(count: int = 2):
            """
            get first [count] of zeros, peaks, and valleys
            :return: dict{'zeros':[],'peaks':[],'valleys':[]}
            """
            w_d = w_n * np.sqrt(1 - zeta ** 2)
            decay_rate = zeta * w_n

            # coefficients of x(t)
            # x(t) = e^(-at) * (A*cos + B*sin)
            A = x0
            B = (v0 + zeta * w_n * x0) / w_d

            # coefficients of v(t)
            # v(t) = e^(-at) * (A_v*cos + B_v*sin)
            A_v = v0
            B_v = -w_n * (zeta * v0 + w_n * x0) / w_d

            # tan(wt) = K
            def find_roots(coeff_cos, coeff_sin, w_freq, count_root):
                roots = []
                # tan(wt) = -cos/sin
                # coeff_cos * cos + coeff_sin * sin = 0
                # sin/cos = -coeff_cos / coeff_sin
                first_angle = np.arctan2(-coeff_cos, coeff_sin)

                if first_angle < 0:
                    first_angle += np.pi

                t_base = first_angle / w_freq
                period = np.pi / w_freq

                for i in range(count_root):
                    time_root = t_base + i * period
                    roots.append(time_root)
                return roots

            # zeros
            t_zeros = find_roots(A, B, w_d, count)
            # peaks and valleys
            t_extrema = find_roots(A_v, B_v, w_d, count * 2)

            results = {
                'zeros': [],
                'peaks': [],
                'valleys': []
            }

            for t in t_zeros:
                results['zeros'].append((t, 0.0))

            for t in t_extrema:
                val = np.exp(-decay_rate * t) * (A * np.cos(w_d * t) + B * np.sin(w_d * t))
                if val > 0:
                    if len(results['peaks']) < count:
                        results['peaks'].append((t, val))
                else:
                    if len(results['valleys']) < count:
                        results['valleys'].append((t, val))

            return results

        if self.t is None:
            t = np.linspace(0, 50, 1000)
        else:
            t = self.t
        if self.initial_displacement == 0.0 and self.initial_velocity == 0.0:
            x0 = 1.0
        else:
            x0 = self.initial_displacement
        c, m, k, v0 = self.damping_coefficient, self.mass, self.stiffness, self.initial_velocity
        zeta = c/(2*np.sqrt(k*m))
        # damping ratio
        w_n = np.sqrt(k / m)
        # natural frequency
        results=dict()
        if zeta < 1.0:
            # underdamped
            x, envelope = cal_underdamped()
            crit_points = cal_critical_points()
            results.update({'crit_points':crit_points, 'envelope':envelope})
        elif np.isclose(zeta, 1.0):
            # critically damped
            x = cal_critically_damped()
            results.update({'crit_points': None, 'envelope': None})
        elif zeta > 1.0:
            # overdamped
            x = cal_overdamped()
            results.update({'crit_points': None, 'envelope': None})
        else:
            return -1
        results.update({'x':x})
        return results


