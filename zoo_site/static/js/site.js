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


/*
2. Placing several banners on the site and rotating them after a period of time,
which can be changed by the administrator using the form element. To start and stop
banner changes, use a page focus check. Each banner provides a click on its own link.
*/
const imageContainer = document.getElementById("imageContainer");
const animationTimeInput = document.getElementById("animationTime");

if (imageContainer) {
    const images = imageContainer.childNodes;
    images.forEach(image => {
        image.addEventListener("mouseover", function () {
            images.forEach(i => {
                if (i.style) {
                    i.style.animationPlayState = "paused";
                }
            });
        });
        image.addEventListener("mouseout", function () {
            images.forEach(i => {
                if (i.style) {
                    i.style.animationPlayState = "running";
                }
            });
        });
        image.addEventListener("click", function () {
            window.open("http://127.0.0.1:8000/main/");
        });
    });
}
if (animationTimeInput) {
    animationTimeInput.addEventListener("input", function () {
        const animationTime = animationTimeInput.value + "s";
        document.documentElement.style.setProperty("--animation-time", animationTime);
    });
}

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


/*
6. Using promo codes when calculating the cost of services/goods/...
*/
const enterButton = document.getElementById("enterButton");
if (enterButton) {
    enterButton.addEventListener("click", function (e) {
        e.preventDefault();

        const priceInput = document.getElementById("priceInput");
        const discountInput = document.getElementById("discountInput");
        const result = document.getElementById("result");

        const price = priceInput.value;
        const discount = discountInput.value;

        if (price <= 0 || discount < 0 || discount > 100) {
            result.innerText = "Invalid Data!"
        } else {
            var general = price - price * (discount / 100);
            result.innerText = `Generally, ${Math.round(general * 100) / 100}\$`;
        }
    });
}


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
        if (size <= 0 || size > 30) {
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
                cell.addEventListener("click", cellSelection);
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
    var maxSelection = document.getElementById("maxSelection").value;
    if (maxSelection > 30) {
        maxSelection = 30;
    } else if (maxSelection < 0) {
        maxSelection = 0;
    }

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


/*
10. In accordance with your subject area, create a base class and a successor class
with five functions (including getters and setters), to provide a demonstration of their
capabilities. Create a decorator for one of the functions and demonstrate its use. Implement
two options: 1) prototypical inheritance in the functional style and 2) the "class"/"extends"
construction
*/
const classFunctionActivator = document.getElementById("classFunctionActivator");
if (classFunctionActivator) {
    classFunctionActivator.addEventListener("click", function (e) {
        e.preventDefault();
        console.clear();

        functionalInheritance();
        classInheritance();
    });
}
function functionalInheritance() {
    function withTimestamp(fn) {
      return function() {
        const timestamp = new Date().toLocaleString();
        const result = fn.apply(this, arguments);
        return `${timestamp}: ${result}`;
      };
    }

    function Animal(name, age) {
        this.name = name;
        this.age = age;
    }
    Animal.prototype.getName = function() {
        return this.name;
    };
    Animal.prototype.setName = function(name) {
        this.name = name;
    };
    Animal.prototype.getAge = function() {
        return this.age;
    };
    Animal.prototype.setAge = function(age) {
        this.age = age;
    };
    Animal.prototype.getDetails = withTimestamp(function() {
        return `Name: ${this.name}, Age: ${this.age}`;
    });

    function Dog(name, age, breed) {
        Animal.call(this, name, age);
        this.breed = breed;

        this.getBreed = function () {
            return this.breed;
        }
        this.setBreed = function (breed) {
            this.breed = breed;
        }
    }
    Dog.prototype = Object.create(Animal.prototype);
    Dog.prototype.bark = function() {
        return `${this.name} barks!`;
    };
    Dog.prototype.getDetails = function() {
        const animalDetails = Animal.prototype.getDetails.call(this);
        return `${animalDetails}, Breed: ${this.getBreed()}`;
    };

    const myAnimal = new Animal("Rover", 5);
    const myDog = new Dog("Buddy", 3, "Golden Retriever");

    console.log(myDog.getName());
    myDog.setName("Badass");
    console.log(myDog.getName());
    console.log(myAnimal.getDetails());
    console.log(myDog.getDetails());
    console.log(myDog.bark());
}
function classInheritance() {
    function withTimestamp(fn) {
      return function() {
        const timestamp = new Date().toLocaleString();
        const result = fn.apply(this, arguments);
        return `${timestamp}: ${result}`;
      };
    }

    class Animal {
        constructor(name, age) {
            this.name = name;
            this.age = age;
        }
        getName() {
            return this.name;
        }
        setName(name) {
            this.name = name;
        }
        getAge() {
            return this.age;
        }
        setAge(age) {
            this.age = age;
        }
        getDetails = withTimestamp(() => {
            return `Name: ${this.name}, Age: ${this.age}`;
        });
    }

    class Dog extends Animal {
        constructor(name, age, breed) {
            super(name, age);
            this.breed = breed;
        }
        getBreed() {
            return this.breed;
        }
        setBreed(breed) {
            this.breed = breed;
        }
        bark() {
            return `${this.name} barks!`;
        }
        getDetails() {
            const animalDetails = super.getDetails();
            return `${animalDetails}, Breed: ${this.getBreed()}`;
        }
    }

    const myAnimal = new Animal("Rover", 5);
    const myDog = new Dog("Buddy", 3, "Golden Retriever");

    console.log(myDog.getName());
    myDog.setName("Badass");
    console.log(myDog.getName());
    console.log(myAnimal.getDetails());
    console.log(myDog.getDetails());
    console.log(myDog.bark());
}


/*
11. Develop scripts that implement an algorithm for solving the problem using associative
arrays. Input of the initial data and Output of the results obtained should be carried out
using the <form> html document form.
2.) An associative array containing information about several cars is given: make of
the car, its number and the name of the owner. Find the names of the owners and
numbers of cars of this make.
*/
const searchButton = document.getElementById("searchButton");
if (searchButton) {
    const carsData = [
        new Map([ ["make", "Toyota"], ["number", "ABC123"], ["owner", "Shallow"] ]),
        new Map([ ["make", "Honda"], ["number", "XYZ789"], ["owner", "Rubin"] ]),
        new Map([ ["make", "Toyota"], ["number", "DEF456"], ["owner", "Sword"] ]),
        new Map([ ["make", "Nissan"], ["number", "A2KHG2"], ["owner", "Casper"] ])
    ];

    searchButton.addEventListener("click", function (e) {
        e.preventDefault();

        const carMake = document.getElementById("carMake").value;
        const resultsDiv = document.getElementById("resultsDiv");
        resultsDiv.innerHTML = "";

        const matchingCars = carsData.filter(car => car.get("make").toLowerCase() === carMake.toLowerCase());
        if (matchingCars.length === 0) {
            resultsDiv.innerHTML = "This make of car was not found.";
        } else {
            const resultList = document.createElement("ul");
            matchingCars.forEach(car => {
                const listItem = document.createElement("li");
                    listItem.textContent = `Owner: ${car.get("owner")}, Number: ${car.get("number")}`;
                    resultList.appendChild(listItem);
                });
            resultsDiv.appendChild(resultList);
        }
    });
}
