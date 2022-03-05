vJoy[0].x = filters.mapRange(xbox360[0].leftStickX, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
vJoy[0].y = filters.mapRange(xbox360[0].leftStickY, -1.0, 1.0, vJoy[0].axisMax, -vJoy[0].axisMax)	# vjoy +/- is opposite xbox's, at least for Magicka

vJoy[0].setButton(14, xbox360[0].rightShoulder);	# A
vJoy[0].setButton(13, xbox360[0].leftShoulder);		# B
