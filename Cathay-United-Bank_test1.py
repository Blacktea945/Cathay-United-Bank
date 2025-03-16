wrong_scores = []
while True:
    user_input = int(input("請輸入成績(輸入 0 結束): "))
    if user_input == 0:
        break
    else:
        wrong_scores.append(user_input)
print("您輸入的成績: ", wrong_scores)

corrected_scores = []
for score in wrong_scores:
    corrected_scores.append(int(str(score)[::-1]))
print("修正後的成績: ", corrected_scores)
