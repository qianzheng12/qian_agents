"""
    This script is used to evaluate the game results using the OpenAI API.

    Usage:
    python evaluate.py --game_result_path ./game_results/game_1.json --evaluation_result ./evaluation_results/game_1_results.json

    Args:
    --game_result_path: str: path to the game result file
    --evaluation_result_path: str: path to the evaluation results file you want to store

"""
import argparse
import json
import os

from Evaluator import Evaluator


def evaluate(game_result_path: str):
    open_ai_api_key = os.getenv("OPENAI_API_KEY")
    evaluator = Evaluator(
        api_key=open_ai_api_key,
        model_config={
            "model": "gpt-4",
            "temperature": 0,
            "top_p": 1
        }
    )

    with open(game_result_path, 'r') as f:
        game_conversations = json.load(f)
    evaluation_results = []
    for conversation in game_conversations:
        evaluation_result = evaluator.evaluate(conversation)
        evaluation_results.append({
            "evaluation": evaluation_result,
            "conversation": conversation
        })

    return evaluation_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game_result_path", type=str,
        help="path to the game result file",
        required=True
    )
    parser.add_argument(
        "--evaluation_result_path", type=str,
        help="path to the evaluation results file you want to store",
        required=True
    )

    args = parser.parse_args()

    evaluation_results = evaluate(args.game_result_path)

    with open(args.evaluation_result_path, 'w') as f:
        json.dump(evaluation_results, f)
