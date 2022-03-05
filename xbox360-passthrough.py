# Face buttons Y,B,A,X
vJoy[0].setButton(14, xbox360[0].a);
vJoy[0].setButton(13, xbox360[0].b);
vJoy[0].setButton(15, xbox360[0].x);
vJoy[0].setButton(12, xbox360[0].y);

# Face buttons Back, Start
vJoy[0].setButton(0, xbox360[0].back)
vJoy[0].setButton(3, xbox360[0].start)

# Analogue buttons L click, R click
vJoy[0].setButton(1, xbox360[0].leftThumb)
vJoy[0].setButton(2, xbox360[0].rightThumb)

# Joysticks
vJoy[0].x = filters.mapRange(xbox360[0].leftStickX, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
vJoy[0].y = filters.mapRange(xbox360[0].leftStickY, -1.0, 1.0, vJoy[0].axisMax, -vJoy[0].axisMax)	# vjoy +/- is opposite xbox's, at least for Magicka
vJoy[0].z = filters.mapRange(xbox360[0].rightStickX, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
vJoy[0].rz = filters.mapRange(xbox360[0].rightStickY, -1.0, 1.0, vJoy[0].axisMax, -vJoy[0].axisMax)	# vjoy +/- is opposite xbox's, at least for Magicka

# D-pad
vJoy[0].setButton(4, xbox360[0].up);
vJoy[0].setButton(5, xbox360[0].down);
vJoy[0].setButton(6, xbox360[0].left);
vJoy[0].setButton(7, xbox360[0].right);

# Shoulders
vJoy[0].setButton(10, xbox360[0].leftShoulder);
vJoy[0].setButton(11, xbox360[0].rightShoulder);

# Triggers rx, ry?
vJoy[0].rx = filters.mapRange(xbox360[0].leftTrigger, 0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
vJoy[0].ry = filters.mapRange(xbox360[0].rightTrigger, 0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
