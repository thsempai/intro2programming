import random

GAME_LIMIT = 1, 50


def main():
    # demander le nom du joueur
    player_name = input("Quel est ton nom: ")

    play = True

    # equivalent : while play == True
    while play:

        # initialisation des variables de jeu
        good_response = random.randint(GAME_LIMIT[0], GAME_LIMIT[1])
        player_response = 0
        counter = 0

        while player_response != good_response:
            # equivalent: counter = counter + 1
            counter += 1

            message = "\nDonne moi un nombre entre " + str(GAME_LIMIT[0]) + " et " + str(GAME_LIMIT[1]) + ": "
            player_response = input(message)

            player_response = int(player_response)

            if player_response < good_response:
                print("\nRaté " + player_name + ", le bon nombre est plus grand.")
            elif player_response > good_response:
                print("\nNon! La bonne réponse est plus petite.")

        print("\nB.I.N.G.O. Félicitations!")
        print("Il t'a fallut " + str(counter) + " coups pour deviner le bon nombre.")

        again = input("\n" + player_name + " ,veux-tu encore joueur? (O/N): ")
        play = again in ('o', 'O')


if __name__ == '__main__':
    main()
