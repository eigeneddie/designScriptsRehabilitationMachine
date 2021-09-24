# designScriptsRehabilitationMachine
Scripts to aid engineering analysis.

Jupyter notebook version: https://colab.research.google.com/drive/15hwoC-izuehkHvqCwJDukQbwlS3xbolc?usp=sharing

The point of these programs is to conduct motor sizing to systems that require actuators (usually electric motors with known lab specifications). 

The script requires you to provide data of predicted load trajectory in the form of torque and rotation speed. The units can vary (I usually use Nm vs RPM, so be careful with unit conversions). In this script, the goal is to see the compatibility of a motor to certain predicted load application to the motor. Since the project I am currently working on involves an electric motor to be coupled with a lead screw, the specification of the leadscrew such as material, lead length, and others must also be considered using the appropriate equations. This script is basically a calculator to be used iteratively.
