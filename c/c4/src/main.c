#include <stdbool.h>
#include <stdio.h>

typedef struct {
    char collum;
    char row;
} MoveTuple;

typedef struct {
    char player; // -1 or 1
    char board[6][7];
    char tops[6]; // what the current top of each collum is
    char moves; // how many moves have been made
    MoveTuple last_move;
} GameState;

GameState game_state_new() {
    GameState game = {
        .player = 1,
        .board = {
            {0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0},
            },
        .tops = {5, 5, 5, 5, 5, 5},
        .moves = 0,
        .last_move = {
            .collum = 0,
            .row = 0,
        }
    };
    return game;
}

const char DIAGONAL_MID_ALLIGN[7] = {3, 2, 1, 0, 1, 2, 3};

int sum(char *array[]) {
    int len = 4;
    int i;
    int sum;

    for (i = 0; i < len; ++i) {
        sum += *array[i];
    }

    return sum;
}

bool game_state_check_tie(GameState *game) {
    char same;
    int i;
    same = game->tops[0];
    for (i = 1; i < 6; ++i) {
        same = same ^ game->tops[i];
    }

    if (same != 0) {
        return false;
    }

    return game->tops[0] == -1;
}

// 0000000
// 0000000
// 0000000
// 0000000
// 000x000 (5,4) 4 diagonal 4 horizontal 0 vertical (only have to check below)
// 0000000

// 1112111 0 
// 1234321 1
// 1356531 2
// 1356531 3
// 1234321 4
// 1112111 5
//
// 0123456


// note to self: this is that pattern garbage with the 4 squares
// 0,0: +1,+1 * 3
// 0,1: +1,+1 * 3
// 0,2: +1,+1 * 3

// 0,3: +1,+1 * 3; -1,-1 * 3

// 1,0: +1,+1 * 3
// 1,1: -1,-1 +1,+1 * 2; +1,+1 * 3
// 1,2: 

bool game_state_check_won(GameState *game) {
    // need at least 7 moves to win
    if (game->moves < 7) {
        return false;
    }

    int i;
    int sum_test = 0;
    int sum_check = (game->player * 4) * -1;
    int sum_check_3 = sum_check + (game->player * -1);
    char last_player;

    if (game->player == 1) {
        last_player = -1;
    } else {
        last_player = 1;
    }

    // horizontals
    if (game->board[game->last_move.collum][3] == last_player) {
        for (i = 0; i < 4; ++i) {
            if (sum(&game->board[game->last_move.row] + (sizeof(char) * i)) == sum_check) {
                return true;
            }
        }
    }

    // diagonals
    sum_test = game->board[game->last_move.row][game->last_move.collum];

    int direction;
    if (game->last_move.collum > 2) {
        direction = -1;
    } else {
        direction = 1;
    }

    int y_offset = DIAGONAL_MID_ALLIGN[game->last_move.row] * direction;
    
    int mid = game->board[game->last_move.collum + y_offset][3];

    // verticals
    if (game->last_move.row > 2) {
        return false;
    }

    sum_test = 0;
    for (i = 0; i < 4; ++i) {
        sum_test += game->board[game->last_move.row][game->last_move.collum + i];
    }

    return sum_test == sum_check;
}

bool game_state_make_move(GameState *game, int collum) {
    // returns True or False if a move was valid
    if (!(0 <= collum <= 6)) {
        return false;
    }

    char collum_top = game->tops[collum];

    if (collum_top == -1) {
        return false;
    }

    game->board[collum_top][collum] = game->player;
    game->tops[collum] = collum_top - 1;
    game->moves += 1;
    game->last_move.collum = collum;
    game->last_move.row = collum_top;

    if (game->player == 1) {
        game->player = -1;
    } else {
        game->player = 1;
    }

    return true;
}

void game_state_debug_print_board(GameState *game) {
    char row;
    char collum;
    for (row = 0; row < 6; ++row) {
        printf("%d", game->board[row][0]);

        for (collum = 1; collum < 7; ++collum) {
            printf("%d", game->board[row][collum]);
        }

        printf("\n");
    }
}

int main() {
    GameState game = game_state_new();
    bool won = game_state_check_won(&game);
    printf("won: %d\n", won);

    game_state_make_move(&game, 3);
    game_state_debug_print_board(&game);
    return 0;
}