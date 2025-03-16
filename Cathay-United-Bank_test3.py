n = int(input("請輸入人數 n: "))
k = 3

def Total(n, k):
    people = list(range(1, n + 1))
    number = 0

    while len(people) > 1:
        number = (number + k - 1) % len(people)
        people.pop(number)
    return people[0]

last = Total(n, k)

print(f"最後留下的同事是第 {last} 順位。")