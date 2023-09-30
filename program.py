import numpy as np
import matplotlib.pyplot as plt

MEASURES = {'THOUSAND_KILOMETER':1e8,'KILOMETER':1e5,'METER':100, 'SGS':1, 'MILIGAL':1e3,'EOTVOS':1e9}
#Input data in SI
#Radius of an object in km
R0 = 49244
#Mass of an object in kg
M0 = 1.02e26
#Radial velocity of an object in 1/s
RAD_VEL = 9648

#Input data in SGS
#Mass of an object in g
MASS= M0 * 1e3
#Radius of an object in cm
RADIUS = R0 * 1e5

#Constants
#Pi constant
PI = np.pi
#Gravitational constant in SGS system
GRAV_CONST = 6.674e-8

#Density function in SGS
DENSITY = MASS / (4/3 * PI * np.power(RADIUS, 3))


class getScale ():
    def rescale(maximum):
        format = 2-round(np.log10(maximum))
        return 10 ** format
    

class Functions:
    def V(rho):
        result = np.zeros_like(rho)
        mask = rho < RADIUS
        result[mask] = 2/3 * PI * GRAV_CONST * DENSITY * (3 * RADIUS ** 2 - rho[mask] ** 2)
        result[~mask] = 4/3 * PI * GRAV_CONST * DENSITY * RADIUS ** 3 / rho[~mask]
        return result
    def DV(rho):
        result = np.zeros_like(rho)
        mask = rho < RADIUS
        result[mask] = 4/3 * PI * GRAV_CONST * DENSITY * rho[mask]
        result[~mask] = 4/3 * PI * GRAV_CONST * DENSITY * RADIUS ** 3 / (rho[~mask]) ** 2
        return result
    def D2V(rho):    
        result = np.zeros_like(rho)
        mask = rho < RADIUS
        result[mask] = -4/3 * PI * GRAV_CONST * DENSITY
        result[~mask] = 8/3 * PI * GRAV_CONST * DENSITY * RADIUS ** 3 / rho[~mask] ** 3
        return result
    

class Graphs:

    plt.figure(figsize=(6, 6))

    x_axis = np.linspace(0, 10 * RADIUS, 1000)
    indexes = np.array([0, 0.4 * RADIUS, 0.8 * RADIUS, RADIUS, 1.5 * RADIUS, 2 * RADIUS, 3 * RADIUS, 4 * RADIUS, 5 * RADIUS, 6 * RADIUS, 10 * RADIUS])
    lines=[]
    def addGraphV(x_axis, y_axis, annotatablex = [], annotatabley = [], offset = (0,0), measurex = 'SGS', measurey = 'SGS', normalizex = False, normalizey = False, linelabel = '', ylabel = '', color = 'steelblue', isSecond = False):
       
        #Getting right scales
        scalex=MEASURES[measurex]
        scaley=MEASURES[measurey]

        #Intermediate calculations
        m_x = max(x_axis)
        m_y = max(y_axis)

        #Normalization of graphic values
        if normalizex:
            scalex/=getScale.rescale(m_x)
        if normalizey:
            scaley/=getScale.rescale(m_y)
        #Setting graph sizes

        
        #Check if should create twinx or format x
        if isSecond:
            axis = plt.gca().twinx()
        else:
            axis = plt.gca()
            plt.xlabel('$\\rho, тыс.км$')
            axis.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.0f}".format(x/scalex)))
        #Setting axis labels
        plt.ylabel(ylabel + ' 1e' + str(round(np.log10(getScale.rescale(m_y)))))

        #Format of axis
        plt.ylim(0, m_y*1.05)
        plt.xlim(0, m_x * 1.05)
        axis.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, loc: "{:.0f}".format(y/scaley)))
        
        #Drawing a graph
        line, = axis.plot(x_axis, y_axis, label=linelabel, color = color)

        #Drawing annotated points
        for i in range(len(annotatablex)):
            axis.scatter(annotatablex[i], annotatabley[i], color=color)
            axis.annotate(f'{annotatabley[i]/scaley:.2f}', (annotatablex[i], annotatabley[i]), xytext=offset, textcoords='offset points')
        #Returning line object for further use in legend
        return line
    
    #Drawing graphs with parameters
    lines.append(addGraphV(x_axis= x_axis, y_axis= Functions.V(x_axis), annotatablex= indexes, annotatabley= Functions.V(indexes), offset= (0,0), measurex= 'THOUSAND_KILOMETER', measurey= 'SGS', normalizex= False, normalizey= True, linelabel= 'График потенциала', ylabel= '$V(\\rho), \\frac{см^2}{с^2}$', color= 'steelblue', isSecond = False))
    lines.append(addGraphV(x_axis= x_axis, y_axis= Functions.DV(x_axis), annotatablex= indexes, annotatabley= Functions.DV(indexes), offset= (0,0), measurex= 'THOUSAND_KILOMETER', measurey= 'SGS', normalizex= False, normalizey= False, linelabel= 'График cилы', ylabel= 'F, Гал', color= 'orange', isSecond = True))

    #Drawing labels
    labels = [line.get_label() for line in lines]
    plt.legend(lines, labels, loc='upper right')
    
    plt.show()