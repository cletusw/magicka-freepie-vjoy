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

def setState1(newState):
	global state1
	state1 = newState

def setCasting1(newValue):
	global casting1
	casting1 = newValue

if starting:
	States = enum('RESET', 'WAIT_TO_LISTEN', 'LISTENING', 'COLD', 'SHIELD', 'WATER', 'LIFE', 'FIRE', 'EARTH', 'LIGHTNING', 'ARCANE')
	THRESHOLD = 0.09
	start_time1 = time.clock()
	state1 = States.LISTENING
	previous1 = {
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
	inputQueue1 = []
	casting1 = False


# Un-buffered inputs (for menus, inventory, or unused)

# Face buttons Y,B,A,X
vJoy[1].setButton(14, xbox360[1].a);
vJoy[1].setButton(13, xbox360[1].b);
vJoy[1].setButton(15, xbox360[1].x);
vJoy[1].setButton(12, xbox360[1].y);

# Face buttons Back, Start
vJoy[1].setButton(0, xbox360[1].back)
vJoy[1].setButton(3, xbox360[1].start)

# Analogue buttons L click, R click
#vJoy[1].setButton(1, xbox360[1].leftThumb)
#vJoy[1].setButton(2, xbox360[1].rightThumb)

# Joysticks
if casting1:
	vJoy[1].x = filters.mapRange(xbox360[1].rightStickX, -1.0, 1.0, -vJoy[1].axisMax, vJoy[1].axisMax)
	vJoy[1].y = filters.mapRange(xbox360[1].rightStickY, -1.0, 1.0, -vJoy[1].axisMax, vJoy[1].axisMax)
else:
	vJoy[1].x = filters.mapRange(xbox360[1].leftStickX, -1.0, 1.0, -vJoy[1].axisMax, vJoy[1].axisMax)
	vJoy[1].y = filters.mapRange(xbox360[1].leftStickY, -1.0, 1.0, -vJoy[1].axisMax, vJoy[1].axisMax)

# Replaced by spellstick emulator below
#vJoy[1].z = filters.mapRange(xbox360[1].rightStickX, -1.0, 1.0, -vJoy[1].axisMax, vJoy[1].axisMax)
#vJoy[1].rz = filters.mapRange(xbox360[1].rightStickY, -1.0, 1.0, -vJoy[1].axisMax, vJoy[1].axisMax)


# Buffered inputs (related to spell-casting)

def queueButtonEvent1(button, newValue):
	inputQueue1.insert(0, lambda: (
		setState1(States.WAIT_TO_LISTEN),
		vJoy[1].setButton(button, newValue)
	))

# Face buttons D-pad, Up, Right, Down, Left
if xbox360[1].up and not previous1['up']:
	previous1['up'] = True
	queueButtonEvent1(4, True)
elif not xbox360[1].up and previous1['up']:
	previous1['up'] = False
	queueButtonEvent1(4, False)

if xbox360[1].down and not previous1['down']:
	previous1['down'] = True
	queueButtonEvent1(5, True)
elif not xbox360[1].down and previous1['down']:
	previous1['down'] = False
	queueButtonEvent1(5, False)

if xbox360[1].left and not previous1['left']:
	previous1['left'] = True
	queueButtonEvent1(6, True)
elif not xbox360[1].left and previous1['left']:
	previous1['left'] = False
	queueButtonEvent1(6, False)

if xbox360[1].right and not previous1['right']:
	previous1['right'] = True
	queueButtonEvent1(7, True)
elif not xbox360[1].right and previous1['right']:
	previous1['right'] = False
	queueButtonEvent1(7, False)

# Shoulder buttons. LB, RB
if xbox360[1].leftShoulder and not previous1['leftShoulder']:
	previous1['leftShoulder'] = True
	queueButtonEvent1(10, True)
elif not xbox360[1].leftShoulder and previous1['leftShoulder']:
	previous1['leftShoulder'] = False
	queueButtonEvent1(10, False)

if xbox360[1].rightShoulder and not previous1['rightShoulder']:
	previous1['rightShoulder'] = True
	queueButtonEvent1(11, True)
elif not xbox360[1].rightShoulder and previous1['rightShoulder']:
	previous1['rightShoulder'] = False
	queueButtonEvent1(11, False)

# Triggers, L trigger, R Trigger
if xbox360[1].leftTrigger > 0.4 and not previous1['leftTrigger']:
	previous1['leftTrigger'] = True
	queueButtonEvent1(8, True)
elif xbox360[1].leftTrigger < 0.2 and previous1['leftTrigger']:
	previous1['leftTrigger'] = False
	queueButtonEvent1(8, False)

if xbox360[1].rightTrigger > 0.4 and not previous1['rightTrigger']:
	previous1['rightTrigger'] = True
	queueButtonEvent1(9, True)
elif xbox360[1].rightTrigger < 0.2 and previous1['rightTrigger']:
	previous1['rightTrigger'] = False
	queueButtonEvent1(9, False)

# Right stick X or Y (for casting)
if (abs(xbox360[1].rightStickX) + abs(xbox360[1].rightStickY)) > 0.6 and not previous1['rightStickXOrY']:
	previous1['rightStickXOrY'] = True
	inputQueue1.insert(0, lambda: (
		setState1(States.WAIT_TO_LISTEN),
		vJoy[1].setButton(16, True),
		setCasting1(True)
	))
elif (abs(xbox360[1].rightStickX) + abs(xbox360[1].rightStickY)) < 0.4 and previous1['rightStickXOrY']:
	previous1['rightStickXOrY'] = False
	inputQueue1.insert(0, lambda: (
		setState1(States.WAIT_TO_LISTEN),
		vJoy[1].setButton(16, False),
		setCasting1(False)
	))


# Spellstick emulator
def setZPositive1():
	vJoy[1].z = vJoy[1].axisMax

def setZNegative1():
	vJoy[1].z = -vJoy[1].axisMax

def setRzPositive1():
	vJoy[1].rz = vJoy[1].axisMax

def setRzNegative1():
	vJoy[1].rz = -vJoy[1].axisMax

if xbox360[1].a and not previous1['a']:
	previous1['a'] = True
	if xbox360[1].leftShoulder:
		inputQueue1.insert(0, lambda: (
			setState1(States.COLD),
			setZPositive1()
		))
	else:
		inputQueue1.insert(0, lambda: (
			setState1(States.FIRE),
			setZPositive1()
		))
elif not xbox360[1].a and previous1['a']:
	previous1['a'] = False

if xbox360[1].b and not previous1['b']:
	previous1['b'] = True
	if xbox360[1].leftShoulder:
		inputQueue1.insert(0, lambda: (
			setState1(States.SHIELD),
			setRzNegative1()
		))
	else:
		inputQueue1.insert(0, lambda: (
			setState1(States.EARTH),
			setRzNegative1()
		))
elif not xbox360[1].b and previous1['b']:
	previous1['b'] = False

if xbox360[1].x and not previous1['x']:
	previous1['x'] = True
	if xbox360[1].leftShoulder:
		inputQueue1.insert(0, lambda: (
			setState1(States.WATER),
			setZNegative1()
		))
	else:
		inputQueue1.insert(0, lambda: (
			setState1(States.LIGHTNING),
			setZNegative1()
		))
elif not xbox360[1].x and previous1['x']:
	previous1['x'] = False

if xbox360[1].y and not previous1['y']:
	previous1['y'] = True
	if xbox360[1].leftShoulder:
		inputQueue1.insert(0, lambda: (
			setState1(States.LIFE),
			setRzPositive1()
		))
	else:
		inputQueue1.insert(0, lambda: (
			setState1(States.ARCANE),
			setRzPositive1()
		))
elif not xbox360[1].y and previous1['y']:
	previous1['y'] = False

# Finite state machine
if state1 == States.LISTENING:
	if len(inputQueue1):
		input1 = inputQueue1.pop()
		input1()
		start_time1 = time.clock()
elif state1 == States.COLD:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.RESET
		vJoy[1].z = 0
		vJoy[1].rz = vJoy[1].axisMax
		start_time1 = time.clock()
elif state1 == States.SHIELD:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.RESET
		vJoy[1].rz = 0
		vJoy[1].z = vJoy[1].axisMax
		start_time1 = time.clock()
elif state1 == States.WATER:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.RESET
		vJoy[1].z = 0
		vJoy[1].rz = vJoy[1].axisMax
		start_time1 = time.clock()
elif state1 == States.LIFE:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.RESET
		vJoy[1].rz = 0
		vJoy[1].z = -vJoy[1].axisMax
		start_time1 = time.clock()
elif state1 == States.FIRE:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.RESET
		vJoy[1].z = 0
		vJoy[1].rz = -vJoy[1].axisMax
		start_time1 = time.clock()
elif state1 == States.EARTH:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.RESET
		vJoy[1].rz = 0
		vJoy[1].z = -vJoy[1].axisMax
		start_time1 = time.clock()
elif state1 == States.LIGHTNING:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.RESET
		vJoy[1].z = 0
		vJoy[1].rz = -vJoy[1].axisMax
		start_time1 = time.clock()
elif state1 == States.ARCANE:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.RESET
		vJoy[1].rz = 0
		vJoy[1].z = vJoy[1].axisMax
		start_time1 = time.clock()
elif state1 == States.RESET:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.WAIT_TO_LISTEN
		vJoy[1].z = 0
		vJoy[1].rz = 0
		start_time1 = time.clock()
else:
	if time.clock() - start_time1 > THRESHOLD:
		state1 = States.LISTENING
