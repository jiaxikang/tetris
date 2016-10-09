import random, pygame, sys

cell_size = 40
cols = 10
rows = 22
fps = 30

colors = {0: (255, 255, 230),
		  1: (255, 0, 0),
          2: (255, 255, 0),
          3: (255, 0, 255),
          4: (255, 128, 0),
          5: (0, 0, 255),
          6: (0, 255, 0),
          7: (160, 160, 160)
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

def collision(board, shape, coord):
	# coord is an tuple of size 2 that will represent the shapes' position on the board
	# coord[0] is y position and coord[1] is x position
	y_add = coord[0]
	x_add = coord[1]
	for y in range(len(shape)):
		for x in range(len(shape[0])):
			try:
			#there is another piece in this position on the board
				if shape[y][x] != 0 and board[y + y_add][x + x_add] != 0:
			
					return True
			except IndexError:
			#collision with walls
				return False
	return False




class playTetris(object):
	def __init__(self):
		pygame.init()
		self.width = cols * cell_size + 300
		self.height = rows * cell_size
		self.gameover = False
		self.gameDisplay = pygame.display.set_mode((self.width, self.height))
		self.gameDisplay.fill(white)
		pygame.display.set_caption("Tetris by Josh")
		self.board = new_board()
		self.clock = pygame.time.Clock()
		self.next_piece = tetris_shapes[random.randrange(0, len(tetris_shapes))]

	def new_piece(self):
		self.piece = self.next_piece[:]
		self.next_piece = tetris_shapes[random.randrange(0, len(tetris_shapes))]

		self.x_coord = int(cols/2 - len(self.piece[0])/2)
		self.y_coord = 0
		print self.x_coord
		if collision(self.piece, self.board, (self.y_coord, self.x_coord)):
			self.gameover = True

	def draw_matrix(self, matrix, coord):
	# draws a grid representation of a matrix
	# will be used for the draw tetrimino shapes and the board itself
		y_add = coord[0]
		x_add = coord[1]
		for y in range(len(matrix)):
			for x in range(len(matrix[0])):
				pygame.draw.rect(self.gameDisplay, colors[matrix[y][x]], (((x + coord[1]) *cell_size, (y + coord[0])*cell_size, cell_size, cell_size)))

	def exit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

	def run(self):
		self.new_piece()

		while 1:
			self.exit()
			if self.gameover:
				pygame.quit()
				quit()
			self.draw_matrix(self.board, (0,0))
			self.draw_matrix(self.piece, (self.y_coord, self.x_coord))
			pygame.display.update()

if __name__ == '__main__':
	Tetris = playTetris()
	Tetris.run()