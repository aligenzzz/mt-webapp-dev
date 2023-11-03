/*
1. The interactivity of the developed site by means of JS
to your liking.
*/
function updateDateTime() {
    var currentDateTime = new Date();
    var formattedDateTime = currentDateTime.toLocaleString();
    var element = document.getElementById("current-datetime");

    if (element) {
        element.innerText = formattedDateTime;
    }
}
setInterval(updateDateTime, 1000);


// 2


/*
3. Animation effect when scrolling (multiple images).
*/
const leftEffect = document.getElementById("left_effect");
const rightEffect = document.getElementById("right_effect");
const text = document.getElementById("text");
const moon = document.getElementById("moon");

if (leftEffect && rightEffect && text && moon) {
    window.addEventListener("scroll",function () {
        let value = scrollY;
        left_effect.style.left = `-${value/0.5}px`;
        right_effect.style.left = `${value/0.35}px`;
        text.style.bottom = `-${value}px`;
        moon.style.height = `${window.innerHeight - value}px`;
    })
}


/*
4. Cards with a volume effect on hover
or a shape with a parallax effect on hover.
*/
const parallax = document.getElementById("parallax");
const walk = {x: 100, y: 50};

if (parallax) {
    parallax.addEventListener("mousemove", function (e) {
        const width = parallax.offsetWidth;
        const height = parallax.offsetHeight;

        let {offsetX: x, offsetY: y} = e;

        const xWalk = Math.round((e.x / width / 2 * walk.x) - (walk.x / 2));
        const yWalk = Math.round((e.y / height / 2  * walk.y) - (walk.y / 2));

        parallax.style.transform = `rotateY(${-xWalk}deg) rotateX(${yWalk}deg)`;
    });
}


/*
5. The ability to change the font size and color of the text, the
background color of the page using the form elements generated when
selecting the appropriate checkbox. The dimensions of the images
should not change.
*/
const fontSizeInput = document.getElementById("fontSize");
const textColorInput = document.getElementById("textColor");
const backgroundColorInput = document.getElementById("backgroundColor");

if (fontSizeInput) {
    fontSizeInput.addEventListener("input", function () {
        const fontSize = fontSizeInput.value + "px";
        document.body.style.fontSize = fontSize;
    });
}
if (textColorInput) {
    textColorInput.addEventListener("input", function () {
        const textColor = textColorInput.value;
        document.body.style.color = textColor;
    });
}
if (backgroundColorInput) {
    backgroundColorInput.addEventListener("input", function () {
        const backgroundColor = backgroundColorInput.value;
        document.body.style.backgroundColor = backgroundColor;
    });
}


// 6


/*
7. Request for the date of birth, calculation of the number of years,
a message about the day of the week of the entered date for adults and
an alert about the need for parental permission to use the site if a minor.
*/
const ageCalculator = document.getElementById("ageCalculator")
if (ageCalculator) {
  ageCalculator.addEventListener("submit", function (e) {
    e.preventDefault();

    const birthDateInput = document.getElementById("birthdate");
    const birthDate = new Date(birthDateInput.value);
    const currentDate = new Date();

    var age = currentDate.getFullYear() - birthDate.getFullYear();
    const monthDiff = currentDate.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && currentDate.getDate() < birthDate.getDate())) {
      age--;
    }
    if (age < 0) {
      document.getElementById("ageResult").innerText = `Invalid data!`;
      return;
    } else {
      document.getElementById("ageResult").innerText = `Your age: ${age} y.o.`;
    }

    const daysOfWeek = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ];
    const dayOfWeek = daysOfWeek[birthDate.getDay()];

    if (age < 18) {
        alert("You need your parents' permission to use this site!");
    } else {
        document.getElementById("dayOfWeek").textContent = `You were born on ${dayOfWeek}`;
        alert("Welcome to this site!");
    }
  });
}


/*
8. When entering the site page, show the user a countdown
that will end in an hour from the moment the user enters the site.
***Make sure that after refreshing the page, the countdown continues
from where it left off.
*/
function startCountdown() {
    const currentTime = new Date().getTime();

    if (sessionStorage.getItem("countdownStartTime")) {
        const startTime = parseInt(sessionStorage.getItem("countdownStartTime"), 10);
        const elapsedTime = currentTime - startTime;
        const remainingTime = 60 * 60 * 1000 - elapsedTime;
        displayTime(remainingTime);
    } else {
        sessionStorage.setItem("countdownStartTime", currentTime.toString());
        displayTime(60 * 60 * 1000);
    }
}
function displayTime(remainingTime) {
    const element = document.getElementById("countdown");
    if (!element) {
        return;
    }

    if (remainingTime <= 0) {
        document.getElementById("countdown").innerText = "00:00 -_-";
        return;
    }

    const minutes = Math.floor(remainingTime / 60000);
    const seconds = Math.floor((remainingTime % 60000) / 1000);

    if (element) {
        if (seconds < 10) {
            element.innerText = `${minutes}:0${seconds}`;
        } else {
            element.innerText = `${minutes}:${seconds}`;
        }
    }

    if (remainingTime > 0) {
        setTimeout(() => displayTime(remainingTime - 1000), 1000);
    }
}
startCountdown();


/*
9. Write a code that will generate a square table (array) (the size is chosen by the user),
in which numbers will be randomly placed. Develop functions to perform actions:
− Transpose the table by pressing the button.
− By clicking on any cell, this cell should be highlighted in color (the color is different
for cells with a value of multiples of two and the rest).
− ***Make it so that no more than n cells can be selected in one row/or column of the table
(the value entered in the field) and the neighbors on the left and right cannot be selected.
− ***By clicking on the corresponding buttons, add both a new row and a new column
*/
const generateTableButton = document.getElementById("generateTable");
const transposeTableButton = document.getElementById("transposeTable");
const addRowButton = document.getElementById("addRow");
const addColumnButton = document.getElementById("addColumn");

if (generateTableButton) {
    generateTableButton.addEventListener("click", function () {
        const size = document.getElementById("tableSize").value;
        if (size <= 0) {
            return;
        }

        const table = document.getElementById("table");
        table.innerHTML = "";

        for (let i = 0; i < size; i++) {
            const row = document.createElement("tr");
            for (let j = 0; j < size; j++) {
                createCell(row);
            }
            table.appendChild(row);
        }
   });
}
if (transposeTableButton) {
    transposeTableButton.addEventListener("click", function () {
        const table = document.getElementById("table");
        if (table.innerHTML === "") {
            return;
        }

        const clonedTable = table.cloneNode(true);
        table.innerHTML = "";

        var rows = clonedTable.getElementsByTagName("tr");
        const rowsCount = rows[0].childElementCount;
        const columnsCount = rows.length;

        for (let i = 0; i < rowsCount; i++) {
            const row = document.createElement("tr");
            for (let j = 0; j < columnsCount; j++) {
                var columns = rows[j].getElementsByTagName("td");
                var cell = columns[i].cloneNode(true);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
    });
}
if (addRowButton) {
    addRowButton.addEventListener("click", function () {
        const table = document.getElementById("table");

        var size = 0;
        if (table.innerHTML === "") {
             size = parseInt(tableSize.value);
        } else {
             size = table.getElementsByTagName("tr")[0].childElementCount;
        }

        const row = document.createElement("tr");
        for (let i = 0; i < size; i++) {
            const cell = document.createElement("td");
            cell.textContent = Math.floor(Math.random() * 100);
            cell.addEventListener("click", cellSelection);
            row.appendChild(cell);
        }
        table.appendChild(row);
    });
}
if (addColumnButton) {
    addColumnButton.addEventListener("click", function () {
        if (table.innerHTML === "") {
            const row = document.createElement("tr");
            createCell(row);
            table.appendChild(row);
            return;
        }

        var rows = table.getElementsByTagName("tr");
        for (let i = 0; i < rows.length; i++) {
            createCell(rows[i]);
        }
    });
}

function createCell(row) {
    const cell = document.createElement("td");
    cell.textContent = Math.floor(Math.random() * 100);
    cell.addEventListener("click", cellSelection);
    row.appendChild(cell);
}
function cellSelection(e) {
    const maxSelection = document.getElementById("maxSelection").value;
    const cell = e.target;
    const row = cell.parentElement;
    const rowCells = Array.from(row.cells);
    const cellIndex = rowCells.indexOf(cell);

    const selectedInRow = rowCells.filter(c => c.classList.contains("selected"));
    const columnCells = Array.from(cell.parentElement.parentElement.rows);
    const selectedInColumn = columnCells
        .map(r => r.cells[cellIndex])
        .filter(c => c.classList.contains("selected"));

    if (cell.classList.contains("selected")) {
        cell.classList.remove("selected");
    } else if (
        selectedInRow.length < maxSelection &&
        selectedInColumn.length < maxSelection &&
        !hasNeighborSelected(rowCells, cellIndex)
    ) {
        cell.classList.add("selected");
    }
}
function hasNeighborSelected(cells, i) {
    if (i > 0 && cells[i - 1].classList.contains("selected")) {
        return true;
    }
    if (i < cells.length - 1 && cells[i + 1].classList.contains("selected")) {
        return true;
    }
    return false;
}


// 10


// 11

