# Guess game agent

This app allows you to simulate two people playing guessing game, where one 
person thinks of a topic and the other person tries to guess it by asking 20 
yes/no questions.

## Set up
pip install openai

Set environment variable OPENAI_API_KEY to your OpenAI API key.

## Run

### start the game

`python main.py --number_of_games 2 --result_path './game_results/game_1.json'`

The result will be stored under game_results in game_1.json file

### Evaluate the game result

`python evaluate.py --game_result_path ./game_results/game_1.json --evaluation_result ./evaluation_results/game_1_results.json`

The evaluation result will be stored under evaluation_results in game_1_results.json file


## Answering question from Assignment

### What main steps will there be?

Identify the class that's required for playing the game, so one guesser and one host.

### How will we get the agents to interact?

By pretending myself as the host to the guesser class, and the guesser class will ask me questions, 

Then I pretend my self as the guesser to the host class, and feed in the guesser question to the host class, then it  will answer the questions.

### What context does each agent have?

Host will have the context of the topic, the conversation history, and guesser will have the conversation history.

### What pieces could you keep static at first to simplify things?

The topic can be static at first, which make things simplified.

### Errors

The most common errors are likely the GPT doesn't return the json format, I have caught all of them, and return the error message.

### will you break up each player into multiple “sub-agents”?

I have breakdown the host to deal with `coming up with topic` and `answering questions`. This helps with get host to come up with more
possible topics without distract it from answering question.

## How can we reliably chain together the agent's “actions”?
Error catching and carefully prompting to ensure the agent respond with json format is the key to reliably chain the actions.

## Evaluation:

### How good are your agents at playing the game? How might we measure this?

I have built a evaluator to evaluate the performance of both host and guesser

### How often do things fail? What kind of failures are there?
It doesn't really fail in my case. But if anything fail, I guess it will fail at json parsing

## Testability:

### How can you organise different experiments?
I always think if we need to test different experiments, we need to have a evaluation framework, and the evaluator itself
is a good starting point I think. With this evaluator, we can be free to change the prompt and see if the performance improved or not.

### Can you parallelize to make experiments faster?
Of course, we can just keep spamming the game with different configuration, prompts. Obviously , if it's on a service, we need to make them all async, and parallelize them.

### How else can you make things more efficient and easy to use?
Build an UI will be much easier to use, and store the result into database will be better than storing in a json file.

## Where I get stuck
The initial issue with host is that it keep forgetting the topic it has, so I used an extra system prompt to make sure it remember the topic.

I also had issue with host always come out with the same topic, so I separated out the topic generation and answering question to make sure it can come up with different topics without distracting 
it from answering the question.

## What I can do with more time
There was a tool called langGraph which is perfect for defining subtask for one agent. I didn't get chance to use it this time, but would like to try in future.



