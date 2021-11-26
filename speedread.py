# file: speedread-terminal/speedread.py

import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class SpeedRead:

	def __init__(self, file:str, words_per_minute:int, pointer:str, word_focus:bool, word_delay:bool, punctuation_delay:bool, height:int, width:int, font_size:int) -> None:
		self.height = height
		self.width = width
		self.height_halved = int(self.height / 2)
		self.width_halved = int(self.width / 2)
		self.pointer = pointer
		self.words_per_minute = words_per_minute
		self.word_focus = word_focus
		self.word_delay = word_delay
		self.punctuation_delay = punctuation_delay
		if font_size == None:
			self.font_size  = int(height / 2)
		else:
			self.font_size = font_size

		pygame.init()
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("SpeedReader")
		self.font = pygame.font.SysFont("DejaVu Sans Mono", self.font_size)

		self.read(self.open_file(file))

	def read(self, file) -> None:
		while True:
			for word in file.split():
				try:
					word_index = self.get_word_index(word)
					padded_word  = self.get_word_padding(word, word_index)

					x = (self.font_size / 3)
					y = ((self.width / 2) - (self.font_size / 4))
					w = (self.font_size / 2)
					h = (self.height - (x*2))

					if self.pointer == 'pipe':
						pygame.draw.rect(self.window, (255, 255, 255), ((y + (w/2.5)), 0, (w/4), self.height)) # focus pointer
					elif self.pointer == 'bar':
						pygame.draw.rect(self.window, (255, 255, 255), (0, 0, self.width, (self.height / 20))) # top
						pygame.draw.rect(self.window, (255, 255, 255), (0, (self.height - (self.height / 20)), self.width, (self.height / 20))) # bottom
					elif self.pointer == 'full':
						pygame.draw.rect(self.window, (255, 255, 255), (0, 0, self.width, (self.height / 20))) # top
						pygame.draw.rect(self.window, (255, 255, 255), ((y + (w/2.5)), 0, (w/4), self.height)) # focus pointer
						pygame.draw.rect(self.window, (255, 255, 255), (0, (self.height - (self.height / 20)), self.width, (self.height / 20))) # bottom
					else:
						pass

					# render word in from center
					text = self.font.render(padded_word, 1, (255,255,255))
					text_center = text.get_rect(center=((self.width/2), (self.height/2))) # center to center
					self.window.blit(text, text_center)

					pygame.draw.rect(self.window, (0, 0, 0), (y, x, w, h)) # clear focus char

					# render focused char in center
					if self.word_focus: # render focus char in red
						focus = self.font.render(word[word_index], 1, (255,0,0))
					else:
						focus = self.font.render(word[word_index], 1, (255,255,255))
					focus_center = focus.get_rect(center=(self.width_halved, self.height_halved)) # center to center
					self.window.blit(focus, focus_center)

					time.sleep(self.get_word_delay(word)) # wpm delay
					pygame.display.update()
					self.window.fill((0, 0, 0)) # fill background colour

					# keyboard exit
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							exit(0)
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_q:
								exit(0)
							if event.key == pygame.K_ESCAPE:
								exit(0)
				except Exception as e:
					exit(0) # silence Traceback on exit
			exit(0)
		exit(0)

	def get_word_padding(self, word: str, index: int) -> int:
		if len(word) >1:
			number_to_left = index
			number_to_right = len(word) - (index + 1)
			if number_to_left < number_to_right:
				word = " " * (number_to_right - number_to_left) + word
			elif number_to_left > number_to_right:
				word = word + " " * (number_to_left - number_to_right)
		return word

	def get_word_index(self, word: str) -> int:
		word_length = len(word)
		if word_length <= 1:
			return 0
		elif 2 <= word_length <= 5:
			return 1
		elif 6 <= word_length <= 9:
			return 2
		elif 10 <= word_length <= 13:
			return 3
		else:
			return 4

	def get_word_delay(self, word: str) -> float:
		if self.word_delay:
			delay_factor = ((1 / float(self.words_per_minute) * 60) + (len(word) / 30))
		else:
			delay_factor =((1 / float(self.words_per_minute) * 60))

		punctuation_delay_factor = {',':2.0, ';':2.0, '...':5.0, '.':2.5, '!':2.5, ':':2.5, '?':3.0}
		if self.punctuation_delay:
			for punctuation in punctuation_delay_factor:
				if word.endswith(punctuation):
					return delay_factor * punctuation_delay_factor[punctuation]
			else:
				return delay_factor
		else:
			return delay_factor

	def open_file(self, file: str) -> str:
		if os.path.isfile(file):
			with open(file, 'r') as f:
				return f.read()
		else:
			print(f"file not found: '{file}'")
			exit()
