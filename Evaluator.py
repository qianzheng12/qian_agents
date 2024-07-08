import ast

import openai

HOST_EVALUATE_PROMPT = (
    "You are a evaluator for the game of guessing topic within 20 questions. \n"
    "You job is to evaluate if the host performing well or not \n"
    "You should evaluate the host using the following scoring system: \n"
    "1 (Terrible) - For instance, the host keep providing wrong answer to the guesser"
    "2 (Good) - For instance, the host providing all the answer correctly to the guesser, might missed one, or didn't tell guesser it guessed correctly\n"
    "3 (Perfect) - For instance, the host provided all the answer correctly and told the guesser it guessed the answer correctly\n"
    "Here is the conversation between the host and the guesser: \n"
    "{game_conversations}\n"
    "Please return your evaluation in the following json format: "
    "{{\n"
    "  'score': 'score',\n"
    "  'comment': 'Your comment here'\n"
    "}}\n"
)

GUESSER_EVALUATE_PROMPT = (
    "You are a evaluator for the game of guessing topic within 20 questions. \n"
    "You job is to evaluate if the guesser performing well or not \n"
    "You should evaluate the guesser using the following scoring system: \n"
    "1 (Terrible) - The guesser keep asking same question or keep guessing the topic without narrowing down the range of topics\n"
    "2 (Good) - The guesser asking the question smartly, and try to narrow down the range of topics\n however didn't guess the topic correctly\n"
    "3 (Perfect) -  The guesser asking the question smartly, and try to narrow down the range of topics and guessed the topic correctly\n"
    "Here is the conversation between the host and the guesser: \n"
    "{game_conversations}\n"
    "Please return your evaluation in the following json format: \n"
    "{{\n"
    "  'score': 'score',\n"
    "  'comment': 'Your comment here'\n"
    "}}\n"
)



class Evaluator:
    def __init__(
            self,
            api_key,
            model_config,

    ):
        self.client = openai.Client(
            api_key=api_key,
        )
        self.chat_history = []
        self.model_config = model_config

    def evaluate_host(self, game_conversations):
        self.chat_history = [
            {
                "role": "system",
                "content": HOST_EVALUATE_PROMPT.format(game_conversations=game_conversations),
            },
            {
                "role": "user",
                'content': 'You can start to evaluate the host now'
            }
        ]
        response = self.client.chat.completions.create(
            **self.model_config,
            messages=self.chat_history,
        )
        evaluation = response.choices[0].message.content
        try:
            evaluation = ast.literal_eval(evaluation)
        except Exception as e:
            raise('gpt did not return correct format')

        return evaluation

    def evaluate_guesser(self, game_conversations):
        self.chat_history = [
            {
                "role": "system",
                "content": GUESSER_EVALUATE_PROMPT.format(game_conversations=game_conversations),
            },
            {
                "role": "user",
                'content': 'You can start to evaluate the host now'
            }
        ]
        response = self.client.chat.completions.create(
            **self.model_config,
            messages=self.chat_history,
        )
        evaluation = response.choices[0].message.content
        try:
            evaluation = ast.literal_eval(evaluation)
        except Exception as e:
            raise('gpt did not return correct format')

        return evaluation

    def evaluate(self, game_conversations):
        host_evaluation = self.evaluate_host(game_conversations)
        guesser_evaluation = self.evaluate_guesser(game_conversations)

        return {
            "host_evaluation_result": host_evaluation,
            "guesser_evaluation_result":guesser_evaluation
        }
