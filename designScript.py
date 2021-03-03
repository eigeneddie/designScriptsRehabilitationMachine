# Motor sizing script
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import calcFunctions as cfnc
from matplotlib import cm
from matplotlib.ticker import LinearLocator
# Motor candidate
# https://www.tokopedia.com/awallaptop/motor-dc-brushless-n5065-270kv-skateboard-electric-12-24v-sensorless?whid=0
# https://www.tokopedia.com/garudawangi/jgb37-3525-dc-12v-brushless-motor-107rpm-gear-reduction-motor-37mm
# https://www.aliexpress.com/item/4000098637815.html --> most likely candidate
# https://www.aliexpress.com/item/1005002074557314.html?spm=a2g0o.detail.0.0.27c05b89LxLA12&gps-id=pcDetailBottomMoreThisSeller&scm=1007.13339.169870.0&scm_id=1007.13339.169870.0&scm-url=1007.13339.169870.0&pvid=ac8fde14-2815-47b5-9395-d6771156ac24&_t=gps-id:pcDetailBottomMoreThisSeller,scm-url:1007.13339.169870.0,pvid:ac8fde14-2815-47b5-9395-d6771156ac24,tpp_buckets:668%230%23131923%2356_668%23888%233325%238_668%232846%238109%231935_668%232717%237563%23518_668%231000022185%231000066059%230_668%233468%2315617%23846

# OBJECTIVE:
# -Determine the motor load in torque-RPM.
# 1. INPUT PARMETERS
# a. iterated Data
lead = 8 # mm/rev
diameter = 8 # mm
miu = 0.2 #friction coefficient
gearReduction = 1 #gearbox reduction
gearEff = 1 #gearbox efficiency
# b. MOTOR SPECS
stallTorque = 10.2 #10.2#10.2#4.7#12.5/56/0.76#voltage/internalResistance/Kv [kg.cm]
noLoadSpeed = 320 #320 #107*56#voltage*Kv [RPM]
'''Kv = 9*np.pi
voltage = 12
internalResistance = 0.020'''
motorTorqueBarang = np.arange(0, stallTorque, 0.001, dtype = float).T
motorSpeedBarang = (noLoadSpeed - noLoadSpeed/stallTorque*motorTorqueBarang)#*60/2/np.pi 

# 3. IMPORT LOAD DATA
# b. import force, velocity, power data (mbd calc)
importForce= pd.read_csv('sliderForce.csv')
importVelocity = pd.read_csv('sliderVelocity.csv')
importPower = pd.read_csv('sliderPower.csv')
# import data
sliderForce = importForce.actuatingForceNewton # [N]
print(np.average(sliderForce))
timeForce = importForce.time # [s]
sliderVelocity = importVelocity.sliderVelocitymmsec # [mm/s]
timeVel = importVelocity.time # [s]
sliderPower = importPower.actuationPowerWatt # [watt]
timePower = importPower.time # [s]

'''#validate
sliderPowerCalc = np.multiply(sliderForce, sliderVelocity/1000)
plt.figure(9)
plt.plot(timeForce, sliderPowerCalc)
plt.plot(timePower, sliderPower)
plt.title('Power')
plt.ylabel('watt]')
plt.xlabel('s')
plt.grid(True)
plt.show()'''

# 4. Calculating motor torque and angular velocity
motorTorque = sliderForce*(lead/2/np.pi/1000)/cfnc.LSEfficiency(miu, lead, diameter)# [N] LSEfficiency(miu, lead, diameter)
motorTorque = motorTorque/gearReduction/gearEff*10.197162 # [kg.cm]
motorSpeed = sliderVelocity*gearReduction*60/lead#  [RPM] *2*np.pi
print(cfnc.LSEfficiency(miu, lead, diameter))
print(cfnc.LSEfficiencyACME(miu, lead, diameter, 30*np.pi/180))

# iterating between lead and diameter
lead_iterateX = np.arange(6, 10, 1)
diameter_iterateY = np.arange(6,16,1)
lead_iterate, diameter_iterate = np.meshgrid(lead_iterateX, diameter_iterateY)
maxTorque = np.amax(np.absolute(sliderForce))*(lead/2/np.pi/1000)/cfnc.LSEfficiency(miu, lead_iterate, diameter_iterate)
maxTorque = maxTorque/gearReduction/gearEff*10.197162

#plot surface
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(lead_iterate, diameter_iterate, maxTorque, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel('lead [mm/rev]')
ax.set_ylabel('diameter [mm]')
ax.set_zlabel('maximum torque [kg.cm]')
plt.show()

plt.figure(1)
plt.plot(abs(motorTorque), abs(motorSpeed))
plt.plot(motorTorqueBarang, motorSpeedBarang)
plt.title('load trajectory')
plt.ylabel('angular velocity [RPM]')
plt.xlabel('torque [kg.cm]')
plt.grid(True)

plt.figure(2)
plt.plot(timeVel, sliderVelocity)
plt.title('sliderVelocity')
plt.ylabel('mm/s')
plt.xlabel('s')
plt.grid(True)

plt.figure(3)
plt.plot(timeForce, sliderForce)
plt.title('slider Force')
plt.ylabel('N')
plt.xlabel('s')
plt.grid(True)
plt.show()
