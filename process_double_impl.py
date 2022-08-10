import time
import msvcrt
import asyncio
import multiprocessing

import keyboard
import signal
import os

import json

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
			'a': make_sound(n_steps=-1),
			'z': make_sound(n_steps=0),		# Middle C
			's': make_sound(n_steps=1),
			'x': make_sound(n_steps=2),		# D
			'd': make_sound(n_steps=3),
			'c': make_sound(n_steps=4),		# E
			'v': make_sound(n_steps=5),		# F
			'g': make_sound(n_steps=6),
			'b': make_sound(n_steps=7),		# G
			'h': make_sound(n_steps=8),
			'n': make_sound(n_steps=9),		# A
			'j': make_sound(n_steps=10),
			'm': make_sound(n_steps=11),	# B
			',': make_sound(n_steps=12),	# C
			'l': make_sound(n_steps=13),
			'.': make_sound(n_steps=14),	# D
			';': make_sound(n_steps=15),
			'/': make_sound(n_steps=16),	# E
			'q': make_sound(n_steps=17),	# F
			'2': make_sound(n_steps=18),
			'w': make_sound(n_steps=19),	# G
			'3': make_sound(n_steps=20),
			'e': make_sound(n_steps=21),	# A
			'4': make_sound(n_steps=22),
			'r': make_sound(n_steps=23),	# B
			't': make_sound(n_steps=24),	# C
			'6': make_sound(n_steps=25),
			'y': make_sound(n_steps=26),	# D
			'7': make_sound(n_steps=27),
			'u': make_sound(n_steps=28),	# E
			'i': make_sound(n_steps=29),	# F
			'9': make_sound(n_steps=30),
			'o': make_sound(n_steps=31),	# G
			'0': make_sound(n_steps=32),
			'p': make_sound(n_steps=33),	# A
			'-': make_sound(n_steps=34),
			'[': make_sound(n_steps=35),	# B
			']': make_sound(n_steps=36),	# C
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


def create_sound_files(keyboard_layout):
	'''
	create pitch-shifted keyboard sounds and save them to disk.
	'''
	base_path = os.path.abspath(os.path.join('html_site', 'sounds', keyboard_layout))
	if not os.path.exists(base_path):
		os.mkdir(base_path)


	counter = 0
	map_file = 'key_mappings.json'
	key_mappings = {}
	for key, sound in make_keyboard_layout(keyboard_layout).items():
		key_mappings[key] = counter
		sound.export(os.path.join(base_path, f'{counter}.mp4'), format='mp4')
		counter += 1

	with open(os.path.join(base_path, map_file), 'w') as file:
		file.write(json.dumps(key_mappings, indent=2))

# Globals
if __name__ == '__main__':
	'''
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
	'''
	create_sound_files('single_row')

