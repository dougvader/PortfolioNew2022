//Variables
const DECKLIST = document.querySelectorAll('.card');
const classNames = ["fa fa-diamond", "fa fa-paper-plane-o", "fa fa-anchor", "fa fa-bolt", "fa fa-cube", "fa fa-leaf", "fa fa-bicycle", "fa fa-bomb", "fa fa-diamond", "fa fa-paper-plane-o", "fa fa-anchor", "fa fa-bolt", "fa fa-cube", "fa fa-leaf", "fa fa-bicycle", "fa fa-bomb"];
let openCards = [];
let moves = 0;
let matches = 0;
let star = 0;
let startTime = 0;
let endTime = 0;
let timer;
let hasWon = false;
const deck = document.querySelector('.deck');
const reset = document.querySelector('.restart');
deck.addEventListener('click', clickACard);
reset.addEventListener('click', clickReset);

//Main
start();

//Functions
function start() {
    hasWon = false;
    startTime = new Date();
    timer = setInterval(displayTimer, 1000);
    let shuffled = [];
    openCards = [];
    moves = 0;
    matches = 0;
    document.querySelector('.moves').textContent = moves;
    shuffled = shuffle(classNames); 
    for (i=0; i<DECKLIST.length; i++) {
        DECKLIST[i].firstElementChild.className = shuffled[i];   
    }
}

function displayTimer() {
    let temp = new Date();
    document.getElementById('time').innerHTML = Math.round((temp - startTime) /1000);
    if (hasWon == true) {
        clearInterval(timer);
    }
}

// Shuffle function from http://stackoverflow.com/a/2450976
function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
    while (currentIndex !== 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }
    return array;
}

function clickACard(evt) {
    if (openCards.length == 0) {
        evt.target.classList.add('show');
        evt.target.classList.add('open');
        addToOpen(evt.target.firstElementChild.className);
    } else if (openCards.length == 1) {
        moves = moves + 1;
        document.querySelector('.moves').textContent = moves;
        if (evt.target.firstElementChild.className == openCards[0]) {
            match(evt.target.firstElementChild.className);
            evt.target.removeEventListener('click', clickACard);
            openCards.pop();
        } else {
            evt.target.classList.add('show');
            evt.target.classList.add('open');
            removeFromOpen(evt.target.firstElementChild.className, openCards[0]);
        }
    }
    if (moves > 0) {
        if ((moves <= 15) && (moves > 0)) {
            document.getElementById('star1').setAttribute('style', 'color: gold');
            document.getElementById('star2').setAttribute('style', 'color: gold');
            document.getElementById('star3').setAttribute('style', 'color: gold');
            star = 3;
        } else if ((moves <= 25) && (moves > 15)) {
            document.getElementById('star1').setAttribute('style', 'color: gold');
            document.getElementById('star2').setAttribute('style', 'color: gold');
            document.getElementById('star3').setAttribute('style', 'color: black');
            star = 2;
        } else if ((moves <= 35) && (moves > 25)) {
            document.getElementById('star1').setAttribute('style', 'color: gold');
            document.getElementById('star2').setAttribute('style', 'color: black');
            document.getElementById('star3').setAttribute('style', 'color: black');
            star = 1;
        } 
    }
} 

function addToOpen(cardClassName) {
    openCards.push(cardClassName);
}

function removeFromOpen(cardClassName1, cardClassName2) {
    setTimeout(function removeShow(){
        for (i=0; i<DECKLIST.length; i++) {
            if (DECKLIST.item(i).firstElementChild.className == cardClassName1) {
                DECKLIST[i].classList.remove('show');
                DECKLIST[i].classList.remove('open');
            } if (DECKLIST.item(i).firstElementChild.className == cardClassName2) {
                DECKLIST[i].classList.remove('show');
                DECKLIST[i].classList.remove('open');
            }
        }
    }, 1000);
    openCards.pop();
}

function match(cardClassName) {
    matches = matches + 1;
    for (i=0; i<DECKLIST.length; i++) {
        if (DECKLIST.item(i).firstElementChild.className == cardClassName) {
            DECKLIST.item(i).classList.add('match');
        }
    }
    if (matches == 8) {
        win();
    }
}

function clickReset() {
    for (i=0; i<DECKLIST.length; i++) {
        DECKLIST[i].classList.remove('show');
        DECKLIST[i].classList.remove('open');
        DECKLIST[i].classList.remove('match');
    }
    start();
    for (i=1; i<4; i++) {
        document.getElementById('star' + i).setAttribute('style', 'color: black');
    }
}

function win() {
    hasWon = true;
    endTime = new Date()
    let timeTaken = Math.round((endTime - startTime) / 1000);
    window.confirm("Congratulations you won with " + moves + ' moves! A star count of ' + star + '. It took you ' + timeTaken + ' seconds to complete.');
}