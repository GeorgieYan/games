#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int row, column = 9;
int choice;
int mine_number = 10;

int main(){
    while (1){
        choice = menu();
        if(choice == 0){
            game();
        }

        else if(choice == 1){
            printf("Game over! \n");
            break;
        }
        else{
            printf("Invalid input, please enter again XD\n");
        }
    }
    return 0;
}

void menu(){
    printf("0 represents mines, * represents unknown coordinates, have fun! \n");
    printf("Enter 0 to play, 1 to exit: \n");
    scanf("%d", &choice);
    int i = choice;
    return i;
}

void game(){
    int i, j;
    int mine_plant = mine_number;
    int cleared_grid, mine_count = 0;
    char map[row][column];
    char mine_planted[row][column];

    for(i = 0; i < row; i++){
        for(j = 0; j < column; j++){
            map[i][j] = '*';
        }
    }

    for(i = 0; i < row; i++){
        for(j = 0; j < column; j++){
            mine_planted[i][j] = '0';
        }
    }

    srand(time(NULL));
    while(mine_number > 0){
        i = rand() % row;
        j = rand() % column;
        while(mine_planted[i][j] == 'M'){
            i = rand() % row;
            j = rand() % column;
        }

        mine_planted[i][j] = 'M';
        mine_number --;
    }

    for(i = 0; i < row; i++){
        for(j = 0; j < column; j++){
            if(mine_planted[i][j] == 'M'){
                continue;
            }
            else{
                if(i - 1 >= 0 && j - 1 >= 0 && mine_planted[i - 1][j - 1] == 'M'){
                    mine_count++;
                }

                if(i - 1 >= 0 && mine_planted[i - 1][j] == 'M'){
                    mine_count++;
                }

                if(i - 1 >= 0 && j + 1 < column && mine_planted[i - 1][j + 1] == 'M'){
                    mine_count++;
                }

                if(j - 1 >= 0 && mine_planted[i][j - 1] == 'M'){
                    mine_count++;
                }

                if(j + 1 < column && mine_planted[i][j + 1] == 'M'){
                    mine_count++;
                }

                if(i + 1 < row && j - 1 >= 0 && mine_planted[i + 1][j - 1] == 'M'){
                    mine_count++;
                }

                if(i + 1 < row && mine_planted[i + 1][j] == 'M'){
                    mine_count++;
                }

                if(i + 1 < row && j + 1 < column && mine_planted[i + 1][j + 1] == 'M'){
                    mine_count++;
                }

                mine_planted[i][j] = mine_count;
            }
        }
    }

    while(1){
        for(i = 0; i < row; i++){
            for(j = 0; j < column; j++){
                printf("%c ", map[i][j]);
            }
            printf("\n");
        }

        printf("Please enter a coordinate: ");
        scanf("%d %d", &i, &j);

        if(mine_planted[i][j] == 'M'){
            for(i = 0; i < row; i++){
                for(j = 0; j < column; j++){
                    printf("%c ", mine_planted[i][j]);
                }
                printf("\n");
            }
            printf("Game over, nice try! \n");
            break;
        }

        cleared_grid++;

        if(cleared_grid == row*column - mine_number){
            printf("Congrats, you won!\n");
            break;
        }
        else{
            map[i][j] = mine_planted[i][j];
        }
    }
}


