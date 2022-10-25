// Enemies our player must avoid
class Enemys {
    // Variables applied to each of our instances go here,
    // we've provided one for you to get started
    constructor(x, y, speed) {
        this.x = x;
        this.y = y;
        this.speed = speed;
        // The image/sprite for our enemies, this uses
        // a helper we've provided to easily load images
        this.sprite = 'images/enemy-bug.png';
    }
    // Update the enemy's position, required method for game
    // Parameter: dt, a time delta between ticks
    update(dt) {
        // You should multiply any movement by the dt parameter
        // which will ensure the game runs at the same speed for
        // all computers. 
        if (this.x > 505) {
            this.x = -202;
        } else {
            this.x = (this.x + (this.speed * 60 * dt)); 
            this.render();
        }
    }
    // Draw the enemy on the screen, required method for game
    render() {
        ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
    }
}

// Now write your own player class
// This class requires an update(), render() and
// a handleInput() method.
class Player {
    constructor(name = 'default', style = 'default', gender = 'male', x = 202, y = 463) {
        this.name = name;
        this.style = style;
        this.gender = gender;
        this.sprite = 'images/char-boy.png'; 
        this.x = x;
        this.y = y;
        this.keyGathered = false;
        this.hasWon = false;
    }

    update(){
        this.render();
    }

    render() {
        ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
    }

    //Handles player to not go off screen
    handleInput(key) { 
        if (this.x >= 101 && key == 'left') {
            this.x = this.x - 101;
        } if (this.x <= 303 && key == 'right') { 
            this.x = this.x + 101;
        } if (this.y > 0 && key == 'up') {
            this.y = this.y - 83;
        } if (this.y <= 415 && key == 'down') {
            this.y = this.y + 83;
        }   
        this.render();                
    }

    //Checks if player collides with an enemy
    checkCollisions() {
        for (i=0; i<allEnemies.length; i++) {
            if (this.x < allEnemies[i].x + 80 && this.x + 80 > allEnemies[i].x && this.y < allEnemies[i].y + 20 && this.y + 20 > allEnemies[i].y) {
                this.collide();
            }
        }
    } 

    //Resets parameters if collision occurs
    collide() {
        this.x = 202;
        this.y = 463;
        this.keyGathered = false;
        this.render();
        key.reset();
        attempts++;
        document.querySelector('.attempts').textContent = attempts;
    }

    //Picks up the key
    getKey() {
        if (this.x == key.x && this.y == key.y) {
            this.keyGathered = true;
            key.x = -505; 
            key.update();
        }
    }

    //Processes the win
    Won() {
        if (this.keyGathered == true) {
            if (this.x == 202 && this.y == 463) {
                this.hasWon = true;
                let endTime = new Date();
                let timeTaken = Math.round((endTime - startTime) / 1000);
                star.x = -505;
                star.update();
                window.confirm('Congratulations you successfully retrieved the key without hitting any bugs. It took you ' + timeTaken + ' seconds to complete, and ' + attempts + ' attempts.');
                start();
            }
        }
    }
}

class Key {
    constructor(x = 202, y = -35) {
        this.x = x;
        this.y = y;
        this.sprite = 'images/Key.png';
    }

    update() {
        this.render();
    }

    render() {
        ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
    }

    reset() {
        this.x = 202;
        this.y = -35;
        this.update();
    }
}

class Star {
    constructor (x = 202, y =  498) {
        this.x = x;
        this.y = y;
        this.sprite = 'images/Star.png';
    }

    update() {
        star.render();
    }

    render() {
        ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
    }
}


// Now instantiate your objects.
// Place all enemy objects in an array called allEnemies
// Place the player object in a variable called player
const allEnemies = [];
const numEnemies = 7;
//Creates unique enemies
for (i=0; i<=numEnemies; i++) {
    if (allEnemies.length == 0) {
        let enemy = new Enemys(-101, 214, 2);
        allEnemies.push(enemy);
    } if (allEnemies.length == 1) {
        let enemy = new Enemys(0, 131, 4);
        allEnemies.push(enemy);
    } if (allEnemies.length == 2) {
        let enemy = new Enemys(-202, 48, 3);
        allEnemies.push(enemy);
    } if (allEnemies.length == 3) {
        let enemy = new Enemys(-202, 297, 3.5);
        allEnemies.push(enemy);
    } if (allEnemies.length == 4) {
        let enemy = new Enemys(-505, 131, 2.5);
        allEnemies.push(enemy);
    } if (allEnemies.length == 5) {
        let enemy = new Enemys(-303, 214, 2.5);
        allEnemies.push(enemy);
    } if (allEnemies.length == 6) {
        let enemy = new Enemys(-303, 48, 2);
        allEnemies.push(enemy);
    }    
}

//Sets up variables for game start
let player = new Player();
let key = new Key();
let star = new Star();
let attempts = 1;
startTime = new Date();
timer = setInterval(displayTimer, 1000);


// This listens for key presses and sends the keys to your
// Player.handleInput() method. You don't need to modify this.
document.addEventListener('keyup', function(e) {
    var allowedKeys = {
        37: 'left',
        38: 'up',
        39: 'right',
        40: 'down'
    };

    player.handleInput(allowedKeys[e.keyCode]);
});

function displayTimer() {
    let temp = new Date();
    document.getElementById('time').innerHTML = Math.round((temp - startTime) /1000);
}

//Restarts the game
function start() {
    player = new Player();
    key = new Key();
    star = new Star();
    attempts = 1;
    document.querySelector('.attempts').textContent = attempts;
    startTime = new Date();
    timer = setInterval(displayTimer, 1000);
}
