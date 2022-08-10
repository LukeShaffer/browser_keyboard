
/* Global Vars */
var file_format = '.mp4';
var current_layout = 'single_row';

var AUDIO_ARRAY = {};
var HELD_KEYS = {};

var double_key_mappings = {
  "a": 0,
  "z": 1,
  "s": 2,
  "x": 3,
  "d": 4,
  "c": 5,
  "v": 6,
  "g": 7,
  "b": 8,
  "h": 9,
  "n": 10,
  "j": 11,
  "m": 12,
  ",": 13,
  "l": 14,
  ".": 15,
  ";": 16,
  "/": 17,
  "q": 18,
  "2": 19,
  "w": 20,
  "3": 21,
  "e": 22,
  "4": 23,
  "r": 24,
  "t": 25,
  "6": 26,
  "y": 27,
  "7": 28,
  "u": 29,
  "i": 30,
  "9": 31,
  "o": 32,
  "0": 33,
  "p": 34,
  "-": 35,
  "[": 36,
  "]": 37
};

var single_key_mappings = {
  "a": 0,
  "w": 1,
  "s": 2,
  "e": 3,
  "d": 4,
  "r": 5,
  "f": 6,
  "g": 7,
  "y": 8,
  "h": 9,
  "u": 10,
  "j": 11,
  "k": 12,
  "o": 13,
  "l": 14
};



const get_current_mapping = () =>{
	var row_mapping = null;
	if (current_layout === 'single_row') row_mapping = single_key_mappings;
	else if (current_layout === 'double_row') row_mapping = double_key_mappings;

	return row_mapping;
};


const get_key_sound_url = (key_name) => {
	var toReturn = `sounds/${current_layout}/`;

	var row_mapping = get_current_mapping();

	if (row_mapping[key_name] === undefined) return null;

	toReturn += `${row_mapping[key_name]}${file_format}`;

	return toReturn; 
};

const stop_everything = () =>{
	for (const [key, sound] of Object.entries(AUDIO_ARRAY)){
		if (!sound) continue;
		sound.pause();
		AUDIO_ARRAY[key] = undefined;
	}
};

const swap_mapping = ()=>{
	console.log(current_layout);
	if (current_layout === 'single_row') {
		document.getElementById('double-button').click();
	}

	else if (current_layout === 'double_row'){
		document.getElementById('single-button').click();
	}
}




document.addEventListener('keydown', (event) => {
	// multiple keydown events are fired on key hold
	if (HELD_KEYS[event.key]) return;

	if (event.ctrlKey) {
		swap_mapping();
		return;
	}

	HELD_KEYS[event.key] = true;

	let audio_file = get_key_sound_url(event.key);
	if (audio_file === null) return;

	if (AUDIO_ARRAY[event.key]) AUDIO_ARRAY[event.key].pause();
	AUDIO_ARRAY[event.key] = new Audio(audio_file);
	AUDIO_ARRAY[event.key].play();
});

document.addEventListener('keyup', (event) => {
	HELD_KEYS[event.key] = false;

	let audio_file = get_key_sound_url(event.key);
	if (audio_file === null && event.key !== ' ') return;

	if (event.key === ' ') {
		stop_everything();
		return;
	}
	
	if (!HELD_KEYS[' ']){
		AUDIO_ARRAY[event.key].pause();
		AUDIO_ARRAY[event.key] = undefined;
	}


	
});