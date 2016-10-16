import random, pygame, sys

cell_size = 40
cols = 10
rows = 22
fps = 1.5

colors = {0: (255, 255, 230),
		  1: (255, 0, 0),
          2: (255, 255, 0),
          3: (255, 0, 255),
          4: (255, 128, 0),
          5: (0, 0, 255),
          6: (0, 255, 0),
          7: (0, 160, 160)
          }
          
white = (255, 255, 255)
black = (0, 0, 0)

tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 2, 2],
	 [2, 2, 0]],
	
	[[3, 3, 0],
	 [0, 3, 3]],
	
	[[4, 0, 0],
	 [4, 4, 4]],
	
	[[0, 0, 5],
	 [5, 5, 5]],
	
	[[6, 6, 6, 6]],
	
	[[7, 7],
	 [7, 7]]
]

def new_board():
	board = [[0 for x in range(cols)] 
			  for y in range(rows)]

	board += [[1 for x in range(cols)]]
	return board

def join_matrixes(mat1, mat2, mat2_off):
	off_y, off_x = mat2_off
	for cy, row in enumerate(mat2):
		for cx, val in enumerate(row):
			mat1[cy+off_y-1	][cx+off_x] += val
	return mat1

def collision(board, shape, coord):
	#coord is an tuple of size 2 that will represent the shapes' position on the board
	#coord[0] is y position and coord[1] is x position
	y_add = coord[0]
	x_add = coord[1]

	if y_add < 0 or y_add > (rows - len(shape)) or x_add < 0 or (x_add > cols - len(shape[0])):
 		return True


	for y in range(len(shape)):
		for x in range(len(shape[0])):
			#there is another piece in this position on the board
			if shape[y][x] != 0 and board[y + y_add][x + x_add] != 0:
				return True
	return False
	# off_x, off_y = offset
	# if off_x < 0 or off_y < 0:
	# 	return True
	# for cy, row in enumerate(shape):
	# 	for cx, cell in enumerate(row):
	# 		try:
	# 			if cell and board[ cy + off_y ][ cx + off_x ]:
	# 				return True
	# 		except IndexError:
	# 			return True
	# return False





class playTetris(object):
	def __init__(self):
		pygame.init()
		self.width = cols * cell_size + 300
		self.height = rows * cell_size
		self.gameover = False
		self.paused = False
		self.gameDisplay = pygame.display.set_mode((self.width, self.height))
		self.gameDisplay.fill(white)
		pygame.display.set_caption("Tetris by Josh")
		self.board = new_board()
		#self.clock = pygame.time.Clock()
		self.next_piece = tetris_shapes[random.randrange(0, len(tetris_shapes))]

	def init_game(self): #resets data for a game restart
		self.score = 0
		self.new_piece()
		self.level = 0
		self.lines = 0

	def new_piece(self):
		self.piece = self.next_piece[:]
		self.next_piece = tetris_shapes[random.randrange(0, len(tetris_shapes))]

		self.x_coord = int(cols/2 - len(self.piece[0])/2)
		self.y_coord = 0
		print self.x_coord
		print self.y_coord
		if collision(self.board, self.piece, (self.y_coord, self.x_coord)):
			self.gameover = True

	def draw_matrix(self, matrix, coord):
	# draws a grid representation of a matrix
	# will be used for the draw tetrimino shapes and the board itself
		y_add = coord[0]
		x_add = coord[1]
		for y in range(len(matrix)):
			for x in range(len(matrix[0])):
				pygame.draw.rect(self.gameDisplay, colors[matrix[y][x]], (((x + coord[1]) *cell_size, (y + coord[0])*cell_size, cell_size, cell_size)))

	def move(self, x):
		if not self.gameover and not self.paused:
			new_x = self.x_coord + x

			if not collision (self.board, self.piece, (self.y_coord, new_x)):
				self.x_coord = new_x

	def drop(self, manual):
		if not self.gameover and not self.paused:
			self.y_coord += 1

			print collision(self.board, self.piece, (self.y_coord, self.x_coord))
			if collision(self.board, self.piece, (self.y_coord, self.x_coord)):
				join_matrixes(self.board, self.piece, (self.y_coord, self.x_coord))
				self.new_piece()
				return True

		return False


	def rotate(self):
		if not self.gameover and not self.paused:
			new_shape = [[0 for x in range(len(self.piece))]
							for y in range(len(self.piece[0]))]

			for y in range(len(self.piece)):
				for x in range(len(self.piece[0])):
					new_shape[x][y] = self.piece[y][x]

			if not collision(self.board, new_shape, (self.y_coord, self.x_coord)):
				self.piece = new_shape

	def run(self):

		key_actions = {
			#'ESCAPE':	self.quit,
			'LEFT':		lambda:self.move(-1),
			'RIGHT':	lambda:self.move(+1),
			'DOWN':		lambda:self.drop(True),
			'UP':		self.rotate,
			# 'p':		self.toggle_pause,
			# 'SPACE':	self.start_game,
			# 'RETURN':	self.insta_drop
		}

		self.init_game()

		while 1:
			if self.gameover:
				pygame.quit()
				quit()
			self.draw_matrix(self.board, (0,0))
			self.draw_matrix(self.piece, (self.y_coord, self.x_coord))
			
			#self.drop(True)
			
			clock = pygame.time.Clock()
			
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					for key in key_actions:
						if event.key == eval("pygame.K_" + key):
							key_actions[key]()
			clock.tick(3)
if __name__ == '__main__':
	Tetris = playTetris()
	Tetris.run()