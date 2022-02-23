import random

class MazeGenerator:
	path = ' '
	wall = 'w'
	unvisited = 'u'
	maze = []
	walls = []

	# Starting location at (1, 1)
	start_h = 1
	start_w = 1

	def __init__(self, width, height):
		
		self.width = width
		self.height = height

		for h in range(0, height):
			line = []
			for w in range(0, width):
				line.append('u')
			self.maze.append(line)
		
		self._start(self.start_h, self.start_w)
		self._make_path()
		self._make_walls()
		self._create_entrance_exit()
		self.print_maze()

	# # Print the maze
	def print_maze(self):
		for i in range(0, len(self.maze)):
			for j in range(0, len(self.maze[0])):
					print(self.maze[i][j], end = " ")
			print("")

	# Mark the starting location as a cell and its surrounding as wall
	# Add walls to the wall[]
	def _start(self, h, w):
		
		self.maze[h][w] = self.path

		# Mark them as walls
		self.maze[h-1][w] = self.wall
		self.maze[h][w-1] = self.wall
		self.maze[h][w+1] = self.wall
		self.maze[h+1][w] = self.wall

		# Add walls to wall[]
		self.walls.append([h-1, w])
		self.walls.append([h, w-1])
		self.walls.append([h, w+1])
		self.walls.append([h+1, w])

	# Check the number of surrouning cells
	def _surrounding_cells(self, rand_wall):
		s_cells = 0
		if (self.maze[rand_wall[0]-1][rand_wall[1]] == ' '):
			s_cells += 1
		if (self.maze[rand_wall[0]+1][rand_wall[1]] == ' '):
			s_cells += 1
		if (self.maze[rand_wall[0]][rand_wall[1]-1] == ' '):
			s_cells +=1
		if (self.maze[rand_wall[0]][rand_wall[1]+1] == ' '):
			s_cells += 1
		return s_cells

	# Delete new created path from wall[] for step 4
	def _delete_wall(self, rand_wall):
		for wall in self.walls:
			if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
				self.walls.remove(wall) 

	# Pick a random wall from wall[] to start the path
	# Check coming & going cells for path-unvisited pair
	def _make_path(self):
		while (self.walls):
			# Pick a random wall
			rand_wall = self.walls[int(random.random()*len(self.walls))-1]

			# Check if it is a left wall
			if (rand_wall[1] != 0):
				if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'u' 
					and self.maze[rand_wall[0]][rand_wall[1]+1] == ' '):

					# Find the number of surrounding cells
					s_cells = self._surrounding_cells(rand_wall)

					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_wall[0]][rand_wall[1]] = ' '

						# Mark the new walls
						# Upper cell
						if (rand_wall[0] != 0):
							if (self.maze[rand_wall[0]-1][rand_wall[1]] != ' '):
								self.maze[rand_wall[0]-1][rand_wall[1]] = 'w'
							if ([rand_wall[0]-1, rand_wall[1]] not in self.walls):
								self.walls.append([rand_wall[0]-1, rand_wall[1]])

						# Bottom cell
						if (rand_wall[0] != self.height-1):
							if (self.maze[rand_wall[0]+1][rand_wall[1]] != ' '):
								self.maze[rand_wall[0]+1][rand_wall[1]] = 'w'
							if ([rand_wall[0]+1, rand_wall[1]] not in self.walls):
								self.walls.append([rand_wall[0]+1, rand_wall[1]])

						# Leftmost cell
						if (rand_wall[1] != 0):	
							if (self.maze[rand_wall[0]][rand_wall[1]-1] != ' '):
								self.maze[rand_wall[0]][rand_wall[1]-1] = 'w'
							if ([rand_wall[0], rand_wall[1]-1] not in self.walls):
								self.walls.append([rand_wall[0], rand_wall[1]-1])
					

					# Delete wall
					self._delete_wall(rand_wall)
					continue

			# Check if it is an upper wall
			if (rand_wall[0] != 0):
				if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'u' 
					and self.maze[rand_wall[0]+1][rand_wall[1]] == ' '):

					s_cells = self._surrounding_cells(rand_wall)

					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_wall[0]][rand_wall[1]] = ' '

						# Mark the new walls
						# Upper cell
						if (rand_wall[0] != 0):
							if (self.maze[rand_wall[0]-1][rand_wall[1]] != ' '):
								self.maze[rand_wall[0]-1][rand_wall[1]] = 'w'
							if ([rand_wall[0]-1, rand_wall[1]] not in self.walls):
								self.walls.append([rand_wall[0]-1, rand_wall[1]])

						# Leftmost cell
						if (rand_wall[1] != 0):
							if (self.maze[rand_wall[0]][rand_wall[1]-1] != ' '):
								self.maze[rand_wall[0]][rand_wall[1]-1] = 'w'
							if ([rand_wall[0], rand_wall[1]-1] not in self.walls):
								self.walls.append([rand_wall[0], rand_wall[1]-1])

						# Rightmost cell
						if (rand_wall[1] != self.width-1):
							if (self.maze[rand_wall[0]][rand_wall[1]+1] != ' '):
								self.maze[rand_wall[0]][rand_wall[1]+1] = 'w'
							if ([rand_wall[0], rand_wall[1]+1] not in self.walls):
								self.walls.append([rand_wall[0], rand_wall[1]+1])

					# Delete wall
					self._delete_wall(rand_wall)

					continue

			# Check the bottom wall
			if (rand_wall[0] != self.height-1):
				if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'u' 
					and self.maze[rand_wall[0]-1][rand_wall[1]] == ' '):

					s_cells = self._surrounding_cells(rand_wall)

					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_wall[0]][rand_wall[1]] = ' '

						# Mark the new walls
						if (rand_wall[0] != self.height-1):
							if (self.maze[rand_wall[0]+1][rand_wall[1]] != ' '):
								self.maze[rand_wall[0]+1][rand_wall[1]] = 'w'
							if ([rand_wall[0]+1, rand_wall[1]] not in self.walls):
								self.walls.append([rand_wall[0]+1, rand_wall[1]])
						if (rand_wall[1] != 0):
							if (self.maze[rand_wall[0]][rand_wall[1]-1] != ' '):
								self.maze[rand_wall[0]][rand_wall[1]-1] = 'w'
							if ([rand_wall[0], rand_wall[1]-1] not in self.walls):
								self.walls.append([rand_wall[0], rand_wall[1]-1])
						if (rand_wall[1] != self.width-1):
							if (self.maze[rand_wall[0]][rand_wall[1]+1] != ' '):
								self.maze[rand_wall[0]][rand_wall[1]+1] = 'w'
							if ([rand_wall[0], rand_wall[1]+1] not in self.walls):
								self.walls.append([rand_wall[0], rand_wall[1]+1])

					# Delete wall
					self._delete_wall(rand_wall)

					continue

			# Check the right wall
			if (rand_wall[1] != self.width-1):
				if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]-1] == ' '):

					s_cells = self._surrounding_cells(rand_wall)

					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_wall[0]][rand_wall[1]] = ' '

						# Mark the new walls
						if (rand_wall[1] != self.width-1):
							if (self.maze[rand_wall[0]][rand_wall[1]+1] != ' '):
								self.maze[rand_wall[0]][rand_wall[1]+1] = 'w'
							if ([rand_wall[0], rand_wall[1]+1] not in self.walls):
								self.walls.append([rand_wall[0], rand_wall[1]+1])
						if (rand_wall[0] != self.height-1):
							if (self.maze[rand_wall[0]+1][rand_wall[1]] != ' '):
								self.maze[rand_wall[0]+1][rand_wall[1]] = 'w'
							if ([rand_wall[0]+1, rand_wall[1]] not in self.walls):
								self.walls.append([rand_wall[0]+1, rand_wall[1]])
						if (rand_wall[0] != 0):	
							if (self.maze[rand_wall[0]-1][rand_wall[1]] != ' '):
								self.maze[rand_wall[0]-1][rand_wall[1]] = 'w'
							if ([rand_wall[0]-1, rand_wall[1]] not in self.walls):
								self.walls.append([rand_wall[0]-1, rand_wall[1]])

					# Delete wall
					self._delete_wall(rand_wall)

					continue

			# Delete the wall from the list anyway
			self._delete_wall(rand_wall)
			

	# Turn all the unvisited spot into walls
	def _make_walls(self):
		for i in range(0, self.height):
			for j in range(0, self.width):
				if (self.maze[i][j] == 'u'):
					self.maze[i][j] = 'w'

	# Entrance & Exit 
	def _create_entrance_exit(self):
		for i in range(0, self.width):
			if (self.maze[1][i] == ' '):
				self.maze[0][i] = ' '
				break
		for i in range(self.width-1, 0, -1):
			if (self.maze[self.height-2][i] == ' '):
				self.maze[self.height-1][i] = ' '
				break

	def get_maze(self):
		return self.maze