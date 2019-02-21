"""
This is a minimal contest submission file. You may also submit the full
hog.py from Project 1 as your contest entry.

Only this file will be submitted. Make sure to include any helper functions
from `hog.py` that you'll need here! For example, if you have a function to
calculate Free Bacon points, you should make sure it's added to this file
as well.

Don't forget: your strategy must be deterministic and pure.
"""

PLAYER_NAME = 'Love chips and coke' # Change this line!

def final_strategy(score, opponent_score):
    probility = [[0]*101]*101
    visited = [[0]*101]*101
    rolls = [[0]*101]*101
    num_count = [[0]*61]*11
    def search(s1, s2):
        if s1 >= 100:
            probility[100][s2] = 1
            visited[100][s2] = 1
            rolls[100][s2] = 1
            return 1
        if s2 >= 100:
            probility[s1][100] = 1
            visited[s1][100] = 1
            rolls[100][s2] = 1
            return 0
        if visited[s1][s2]:
            return probility[s1][s2]
        for roll in range(11):
            if roll == 0:
                new_s1 = s1 + free_bacon(s2)
                new_s2 = s2 + search_opponent(new_s1, s2)
                current_pro = search(new_s1, new_s2)
                if current_pro > probility[s1][s2]:
                    probility[s1][s2] = current_pro
                    rolls[s1][s2] = roll
            else:
                pro = 0
                for increasement in (roll, roll*6+1):
                    new_s1 = s1 + increasement
                    new_s2 = search_opponent(new_s1, s2)
                    pro += search(new_s1, new_s2) *  num_count[roll][increasement]
                pro /= 6 ** roll
                if pro > probility[s1][s2]:
                    probility[s1][s2] = pro
                    rolls[s1][s2] = roll
        return probility[s1][s2]
    def search_opponent(s1, s2):
        if visited[s2][s1]:
            return rolls[s2][s1]
        search(s2, s1)
        return rolls[s2][s1]
    def counting_num():
        num_count[0][0] = 1
        print("0000", num_count[0][0])
        for i in range(1, 11):
            for j in range(i * 6 + 1):
                num_count[i][j] = 0
                if j >= i:
                    for k in range(max(0, j-6), j):
                        print(i,j,k,num_count[i-1][k])
                        num_count[i][j] += num_count[i-1][k]
                print(num_count[i][j])
    counting_num()
    for i in range(11):
        for j in range(i*6+1):
            print(i, j, num_count[i][j])
    for i in range(101):
        for j in range(101):
            if not visited[i][j]:
                search(i, j)
    return rolls[score][opponent_score]

def is_swap(player_score, opponent_score):
    """
    Return whether the two scores should be swapped
    """
    result = False
    while player_score and opponent_score:
        if player_score % 10 == opponent_score % 10:
            result = True
            break
        player_score //= 10
        opponent_score //= 10
    return result

def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    points = min(score % 10, score // 10) + 1
    return points
