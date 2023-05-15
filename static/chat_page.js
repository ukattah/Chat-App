let timeoutID;
let timeout = 15000;

window.addEventListener("load", setup);

function setup() {
	document.getElementById("btn").addEventListener("click", makePost);
	timeoutID = window.setTimeout(poller, timeout);
}

function makePost() {
	console.log("Sending POST request");
	const message = document.getElementById("msgId").value
	const author = document.getElementById("authorId").value

	fetch("/new_message/", {
		method: "post",
		headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
		body: `author=${author}&message=${message}`
		})
		.then((response) => {
			return response.json();
		})
		.then((result) => {
			updateTable(result)
			clearInput();
		})
		.catch(() => {
			console.log("Error posting new message!");
		});
}

function poller() {
	console.log("Polling for new messages");
	fetch("/messages/")
	.then((response) => {
		return response.json();
	})
	.then((results) => {
		updateTable(results);
		let chat_window = document.getElementById("chat_window");
		let messages = "";
		for (let index in results) {
		current_set = results[index];
		for (let key in current_set) {
		author = key;
		message = current_set[key];
		messages += `${author}:\n${message}\n\n`;
		}
		}
		chat_window.value = messages;
		})
	.catch(() => {
		chat_window.value = "error retrieving messages from server";
	});
}

function updateTable(result) {
	console.log("Updating the chat");

	//console.log(result);

	// deleting table original contents
	const table = document.getElementById("chat_window");
	while (table.rows.length > 0) {
		table.deleteRow(0);
	}
	// console.log(result)

	// add the up-to-date table contents sent from server
	for (var i = 0; i < result.length; i++) {
		addRow(result[i]);
	}

	timeoutID = window.setTimeout(poller, timeout);
}

function addRow(msg) {
	const tableRef = document.getElementById("chat_window");
	const newRow = tableRef.insertRow();

	// create cells for author and message
	const authorCell = newRow.insertCell(0);
	const messageCell = newRow.insertCell(1);

	// set the text content of the cells
	authorCell.innerText = "User: " + msg[0] + ":";
	messageCell.innerText = msg[1];

	// apply styles to the cells
	authorCell.style.display = "block";
	messageCell.style.display = "block";

	// add line breaks between author and message and after the message
	const lineBreak1 = document.createElement("br");
	const lineBreak2 = document.createElement("br");
	messageCell.appendChild(lineBreak1);
	messageCell.appendChild(lineBreak2);
}

function clearInput() {
	console.log("Clearing input");
	document.getElementById("msgId").value = "";
}


