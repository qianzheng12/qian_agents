import openai

GUESSER_SYSTEM_PROMPT_TEMPLATE = (
    "You are currently in a game with me of guessing topic within 20 questions. "
    "You are trying to guess what object or living things (we call it topic) the I am thinking of by asking yes/no questions. "
    "I will answer your questions with 'yes', 'no' \n\n"
    "You should try to ask me questions smartly, instead of keep guessing the specific topic, but try to ask the question to narrow down the range of topics "
    "You should just response with the question you want to ask next without any explanation."
)


class Guesser:

    # Constructor to initialise Guess with openai api key
    def __init__(
            self,
            api_key,
            model_config
    ):
        self.client = openai.Client(
            api_key=api_key,
        )
        self.chat_history = []
        self.model_config = model_config
        self.chat_history = [
            {
                "role": "system",
                "content": GUESSER_SYSTEM_PROMPT_TEMPLATE,
            }
        ]

    def guess(self, host_answer):
        self.chat_history.append({'role': 'user', 'content': host_answer})
        response = self.client.chat.completions.create(
            **self.model_config,
            messages=self.chat_history,
        )
        guess = response.choices[0].message.content
        if not guess:
            guess = "I am sorry, I was not paying attention, can you repeat the question"

        self.chat_history.append({'role': 'assistant', 'content': guess})
        return guess
