import random, string, threading, time
from .gameconfig import *

def transform_coordinates(x, y):
	result = field_width*(y-1)+x
	return result

def restoration_coordinates(point):
	y = round(point/field_width)
	x = point - field_width*(y-1)
	return [x, y]

class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move_to(self, x, y):
		self.x = x
		self.y = y

def check_lose(my_snake, room, direction):
	if direction==1:
		if my_snake.cells[0].y==1:
			my_snake.room.kill_snake(my_snake.key)
			return 1

		for snake in room.snakes:
			if snake.key == my_snake.key:
				for i in range(2, snake.length):
					if (snake.cells[0].y-1==snake.cells[i].y) and (snake.cells[0].x == snake.cells[i].x):
						return 1
			else:
				for i in range(snake.length):
					if (my_snake.cells[0].y-1==snake.cells[i].y) and (my_snake.cells[0].x == snake.cells[i].x):
						return 1

	if direction==2:
		if my_snake.cells[0].x==field_width:
			my_snake.room.kill_snake(my_snake.key)
			return 1

		for snake in room.snakes:
			if snake.key == my_snake.key:
				for i in range(2, snake.length):
					if (snake.cells[0].y==snake.cells[i].y) and (snake.cells[0].x+1 == snake.cells[i].x):
						return 1
			else:
				for i in range(snake.length):
					if (my_snake.cells[0].y==snake.cells[i].y) and (my_snake.cells[0].x+1 == snake.cells[i].x):
						return 1

	if direction==3:
		if my_snake.cells[0].y==field_height:
			my_snake.room.kill_snake(my_snake.key)
			return 1

		for snake in room.snakes:
			if snake.key == my_snake.key:
				for i in range(2, snake.length):
					if (snake.cells[0].y+1==snake.cells[i].y) and (snake.cells[0].x == snake.cells[i].x):
						return 1
			else:
				for i in range(snake.length):
					if (my_snake.cells[0].y+1==snake.cells[i].y) and (my_snake.cells[0].x == snake.cells[i].x):
						return 1

	if direction==4:
		if my_snake.cells[0].x==1:
			return 1

		for snake in room.snakes:
			if snake.key == my_snake.key:
				for i in range(2, snake.length):
					if (snake.cells[0].y==snake.cells[i].y) and (snake.cells[0].x-1 == snake.cells[i].x):
						return 1
			else:
				for i in range(snake.length):
					if (my_snake.cells[0].y==snake.cells[i].y) and (my_snake.cells[0].x-1 == snake.cells[i].x):
						return 1
	return 0



class Snake:
	skins = ['red', 'blue', 'pink', 'yellow', 'black']

	def __init__(self, room, name):
		self.name = name
		x = random.randint(3, field_width-3)
		y = random.randint(3, field_height-3)
		self.length = 2
		self.direction = random.randint(1, 4)
		self.room = room
		self.cells = [Cell(x, y), Cell(x, y-1 if self.direction==3 else y+1)]
		self.skin = random.choice(__class__.skins)
		# random string key
		self.key = "".join(random.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits) for x in range(34))

		def motor(snake):
			while 1:
				# We check if there is a snake head in the apple cell, if so, it grows.
				if (snake.cells[0].x==snake.room.apple.x) and (snake.cells[0].y==snake.room.apple.y):
					snake.extend()
					snake.room.apple = Apple(random.randint(1, field_width), random.randint(1,field_height))

				if snake.direction==1:
					if check_lose(snake, snake.room, 1) == 1:
						snake.room.kill_snake(snake.key)
						return
					snake.move_top()

				if snake.direction==2:
					if check_lose(snake, snake.room, 2) == 1:
						snake.room.kill_snake(snake.key)
						return
					snake.move_right()

				if snake.direction==3:
					if check_lose(snake, snake.room, 3) == 1:
						snake.room.kill_snake(snake.key)
						return
					snake.move_bottom()

				if snake.direction==4:
					if check_lose(snake, snake.room, 4) == 1:
						snake.room.kill_snake(snake.key)
						return
					snake.move_left()

				time.sleep(game_interval) 	# Interval time to move snake's cells

		threading.Thread(target=motor, args=(self, )).start()

	def move_top(self):
		if self.cells[1].y < self.cells[0].y: return

		oldcells = []
		for cell in self.cells:
			oldcells.append([cell.x, cell.y]);


		self.cells[0].move_to(self.cells[0].x, self.cells[0].y-1)
		for i in range(1, self.length):
			self.cells[i].move_to(oldcells[i-1][0], oldcells[i-1][1])

	def move_right(self):
		if self.cells[1].x > self.cells[0].x: return

		oldcells = []
		for cell in self.cells:
			oldcells.append([cell.x, cell.y])


		self.cells[0].move_to(self.cells[0].x+1, self.cells[0].y)
		for i in range(1, self.length):
			self.cells[i].move_to(oldcells[i-1][0], oldcells[i-1][1])

	def move_bottom(self):
		if self.cells[1].y > self.cells[0].y: return

		oldcells = []
		for cell in self.cells:
			oldcells.append([cell.x, cell.y])


		self.cells[0].move_to(self.cells[0].x, self.cells[0].y+1)
		for i in range(1, self.length):
			self.cells[i].move_to(oldcells[i-1][0], oldcells[i-1][1])

	def move_left(self):
		if self.cells[1].x < self.cells[0].x: return

		oldcells = []
		for cell in self.cells:
			oldcells.append([cell.x, cell.y])


		self.cells[0].move_to(self.cells[0].x-1, self.cells[0].y)
		for i in range(1, self.length):
			self.cells[i].move_to(oldcells[i-1][0], oldcells[i-1][1])

	def move(self, direction):
		if (direction==1) and (self.direction != 3) and not ( (self.cells[0].x == self.cells[1].x) and (self.cells[0].y == self.cells[1].y+1) ):
			self.direction = direction
		if (direction == 2) and (self.direction != 4) and not ( (self.cells[0].x+1 == self.cells[1].x) and (self.cells[0].y == self.cells[1].y) ):
			self.direction = 2
		if (direction == 3) and (self.direction != 1) and not ( (self.cells[0].x == self.cells[1].x) and (self.cells[0].y+1 == self.cells[1].y) ):
			self.direction = 3
		if (direction == 4) and (self.direction != 2) and not ( (self.cells[0].x == self.cells[1].x+1) and (self.cells[0].y == self.cells[1].y) ):
			self.direction = 4

	def extend(self):
		if (self.direction == 1):
			self.cells.append(Cell(self.cells[self.length-1].x, self.cells[self.length-1].y+1))
			self.length += 1
			return

		if (self.direction == 2):
			self.cells.append(Cell(self.cells[self.length-1].x-1, self.cells[self.length-1].y))
			self.length += 1
			return

		if (self.direction == 3):
			self.cells.append(Cell(self.cells[self.length-1].x, self.cells[self.length-1].y-1))
			self.length += 1
			return

		if (self.direction == 4):
			self.cells.append(Cell(self.cells[self.length-1].x+1, self.cells[self.length-1].y))
			self.length += 1
			return


class Apple:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Room:
	amount = 0
	collector = []

	def __init__(self):
		self.__class__.amount += 1
		self.id = self.__class__.amount

		self.apple = Apple(random.randint(1, field_width), random.randint(1, field_height))
		self.snakes = []
		__class__.collector.append(self)

	def init_snake(self, name):
		if len(self.snakes) >= max_room_players: return None
		snake = Snake(self, name)
		self.snakes.append(snake)
		return snake.key

	def kill_snake(self, delete_snake_key):
		for snake in self.snakes:
			if snake.key == delete_snake_key:
				self.snakes.remove(snake)

	def is_auth(self, key):
		for snake in self.snakes:
			if snake.key == key: return True

		return False

	def get_snake(self, key):
		for snake in self.snakes:
			if snake.key == key: return snake

def get_room(id=None):
	rooms = Room.collector

	if id == None:
		if len(rooms) == 0:
			return Room()
		for room in rooms:
			if len(room.snakes) <= max_room_players: return room

	elif len(rooms) >= id and len(rooms[id-1].snakes) <= max_room_players:
   		return rooms[id-1]
