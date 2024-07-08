import json
import os

from Guesser import Guesser
from Host import Host


def main():
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
        "question": "You can start to think of the topic",
        "answer": answer,
    })
    count = 0
    while correct_guess != 'true':
        if count == 21:
            guesser_win_the_game = False
            break
        user_guess = guesser.guess(answer)
        answer, correct_guess = host.answer(user_guess)
        conversations.append({
            "question": user_guess,
            "answer": answer,
            "correct_guess": correct_guess,
        })
        count += 1
    result = {
        "topic": topic,
        "guesser_win_the_game": guesser_win_the_game,
        "conversations": conversations
    }
    with open("conversation.json", "w") as file:
        json.dump(result, file, indent=4)


if __name__ == "__main__":

    # Read the number of game to run from args
    args = sys.argv

    main()