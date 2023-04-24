use raylib::prelude::*;

const PLAYERSPEED: f32 = 20.0;
const PLAYERSPEEDGROWTH: f32 = 2.0;
const PLAYERMAXSPEED: f32 = 200.0;
const PLAYERWIDTH: i32 = 20;
const PLAYERHEIGHT: i32 = 20;

#[derive(Debug, Default)]
struct Position {
    x: f32,
    y: f32,
}

#[derive(Debug, Default)]
struct Size {
    width: i32,
    height: i32,
}

#[derive(Debug, Default)]
struct Object {
    position: Position,
    size: Size,
    color: Color,
}

impl Object {
    // can assume all objects are rectangles for now
    pub fn within_other(&self, other: &Object) -> bool {
        let within_x = other.position.x <= self.position.x
            && self.position.x <= (other.position.x + other.size.width as f32);
        // note: do I need to do something special here bc of negative y
        let within_y = other.position.y <= self.position.y
            && self.position.y <= (other.position.y + other.size.height as f32);
        within_x & within_y
    }
}

#[derive(Debug)]
struct Goal {
    pub object: Object,
    callback: fn(),
    triggered: bool,
    trigger_once: bool,
}

#[derive(Debug, Default)]
struct GoalManager {
    pub goals: Vec<Goal>,
}

impl GoalManager {
    pub fn update(&mut self, player: &Player) {
        for goal in &mut self.goals[..] {
            if player.object.within_other(&goal.object) || goal.object.within_other(&player.object)
            {
                if goal.trigger_once & goal.triggered {
                    continue;
                }
                goal.callback.to_owned()();
                goal.triggered = true;
            }
        }
    }

    pub fn add_goal(&mut self, goal: Goal) {
        self.goals.push(goal);
    }
}

#[derive(Debug)]
struct Player {
    pub object: Object,
    speed: f32,
}

impl Default for Player {
    fn default() -> Self {
        Player {
            object: Object {
                position: Position::default(),
                size: Size {
                    width: PLAYERWIDTH,
                    height: PLAYERHEIGHT,
                },
                color: Color::BLACK,
            },
            speed: PLAYERSPEED,
        }
    }
}

impl Player {
    pub fn update(&mut self, delta: f32, game_handle: &RaylibHandle) {
        let mut position_move = Position::default();

        if game_handle.is_key_down(KeyboardKey::KEY_D) {
            position_move.x += self.speed * delta;
        }
        if game_handle.is_key_down(KeyboardKey::KEY_A) {
            position_move.x -= self.speed * delta;
        }
        if game_handle.is_key_down(KeyboardKey::KEY_W) {
            position_move.y -= self.speed * delta;
        }
        if game_handle.is_key_down(KeyboardKey::KEY_S) {
            position_move.y += self.speed * delta;
        }

        // if moved
        if position_move.x != 0.0 || position_move.y != 0.0 {
            let new_x = position_move.x + self.object.position.x;
            let new_y = position_move.y + self.object.position.y;

            if !(new_x < 0.0
                || new_x > (game_handle.get_screen_width() - self.object.size.width) as f32)
            {
                self.object.position.x = new_x;
            }
            if !(new_y < 0.0
                || new_y > (game_handle.get_screen_height() - self.object.size.height) as f32)
            {
                self.object.position.y = new_y;
            }

            if self.speed < PLAYERMAXSPEED {
                self.speed += PLAYERSPEEDGROWTH;
            }
        } else {
            self.speed = PLAYERSPEED;
        }
    }
}

fn draw_object(painter: &mut RaylibDrawHandle, object: &Object) {
    painter.draw_rectangle(
        object.position.x as i32,
        object.position.y as i32,
        object.size.width,
        object.size.height,
        object.color,
    );
}

fn main() {
    let (mut rl, thread) = raylib::init().size(640, 480).title("Test program").build();

    let mut player = Player::default();
    let mut goal_manager = GoalManager::default();

    goal_manager.add_goal(Goal {
        object: Object {
            position: Position {
                x: 100_f32,
                y: 100_f32,
            },
            size: Size {
                width: 10,
                height: 10,
            },
            color: Color::GREEN,
        },
        callback: || println!("You won!"),
        triggered: false,
        trigger_once: true,
    });

    while !rl.window_should_close() {
        let delta = rl.get_frame_time();
        player.update(delta, &rl);
        goal_manager.update(&player);

        let mut painter = rl.begin_drawing(&thread);
        painter.clear_background(Color::WHITE);
        painter.draw_fps(0, 0);

        draw_object(&mut painter, &player.object);

        for goal in &goal_manager.goals[..] {
            draw_object(&mut painter, &goal.object);
        }
    }
}
