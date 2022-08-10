import time
import msvcrt
import asyncio
import multiprocessing

import keyboard
import signal
import os

from pydub import AudioSegment
from pydub.playback import play


# Just need to define it here
SOUND = AudioSegment.from_file('sounds/Middle_C.m4a')

def make_sound(sound=SOUND, n_steps=0):
	# 12 half-steps in an octave
	octaves = n_steps / 12

	new_sample_rate = int(sound.frame_rate * (2 ** octaves))

	new_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
	new_sound = new_sound.set_frame_rate(44100)

	return new_sound



def make_keyboard_layout(layout='single_row'):
	'''
	Defines the keyboard layout you would like to use for this program.
		
	Current options are 'single_row' and 'double_row'

	This function returns a dictionary of key names to n_steps to shift the
	middle c down by.

	single_row:
		Notes will be based on the middle row of a traditional US keyboard.
		The keys [a, s, d, ...] will correspond to the white keys, and the row above that
		[q, w, e] will correspond to the black keys (if any).

		Middle C will be located on the 'g' key.

	double_row:
		The rows of keys will be split into 2 for a greater pitch range.
		the row [z, x, c...] will be the lower keys, with [a, s, d] now becoming the black keys.
		And [q, w, e] will become a second row of white keys with the [1, 2, 3] keys being those black keys
	'''
	if layout == 'single_row':
		return {
			'a': make_sound(n_steps=-7),   	# F
			'w': make_sound(n_steps=-6),
			's': make_sound(n_steps=-5), 	# G
			'e': make_sound(n_steps=-4),
			'd': make_sound(n_steps=-3), 	# A
			'r': make_sound(n_steps=-2),
			'f': make_sound(n_steps=-1), 	# B
			'g': make_sound(n_steps=0),  	# Middle C
			'y': make_sound(n_steps=1),
			'h': make_sound(n_steps=2),		# D
			'u': make_sound(n_steps=3),
			'j': make_sound(n_steps=4),  	# E
			'k': make_sound(n_steps=5),  	# F
			'o': make_sound(n_steps=6),  
			'l': make_sound(n_steps=7),  	# G
		}
	elif layout == 'double_row':
		return {
			'a': -1,
			'z': 0,		# Middle C
			's': 1,
			'x': 2,		# D
			'd': 3,
			'c': 4,		# E
			'v': 5,		# F
			'g': 6,
			'b': 7,		# G
			'h': 8,
			'n': 9,		# A
			'j': 10,
			'm': 11,	# B
			',': 12,	# C
			'l': 13,
			'.': 14,	# D
			';': 15,
			'/': 16,	# E
			'q': 17,	# F
			'2': 18,
			'w': 19,	# G
			'3': 20,
			'e': 21,	# A
			'4': 22,
			'r': 23,	# B
			't': 24,	# C
			'6': 25,
			'y': 26,	# D
			'7': 27,
			'u': 28,	# E
			'i': 29,	# F
			'9': 30,
			'o': 31,	# G
			'0': 32,
			'p': 33,	# A
			'-': 34,
			'[': 35,	# B
			']': 36,	# C
		}
		

def keydown_handler(kb_event):
	key = kb_event.name
	if key == QUIT_KEY:
		os.kill(os.getpid(), signal.CTRL_C_EVENT)
		

	sound = KEYBOARD.get(key)

	if sound is not None:
		if HELD_KEYS.get(key) is None:
			if THREAD_CONTAINER.get(key) is not None:
				if THREAD_CONTAINER[key].is_alive():
					THREAD_CONTAINER[key].kill()

			THREAD_CONTAINER[key] = multiprocessing.Process(target=play, args=(sound,), daemon=True)
			THREAD_CONTAINER[key].start()
			HELD_KEYS[key] = True
	else:
		return

def keyup_handler(kb_event):
	key = kb_event.name

	if THREAD_CONTAINER.get(key) is not None:
		if THREAD_CONTAINER[key].is_alive():
			THREAD_CONTAINER[key].kill()
		THREAD_CONTAINER[key] = None
		HELD_KEYS[key] = None


# Globals
if __name__ == '__main__':
	# sound = AudioSegment.from_file('sounds/smoke_weed_everyday.m4a')
	KEYBOARD = make_keyboard_layout(layout='single_row')
	QUIT_KEY = '`'

	THREAD_CONTAINER = {}
	HELD_KEYS = {}

	print(f'Press {QUIT_KEY} (under esc) to exit!')
	# keyboard for keyup detection
	keyboard.on_press(keydown_handler, suppress=True)
	keyboard.on_release(keyup_handler)
	keyboard.wait()

