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
    probility = [[0 for column in range(101)]for row in range(101)]
    visited = [[0 for column in range(101)]for row in range(101)]
    rolls = [[0 for column in range(101)] for row in range(101)]
    num_count = [[0 for column in range(61)] for row in range(11)]
    def search(s1, s2):
        # 有分数为100以上的时候
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
        # 如果有访问过
        if visited[s1][s2]:
            return probility[s1][s2]
        # 从投0-10
        for roll in range(11):
            # 投0的情况
            if roll == 0:
                # 分别获取双方的投的数量，然后search获取这个情况下的概率
                new_s1 = s1 + free_bacon(s2)
                new_s2 = s2 + search_opponent(new_s1, s2)
                current_pro = search(new_s1, new_s2)
                #对比概率大小，因为pro初始是0，这个其实会覆盖的
                if current_pro > probility[s1][s2]:
                    probility[s1][s2] = current_pro
                    rolls[s1][s2] = roll
            else:
                #不是投0的情况， pro是概率之和
                pro = 0
                #投的可能值是roll-roll*6
                for increasement in range(roll, roll*6+1):
                    new_s1 = s1 + increasement
                    #单纯的优化，如果新的值上100，剩下投出来的值都上100，可以直接计算，概率为1
                    if new_s1 >= 100:
                        for j in range(increasement, roll*6+1):
                            pro += num_count[roll][j]
                        break
                    #一般情况，值颗没上100，搜索对方的新的值
                    new_s2 = s2 + search_opponent(new_s1, s2)
                    pro += search(new_s1, new_s2) *  num_count[roll][increasement]
                #算一个总体概率
                pro /= 6 ** roll
                #如果概率大，覆盖
                if pro > probility[s1][s2]:
                    probility[s1][s2] = pro
                    rolls[s1][s2] = roll
        return probility[s1][s2]
    #用于搜索对手的值
    def search_opponent(s1, s2):
        if s1 >= 100:
            return 0
        if visited[s2][s1]:
            return rolls[s2][s1]
        #对对方的投的值搜索
        search(s2, s1)
        return rolls[s2][s1]
    def counting_num():
        num_count[0][0] = 1
        for i in range(1, 11):
            for j in range(i * 6 + 1):
                num_count[i][j] = 0
                if j >= i:
                    for k in range(max(0, j-6), j):
                        num_count[i][j] += num_count[i-1][k]
    counting_num()
    #从后往前遍历search
    for i in range(200, 1, -1):
        for j in range(max(0, i-100), min(101,i+1)):
            if not visited[i-j][j]:
                search(i-j, j)
    """
    for i in range(101):
        for j in range(101):
            if not visited[i][j]:
                search(i, j)
    """
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
