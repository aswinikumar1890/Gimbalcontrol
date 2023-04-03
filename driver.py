from gimbalcontrol import GimbalControl as GC
import time
from datetime import datetime
gc = GC('params.json')

# roll -45 to +45
# pitch -320 to +320
# yaw -90 to +45

def main():

	gc.reset
	stime = datetime.now()
	stop = False
	while not stop:
		try:
			args = input('<op> <val1> <val2>:').strip().split()
			if args[0] in ['pitch','yaw','roll']:
				gc.moveto(args[0],float(args[1]))
			elif args[0]== 'left':
				gc.moveleft
			elif args[0]== 'right':
				gc.moveright
			elif args[0]== 'up':
				gc.moveup
			elif args[0]== 'down':
				gc.movedown
			elif args[0]== 'reset':
				gc.reset
			elif args[0]== 'stop':
				gc.stop
			elif args[0]== 'speed':
				gc.setspeed(int(args[1]))
			elif args[0] == 'getspeed':
				speed_curr = gc.getspeed
				print(speed_curr)
			elif args[0] == 'sweep':
				gc.sweep(int(args[1]),int(args[2]))
			elif args[0] == 'getposition':
				pos = gc.getposition
				print(pos)
			elif args[0] == 'setposition':
				gc.setposition(pos={"pitch":float(args[1]),"roll":float(args[2]),"yaw":float(args[3])})
			elif args[0] == 'q' or args[0] == 'quit':
				gc.reset
				break
			else:
				print(f'unknown operation {args[0]}')
		except Exception as e:
			print(e)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        gc.reset()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
