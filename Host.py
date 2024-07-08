import ast

import openai


HOST_SYSTEM_PROMPT_TEMPLATE = (
    "You are currently in a game with me of guessing topic within 20 questions. "
    "You are the host and I am the guesser. "
    "You are trying to make me guess what object or living things (we call it topic) you are thinking of by providing me with the information about the topic. "
    "I will ask you yes/no questions to guess the topic. "
    "You should answer my questions with 'yes', 'no' \n\n"
    
    "After the first turn, you should start to only provide response in a json format with the following structure: \n"
    "{\n"
    "  'answer': 'answer to the question I asked (yes or no)\n"
    "  'correct_guess': 'true' if I guessed the topic correctly, 'false' if I did not guess the topic correctly \n"
    "}\n"

)

GENERATE_TOPIC_PROMPT_TEMPLATE = (
    "I want to play a game for guessing the topic within 20 questions. and your job is to provide me with the topic as an answer."
    "Please  provide me with the topic to play the game, think about all the living things or objects. There are different kinds of animal, pets, birds, fruits, vegetables, etc. "
    "For example, Cats, Apples, Oranges, White house, Water bottle, car, chair, kangaroo, whales etc."
    "Remember only provide specific object or living things as the topic. Not the general topic like 'animal', 'fruit', 'vegetable'."
    "Please just response with the topic you suggest of without any extra information. "
)



class Host:

    # Constructor to initialise Host with openai api key
    def __init__(
            self,
            api_key,
            model_config
    ):
        self.topic = None
        self.client = openai.Client(
            api_key=api_key,
        )
        self.chat_history = []
        self.model_config = model_config
        self.chat_history = [
            {
                "role": "system",
                "content": HOST_SYSTEM_PROMPT_TEMPLATE,
            }
        ]

    def generate_topic(self, override_model_config=None):
        messages = [
            {
                "role": "system",
                "content": GENERATE_TOPIC_PROMPT_TEMPLATE,
            },
            {
                "role": "user",
                "content": "You can start to think of the topic",
            }
        ]
        if override_model_config:
            model_config = override_model_config
        else:
            model_config = self.model_config
        response = self.client.chat.completions.create(
            **model_config,
            messages=messages,
        )

        topic = response.choices[0].message.content
        if topic:
            self.topic = topic
            return topic
        else:
            raise Exception("Model failed to generate topic, aborting the game")

    def answer(self, user_guess, override_model_config=None):
        self.chat_history.append({'role': 'user', 'content': user_guess})
        messages = self.chat_history.copy()
        messages.append({
            'role': 'system',
            'content': f"Remember the topic you have in mind is {self.topic} "
                       f"I asked a question: {user_guess}"
                       f"Remember firstly think if the answer is yes or no, "
                       f"Then think if I have guessed the topic correctly or not, "
                       f"you should always provide response in a json format"
        })
        if override_model_config:
            model_config = override_model_config
        else:
            model_config = self.model_config
        response = self.client.chat.completions.create(
            **model_config,
            messages=messages,
        )

        answer = response.choices[0].message.content
        try:
            json_response = ast.literal_eval(answer)
            answer = json_response['answer']
            correct_guess = json_response.get('correct_guess')
        except Exception as e:
            answer = "Something went wrong on my side, can you ask your question again"
            correct_guess = False
        self.chat_history.append({'role': 'assistant', 'content': answer})
        return answer, correct_guess
