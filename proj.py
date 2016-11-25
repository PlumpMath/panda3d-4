from direct.showbase.ShowBase import ShowBase
import sys
import math
from pandac.PandaModules import WindowProperties
from direct.gui.OnscreenText import OnscreenText
props = WindowProperties()
props.setCursorHidden(True)
props.setMouseMode(WindowProperties.M_relative)
class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.win.requestProperties(props)
		self.disableMouse()
		self.bunny = self.loader.loadModel('./models/bvw-f2004--bunny/bunny')
		self.bunny.reparentTo(self.render)
		self.bunny.setPos(0,20,0)

		self.env = self.loader.loadModel('./models/bvw-f2004--streetscene/street-scene')
		self.env.reparentTo(self.render)
		self.env.setPos(-20,20,0)
		self.call1 = OnscreenText(text = 'Position (Bunny):' , pos = (-.85, .8), scale = .09 , fg = (1,1,1,1))
		self.call2 = OnscreenText(text = 'Position (Camera):' , pos = (-.85, .7), scale = .09 , fg = (1,1,1,1))
		self.call3 = OnscreenText(text = 'Rotation (Bunny):' , pos = (-.85, 0.6), scale = .09 , fg = (1,1,1,1))
		self.call4 = OnscreenText(text = 'Rotation (Camera):' , pos = (-.85, 0.5), scale = .09 , fg = (1,1,1,1))

		self.accept('wheel_up',self.Big)
		self.accept('wheel_down',self.Little)
		self.accept('escape',sys.exit)
		self.accept('space', self.jump)

		taskMgr.add(phys,'time')
		taskMgr.add(mouse,'mouse')
		taskMgr.add(texter,'text')

		self.buttons = {key : False for key in 'wsadol976428k;rf'}
		for key in self.buttons:
			self.accept(key,self.buttonD,[key])
			self.accept(key+'-up',self.buttonU,[key])

	def buttonU(self,button):
		self.buttons[button] = False;
	def buttonD(self,button):
		self.buttons[button] = True;
	def jump(self):
		if base.bunny.getZ() == 0:
			self.bunny.setZ(.01)
			self.vz = .5
	def Big(self):
		sc = self.bunny.getScale()
		self.bunny.setScale(sc+.03)
	def Little(self):
		sc = self.bunny.getScale()
		self.bunny.setScale(sc-.03)

def phys(task):
	x,y,z = base.bunny.getPos()
	xc,yc,zc = base.camera.getPos()
	h,p,r = base.camera.getHpr()
	hh,pp,rr = base.bunny.getHpr()
	camvz,camvy,camvx = 0,0,0
	vy,vx = 0,0
	if z < 0:
		base.bunny.setZ(0)
		base.vz = .01
	if z != 0:
		base.vz -= .01
		base.bunny.setZ(base.bunny.getZ() + base.vz)
	if base.buttons['w']:
		vy = -.2*math.cos(hh*math.pi/180)
		vx = .2*math.sin(hh*math.pi/180)
	if base.buttons['s']:
		vy = .2*math.cos(hh*math.pi/180)
		vx = -.2*math.sin(hh*math.pi/180)
	if base.buttons['d']:
		vx = -.2*math.cos(hh*math.pi/180)
		vy = -.2*math.sin(hh*math.pi/180)
	if base.buttons['a']:
		vx = .2*math.cos(hh*math.pi/180)
		vy = .2*math.sin(hh*math.pi/180)
	if zc < 0:
		base.camera.setZ(0)
		camvz = .01
	else:
		if base.buttons['o']:
			camvx -= .2*math.sin(h*math.pi/180)
			camvy += .2*math.cos(h*math.pi/180)
			camvz += .2*math.sin(p*math.pi/180)
		if base.buttons['l']:
			camvx += .2*math.sin(h*math.pi/180)
			camvy -= .2*math.cos(h*math.pi/180)
			camvz -= .2*math.sin(p*math.pi/180)
		if base.buttons['r']:
			camvz += .2
		if base.buttons['f']:
			camvz -= .2
		if base.buttons['k']:
			camvx -= .2*math.cos(h*math.pi/180)
			camvy -= .2*math.sin(h*math.pi/180)
		if base.buttons[';']:
			camvx += .2*math.cos(h*math.pi/180)
			camvy += .2*math.sin(h*math.pi/180)
	if base.buttons['9']:
		base.bunny.setR(rr+4)
	if base.buttons['7']:
		base.bunny.setR(rr-4)
	if base.buttons['6']:
		base.bunny.setH(hh+4)
	if base.buttons['4']:
		base.bunny.setH(hh-4)
	if base.buttons['2']:
		base.bunny.setP(pp+4)
	if base.buttons['8']:
		base.bunny.setP(pp-4)

	base.bunny.setY( y + vy )
	base.bunny.setX( x + vx )
	base.camera.setPos( xc + camvx, yc + camvy ,zc + camvz )
	return task.cont
def mouse(task):
	if base.mouseWatcherNode.hasMouse():
		props = base.win.getProperties()
		x=base.mouseWatcherNode.getMouseX()
		y=base.mouseWatcherNode.getMouseY()
		h,p,r = base.camera.getHpr()
		base.camera.setHpr(h - 10*math.atan(x),p + 10*math.atan(y),0)
		base.win.movePointer(0,
            int(props.getXSize() / 2),
            int(props.getYSize() / 2))
	return task.cont
def texter(task):
	x,y,z = base.bunny.getPos()
	xc,yc,zc = base.camera.getPos()
	h,p,r = base.camera.getHpr()
	hh,pp,rr = base.bunny.getHpr()
	base.call1.setText('Position (Bunny): %u %i %d' %(x,y,z))
	base.call2.setText('Position (Camera): %u %i %d' %(xc,yc,zc))
	base.call3.setText('Rotation (Bunny): %u %i %d' %(hh,pp,rr))
	base.call4.setText('Rotation (Camera): %u %i %d' %(h,p,r))
	return task.cont

MyApp().run()
