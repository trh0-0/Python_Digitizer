'''
Python Digitizer
======================================================================
This code is a tool to extract digitized data from a plot image or map

Created by
    Jonathan Mocko-Strand
    Franke Hsu
    In-Ok Jun
    Samira Ardani
    Tiffany Hall
 
Final Group Project
Fall 2013, OCNG 658
Texas A&M University
''' 

import numpy as np
import matplotlib.pyplot as plt
import Tkinter,tkFileDialog 
from matplotlib.widgets import Button, RadioButtons, CheckButtons


################################################################################
# Functions for GUI
################################################################################
def import_button(event):
    '''
    This is a button to import the image
    '''
    root = Tkinter.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename()
    im = plt.subplot(111).imshow(np.flipud(plt.imread(str(file_path))), origin = 'lower')
    
    frame1 = plt.gca()    
    for xlabel_i in frame1.axes.get_xticklabels():
        xlabel_i.set_visible(False)
    for ylabel_i in frame1.axes.get_yticklabels():
        ylabel_i.set_visible(False)     
                 
 
def x_scale_button(label):
    '''
    This is a radio button to select the X-axis scale
    '''    
    if label== 'Linear': 
        plt.title( 'linear', loc = 'right')
        logx == 0
    elif label==  'Log': 
        plt.title( 'log', loc='right')
        logx == 1


def y_scale_button(label):
    '''
    This is a radio button to select the Y-axis scale
    '''    
    if label == 'Linear': 
        plt.title( 'linear', loc = 'right')
        logy == 0
    elif label==  'Log': 
        plt.title( 'log', loc='right')
        logy == 1
        
        
def calculate_button(event):
    '''
    This is a button to calculate x & y value and plot the results
    '''
    x,y= calculation(xmin, xmax, ymin, ymax, xaxis, yaxis, logx, logy, xdata, ydata)
    print x,y
    plt.figure()
    plt.plot(x, y)
    plt.show()


def save_button(event):
    '''
    This is a button to save the results as a file
    
    '''
    root = Tkinter.Tk()
    root.withdraw()
    file_path = tkFileDialog.asksaveasfile()
    file_path.writelines('This is the output file of the digitizer\n')
    file_path.writelines('*- Column 0 = x data\n')
    file_path.writelines('*- Column 1 = y data\n')    
    np.savetxt(file_path,np.hstack([xdata,ydata]).reshape(-1,2),delimiter=' ',fmt=['%i','%i'])    
    file_path.close()
    return()     
    
    
################################################################################
# Functions for the model
################################################################################                                                                                  
def click_point(event):
    '''
    This function is to deal with clicking the points
      - Clinking with 'A' button: Axis points
      - Clinking with the other buttons: Data points
      - Output: xaxis, yaixs, xdata, ydata
    '''
    print('Press', event.key)
        
    if event.key == 'a':
        print 'Xaxis = %f,  Yaxis = %f'  %(event.xdata, event.ydata)
        xaxis.append(event.xdata)
        yaxis.append(event.ydata)
    else:
        print 'Xdata = %f,  Ydata = %f'  %(event.xdata, event.ydata)
        xdata.append(event.xdata)
        ydata.append(event.ydata)


def calculation(xmin, xmax, ymin, ymax, xaxis, yaxis, logx, logy, xdata, ydata):
    '''
    This function is to compute the coordinates of the actual data points
      - Output: xpts, ypts
    '''
    xaxis = np.array(xaxis)
    yaxis = np.array(yaxis)
    xdata = np.array(xdata)
    ydata = np.array(ydata)
    xpts  = np.zeros(np.size(xdata))
    ypts  = np.zeros(np.size(ydata))
    
    # check the coordinate system (linear or logscale)
    if logx == 1:
        xmin = np.log10(xmin)
        xmax = np.log10(xmax)
    if logy == 1:
        ymin = np.log10(ymin)
        ymax = np.log10(ymax)
    
    # calculate the point using linear interpolation        
    for i in range(len(xdata)):    
        xpts[i] = xmin + (xmax - xmin) * \
                 (xdata[i] - np.min(xaxis)) / (np.max(xaxis) - np.min(xaxis))
        ypts[i] = ymin + (ymax - ymin) * \
                 (ydata[i] - np.min(yaxis)) / (np.max(yaxis) - np.min(yaxis))   
    
    # change the coordinate system of result for logscale plot 
    if logx == 1:
        for i in range(len(xdata)): xpts[i] = 10**xpts[i]
    if logy == 1:
        for i in range(len(ydata)): ypts[i] = 10**ypts[i]
    
    return xpts, ypts
            

          
################################################################################
# Scripts for the model
################################################################################
# Empty list    
xaxis = []
yaxis = []
xdata = []
ydata = []

# Setup the window size
fig = plt.figure('Figure', facecolor='w', edgecolor='w')

# X_Scale Button
logx = 0
xax = plt.axes([0.01, 0.5, 0.15, 0.1]) 
xradio = RadioButtons(xax,('X-Linear','X-Log'))
xradio.on_clicked(x_scale_button)

# Y_Scale Button
logy = 0
yax = plt.axes([0.01, 0.4, 0.15, 0.1]) 
yradio = RadioButtons(yax,('Y-Linear','Y-Log'))
yradio.on_clicked(y_scale_button)

# Import Button
import_ax = plt.axes([0.01, 0.25, 0.15, 0.05])
import_button = Button(import_ax,'Import',image=None,color='0.95',hovercolor='0.65')        
import_button.on_clicked(import_button)

# Calculation Button
cal_ax = plt.axes([0.01, 0.20, 0.15, 0.05])
cal_button = Button(cal_ax,'Calculate',image=None,color='0.95',hovercolor='0.65')
cal_button.on_clicked(calculate_button)

# Save Button
save_ax = plt.axes([0.01, 0.15, 0.15, 0.05])
save_button = Button(save_ax,'Save',image = None,color='0.95',hovercolor='0.65')    
save_button.on_clicked(save_button)

# Openning a Matplotlib page
plt.show()

# Input the axis information by user :
xmin = input('Enter xmin:  ')
xmax = input('Enter xmax:  ')
ymin = input('Enter ymin:  ')
ymax = input('Enter ymax:  ')

# Get the axis points & data points by user:
print '1) Select the axis points, such as (xmin, ymin), (xmax, ymin), (xmin, ymax) or (xmax, ymax), by press button A (minimum 3 points)'
print '2) Select the data points by press any button (except A, shift, control, win key)'
fig.canvas.mpl_connect('key_press_event', click_point)