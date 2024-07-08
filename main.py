"""
    Main file to run the game

    Command:
    python main.py --number_of_games 2 --result_path './game_results/test.json'

    Args:
    --number_of_games: int: how many number of games you want agents to play
    --result_path: str: the path of the result file to be saved

"""
import argparse
import json
import os

from Guesser import Guesser
from Host import Host


def game():
    open_ai_api_key = os.getenv("OPENAI_API_KEY")

    host = Host(
        api_key=open_ai_api_key,
        model_config={
            "model": "gpt-4",
            "temperature": 0,
            "top_p": 1
        }
    )

    guesser = Guesser(
        api_key=open_ai_api_key,
        model_config={
            "model": "gpt-4",
            "temperature": 0,
            "top_p": 1
        }
    )
    guesser_win_the_game = True
    correct_guess = False
    conversations = []
    topic = host.generate_topic(
        override_model_config={
            "model": "gpt-4",
            "temperature": 1,
            "top_p": 1
        }
    )
    answer = "I have thought of the topic"
    conversations.append({
        "host": "You can start to think of the topic",
        "guesser": answer,
    })
    count = 0
    while correct_guess != 'true':
        if count == 21:
            guesser_win_the_game = False
            break
        user_guess = guesser.guess(answer)
        answer, correct_guess = host.answer(user_guess)
        conversations.append({
            "host": user_guess,
            "guesser": answer,
            "correct_guess": correct_guess,
        })
        count += 1
    result = {
        "topic": topic,
        "guesser_win_the_game": guesser_win_the_game,
        "conversations": conversations
    }

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--number_of_games", type=int,
        help="how many number of games you want agents to play",
        required=True
    )
    parser.add_argument(
        "--result_path", type=str,
        help="the path of the result file to be saved",
        required=True
    )

    args = parser.parse_args()

    result_path = args.result_path
    game_results = []

    for _ in range(args.number_of_games):
        result = game()
        game_results.append(result)

    with open(args.result_path, "w") as f:
        json.dump(game_results, f)