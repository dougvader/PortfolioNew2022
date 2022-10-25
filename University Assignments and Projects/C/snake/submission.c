//avr-gcc -mmcu=atmega32u4 -Os -DF_CPU=8000000L snake.c -o snake.o -L../cab202_teensy -I../cab202_teensy -lcab202_teensy -lm -std=gnu99
//avr-objcopy -O ihex snake.o snake.hex

/*  CAB202 Assignment 2
*	
*
*	
*	Queensland University of Technology
*/

#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "lcd.h"
#include "graphics.h"
#include "cpu_speed.h"
#include "sprite.h"
#include "macros.h"


// Constants
#define EAST (1)
#define SOUTH (2)
#define WEST (3)
#define NORTH (4)

bool game_over = false;
bool moving = false;
bool walls = false;
bool collided = false;


// Variables
int	move_direction = EAST;
int lives = 5;
int score = 0;
int level = 0;
int snake_length = 2;
Sprite food;
Sprite snake_head;
Sprite snake_tail[10];
int food_x;
int food_y;

// Functions
void Game();
void ShowScore();
void StartScreen();
void Initialize();
void UpdateInputs();
void SetupScreen();

void SetupSnakeHead();
void SetupSnakeTail();
bool SpritesCollided();

void DrawFood();
void MoveSnake();
void EatFood();
void UpdateSnake();
bool SpritesCollidedFood();
bool SpritesCollidedTail();
void Walls();
void CheckCollisionSnake();
void CheckCollisionWalls();
void GameOver();

// Sprites
    	unsigned char bitmap [] = {
        0b11100000,
        0b11100000,
        0b11100000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000};

//Game
void Game() {
	Initialize();
	StartScreen();
	_delay_ms(500);
    clear_screen();
	ShowScore();
	SetupSnakeHead();
	//SetupSnakeTail();
	DrawFood();
	show_screen();
}

//Process
void process() {
	clear_screen();
	CheckCollisionWalls();
	//Walls();
	if (SpritesCollidedFood()) {
		EatFood();
	}
	
	if (collided == true){
		lives--;
		snake_length = 2; 
		SetupSnakeHead();
		draw_sprite(&snake_head);
		collided = false;
	}
	
	if ((PINF>>PF5) & 1) {
		walls = true;
    }
	
	if ((PINF>>PF6) & 1) {
		walls = false;
    }
	
	if (lives == 0){
		GameOver();
		_delay_ms(500);
	}
	
	if( walls ){
         draw_line(0, 15, 57, 15);
         draw_line(81, 30, 45, 30);
         draw_line(21, 42, 21, 21);
     }
	
/* 	if (SpritesCollidedTail()) {
		lives--;
		draw_sprite(&snake_head);
		//SetupSnakeHead();
	} */
	
	UpdateInputs();
	ShowScore();
	UpdateSnake();
	MoveSnake();
	CheckCollisionSnake();
	show_screen();
}

// Main 
int main() {
	Game();
    while ( !game_over ) {
        process();
		_delay_ms(100);
	}
}

//Initialize 
void Initialize() {
		//set clock speed
	set_clock_speed(CPU_8MHz);
		// Initialising the LCD screen
	lcd_init(LCD_DEFAULT_CONTRAST);
	
		// Thumb-stick inputs
	DDRD = DDRD & 0b11111101;
	DDRB = DDRB & 0b01111111;	
	DDRD = DDRD & 0b11111110;
	DDRB = DDRB & 0b11111101;
	DDRB = DDRB & 0b11111110;	
	
	    // Initalising the push buttons as inputs
    DDRF &= ~((1 << PF5) | (1 << PF6));
	
		// set seed
	srand(0);
}

void ShowScore() {
    char value[90];
    sprintf(value, "%d", lives);
    draw_string(1, 1, "L: ");
    draw_string(11, 1, value);
    sprintf(value, "%d  ", score);
    draw_string(20, 1, "S: ");
    draw_string(30, 1, value);
    
    //Game border
    draw_line(83, 9, 83, 47);
    draw_line(0, 9, 0, 47);
    draw_line(0, 47, 83, 47);
    draw_line(0, 9, 83, 9);
    //show_screen();
}

void UpdateInputs() {
	if (((PIND >> 1) &0b1)) {
		move_direction = NORTH;
		moving = true;	
	}
	
	if (((PINB >> 7) &0b1)) {
		move_direction = SOUTH;
		moving = true;	
	}
	
	if (((PINB >> 1) &0b1)) {
		move_direction = WEST;
		moving = true;	
	}
	
	if (((PIND >> 0) &0b1)) {
		move_direction = EAST;
		moving = true;	
	}	
}

void StartScreen() {
	draw_string(9, 5, "Doug Brennan");
	draw_string(9, 17, "n7326645");
	show_screen();
	_delay_ms(2000);
}

void SetupSnakeHead() {
    //sets up snake head
    init_sprite(&snake_head, 30, 45, 3, 3, bitmap);
    draw_sprite(&snake_head);
}

void SetupSnakeTail(){
    //sets up snake tail
	for (int i = 0; i < snake_length; i++) {
		init_sprite(&snake_tail[0], snake_head.x , 35, 3, 3, bitmap);
		draw_sprite(&snake_tail[0]); 
	}
}

void DrawFood() {
    //spawns food at random location within screen bounds   
    food_x = rand() % LCD_X;
	food_y = rand() % LCD_Y;
	while (food_x <= 0 || food_x >= 82) {
		food_x = rand() % 40;
	}
	while (food_y <= 11 || food_y>= 45) {
		food_y = rand() % (LCD_Y - 1);
	} 
    init_sprite(&food, food_x, food_y, 3, 3, bitmap );  
    draw_sprite(&food );
}

void CheckCollisionSnake() {
	for (int i = 0; i <= snake_length; i++) {
		if (snake_head.x == snake_tail[i].x && snake_head.y == snake_tail[i].y) {
			collided = true;
		} 
	}
}

void CheckCollisionWalls() {
	int x1 = snake_head.x;
    int y1 = snake_head.y;
		
/* 	if( walls ){
         draw_line(0, 9, 57, 9);
         draw_line(81, 30, 45, 30);
         draw_line(21, 42, 21, 21); */
     
	 
	//Collide Walls
	if(walls){       
        if( ((x1 >= 0) && (x1 <= 57) && y1 <= 15) || ((x1 >= 45) && (x1 <= 81) && y1 == 30) || ((y1 >= 21) && (y1 <= 42) && x1 == 21)){
			collided = true;
        }
    }
}

void MoveSnake() {
	int snake_x;
	int snake_y;
	int old_x = snake_head.x;
	int old_y = snake_head.y;

//Update Food
	init_sprite( &food, food_x, food_y, 3, 3, bitmap );
	draw_sprite(&food);
	
//Move Snake
	if (move_direction == EAST){	
		snake_x = snake_head.x + 3;
		snake_y = snake_head.y;
	}
	if (move_direction == WEST){
		snake_x = snake_head.x - 3;
		snake_y = snake_head.y;
	}
	if (move_direction == NORTH){
		snake_x = snake_head.x;
		snake_y = snake_head.y - 3;
	}
	if (move_direction == SOUTH){
		snake_x = snake_head.x;
		snake_y = snake_head.y + 3;
	}
	
//Snake Collide Walls
	if (snake_head.x >= 83 && move_direction == EAST) {
		init_sprite(&snake_head, 0, snake_y, 3, 3, bitmap);
	} else if (snake_head.x <= 0 && move_direction == WEST){
        init_sprite(&snake_head, 83, snake_y, 3, 3, bitmap); 
    } else if (snake_head.y >= 47 && move_direction == SOUTH){
        init_sprite(&snake_head, snake_x, 9, 3, 3, bitmap); 
    } else if (snake_head.y <= 11 && move_direction == NORTH){
        init_sprite(&snake_head, snake_x, 47, 3, 3, bitmap); 
    } else {
      init_sprite(&snake_head, snake_x, snake_y, 3, 3, bitmap);  
    }
	draw_sprite(&snake_head);

	
	
	snake_tail[0].x = old_x;
	snake_tail[0].y = old_y;
	
		//Move Tail
	for (int i = snake_length; i > 0; i--) {
		init_sprite(&snake_tail[i], snake_tail[i-1].x, snake_tail[i-1].y, 3, 3, bitmap);	
		draw_sprite(&snake_tail[i]);
	}
			
	snake_tail[0].x = old_x;
	snake_tail[0].y = old_y;
	
	for (int i = 0; i < snake_length; i++) {
		draw_sprite(&snake_tail[i]);
	}

/* 	//Collide tail
	for (int i = 0; i < snake_length; i++){
		if (snake_head.x == snake_tail[i].x && snake_head.y == snake_tail[i].y) {
			collided = true;
		}
	} */	
}

void EatFood() {
	DrawFood();
    if (walls == true) {
		score =+ 2;
	} else {
		score++;
	}
	snake_length++;
}

bool SpritesCollidedFood() {
	int snake_head_top = round(snake_head.y);
	int snake_head_bottom = snake_head_top + 2; //height - 1
	int snake_head_left = round(snake_head.x);
	int snake_head_right = snake_head_left + 2; //length -1
	
	int food_top = round(food.y);
	int food_bottom = food_top + 2; //height - 1
	int food_left = round(food.x);
	int food_right = food_left + 2; //length - 1
	
	return !(
		snake_head_bottom < food_top
		|| snake_head_top > food_bottom
		|| snake_head_right < food_left
		|| snake_head_left > food_right
		);
}

bool SpritesCollidedTail() {
	int snake_head_top = round(snake_head.y);
	int snake_head_bottom = snake_head_top + 2; //height - 1
	int snake_head_left = round(snake_head.x);
	int snake_head_right = snake_head_left + 2; //length -1
	int x1 = snake_head.x;
    int y1 = snake_head.y;
	
/* 	if( walls ){
         draw_line(0, 10, 55, 10);
         draw_line(83, 30, 45, 30);
         draw_line(20, 43, 20, 20);
     } */
	
	//Collide Walls
	if(walls){       
        if( ((x1 >= 0) && (x1 <= 55) && y1 == 10) || ((x1 >= 45) && (x1 <= 83) && y1 == 30) || ((y1 >= 20) && (y1 <= 43) && x1 == 20)){
			collided = true;
        }
    }
	
/* 		//Move Tail
		if (snake_head.x == snake_tail[i].x && snake_head.y == snake_tail[i].y) {
			return true;
		}
	} */

/* 	for (int i = 0; i < snake_length; i++){
		return !(
			snake_head_bottom <= round(snake_tail[i].y)
			|| snake_head_top >= (round(snake_tail[i].y)) + 2
			|| snake_head_right <= round(snake_tail[i].x)
			|| snake_head_left >= (round(snake_tail[i].x)) + 2
			);
	} */
	
/* 	for (int i = 0; i < snake_length; i++){
		int snake_tail_top[i] = round(snake_tail[i].y);
		int snake_tail_bottom[i] = snake_tail_top[i] + 2; //height - 1
		int snake_tail_left[i] = round(snake_tail[i].x);
		int snake_tail_right[i] = snake_tail_left[i] + 2; //length -1
		return !(
			snake_head_bottom < snake_tail_top[i]
			|| snake_head_top > snake_tail_bottom[i]
			|| snake_head_right < snake_tail_left[i]
			|| snake_head_left > snake_tail_right[i]
			);
	} */	
}	

void GameOver() {  
    clear_screen();
    char * gameover = "GAME OVER";
    draw_string(20, 20, gameover);
    show_screen();
	_delay_ms(500);
	game_over = true;
}

void UpdateSnake() {
	draw_sprite(&snake_head);
	for (int i = 0; i < snake_length; i++) {
		draw_sprite(&snake_tail[i]);
	}
}
