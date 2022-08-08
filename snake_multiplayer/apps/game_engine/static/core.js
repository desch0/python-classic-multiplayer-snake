var field = document.getElementsByClassName('field_box')[0];
var loseBox = document.getElementsByClassName('lose_box')[0];
var reloadBtn = document.getElementsByClassName('lose_repeatgame_btn')[0];


reloadBtn.onclick = function() {window.location.reload();};

var reloadBtn = document.getElementsByClassName('lose_repeatgame_btn')[0];

function randint(min, max) {
	return Math.round(min + Math.random()*(max-min));
};

// cells initialization
function init(cells_amount) {
	for (var i=0; i<cells_amount; i++) {
		var newCell = document.createElement('div');
	 	newCell.className = 'cell';
		field.appendChild(newCell);
	};
};

init(fieldWidth*fieldHeight);

function transformCoordinates(x,y) {
	var result = fieldWidth*(y-1)+x;
	return result-1;
};


function clearField() {
	for (var i = 0; i<field.children.length; i++) {
		field.children[i].className = "cell";
	}
}

function lose() {
	loseBox.style.display = "block";
	setTimeout(function() {
		loseBox.style.opacity = "1";
	}, 100);
}

var key;
var isLose = false;

const webSocket = new WebSocket('ws://'+window.location.host+'/ws/room');
webSocket.onmessage = function(e) {
	let response = JSON.parse(e.data);
	if(response['type'] == "key") {
		key = response['key'];
	}
	if (response['type'] == "data") {
		clearField();
		snakesCount = 0;
		var appleCellCoordinates = Number(response['appleCell']);
		var appleCell = document.getElementsByClassName('cell')[appleCellCoordinates-1];
		appleCell.className = 'cell apple_cell';

		var names = [];
		var snakes = response['snakesCells'];

		for (var i = 0; i < snakes.length; i++) {

			names.push(snakes[i][0]);
			var skin = snakes[i][1];
			var cells = snakes[i][2];

			for (var x = 0; x < cells.length; x++) {
				var cell = document.getElementsByClassName('cell')[cells[x]-1];
				cell.className = 'cell '+skin;
			}

		}

		if(response['is_alive'] == false) {
			isLose = true;
			lose();
		}

	}
}

setTimeout(function() {
	webSocket.send(JSON.stringify({"type": "start_game", "name": playerName}));
}, 100);
function socketMove(direction) {
	webSocket.send(JSON.stringify({'type': 'change_direction', 'key': key, 'action': String(direction)}));
}

window.onkeydown = function(event) {
	if (event.keyCode == 38) { socketMove(1); };
	if (event.keyCode == 39) { socketMove(2); };
	if (event.keyCode == 40) { socketMove(3); };
	if (event.keyCode == 37) { socketMove(4); };
};
