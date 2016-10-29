import random, pygame, sys

cell_size = 40
cols = 10
rows = 22
fps = 30

colors = {0: (0, 0, 0),
		  1: (255, 0, 0),
          2: (255, 255, 0),
          3: (255, 0, 255),
          4: (255, 128, 0),
          5: (0, 0, 255),
          6: (0, 255, 0),
          7: (0, 160, 160),
          8: (35, 35, 35)
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

def remove_row(board, row):
	del board[row]
	return [[0 for i in range(cols)]] + board

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



class playTetris(object):
	def __init__(self):
		pygame.init()
		self.width = cols * cell_size + 280
		self.height = rows * cell_size
		self.gameover = False
		self.paused = False
		self.gameDisplay = pygame.display.set_mode((self.width, self.height))
		self.trans = pygame.Surface((self.width, self.height), pygame.SRCALPHA) #used to create transparent surfaces
		
		pygame.display.set_caption("Tetris by Josh")
		self.board = new_board()
		self.next_piece = tetris_shapes[random.randrange(0, len(tetris_shapes))]

	def init_game(self): #resets data for a game restart
		self.board = new_board()
		self.gameover = False
		self.score = 0
		self.new_piece()
		self.level = 1
		self.lines = 0
		pygame.time.set_timer(pygame.USEREVENT, 1000) #sets a timer for the speed of tetris drop

	def new_piece(self):
		self.piece = self.next_piece[:]
		self.next_piece = tetris_shapes[random.randrange(0, len(tetris_shapes))]

		self.x_coord = int(cols/2 - len(self.piece[0])/2)
		self.y_coord = 0
		print self.x_coord
		print self.y_coord
		if collision(self.board, self.piece, (self.y_coord, self.x_coord)):
			self.gameover = True

	def draw_matrix(self, matrix, coord, ghost = 0):
	# draws a grid representation of a matrix
	# will be used for the draw tetrimino shapes and the board itself
		y_add = coord[0]
		x_add = coord[1]
		for y in range(len(matrix)):
			for x in range(len(matrix[0])):
				if matrix[y][x] != 0:
					if not ghost:
						pygame.draw.rect(self.gameDisplay, colors[matrix[y][x]], (((x + coord[1]) *cell_size, (y + coord[0])*cell_size, cell_size, cell_size,)))
						pygame.draw.rect(self.gameDisplay, white, (((x + coord[1]) *cell_size, (y + coord[0])*cell_size, cell_size, cell_size)), 1)
					else:
						pygame.draw.rect(self.gameDisplay, (40, 40, 40), (((x + coord[1]) *cell_size, (y + coord[0])*cell_size, cell_size, cell_size,)))
						pygame.draw.rect(self.gameDisplay, colors[matrix[y][x]], (((x + coord[1]) *cell_size, (y + coord[0])*cell_size, cell_size, cell_size,)), 3)
	def draw_background(self):
		pygame.draw.rect(self.gameDisplay, black, (0, 0, cell_size*cols, cell_size*rows))
		for y in range(rows):
			for x in range(cols):
				pygame.draw.rect(self.gameDisplay, white, (x*cell_size, y*cell_size, cell_size, cell_size), 1)


	def move(self, x):
		if not self.gameover and not self.paused:
			new_x = self.x_coord + x

			if not collision (self.board, self.piece, (self.y_coord, new_x)):
				self.x_coord = new_x

	def inst_drop(self):
		if not self.gameover and not self.paused:
			while not self.drop(True):
				pass
				
				
	def ghost(self):
		y_end = self.y_coord

		while not collision(self.board, self.piece, (y_end, self.x_coord)):
			y_end += 1

		self.draw_matrix(self.piece, (y_end - 1, self.x_coord), 1)

	def drop(self, manual):
		if not self.gameover and not self.paused:
			self.y_coord += 1
			
			if manual:
				self.score += 1

			if collision(self.board, self.piece, (self.y_coord, self.x_coord)):
				join_matrixes(self.board, self.piece, (self.y_coord, self.x_coord))
				self.new_piece()

				
				while 1: #looking for possible rows being cleared when a collision occurs
					for i,row in enumerate(self.board[:-1]):
						if 0 not in row:
							self.board = remove_row(self.board, i)
							self.lines += 1
							self.score += 100
							break
					else:
						break

				if self.lines > self.level * 6:
					self.level += 1
					pygame.time.set_timer(pygame.USEREVENT, 1000 - (self.level - 1) * 100)

				return 1
		return 0




	def message(self, msg, location, size):
		myfont = pygame.font.Font(None, size)
		text = myfont.render(msg, 1, black)
		
		text_rect = text.get_rect()
		text_rect.center = location
		self.gameDisplay.blit (text, text_rect)

	def labels(self):
		self.message("Next Piece", (550, 30), 30)
		self.message("Level: %d" % self.level, (540, 200), 30)
		self.message("Score: %d" % self.score, (540, 230), 30)
		self.message("Lines: %d" % self.lines, (540, 260), 30)
		self.message("Press 'p' to pause", (540, 400), 30)


	def rotate(self):
		if not self.gameover and not self.paused:
			new_shape = [[0 for x in range(len(self.piece))]
							for y in range(len(self.piece[0]))]

			for x in range(len(self.piece[0])):
				for y in range(len(self.piece)):
					new_shape[x][len(self.piece) - y - 1] = self.piece[y][x]

			if not collision(self.board, new_shape, (self.y_coord, self.x_coord)):
				self.piece = new_shape

	def toggle_pause(self):
		self.paused = not self.paused

	def paused_screen(self):
		self.trans.fill((255,255,255,128))                         
		self.gameDisplay.blit(self.trans, (0,0))

		self.message("Game has been paused", (self.width/2, self.height/2 - 60), 50)
		self.message("Press 'p' to unpause", (self.width/2, self.height/2 + 60), 50)
	
	def game_over_screen(self):
		self.trans.fill((255, 255, 255, 128))
		self.gameDisplay.blit(self.trans, (0,0))
		self.message("GAME OVER", (self.width/2, self.height/2 - 60), 50)
		self.message("Would you like to start again", (self.width/2, self.height/2 + 60), 50)
		self.message("Press 'y' or 'n'", (self.width/2, self.height/2 + 120), 50)




	def run(self):

		key_actions = {
			'LEFT':		lambda:self.move(-1),
			'RIGHT':	lambda:self.move(+1),
			'DOWN':		lambda:self.drop(True),
			'UP':		self.rotate,
			'p':		self.toggle_pause,
			'SPACE':	self.inst_drop,
		}

		self.init_game()
		clock = pygame.time.Clock()
		pygame.key.set_repeat(250, 10)
		while 1:
			

			
			self.gameDisplay.fill(white)
			self.labels()
			self.draw_background()
			self.draw_matrix(self.board, (0,0))
			self.draw_matrix(self.next_piece, (2, cols + 2))
			self.ghost()
			self.draw_matrix(self.piece, (self.y_coord, self.x_coord))
			
			if self.gameover:
				self.game_over_screen()
			
			if self.paused:
				self.paused_screen()
			
			
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.USEREVENT:
					self.drop(False)

				elif event.type == pygame.QUIT:
					pygame.quit()
					quit()

				elif event.type == pygame.KEYDOWN:
					for key in key_actions:
						if event.key == eval("pygame.K_" + key):
							key_actions[key]()

						if event.key == pygame.K_y and self.gameover:
							print ("HI")
							self.init_game()

						if event.key == pygame.K_n and self.gameover:
							pygame.quit()
							quit()

			clock.tick(fps)

if __name__ == '__main__':
	Tetris = playTetris()
	Tetris.run()