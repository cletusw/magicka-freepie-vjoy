import time

def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	return type('Enum', (), enums)

def setState(newState):
	global state
	state = newState

def setCasting(newValue):
	global casting
	casting = newValue

if starting:
	States = enum('RESET', 'WAIT_TO_LISTEN', 'LISTENING', 'COLD', 'SHIELD', 'WATER', 'LIFE', 'FIRE', 'EARTH', 'LIGHTNING', 'ARCANE')
	THRESHOLD = 0.09
	start_time = time.clock()
	state = States.LISTENING
	previous = {
		'a': False,
		'b': False,
		'x': False,
		'y': False,
		'up': False,
		'down': False,
		'left': False,
		'right': False,
		'leftShoulder': False,
		'rightShoulder': False,
		'leftTrigger': False,
		'rightTrigger': False,
		'rightStickXOrY': False,
	}
	inputQueue = []
	casting = False


# Un-buffered inputs (for menus, inventory, or unused)

# Face buttons Y,B,A,X
vJoy[0].setButton(14, xbox360[0].a);
vJoy[0].setButton(13, xbox360[0].b);
vJoy[0].setButton(15, xbox360[0].x);
vJoy[0].setButton(12, xbox360[0].y);

# Face buttons Back, Start
vJoy[0].setButton(0, xbox360[0].back)
vJoy[0].setButton(3, xbox360[0].start)

# Analogue buttons L click, R click
#vJoy[0].setButton(1, xbox360[0].leftThumb)
#vJoy[0].setButton(2, xbox360[0].rightThumb)

# Joysticks
if casting:
	vJoy[0].x = filters.mapRange(xbox360[0].rightStickX, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
	vJoy[0].y = filters.mapRange(xbox360[0].rightStickY, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
else:
	vJoy[0].x = filters.mapRange(xbox360[0].leftStickX, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
	vJoy[0].y = filters.mapRange(xbox360[0].leftStickY, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)

# Replaced by spellstick emulator below
#vJoy[0].z = filters.mapRange(xbox360[0].rightStickX, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)
#vJoy[0].rz = filters.mapRange(xbox360[0].rightStickY, -1.0, 1.0, -vJoy[0].axisMax, vJoy[0].axisMax)


# Buffered inputs (related to spell-casting)

def queueButtonEvent(button, newValue):
	inputQueue.insert(0, lambda: (
		setState(States.WAIT_TO_LISTEN),
		vJoy[0].setButton(button, newValue)
	))

# Face buttons D-pad, Up, Right, Down, Left
if xbox360[0].up and not previous['up']:
	previous['up'] = True
	queueButtonEvent(4, True)
elif not xbox360[0].up and previous['up']:
	previous['up'] = False
	queueButtonEvent(4, False)

if xbox360[0].down and not previous['down']:
	previous['down'] = True
	queueButtonEvent(5, True)
elif not xbox360[0].down and previous['down']:
	previous['down'] = False
	queueButtonEvent(5, False)

if xbox360[0].left and not previous['left']:
	previous['left'] = True
	queueButtonEvent(6, True)
elif not xbox360[0].left and previous['left']:
	previous['left'] = False
	queueButtonEvent(6, False)

if xbox360[0].right and not previous['right']:
	previous['right'] = True
	queueButtonEvent(7, True)
elif not xbox360[0].right and previous['right']:
	previous['right'] = False
	queueButtonEvent(7, False)

# Shoulder buttons. LB, RB
if xbox360[0].leftShoulder and not previous['leftShoulder']:
	previous['leftShoulder'] = True
	queueButtonEvent(10, True)
elif not xbox360[0].leftShoulder and previous['leftShoulder']:
	previous['leftShoulder'] = False
	queueButtonEvent(10, False)

if xbox360[0].rightShoulder and not previous['rightShoulder']:
	previous['rightShoulder'] = True
	queueButtonEvent(11, True)
elif not xbox360[0].rightShoulder and previous['rightShoulder']:
	previous['rightShoulder'] = False
	queueButtonEvent(11, False)

# Triggers, L trigger, R Trigger
if xbox360[0].leftTrigger > 0.4 and not previous['leftTrigger']:
	previous['leftTrigger'] = True
	queueButtonEvent(8, True)
elif xbox360[0].leftTrigger < 0.2 and previous['leftTrigger']:
	previous['leftTrigger'] = False
	queueButtonEvent(8, False)

if xbox360[0].rightTrigger > 0.4 and not previous['rightTrigger']:
	previous['rightTrigger'] = True
	queueButtonEvent(9, True)
elif xbox360[0].rightTrigger < 0.2 and previous['rightTrigger']:
	previous['rightTrigger'] = False
	queueButtonEvent(9, False)

# Right stick X or Y (for casting)
if (abs(xbox360[0].rightStickX) + abs(xbox360[0].rightStickY)) > 0.6 and not previous['rightStickXOrY']:
	previous['rightStickXOrY'] = True
	inputQueue.insert(0, lambda: (
		setState(States.WAIT_TO_LISTEN),
		vJoy[0].setButton(16, True),
		setCasting(True)
	))
elif (abs(xbox360[0].rightStickX) + abs(xbox360[0].rightStickY)) < 0.4 and previous['rightStickXOrY']:
	previous['rightStickXOrY'] = False
	inputQueue.insert(0, lambda: (
		setState(States.WAIT_TO_LISTEN),
		vJoy[0].setButton(16, False),
		setCasting(False)
	))


# Spellstick emulator
def setZPositive():
	vJoy[0].z = vJoy[0].axisMax

def setZNegative():
	vJoy[0].z = -vJoy[0].axisMax

def setRzPositive():
	vJoy[0].rz = vJoy[0].axisMax

def setRzNegative():
	vJoy[0].rz = -vJoy[0].axisMax

if xbox360[0].a and not previous['a']:
	previous['a'] = True
	if xbox360[0].leftShoulder:
		inputQueue.insert(0, lambda: (
			setState(States.COLD),
			setZPositive()
		))
	else:
		inputQueue.insert(0, lambda: (
			setState(States.FIRE),
			setZPositive()
		))
elif not xbox360[0].a and previous['a']:
	previous['a'] = False

if xbox360[0].b and not previous['b']:
	previous['b'] = True
	if xbox360[0].leftShoulder:
		inputQueue.insert(0, lambda: (
			setState(States.SHIELD),
			setRzNegative()
		))
	else:
		inputQueue.insert(0, lambda: (
			setState(States.EARTH),
			setRzNegative()
		))
elif not xbox360[0].b and previous['b']:
	previous['b'] = False

if xbox360[0].x and not previous['x']:
	previous['x'] = True
	if xbox360[0].leftShoulder:
		inputQueue.insert(0, lambda: (
			setState(States.WATER),
			setZNegative()
		))
	else:
		inputQueue.insert(0, lambda: (
			setState(States.LIGHTNING),
			setZNegative()
		))
elif not xbox360[0].x and previous['x']:
	previous['x'] = False

if xbox360[0].y and not previous['y']:
	previous['y'] = True
	if xbox360[0].leftShoulder:
		inputQueue.insert(0, lambda: (
			setState(States.LIFE),
			setRzPositive()
		))
	else:
		inputQueue.insert(0, lambda: (
			setState(States.ARCANE),
			setRzPositive()
		))
elif not xbox360[0].y and previous['y']:
	previous['y'] = False

# Finite state machine
if state == States.LISTENING:
	if len(inputQueue):
		input = inputQueue.pop()
		input()
		start_time = time.clock()
elif state == States.COLD:
	if time.clock() - start_time > THRESHOLD:
		state = States.RESET
		vJoy[0].z = 0
		vJoy[0].rz = vJoy[0].axisMax
		start_time = time.clock()
elif state == States.SHIELD:
	if time.clock() - start_time > THRESHOLD:
		state = States.RESET
		vJoy[0].rz = 0
		vJoy[0].z = vJoy[0].axisMax
		start_time = time.clock()
elif state == States.WATER:
	if time.clock() - start_time > THRESHOLD:
		state = States.RESET
		vJoy[0].z = 0
		vJoy[0].rz = vJoy[0].axisMax
		start_time = time.clock()
elif state == States.LIFE:
	if time.clock() - start_time > THRESHOLD:
		state = States.RESET
		vJoy[0].rz = 0
		vJoy[0].z = -vJoy[0].axisMax
		start_time = time.clock()
elif state == States.FIRE:
	if time.clock() - start_time > THRESHOLD:
		state = States.RESET
		vJoy[0].z = 0
		vJoy[0].rz = -vJoy[0].axisMax
		start_time = time.clock()
elif state == States.EARTH:
	if time.clock() - start_time > THRESHOLD:
		state = States.RESET
		vJoy[0].rz = 0
		vJoy[0].z = -vJoy[0].axisMax
		start_time = time.clock()
elif state == States.LIGHTNING:
	if time.clock() - start_time > THRESHOLD:
		state = States.RESET
		vJoy[0].z = 0
		vJoy[0].rz = -vJoy[0].axisMax
		start_time = time.clock()
elif state == States.ARCANE:
	if time.clock() - start_time > THRESHOLD:
		state = States.RESET
		vJoy[0].rz = 0
		vJoy[0].z = vJoy[0].axisMax
		start_time = time.clock()
elif state == States.RESET:
	if time.clock() - start_time > THRESHOLD:
		state = States.WAIT_TO_LISTEN
		vJoy[0].z = 0
		vJoy[0].rz = 0
		start_time = time.clock()
else:
	if time.clock() - start_time > THRESHOLD:
		state = States.LISTENING

#diagnostics.watch(state)
#diagnostics.watch(vJoy[0].z)
#diagnostics.watch(vJoy[0].rz)
#diagnostics.watch(previous['a'])
#diagnostics.watch(previous['b'])
#diagnostics.watch(previous['x'])
#diagnostics.watch(previous['y'])
