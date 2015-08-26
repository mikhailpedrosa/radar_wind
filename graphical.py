__author__ = 'Mikhail Pedrosa <mikhailj.pedrosa@gmail.com> e Arthur Costa <arthur.opa@gmail.com>'
__description__ = 'Methods for Plot Images, Vector and Graphs'
__version__ = '0.1'
__date__ = '13/04/2015'

import pyart
import wradlib as wrl
import matplotlib.pyplot as plt
from filters import *
from memory_profiler import profile


#@profile()
def plot_image_no_map(radar):
    """
    Funcao para Plotar Imagem do Radar
    Plot function for Radar Image
    :param localdir: Directory of PyFuncemeClimateTools - Diretorio do PyFuncemeClimateTools
    :param radar: Radar Object - Objeto Radar
    :return:
    """

    #create the plot using RadarDisplay
    display = pyart.graph.RadarDisplay(radar)
    display.plot('velocity', 0, vmin=-35., vmax=35.)

    # axislabels = '#000066', '#14217A', '#20398A', '#2D519B', '#3B6BAC', '#4A85BE', '#59A0D0', '#66B7E0', '#75D2F2', '#FFFFFF',
    #             '#FFEA00', '#FFCC00', '#FFB600', '#FF9900', '#FF7E00', '#FF6600', '#FF4900', '#FF3300', '#FF0000'

    #display.plot_colorbar(field= ['#000066', '#20398A', '#3B6BAC', '#59A0D0', '#66B7E0', '#75D2F2', '#FFFFFF', '#FFEA00', '#FFCC00', '#FFB600', '#FF7E00', '#FF4900', '#FF0000'])

    display.plot_range_rings([100., 200., 300., 400.])
    #display.plot_cross_hair(radar.latitude['data'], radar.longitude['data'] )
    #display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0])
    plt.show()
    #plt.title("Funceme - Radar Qxb Band S \n Time: {:}".format(radar.time['units']))
    #plt.savefig('Radar_Qxb_Band_S - Image Velocity Wind (No Map).png', format='png')
    plt.close()


#@profile()
def plot_graph_points_no_filters(radar, r):

    azimuth = radar.azimuth['data'].reshape(10,360)
    velocity = radar.fields['velocity']['data'].reshape(10,360,253)

    y = velocity[2,:,r]
    x = azimuth[2, :]

    figure = plt.figure()
    ax = figure.add_subplot(111)

    plt.scatter (x, y, label='Raw Vr' )

    ax.spines['bottom'].set_position('center')
    # ax.spines['top'].set_color('none')
    # ax.spines['left'].set_smart_bounds(True)
    # ax.spines['bottom'].set_smart_bounds(True)
    # ax.xaxis.set_ticks_position('bottom')
    # ax.yaxis.set_ticks_position('left')

    plt.grid()
    plt.ylim(-35.,35.)
    plt.xlim(0,360)
    plt.title("Radar Qxb Band S - Velocity x Azimuth - ({:.2f} km Range)".format((r*1498)/1000.), fontstyle='italic')
    plt.ylabel('Radial Velocity (m/s)')
    ax.set_xlabel('Azimuth (degree)')
    ax.xaxis.set_label_coords(0.5,-0.05)
    plt.legend(fontsize='10')
    #plt.show()
    plt.savefig("Radar_Qxb_Band_S - Velocity x Azimuth - ({:.2f} km Range) - Points (No Filter).png".format((r*1498)/1000.), format='png')
    plt.close()

#@profile()
def plot_graph_lines_no_filters(radar, r):

    azimuth = radar.azimuth['data'].reshape(10,360)
    velocity = radar.fields['velocity']['data'].reshape(10,360,253)

    y = velocity[2,:,r]
    x = azimuth[2, :]

    figure = plt.figure()
    ax = figure.add_subplot(111)

    plt.plot(x, y, lw='1', label='Raw Vr')

    ax.spines['bottom'].set_position('center')
    # ax.spines['top'].set_color('none')
    # ax.spines['left'].set_smart_bounds(True)
    # ax.spines['bottom'].set_smart_bounds(True)
    # ax.xaxis.set_ticks_position('bottom')
    # ax.yaxis.set_ticks_position('left')

    plt.grid()
    plt.ylim(-35.,35.)
    plt.xlim(0,360)
    plt.title("Radar Qxb Band S - Velocity x Azimuth ({:.2f} km Range)".format((r*1498)/1000.), fontstyle='italic')
    plt.ylabel('Radial Velocity (m/s)')
    ax.set_xlabel('Azimuth (degree)')
    ax.xaxis.set_label_coords(0.5,-0.05)
    plt.legend(fontsize='10')
    #plt.show()
    plt.savefig('Radar_Qxb_Band_S - Velocity x Azimuth ({:.2f} km Range) - Line (No Filter).png'.format((r*1498)/1000.), format='png')
    plt.close()


#@profile()
def plot_image_map(radar):
    """
    Funcao para Plotar Imagem do Radar
    Plot function for Radar Image
    :param radar: Radar Object - Objeto Radar
    :return:
    """

    #create the plot using RadarMapDisplay
    display = pyart.graph.RadarMapDisplay(radar)
    display.plot_ppi_map('velocity', 0, vmin=-35., vmax=35.,
                         min_lat=-9.6, max_lat=-0.9,
                         max_lon=325.5, min_lon=316.,
                         lat_lines=radar.latitude['data'],
                         lon_lines=radar.longitude['data'])
    display.plot_range_rings([100., 200., 300., 400.])
    display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0])
    plt.title("Funceme - Radar Qxb Band S \n Time: {:}".format(radar.time['units']))
    #plt.show()
    plt.savefig("Radar_Qxb_Band_S - Image Velocity Wind.png", format='png')
    plt.close()


#@profile()
def plot_graph_points_filters(radar, r):

    azimuth = radar.azimuth['data'].reshape(10,360)
    velocity = radar.fields['velocity']['data'].reshape(10,360,253)

    y = velocity[2,:,r]
    x = azimuth[2, :]

    #y_ma = moving_average(y,3)
    y_median = median1D(y,3)
    y_gauss = gaussian2D(y)

    plt.figure()
    ax1 = plt.subplot(211)
    ax1.scatter(x, y_median, lw='1', label='Median')

    ax2 = plt.subplot(212)
    ax2.scatter(x, y_gauss, lw='1', label='Gaussian')

    ax1.spines['bottom'].set_position('center')
    ax2.spines['bottom'].set_position('center')

    ax1.grid()
    ax2.grid()

    ax1.set_ylim(-35.,35.)
    ax1.set_xlim(0,360)

    ax2.set_ylim(-35.,35.)
    ax2.set_xlim(0,360)

    ax1.set_title("Radar Qxb Band S - Velocity x Azimuth ({:.2f} km Range)".format((r*1498)/1000.), fontstyle='italic')

    ax2.set_ylabel('Radial Velocity (m/s)')
    ax2.set_xlabel('Azimuth (degree)')
    ax2.xaxis.set_label_coords(0.5,-0.05)
    ax2.yaxis.set_label_coords(-0.1,1.0)

    ax1.legend(fontsize='10')
    ax2.legend(fontsize='10')

    #plt.show()
    plt.savefig("Radar_Qxb_Band_S - Velocity x Azimuth (Median e Gaussian)- ({:.2f} km Range) - Points.png".format((r*1498)/1000.), format='png')
    plt.close()


#@profile()
def plot_graph_lines_filters(radar, r):

    azimuth = radar.azimuth['data'].reshape(10,360)
    velocity = radar.fields['velocity']['data'].reshape(10,360,253)

    y = velocity[2,:,r]
    x = azimuth[2, :]

    y_ma = movingAverage1D(y,5)
    #y_median = median(y,3)
    #y_gauss = gaussian(y)

    plt.figure()
    ax1 = plt.subplot(111)
    ax1.plot(x, y_ma, lw='1', label='Median')

    #ax2 = plt.subplot(212)
    #ax2.plot(x, y_gauss, lw='1', label='Gaussian')

    ax1.spines['bottom'].set_position('center')
    #ax2.spines['bottom'].set_position('center')

    ax1.grid()
    #ax2.grid()

    ax1.set_ylim(-35.,35.)
    ax1.set_xlim(0,360)

    #ax2.set_ylim(-35.,35.)
    #ax2.set_xlim(0,360)

    ax1.set_title("Radar Qxb Band S - Velocity x Azimuth ({:.2f} km Range)".format((r*1498)/1000.), fontstyle='italic')

    # ax2.set_ylabel('Radial Velocity (m/s)')
    # ax2.set_xlabel('Azimuth (degree)')
    # ax2.xaxis.set_label_coords(0.5,-0.05)
    # ax2.yaxis.set_label_coords(-0.1,1.0)

    ax1.legend(fontsize='10')
    #ax2.legend(fontsize='10')

    plt.show()
    #plt.savefig("Radar_Qxb_Band_S - Velocity x Azimuth (Median e Gaussian)- ({:.2f} km Range).png".format((r*1498)/1000.), format='png')
    plt.close()

#@profile()
def plot_graph(radar, r):

    azimuth = radar.azimuth['data'].reshape(10,360)
    velocity = radar.fields['velocity']['data'].reshape(10,360,253)

    y = velocity[2,:,r]
    x = azimuth[2, :]

    #y = movingAverage1D(y,3)
    #y = median1D(y,3)
    y = gaussian1D(y)
    #y = moving_triangle(y)
    print y
    figure = plt.figure()
    ax = figure.add_subplot(111)
    plt.plot(x, y, lw='1', label='Raw Vr')
    #plt.scatter (x, y, label='Raw Vr' )
    ax.spines['bottom'].set_position('center')
    # ax.spines['top'].set_color('none')
    # ax.spines['left'].set_smart_bounds(True)
    # ax.spines['bottom'].set_smart_bounds(True)
    # ax.xaxis.set_ticks_position('bottom')
    # ax.yaxis.set_ticks_position('left')

    plt.grid()
    plt.ylim(-35.,35.)
    plt.xlim(0,360)
    plt.title("Radar Quixeramobim - Velocity x Azimuth ({:.2f} km Range)".format((r*1490)/1000.), fontstyle='italic')
    plt.ylabel('Velocity (m/s)')
    ax.set_xlabel('Azimuth (degree)')
    ax.xaxis.set_label_coords(0.5,-0.05)
    plt.legend(fontsize='10')
    plt.show()
    #plt.savefig("Radar_Qxb_Band_S - Velocity x Azimuth - Median ({:.2f} km Range).png".format((r*1490)/1000.), format='png')
    plt.close()


#@profile()
def plot_vector_barbs(velocity_radial_f, azimuth, ranges, r, e, u, v):

    ran, theta = np.meshgrid(ranges[r], azimuth[e,:])

    plt.figure()
    plt.subplot(111, polar=True)
    plt.barbs(u[e,:,r], v[e,:,r], ran, theta)
    plt.show()
    #plt.savefig('Radar_Qxb_Band_S - Barbs ({:.2f} km Range) ME.png'.format((r*1498)/1000.), format='png')
    plt.close()


#@profile()
def plot_vector_quiver(velocity_radial, azimuth, ranges, r, e, matriz, u, v):

    print azimuth.shape, ranges.shape
    #ranges = ranges/1000
    ran, theta = np.meshgrid(ranges/1000, azimuth[e,:])
    x = ran * np.cos(theta)
    y = ran * np.sin(theta)

    m = matriz[0,ran * np.sin(theta),ran * np.cos(theta)]
    print theta.shape, ran.shape

    plt.figure()
    # plt.subplot(111, polar=True)
    # plt.quiver(theta[:,0:250:50], ran[:,0:250:50], u[0,:,0:250:50], v[0,:,0:250:50])
    plt.subplot(111)
    plt.quiver(x, y, m)
    plt.show()
    #plt.savefig('Radar_Qxb_Band_S - Quiver ({:.2f} km Range) No Filter.png'.format((r*1498)/1000.), format='png')
    plt.close()


def faz_figura_temporaria(data, azimuths, ranges):
    ##### TEMP

    # mask data array for better presentation
    mask_ind = np.where(data <= np.nanmin(data))
    print mask_ind
    data[mask_ind] = np.nan
    print data[mask_ind]
    ma = np.ma.array(data, mask=np.isnan(data))
    print ma
    # plot
    ax, caax, paax, pm = wrl.vis.plot_cg_ppi(ma, refrac=False, r=ranges/1000., az=azimuths, autoext=True,
                                             vmin=-20., vmax=20.)
    ax = wrl.vis.plot_ppi_crosshair(site=(0,0), ranges=[100,200,300,380],ax=ax)

    title = "FUNCEME Band S Wind Radar Quixeramobim-CE"
    titleobj = plt.title(title)
    titleobj.set_y(1.05)

    cbar = plt.gcf().colorbar(pm, pad=0.075)
    cbar.set_label('radial velocity [m/s]')

    caax.set_xlabel("Distance from radar (km)")

    caax.set_ylabel("Distance from radar (km)")

    plt.text(1.0, 1.05, 'azimuth', transform=caax.transAxes, va='bottom', ha='right')

    #pl.savefig("clutter_mask.png")
    #pl.close()
    plt.show()