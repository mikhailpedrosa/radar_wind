__author__ = 'Mikhail Pedrosa <mikhailj.pedrosa@gmail.com> e Arthur Costa <arthur.opa@gmail.com>'
__description__ = 'Reading Methods of RAWs Files'
__version__ = '0.1'
__date__ = '13/04/2015'

import pyart
import os
import glob
from graphical import plot_image_no_map
from memory_profiler import profile

DIR='/home/mikhail/ProjetosGIT/radar_wind/'

#@profile()
def read_raws():
    """
    Leitura do arquivo bruto (Sigmet) do Radar
    Reading the raw file (Sigmet) Radar
    :return: Radar object with all its features - Objeto Radar com todas as suas Caracteristicas
    """
    rawfiles = glob.glob(os.path.join(DIR, '*.RAW*'))
    for rawfile in rawfiles:
        radar = pyart.io.read_sigmet(rawfile)
        filename = rawfile.split("/")[-1]
        plot_image_no_map(radar, filename)

    return radar

#@profile()
def read_radar():
    filename = 'XXX140331061059.RAW1JMJ'
    local_dir = os.path.dirname(__file__)
    radar = pyart.io.read(filename)

    return radar