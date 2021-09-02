import random

count = random.randint(1, 5)
explosion = 0


def game():
    number = 0
    if explosion != 2:
        hod = input("Вы двигаетесь дальше? Отвечайте да или нет ")
        if hod == "Да" or 'да':
            if count == 1 or count == 5:  # 1 и 5 мины
                print("Число ячейки", count)
                print("Танк поврежден!")
                hod = input("Ваш танк поврежден, хотите двигаться дальше? Отвечайте только да или нет ")
                number += 1
                if hod == "Да":
                    number += 1

            else:
                number += 1  # 2 3 4 не мины
                print("Число ячейки", count)
                print("Вы успешно прошли дальше. Хотите двигаться вперед? Вы уже прошли", number,
                      " ходов. Отвечайте да или нет?")
                print(hod)
                if hod == "Да":
                    if count == 1 or count == 5:
                        print("Число ячейки", count)
                        print("Танк поврежден!")
                        hod = input("Ваш танк поврежден, хотите двигаться дальше? Отвечайте только да или нет ")
                        number += 1
                    else:
                        number += 1  # 2 3 4 не мины
                        print("Число ячейки", count)
                        print("Вы успешно прошли дальше. Хотите двигаться вперед? Вы уже прошли", number,
                              " ходов. Отвечайте да или нет?")
                        print(hod)
                    # if hod == "Да":
        else:
            print("Вы дошли до ", number, " ячейки. На этом игра окончена")
game()