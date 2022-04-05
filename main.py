from core.solver import Solver
from core.web_interface import WebInterface


def main():
    interface = WebInterface(headless=True)
    nb_letters, first_letter = interface.get_first_round()

    solver = Solver(nb_letters=nb_letters, first_letter=first_letter)

    while interface.round <= 6:
        print(solver)
        next_word = solver.get_prediction()
        print(f'[Round {interface.round}] Trying word : "{next_word}"')
        result = interface.get_result(next_word)

        if result["win?"]:
            print(f'Victory ! Word is "{next_word}"')
            break
        else:
            if len(result.keys()) == 1:
                # Word does not exist, remove it from dictionary
                solver.delete_word(next_word)
            else:
                # Word exists, delete wrong words from solver
                solver.delete_candidates(result)
    else:
        print(f"You lose")


if __name__ == "__main__":
    main()
