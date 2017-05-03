#
# Basic satellite imagery plot
#
# Shellb3 functions
import numpy as np
from netCDF4 import Dataset # So we can open netCDF files
import sys
from matplotlib import pyplot as plt # Load plotting tools
from mpl_toolkits.basemap import Basemap # Get basemap
import matplotlib.colors as colors
#
# User defined functions
from colormap_define import colormap_define
#
# ----------------------------------------------------
def plot_geo():
 #
 # Manual entry of one file. To be updated for looping
 filenc = '/data/users/snebuda/simtb/gsi/thompson/simtb12.g15asr.2014121106.nc'
 filepng = 'simtb12.tbsim.ch4.g15'
 var_title = 'Tb_sim'
 channel = 4
 proj = 'nh'
 tb_min = 200
 tb_max = 330
 plot_type = 'linear'
 cmap = 'tbmap'
 interact_show = 'noshow'
 #
 f = Dataset(filenc, 'r', format = 'NETCDF4')
 #
 date_str = f.getncattr('Valid_Date')
 date_int = int(date_str);
 da = date_int % 100
 date_int = (date_int - da) / 100
 mo = date_int % 100
 yr = (date_int - mo) / 100
 #
 hr = int(f.getncattr('Valid_Time')) / 10000
 #
 obstype = f.getncattr('Obstype')
 time_str = f.getncattr('Valid_Time')
 foresec = f.getncattr('Forecast_length_in_seconds') 
 desc = f.getncattr('Description')
 #
 forehr = int(foresec / 3600.0)
 lons = f.variables['Longitude'][:]
 lats = f.variables['Latitude'][:]
 var = f.variables[var_title][:]
 wave = f.variables['Wavelength'][:]
 f.close()
 #
 symsize = 2
 #
 if obstype == 'imga_g15':
     lon_0 = -135.0
     nc = channel - 2 # instrument channel number to GSI array slot
     if nc <= 0 or nc > 2:
         sys.exit('Available channel range for GOES-E/W 2-5')
     symsize = 1
 elif obstype == 'imga_g13':
     lon_0 = -75.0
     nc = channel - 2
     if nc <= 0 or nc > 2:
         sys.exit('Available channel range for GOES-E/W 2-5')
     symsize = 1
 elif obstype == 'sevasr_m10':
     lon_0 = 0.0
     nc = channel - 4
     if nc < 0 or nc > 7:
         sys.exit('Available channel range for SEVIRI 4-11')
     symsize = 4
     if proj == 'nh': symsize = 16
 #
 if var.ndim == 2:
     var = var[nc, :]
 #
 # Data plot range
 if tb_max == -999.0:
     tb_max = np.amax(var)
 if tb_min == -999.0:
     tb_min = np.amin(var)
 #
 # Set data outside the acceptable plotting range to missing
 var[(var < tb_min)] = np.nan
 var[(var > tb_max)] = np.nan
 #
 if plot_type == 'log10':
     var[(var <= 0.0001)] = np.nan
     if tb_min <= 0.0:
         tb_min = 0.0001
 #
 # Get colormap for plot
 tbmap = colormap_define()
 #
 if cmap == 'tbmap':
     my_cmap = tbmap
 else:
     my_cmap = cmap
 #
 fig = plt.figure(figsize = (16, 10), dpi = 100)
 #
 ax1 = fig.add_subplot(111)
 ax1.set_title(var_title)
 #
 mfull = Basemap(projection = 'geos', lon_0 = lon_0, resolution = None)
 #
 llx = -mfull.urcrnrx / 2.0
 lly = -mfull.urcrnry / 2.0
 urx = mfull.urcrnrx / 2.0
 ury = mfull.urcrnry / 2.0
 if proj == 'nh':
     llx = -0.70 * mfull.urcrnrx / 2.0
     lly = 0.0
     urx = 0.70 * mfull.urcrnrx / 2.0
     ury = 0.45 * mfull.urcrnry
 #
 m1 = Basemap(projection = 'geos', lon_0 = lon_0, resolution = 'l', 
              llcrnrx = llx, llcrnry =lly, urcrnrx = urx, urcrnry = ury)
 m1.drawmapboundary(fill_color = 'white') # Draws upper circle
 m1.drawcoastlines(color = 'black', linewidth = 0.5) # Draws continental bdry
 x,y = m1(lons, lats)
 # 
 if plot_type == 'log10':
     m1.scatter(x, y, c = var, cmap = my_cmap, edgecolor = '',
                linewidth = 0.0,
                norm = colors.LogNorm(vmin = tb_min, vmax = tb_max), 
                s = symsize, marker = 's')
 else:
     m1.scatter(x, y, c = var, cmap = my_cmap, edgecolor = '',
                linewidth = 0.0, vmin = tb_min, vmax = tb_max, 
                s = symsize, marker = 's') # Plots the imagery.
 #
 plt.colorbar(ax = ax1, orientation = 'horizontal', label = '')
 #
 title = '{0} {1:d}hr Forecast Valid {2} {3} UTC Channel {4:d} {5:4.1f}$\mu$mz\n{6}'.format(obstype, forehr, date_str, time_str[0:2], channel, wave[nc],  desc)
 fig.suptitle(title, fontsize = 12)
 #
 filepng = filepng + '.png'
 fig.savefig(filepng)
 if interact_show == 'show': plt.show()
 #
 success_flag = 1
 #
 return success_flag
