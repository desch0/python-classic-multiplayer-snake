import json
from channels.generic.websocket import WebsocketConsumer
from .scheme import *
import asyncio
import threading

class GameDataConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()

	def disconnect(self, close_code):
		self.room.kill_snake(self.key)

	def receive(self, text_data):
		meta = json.loads(text_data)

		if meta['type'] == 'start_game':
			name = meta['name']
			self.room = get_room()
			self.key = self.room.init_snake(name)
			if self.key != None:
				self.send(json.dumps({'type': 'key', 'key': self.key}))
				threading.Thread(target=self.stream, args=()).start()

		if meta['type'] == 'change_direction':
			key = meta['key']
			action = int(meta['action'])

			if self.room.is_auth(key):
				snake = self.room.get_snake(key)
				snake.move(action)

	def render_response(self):
		is_alive = False
		snakes_cells = []
		for snake in self.room.snakes:
			snakes_cells.append([snake.name, snake.skin, [transform_coordinates(cell.x, cell.y) for cell in snake.cells]])
			if snake.key == self.key: is_alive = True

		return json.dumps({
			'type': 'data',
			'appleCell' : transform_coordinates(self.room.apple.x, self.room.apple.y),
			'snakesCells': snakes_cells,
			'is_alive': is_alive
		})

	def stream(self):
		while True:
			self.send(self.render_response())
			time.sleep(0.02)
