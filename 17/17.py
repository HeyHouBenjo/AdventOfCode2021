import math
import re

with open("input") as file:
	target = file.read().removesuffix("\n")
	minX, maxX, minY, maxY = [int(v) for v in re.search(r"x=(.+)\.\.(.+), y=(.+)\.\.(.+)", target).groups()]

# minimize the set of velocities to check via bounds
# lower x bound cant be lower than a
# where a(a+1)/2 = minX (little gauss)
# because posX loses 1 every step and posX must at least reach minX
# isolating a gives -0.5 + sqrt(0.25 + 2 * minX)
# ceiling is enough because if minX gets a bit higher then a cannot reach it anymore
xBounds = math.ceil(-0.5 + math.sqrt(0.25 + 2 * minX)), maxX

# yPos is symmetric on the way back down and starts with 0
yBounds = minY, -minY

xRange = range(xBounds[0], xBounds[1] + 1)
yRange = range(yBounds[0], yBounds[1] + 1)

validCount = 0
allMaxYReached = []

# simulate all possible velocities
for vx, vy in [(x, y) for x in xRange for y in yRange]:
	posX, posY = 0, 0
	maxYReached = 0
	while posX <= maxX and posY >= minY:
		if posX >= minX and posY <= maxY:
			# target hit
			validCount += 1
			allMaxYReached.append(maxYReached)
			break
		posX += vx
		posY += vy
		vx -= 1 if vx > 0 else 0
		vy -= 1
		maxYReached = max(posY, maxYReached)

print(max(allMaxYReached))
print(validCount)
