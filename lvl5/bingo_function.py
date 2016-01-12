import random

GAME_LIMIT = 1, 50


def bingo():
    print("\nB.I.N.G.O. Félicitations!")


def user_response():
    message = "\nDonne moi un nombre entre " + str(GAME_LIMIT[0]) + " et " + str(GAME_LIMIT[1]) + ": "
    response = input(message)

    response = int(response)
    return response


def verification(response, good_response, name):
    if response < good_response:
        print("\nRaté " + name + ", le bon nombre est plus grand.")
    elif response > good_response:
        print("\nNon! La bonne réponse est plus petite.")
    return response == good_response


def main():
    # demander le nom du joueur
    player_name = input("Quel est ton nom: ")

    play = True

    # equivalent : while play == True
    while play:

        # initialisation des variables de jeu
        good_response = random.randint(GAME_LIMIT[0], GAME_LIMIT[1])
        response_ok = False
        counter = 0

        while not response_ok:
            # equivalent: counter = counter + 1
            counter += 1
            player_response = user_response()
            response_ok = verification(player_response, good_response, player_name)

        bingo()
        print("Il t'a fallut " + str(counter) + " coups pour deviner le bon nombre.")

        again = input("\n" + player_name + " ,veux-tu encore joueur? (O/N): ")
        play = again in ('o', 'O')


if __name__ == '__main__':
    main()
