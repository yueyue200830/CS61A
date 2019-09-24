#include <bits/stdc++.h>

using namespace std;
using namespace chrono;

int c=0;
double probility[101][101]={0};
int visited[101][101]={0};
int rolls[101][101]={0};
int num_count[61][11]={0};

int final_strategy(int score, int opponent_score);
void get_strategy();
double Search(int s1, int s2);
int search_opponent(int s1, int s2);
void counting_num();
int free_bacon(int score);

int main()
{
    auto start = system_clock::now();
    cout << final_strategy(0, 0) << endl;
    for (int i = 0; i <=100; i++){
        for (int j = 0; j<= 100; j++){
            //cout<<i<<","<<j<<","<<rolls[i][j]<<","<<probility[i][j]<<endl;
        }
    }
    auto end   = system_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    cout <<  "»¨·ÑÁË"
         << double(duration.count()) * microseconds::period::num / microseconds::period::den
         << "Ãë" << endl;
    return 0;
}


int final_strategy(int score, int opponent_score){
    if(score == 0){
        get_strategy();
    }
    return rolls[score][opponent_score];
}

void get_strategy(){
    counting_num();
    for (int i = 200; i >= 2; i--) {
        for (int j = max(0, i-100); j < min(101, i+1); j++) {
            //cout << i-j<<","<<j<<endl;
            c = 0;
            if (!visited[i-j][j]) {
                Search(i-j, j);
            }
            //cout<<"c                "<<c<<endl;
        }
    }
}

 double Search(int s1, int s2){
      //printf("%d %d %d\n", c, s1, s2);
      //c++;
        if (s1 >= 100){
            probility[100][s2] = 1;
            visited[100][s2] = 1;
            rolls[100][s2] = 1;
            return 1;
        }
        if (s2 >= 100) {
            probility[s1][100] = 1;
            visited[s1][100] = 1;
            rolls[100][s2] = 1;
            return 0;
        }
        if (visited[s1][s2])
            return probility[s1][s2];
        visited[s1][s2] = 1;
        for (int roll = 0; roll <= 10; roll++) {
            if (roll == 0){
                int new_s1 = s1 + free_bacon(s2);
                /*
                int new_s2 = s2 + search_opponent(new_s1, s2);
                double current_pro = Search(new_s1, new_s2);
                */
                int roll2 = search_opponent(new_s1, s2);
                double pro2 = 0;
                if (roll2 == 0) {
                    pro2 = Search(new_s1, s2+free_bacon(new_s1));
                } else {
                    for (int inc = roll2; inc <= roll2*6; inc++) {
                        pro2 += Search(new_s1, s2+inc) * num_count[roll2][inc];
                    }
                    pro2 /= pow(6.0, double(roll2));
                }
                //cout << "roll0"<<s1<<","<<s2<<","<<new_s1<<","<<new_s2<<","<<current_pro<<endl;
                if (pro2 > probility[s1][s2]) {
                    probility[s1][s2] = pro2;
                    rolls[s1][s2] = roll;
                }
            } else {
                double pro = 0;
                //cout << s1 << ","<<s2<<endl;
                for (int increasement = roll; increasement <= roll * 6; increasement++) {
                    int new_s1 = s1 + increasement;
                    /*
                    if (new_s1 >= 100){
                        for (int j = increasement; j <= roll*6; j++)
                            pro += num_count[roll][j];
                        break;
                    }*/
                    int roll2 = search_opponent(new_s1, s2);
                    //cout << s1<<","<<s2<<","<<new_s1<<","<<roll2<<endl;
                    double pro2 = 0;
                    if (roll2 == 0) {
                        pro2 = Search(new_s1, s2+free_bacon(new_s1));
                        //cout << s1<<","<<s2<<","<<new_s1<<","<<free_bacon(new_s1) <<"," <<pro2<<endl;
                    } else {
                        for (int inc = roll2; inc <= roll2*6; inc++) {
                            //cout <<s1<<","<<s2<<","<< new_s1 << ","<<s2+inc<<endl;
                            pro2 += Search(new_s1, s2+inc) * num_count[roll2][inc];
                        }
                        pro2 /= pow(6.0, double(roll2));
                    }
                    //int new_s2 = s2 + search_opponent(new_s1, s2);
                    //cout << s1 <<","<<s2 <<","<<new_s1 <<","<<new_s2<<endl;
                    //cout <<s1<<","<<s2<<","<<pro2<<endl;
                    pro += pro2 * double(num_count[roll][increasement]);
                    //cout << pro2<<","<<pro<<endl;
                    //cout << pro <<",";
                }
                //cout <<pro<<",";
                pro /= pow(6.0, double(roll));
                //cout <<roll << "," << pro<<endl;
                if (pro > probility[s1][s2]) {
                    probility[s1][s2] = pro;
                    rolls[s1][s2] = roll;
                }
                //cout << roll << ","<<pro<<","<<probility[s1][s2]<<endl;
            }
        }
        return probility[s1][s2];
 }

 int search_opponent(int s1, int s2) {
        if (s1 >= 100)
            return 0;
        if (visited[s2][s1]) {
            return rolls[s2][s1];
        }
        Search(s2, s1);
        return rolls[s2][s1];
 }

 void counting_num(){
        num_count[0][0] = 1;
        for (int i = 1; i <= 10; i++) {
            for (int j = 0; j <= i*6; j++) {
                num_count[i][j] = 0;
                if (j >= i) {
                    for (int k = max(0, j-6); k < j; k++)
                        num_count[i][j] += num_count[i-1][k];
                }
            }
        }
 }

 /*
def is_swap(player_score, opponent_score):
    result = False
    while player_score and opponent_score:
        if player_score % 10 == opponent_score % 10:
            result = True
            break
        player_score //= 10
        opponent_score //= 10
    return result
*/

int free_bacon(int score) {
    int points = min(score % 10, score / 10) + 1;
    return points;
}
