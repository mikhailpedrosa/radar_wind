__author__ = 'Mikhail Pedrosa <mikhailj.pedrosa@gmail.com> e Arthur Costa <arthur.opa@gmail.com>'
__description__ = 'Single-Doppler Radar Wind-Field Retrieval Experiment On a Qualified Velocity-Azimuth Processing Technique'
__version__ = '0.1'
__date__ = '13/04/2015'

import cv2
import datetime
from read import read_radar
from graphical import *
from vap import vap
from filters import *

ElevationRadar = { 'X': ["0.5", "1.5", "2.5", "3.5", "4.5", "5.5", "6.5", "7.5", "8.5", "9.5", "10.5", "11.5", "12.5"],
                   'S': ["-0.5", "0.0", "0.5", "1.0", "2.0", "3.0", "4.0", "5.5", "7.0", "8.5"],
}

if __name__ == '__main__':

    print "----Velocity-Azimuth Processing Technique----"

    #Range (1-253)
    r = 67
    e = 3 #Elevation 0.5
    radar = read_radar()

    start = datetime.datetime.now()

    _sweep_number = radar.nsweeps
    _azimuth = radar.nrays/10
    _range = radar.ngates

    azimuth = radar.azimuth['data'].reshape(_sweep_number,_azimuth)
    ranges = radar.range['data']
    velocity_radial = radar.fields['velocity']['data'].reshape(_sweep_number,_azimuth,_range)

    rang, theta = np.meshgrid(ranges, azimuth[e,:])

    # Filters OpenCV (Image Smoothing) - Gaussian, Median e Average

    #velocity_radial_f = cv2.GaussianBlur(velocity_radial, (3,3), 0)
    velocity_radial_f = cv2.medianBlur(velocity_radial, 3)
    #velocity_radial_f = cv2.blur(velocity_radial, (3,3))

    # Methods - Moving_Average, Median e Average

    #velocity_radial_f = movingAverage2D(velocity_radial,3)
    #velocity_radial_f = median2D(velocity_radial,3)
    #velocity_radial_f = gaussian2D(velocity_radial,3)

    # Velocity-Azimuth Processing Technique
    matriz, u, v = vap(radar, velocity_radial_f, _sweep_number, _azimuth, _range, e)
    print matriz

    #np.save('vectoru', u)
    #np.save('vectorv', v)
    #u = np.load('vectoru.npy')
    #v = np.load('vectorv.npy')

    # Plot Image

    #print np.nanmax(velocity_radial[0,:,:]), "\n", np.nanmax(velocity_radial_f[0,:,:]), "\n", np.nanmax(velocity_radial[0,:,:] - velocity_radial_f[0,:,:])
    #dif = velocity_radial[0,:,:] - velocity_radial_f[0,:,:]
    #faz_figura_temporaria(velocity_radial_f[e,:,:], azimuth[e,:], ranges)
    dif = datetime.datetime.now() - start
    print '%i s' % dif.seconds


    #plot_image_no_map(radar)
    #plot_image_map(radar)
    #plot_graph_lines_no_filters(radar, r)
    #plot_graph_points_no_filters(radar, r)
    #plot_graph_lines_filters(radar, r)
    #plot_graph_points_filters(radar, r)
    #plot_graph(radar, r)
    #plot_vector_barbs(velocity_radial_f, azimuth, ranges, r, e, u, v)
    plot_vector_quiver(velocity_radial_f, azimuth, ranges, r, e, matriz, u, v)