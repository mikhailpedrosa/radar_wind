__author__ = 'Mikhail Pedrosa <mikhailj.pedrosa@gmail.com> e Arthur Costa <arthur.opa@gmail.com>'
__description__ = 'Velocity-Azimuth Processing Technique'
__version__ = '0.1'
__date__ = '13/04/2015'

import numpy as np
from memory_profiler import profile

ELEVATION_LIST = {
    'X': ["0.5", "1.5", "2.5", "3.5", "4.5", "5.5", "6.5", "7.5", "8.5", "9.5", "10.5", "11.5", "12.5"],
    'S': ["-0.5", "0.0", "0.5", "1.0", "2.0", "3.0", "4.0", "5.5", "7.0", "8.5"],
}

#@profile()
def vap(radar, velocity_radial, nsweeps, nrays, ngates, e):
    """
    Implementacao da tecnica de Processamento VAP (Velocity-Azimuth Processing)
    Implementation of the technical processing of VAP (Velocity-Azimuth Processing)
    :param radar: Radar object - Objeto Radar
    :param velocity_radial: variable velocity
    :param nsweeps: elevations
    :param nrays: azimuths
    :param ngates: ranges
    :return: Vectors u and v
    """
    #The horizontal wind components u and v
    u = np.zeros((1,360,253))
    v = np.zeros((1,360,253))

    u_1 = np.zeros((1,360,253))
    u_2 = np.zeros((1,360,253))
    v_1 = np.zeros((1,360,253))
    v_2 = np.zeros((1,360,253))

    azimuth = radar.azimuth['data']
    matriz = np.zeros((1,360,253))

    print nsweeps, nrays, ngates

    for theta in range(nrays-1):
        for rang in range(ngates-1):
            u_1[0, theta, rang] = np.multiply(velocity_radial[0, theta + 1, rang], np.cos(azimuth[theta] - 1))
            u_2[0, theta, rang] = np.multiply(velocity_radial[0, theta - 1, rang], np.cos(azimuth[theta] + 1))

            u[0, theta, rang] = (u_1[0, theta, rang] - u_2[0, theta, rang]) / float(np.sin(2))

            # print elevation, theta, rang, "\n", u_1[elevation, theta, rang], "\n", u_2[elevation, theta, rang], "\n", u[elevation, theta, rang]

            v_1[0, theta, rang] = np.multiply(velocity_radial[0, theta - 1, rang], np.sin(azimuth[theta] + 1))
            v_2[0, theta, rang] = np.multiply(velocity_radial[0, theta + 1, rang], np.sin(azimuth[theta] - 1))

            v[0, theta, rang] = (v_1[0, theta, rang] - v_2[0, theta, rang]) / float(np.sin(2))

            matriz[0,theta, rang] = u[0, theta, rang] * np.sin(theta) + v[0, theta, rang] * np.cos(theta)
            # print elevation, theta, rang
    return matriz, u, v