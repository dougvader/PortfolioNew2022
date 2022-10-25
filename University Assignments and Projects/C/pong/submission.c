//gcc pong.c -std=gnu99 -I../zdk -L../zdk -lzdk -lncurses -o pong
//gcc -o a1_n7326645 *.c -std=gnu99 -Wall -Werror -I../ZDK -L../ZDK -lzdk -lncurses -lm
#include <stdlib.h>
#include <math.h>
#include <cab202_graphics.h>
#include <cab202_sprites.h>
#include <cab202_timers.h>
#include <time.h>

#define DELAY 10 /* milliseconds */
#define RAILWIDTH (40)

bool game_over = false;
bool update_screen = true;

// Global Variables
sprite_id help;
sprite_id paddle_right;
sprite_id paddle_left;
sprite_id ball;
sprite_id game_over_sprite;
sprite_id gravity;
sprite_id rails_top[RAILWIDTH];
sprite_id rails_bottom[RAILWIDTH];

double initial_time = 0;
int the_time = 0;
int seconds;
int minutes;
int h;
int w;
int lives = 5;
int score = 0;
int level;
double ball_speed = 0.25;

// Declare Functions
void draw_border();
void draw_help();
void key_continue();
void draw_top_text();
void start_timer();
void user_paddle();
void computer_paddle();
int get_paddle_height();
void update_right_paddle();
void update_left_paddle();
void yes_game_over();
void draw_ball();
void update_ball();
void checkAdvanceLevel();
void reset();
void draw_gravity();
void accelerate_ball_towards_star();
void setup_rail();

sprite_id setup_a_rail_top();
sprite_id setup_a_rail_bottom();

//Sprites
char * help_img = 
/**/	"Hello and welcome to Dougie's Pong Bonanza."
/**/    "           Student #n7326645               "
/**/	"                                           "
/**/ 	"             How to play:                  "
/**/	"       - 8/5: Move up or down              "
/**/	"       -  Q : Quit game                    "
/**/	"       -  H : Display help menu            "
/**/	"       -  L : Advance level                "
/**/	"                                           "
/**/	"        Press any key to begin             ";

char * paddle_img = 
/**/    "|"
/**/    "|"
/**/    "|"
/**/    "|"
/**/    "|"
/**/    "|"
/**/    "|";

char * ball_img = 
/**/    "O";

char * game_over_img = 
/**/ 	"   OH NO!  "
/**/    "  You Lost "
/**/    "Play Again?"
/**/    "    Y/N    ";

char * gravity_img = 
/**/    " _^^_ "
/**/    "/    /"
/**/    "/ __ /"
/**/    "/ }{ /"
/**/    "<><><>"
/**/    "|_^^_|";

char * rail_img = 
/**/    "=";

//Game Functions
void game() {
// Variables
	int h = screen_height();
	int w = screen_width();
	int angle = rand() % 360;
	lives = 5;
	score = 0;
	level = 1;
	
//Functions
		// Welcome Message and Timer Start
	show_screen();
	setup_screen();
	draw_border(h, w);
	draw_help(h, w);
	show_screen();
	key_continue();
	clear_screen();
	draw_border(h, w);
	start_timer(h, w);
	show_screen();
		
		//Level 1
	clear_screen();
	draw_border(h, w);
	setup_rail();
	user_paddle(h, w, paddle_img);
	draw_gravity(h, w);
	computer_paddle(h, w, paddle_img);
	sprite_draw(paddle_right);
	draw_ball(h, w, ball_img);
	sprite_draw(ball);
	sprite_turn_to(ball, ball_speed, 0);
	while (angle > 45 && angle < 315) {
		angle = rand() % 360;
	}
	sprite_turn( ball, angle );
	show_screen();
}

//Game Algorithms
void process() {
	sprite_step(ball);
	//Variables
	int h = screen_height();
	int w = screen_width();
    int key = get_char();
	update_right_paddle(key, h, w);
	update_left_paddle(h, w);
	update_ball(h, w);
	
    if ( key == 'q' || lives == 0)  {
		yes_game_over(h, w);
    } 
	
	if (key == 'h' || key == 'H'){
		draw_help(h, w);
		show_screen();
		wait_char();
	}
	
	if (level > 4){
		reset();
		level = 1;
	}
	
	checkAdvanceLevel(key);
	draw_border(h, w);
	sprite_draw(paddle_right);
	draw_top_text();
	show_screen();
}

// Clean up game
void cleanup(void) {
    // STATEMENTS
}

// Program entry point.
int main(void) {
    setup_screen();

#if defined(AUTO_SAVE_SCREEN)
    auto_save_screen(true);
#endif
	setup_screen();
	game();
	show_screen();

    while ( !game_over ) {
        process();

        if ( update_screen ) {
            show_screen();
        }
        timer_pause(DELAY);
    }

    cleanup();
    return 0;
}

void setup_rail(void){
	int w = screen_width();
	int ctr = 0;
	int rail_x = ((w/2) - (RAILWIDTH/2)) + ctr;
	for ( int i = 0; i < RAILWIDTH; i++ ) {
		rails_top[i] = setup_a_rail_top(rail_x, ctr);
		rails_bottom[i] = setup_a_rail_bottom(rail_x, ctr);
		ctr++;
    }
}

sprite_id setup_a_rail_top(int rail_x, int ctr) {
	int h = screen_height();
    int rail_y = (h/3);
    sprite_id rail = sprite_create(rail_x + ctr, rail_y, 1, 1, rail_img);

    return rail;
}

sprite_id setup_a_rail_bottom(int rail_x, int ctr) {
	int h = screen_height();
    int rail_y = (h/3) * 2;
    sprite_id rail = sprite_create(rail_x + ctr, rail_y, 1, 1, rail_img);

    return rail;
}

void reset_time(void){
	initial_time = get_current_time();
}

void draw_gravity(int h, int w){
	gravity = sprite_create((w/2)-3.5, (h/2)-2, 6, 6, gravity_img);
}

void reset(){
	game();
}

void checkAdvanceLevel(int key){
	if (key == 'l' || key == 'L'){
		reset_time();
		level++;
		lives = 5;
	}
	if (level > 1){
		sprite_draw(paddle_left);
	} 
	if (level == 3){
		if (seconds >= 5){
			sprite_draw(gravity);
		}
	}
	if (level == 4){
		for ( int i = 0; i < RAILWIDTH; i++ ) {
			sprite_draw(rails_top[i]);
			sprite_draw(rails_bottom[i]);
		}
	}
}

bool sprites_collided_rails(sprite_id rail) {
	int ball_x = round(sprite_x(ball)),
		ball_y = round(sprite_y(ball));

	int rail_x = round(sprite_x(rail)),
		rail_y = round(sprite_y(rail));
						
	return (ball_x == rail_x && ball_y == rail_y);
	
}

bool sprites_collided_right( sprite_id ball, sprite_id paddle_right) {
	int ball_top = round( sprite_y( ball ) ),
		ball_bottom = ball_top + sprite_height(ball) - 1,
		ball_left = round( sprite_x( ball ) ),
		ball_right = ball_left + sprite_width(ball) - 1;

	int paddle_right_top = round( sprite_y( paddle_right ) ),
		paddle_right_bottom = paddle_right_top + sprite_height(paddle_right) - 1,
		paddle_right_left = round( sprite_x( paddle_right ) ),
		paddle_right_right = paddle_right_left + sprite_width( paddle_right ) - 1;
		
	return !(
		ball_bottom < paddle_right_top
		|| ball_top > paddle_right_bottom
		|| ball_right < paddle_right_left
		|| ball_left > paddle_right_right
		);
}

bool sprites_collided_left( sprite_id ball, sprite_id paddle_left) {
	int ball_top = round( sprite_y( ball ) ),
		ball_bottom = ball_top + sprite_height(ball) - 1,
		ball_left = round( sprite_x( ball ) ),
		ball_right = ball_left + sprite_width(ball) - 1;
		
	int paddle_left_top = round( sprite_y( paddle_left ) ),
		paddle_left_bottom = paddle_left_top + sprite_height(paddle_left) - 1,
		paddle_left_left = round( sprite_x( paddle_left ) ),
		paddle_left_right = paddle_left_left + sprite_width( paddle_left ) - 1;
		
	return !(
		ball_bottom < paddle_left_top
		|| ball_top > paddle_left_bottom
		|| ball_right < paddle_left_left
		|| ball_left > paddle_left_right
		);
}

void update_ball(int h, int w){
	int y_star = h/2;
	int x_star = w/2;
	bool dir_changed = false;
	int bx = round( sprite_x( ball ) );
	int by = round( sprite_y( ball ) );
	
	// (t) Get the displacement vector of the ball.
	double bdx = sprite_dx( ball );
	double bdy = sprite_dy( ball );
	double x_dist = x_star - sprite_x(ball);
	double y_dist = y_star - sprite_y(ball);
	double dist = sqrt(pow(x_dist,2) + pow(y_dist,2));
	//  (g) Normalise dx and dy by dividing them both by dist. 
	x_dist = x_dist / dist;
	y_dist = y_dist / dist;
	
		// Ball goes off screen
	if (bx > w - 1) {
		lives--;
		reset_time();
		double angle = rand() % 360;
		sprite_destroy(ball);
		draw_ball(h, w, ball_img);
		sprite_draw(ball);
		sprite_turn_to(ball, ball_speed, 0);
		while (angle > 45 && angle < 315) {
			angle = rand() % 360;
		}
		sprite_turn( ball, angle );
		process();		
	} else if (bx < 1 && level > 1) {
		score++;
		reset_time();
		double angle = rand() % 360;
		sprite_destroy(ball);
		draw_ball(h, w, ball_img);
		sprite_draw(ball);
		sprite_turn_to(ball, ball_speed, 0);
		while (angle > 45 && angle < 315) {
			angle = rand() % 360;
		}
		sprite_turn( ball, angle );
		process();
	} else if (bx < w-w +1){
		bdx = -bdx;
		dir_changed = true;
	}
	
	if (level == 3 && dist < 25 && seconds >= 5){
		x_dist = x_dist * 0.16;
		y_dist = y_dist * 0.16;
		//sprite_turn(ball, -90);
		sprite_draw(ball);
		accelerate_ball_towards_star(x_star, y_star);
	}
	
	if (level == 4){
		for (int i = 0; i < RAILWIDTH; i++ ) {
			if (rails_top[i]->is_visible && sprites_collided_rails(rails_top[i])){
				sprite_hide(rails_top[i]);
				bdy = -bdy;
				dir_changed = true;
			}
			if (rails_bottom[i]->is_visible && sprites_collided_rails(rails_bottom[i])){
				sprite_hide(rails_bottom[i]);
				bdy = -bdy;
				dir_changed = true;
			}
		}
	}
	int paddle_right_top = round( sprite_y( paddle_right ) );
	int paddle_right_bottom = paddle_right_top + sprite_height(paddle_right) - 1;
	
		// If Ball and right paddle collide
	if (sprites_collided_right(ball, paddle_right)){
		if (sprite_y(ball) < paddle_right_top || sprite_y(ball) > paddle_right_bottom){
			bdy = -bdy;
			sprite_back( ball );
		} else {
			score++;
			bdx = -bdx;
		}
		dir_changed = true;
	} 
	int paddle_left_top = round( sprite_y( paddle_left ) );
	int	paddle_left_bottom = paddle_left_top + sprite_height(paddle_left) - 1;
	
	if (sprites_collided_left(ball, paddle_left) && level > 1) {
		if (sprite_y(ball) < paddle_left_top || sprite_y(ball) > paddle_left_bottom){
			bdy = -bdy;
			sprite_back( ball );
		} else {
			bdx = -bdx;
		}
		dir_changed = true;
	}

	// (v) Test to see if the ball hit the top or bottom border.
	if ( by == h - 1 || by == h-h+2) {
		bdy = -bdy;
		dir_changed = true;
	}

	// (w) Test to see if the ball needs to step back and change direction.
	if ( dir_changed ) {
		sprite_back( ball );
		sprite_turn_to( ball, bdx, bdy );
	}

    //  (b) [Optional] Modify these two lines _if necessary_ to accommodate the 
    //		modified dynamics introduced by bouncing off walls and floor.
    //bdx = sprite_dx(ball);
    //bdy = sprite_dy(ball);

    clear_screen();
    sprite_draw(ball);
}

void accelerate_ball_towards_star(int x_star, int y_star){

	double x_diff = x_star - sprite_x(ball);
	double y_diff = y_star - sprite_y(ball);
	double dist_squared = pow(x_diff,2) + pow(y_diff,2);
	bool center_hit = false;
	
	if (dist_squared < 1e-10){
		dist_squared = 1e-10;
	}
	double dist = sqrt(dist_squared);	
	if (dist < 25 && dist > 5 && center_hit == false){
		double dx = sprite_dx(ball);
		double dy = sprite_dy(ball);
		double GM = 1;
		double magnitude = GM/dist_squared;
		dx = dx + (magnitude * x_diff / dist);
		dy = dy + (magnitude * y_diff / dist);
		double v = sqrt(pow(dx,2) + pow(dy,2));
		if (v > 1){
			dx = dx / v;
			dy = dy / v;
		}
		sprite_turn_to(ball, dx, dy);		
	} else if (dist < 3){
		center_hit = true;
	}
}

void draw_ball(int h, int w, char * ball_img) {
	ball = sprite_create(w/2, h/2, 1, 1, ball_img);
}

void yes_game_over(int h, int w) {
	clear_screen();
	game_over_sprite = sprite_create((w/2)-5.5, (h/2)-2, 11, 4, game_over_img);
	sprite_draw(game_over_sprite);
	show_screen();
	int key = wait_char();
	if (key == 'y' || key == 'Y') {
		reset();
	} else if (key == 'n' || key == 'N') {
		game_over = true;
	} 
}

void update_right_paddle(int key, int h, int w) {
		    // Move paddle up or down
    int yp = round(sprite_y(paddle_right));
	
	if (key == '8' && yp >= h-h+4) {
		sprite_move_to(paddle_right, w-4, yp -1);
	} else if ( '5' == key && yp <= h -9 ) {
        sprite_move(paddle_right, 0, +1);
	}
}

void update_left_paddle(int h, int w) {
		    // Move paddle up or down
    int yp = round(sprite_y(paddle_left));
	if (level > 1){
		if((yp + 6) < sprite_y(ball) && (yp +7) <= h-2){
			sprite_move(paddle_left, 0 , 1);
		} else if (yp > sprite_y(ball) && yp >= h-h+4){
			sprite_move(paddle_left, 0 , -1);
		}
	}
}

int get_paddle_height(int h, int w) {
	int paddle_height;
	if (h >= 21) {
		paddle_height = 7;
	} else;
		paddle_height = (h-3-1) / 2;
	return paddle_height;
}

void draw_border(int h, int w) {
//Draw Border
	//top
	draw_line(0, 0, w-1, 0, '*');
	//bottom
	draw_line(0, h-1, w-1, h-1, '*');
	//left
	draw_line(0, h-1, 0, 0, '*');
	//right
	draw_line(w-1, h-1, w-1, 0, '*');
//Draw Line Below Top
	draw_line(0, h-h+2, w-1, h-h+2, '*');
}

void draw_help(int h, int w) {
//Create Help Screen Sprite
	help = sprite_create((w/2)-21.5, (h/2)-5, 43, 10, help_img);	
	sprite_draw(help);
}

void key_continue() {
//Any Key To Continue
	getchar();
}

void draw_top_text() {
	int h = screen_height();
	
	the_time = (get_current_time() - initial_time);
	seconds = the_time % 60;
	minutes = floor(the_time/60);
	
//Draw Top Text
	draw_formatted(1, h-h+1, "Lives = %d           *Score = %d          *Level = %d          *Elapsed Time = %d:%d", lives, score, level, minutes, seconds);
}

void start_timer(int h, int w) {
//Game start timer
	draw_string((w/2)-6, (h/2)-2.5, "Game beginning in ");
	show_screen();
	timer_pause(1000);
	draw_string(w/2,(h/2)-1.5, "\t3");
	show_screen();
	timer_pause(1000);
	draw_string(w/2,(h/2)-.5, "\t2");
	show_screen();
	timer_pause(1000);
	draw_string(w/2,(h/2)+.5, "\t1");
	show_screen();
	timer_pause(1000); 
	draw_string(w/2,(h/2)+1.5, "\tGO!");
	show_screen();
	timer_pause(1000); 
	initial_time = get_current_time();
}

void computer_paddle(int h, int w, char * paddle_img) {
	int paddle_height = 7; 
	//if (h >= 21) {
		//paddle_height = 7;
	//} else;
		//paddle_height = (h-3-1) / 2;
	paddle_left = sprite_create(4, (h/2) -3.5, 1, paddle_height, paddle_img);
}

void user_paddle(int h, int w, char * paddle_img) {
	int paddle_height = 7; 
	//if (h >= 21) {
		//paddle_height = 7;
	//} else;
		//paddle_height = (h-3-1) / 2;
	paddle_right = sprite_create(w-4, (h/2) -3.5, 1, paddle_height, paddle_img);
}