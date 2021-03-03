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
#https://www.aliexpress.com/item/32922733593.html?spm=a2g0o.productlist.0.0.12835f9fIHb01w&algo_pvid=bbb5385b-64a2-493a-abb2-f3039edf3df0&algo_expid=bbb5385b-64a2-493a-abb2-f3039edf3df0-26&btsid=0bb0624716144817922545553e1790&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_

 
#https://www.tokopedia.com/tutikstore1/motor-brushless-n5065-330kv-outrunner-sensored-untuk-penyeimbang?whid=0
#https://www.aliexpress.com/item/32922733593.html?spm=a2g0o.productlist.0.0.12835f9fIHb01w&algo_pvid=bbb5385b-64a2-493a-abb2-f3039edf3df0&algo_expid=bbb5385b-64a2-493a-abb2-f3039edf3df0-26&btsid=0bb0624716144817922545553e1790&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_
#https://www.aliexpress.com/item/32292880708.html?spm=a2g0o.productlist.0.0.4e1c706alBmL0x&ad_pvid=202102272326403384652253592160039347259_1&s=p
#https://www.aliexpress.com/item/4000474175391.html?spm=a2g0o.detail.1000060.1.90503649Laids6&gps-id=pcDetailBottomMoreThisSeller&scm=1007.13339.169870.0&scm_id=1007.13339.169870.0&scm-url=1007.13339.169870.0&pvid=bc091ad0-1943-4cd8-9a02-a705bf6e3e56&_t=gps-id:pcDetailBottomMoreThisSeller,scm-url:1007.13339.169870.0,pvid:bc091ad0-1943-4cd8-9a02-a705bf6e3e56,tpp_buckets:668%230%23131923%2340_668%230%23131923%2340_668%23888%233325%233_668%23888%233325%233_668%232846%238107%231934_668%232717%237561%23344_668%231000022185%231000066059%230_668%233468%2315618%23923_668%232846%238107%231934_668%232717%237561%23344_668%233164%239976%2321_668%233468%2315618%23923

'''
dilema:
Required for application: 
Max RPM: 2250 RPM
Max Torque: 0.22 Nm

alternative motor 1: noLoad RPM (3-5x), stall torque (2x), 
                    smaller (dia = 30, length =30) dissipate less heat,
                    sensorless
                    price- ~$20-25

alternative motor 2: noLoad RPM (2x), stall torque (10-14x), 
                    bigger (dia = 50, length =50) dissipate more heat,
                    sensored (hall effect)
                    price- ~$35-40

NOTE: Make a speed torque comparison + max continuous torque line of 3 motors
'''

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
Kv = 330#800 #1000#330 # RPM/V
voltage = 12
internalResistance = 0.038#0.035#0.052#0.038
stallTorque = voltage/internalResistance/(Kv*2*np.pi/60) #[N.m]
noLoadSpeed = voltage*Kv #[RPM]

motorTorqueBarang = np.arange(0, stallTorque, 0.001, dtype = float).T # [N.m]
motorSpeedBarang = (noLoadSpeed - noLoadSpeed/stallTorque*motorTorqueBarang)# [RPM] *60/2/np.pi 

# 3. IMPORT LOAD DATA
# b. import force, velocity, power data (mbd calc)
importForce= pd.read_csv('sliderForce135kg.csv')
importVelocity = pd.read_csv('sliderVelocity135kg.csv')
importPower = pd.read_csv('sliderPower135kg.csv')
# import data
sliderForce = importForce.actuatingForceNewton # [N]
print(np.average(sliderForce))
timeForce = importForce.time # [s]
sliderVelocity = importVelocity.sliderVelocitymmsec # [mm/s]
timeVel = importVelocity.time # [s]
sliderPower = importPower.actuationPowerWatt # [watt]
timePower = importPower.time # [s]

#validate
sliderPowerCalc = np.multiply(sliderForce, sliderVelocity/1000)
plt.figure(9)
plt.plot(timeForce, sliderPowerCalc)
plt.plot(timePower, sliderPower)
plt.title('Power')
plt.ylabel('watt]')
plt.xlabel('s')
plt.grid(True)
plt.show()

# 4. Calculating motor torque and angular velocity
motorTorque = sliderForce*(lead/2/np.pi/1000)/cfnc.LSEfficiency(miu, lead, diameter)# [Nm] LSEfficiency(miu, lead, diameter)
motorTorque = motorTorque/gearReduction/gearEff # [Nm]
motorSpeed = sliderVelocity*gearReduction*60/lead#  [RPM] *2*np.pi
print(cfnc.LSEfficiency(miu, lead, diameter))
print(cfnc.LSEfficiencyACME(miu, lead, diameter, 30*np.pi/180))

'''# iterating between lead and diameter
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
plt.show()'''

plt.figure(1)
plt.plot(abs(motorTorque), abs(motorSpeed))
plt.plot(motorTorqueBarang, motorSpeedBarang)
plt.title('load trajectory')
plt.ylabel('angular velocity [RPM]')
plt.xlabel('torque [Nm]')
plt.grid(True)


plt.figure(2)
plt.plot(timeVel, np.multiply((motorTorque), (motorSpeed)))
plt.title('motor Power')
plt.ylabel('watt')
plt.xlabel('s')
plt.grid(True)
plt.show()
'''plt.figure(3)
plt.plot(timeForce, sliderForce)
plt.title('slider Force')
plt.ylabel('N')
plt.xlabel('s')
plt.grid(True)
plt.show()'''
