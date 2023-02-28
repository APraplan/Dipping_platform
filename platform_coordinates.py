# Anycubic
SAFE_MOVE_HEIGHT = 150
MIN_X_FOR_ROTATION = 30
MAX_X_FOR_ROTATION = 190

HEIGHT_STORE_1 = 200
HEIGHT_STORE_2 = 170
HEIGHT_STORE_3 = 140
HEIGHT_STORE_4 = 110
HEIGHT_STORE_5 = 80

# Dynamixel 1
UP = 0
DOWN = 2051
LEFT = 1026
RIGHT = 3077

# Dynamixel 2
ANGLE_MINUS_90 = 0
ANGLE_0 = 0
ANGLE_90 = 0


class Solution:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


# Solutions
solution1 = Solution(10, 10, 10)
solution2 = Solution(50, 10, 10)
clean_solution = Solution(25, 25, 10)

