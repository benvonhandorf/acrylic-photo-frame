from pixelring import PixelRing

class APA102Ring(PixelRing):
	def __init__(self, apa102, offset, count):
		super().__init__(offset, count)
		self.apa102 = apa102
		self.brightness = 10

	def set(self, position, color):
		if(position < 0):
			position = position + self.count

		position = position % self.count

		colorWithBrightness = (color[0], color[1], color[2], self.brightness)

		self.apa102[self.offset + position] = colorWithBrightness

	def get(self, position):
		if(position < 0):
			position = position + self.count

		position = position % self.count

		colorWithBrightness = self.apa102[self.offset + position]

		return (colorWithBrightness[0], colorWithBrightness[1], colorWithBrightness[2])

	def write(self):
		self.apa102.write()
		self.apa102.write()
