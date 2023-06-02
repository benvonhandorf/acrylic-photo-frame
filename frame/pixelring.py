import math

class PixelRing:
	def __init__(self, offset, count):
		self.offset = offset
		self.count = count
		self.baseHSV = (0, 0, 0)
		self.sourceHSV = list( (0,0,0) for x in range(0, count))
		self.targetHSV = list( (0,0,0) for x in range(0, count))
		self.animationFrames = 0
		self.animationFrameCount = 0
		self.defaultAnimationFrames = 10

	def fill(self, color):
		for x in range(0, self.count):
			# print("Setting position " + str(x))
			self.set(x, color)

	def rotateCW(self):
		outstandingColor = self.get(self.count - 1)

		for x in reversed(range(1, self.count)):
			self.set(x, self.get(x - 1))

		self.set(0, outstandingColor)

	def rotateCCW(self):
		outstandingColor = self.get(0)

		for x in range(0, self.count - 1):
			self.set(x, self.get(x + 1))

		self.set(self.count - 1, outstandingColor)

	def push(self, newColor):
		for x in range(0, self.count):
			existingColor = self.get(x)
			self.set(x, newColor)
			newColor = existingColor


	def apply(self, func):
		for x in range(0, self.count):
			newValue = func(get(self, x), x)
			self.set(x, newValue)

	def clear(self):
		self.fill((0,0,0))

	def avgColors(self, color1, color1weight, color2, color2weight):
		newColor = (int((color1[0] * color1weight + color2[0] * color2weight) / (color1weight + color2weight)),
			int((color1[1] * color1weight + color2[1] * color2weight) / (color1weight + color2weight)),
			int((color1[2] * color1weight + color2[2] * color2weight) / (color1weight + color2weight)))

		return newColor

	def flare(self, position, radius, color):
		self.set(position, color)

		for x in range(0, radius):
			existingColor = self.get(position + x + 1)
			flareColor = self.avgColors(color, radius - x, existingColor, x + 1)
			self.set(position + x + 1, flareColor)
			existingColor = self.get(position - x - 1)
			flareColor = self.avgColors(color, radius - x, existingColor, x + 1)
			self.set(position - x - 1, flareColor)

	def rocket(self, position, direction, trail, color):
		self.set(position, color)

		for x in range(0, trail):
			existingColor = self.get(position + (x  * direction))
			flareColor = self.avgColors(color, trail - x, existingColor, x + 1)
			self.set(position + (x  * direction), flareColor)

	def setBaseHSV(self, hsv):
		self.baseHSV = hsv

	def avgHSV(self, color1, color2, animationFraction):
		color2weight = math.sin(animationFraction * 1.57)
		color1weight = 1.0 - color2weight
		newColor = ((color1[0] * color1weight + color2[0] * color2weight),
			(color1[1] * color1weight + color2[1] * color2weight) / (color1weight + color2weight),
			(color1[2] * color1weight + color2[2] * color2weight) / (color1weight + color2weight))

		return newColor

	def pushOffsetHSV(self, offset):
		self.animationFrames = self.defaultAnimationFrames
		self.animationFrameCount = 0

		alteredHSV = (self.baseHSV[0] + offset[0], self.baseHSV[1] + offset[1], self.baseHSV[2] + offset[2])

		self.targetHSV.insert(0, alteredHSV)
		self.targetHSV = self.targetHSV[0:self.count]

	def animate(self):
		if self.animationFrameCount >= self.animationFrames:
			return False

		self.animationFrameCount = self.animationFrameCount + 1
		animationFraction = self.animationFrameCount / self.animationFrames

		for cell in range(0, self.count):
			cellHSV = self.avgHSV(self.sourceHSV[cell], self.targetHSV[cell], animationFraction)
			colorRGB = PixelRing.hsvToRGBByte(cellHSV) 
			self.set(cell, colorRGB)  

			if animationFraction >= 1.0:
				self.sourceHSV[cell] = self.targetHSV[cell]

		return True

	def normalizeByte(data):
		if data > 255:
			data = 255

		if data < 0:
			data = 0

		return int(data)

	def hsvToRGBByte(hsv):
		rgb = PixelRing.hsvtorgb(hsv[0], hsv[1], hsv[2])
		rgb = (PixelRing.normalizeByte(rgb[0] * 255), PixelRing.normalizeByte(rgb[1] * 255), PixelRing.normalizeByte(rgb[2] * 255)) 

		return rgb

	def hsvtorgb(h,s,v):
		if s == 0.0: return (v, v, v)
		i = int(h*6.) # XXX assume int() truncates!
		f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
		if i == 0: return (v, t, p)
		if i == 1: return (q, v, p)
		if i == 2: return (p, v, t)
		if i == 3: return (p, q, v)
		if i == 4: return (t, p, v)
		if i == 5: return (v, p, q)

	
