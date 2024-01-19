import json
import time
import os
from typing import List
import csv

from dotenv import load_dotenv
import openai
import google.generativeai as genai

load_dotenv()

instruction = """
Instructions:

You are a llm-decision-making-contest robot. You will receive a message from the user and decide which method to use based on the user's intention. You will return only an integer that corresponds to that method, and nothing else. Do not answer any questions, do not output anything besides a single integer, no special characters. Do not engage in conversation. The methods are described as follows:

(1) news: a message containing news from another company, a newsletter or a news website.

(2) product report: a message detailing metrics, errors, and alerts from cloud applications

(3) conversation: any message that represents a question or an answer based on a previous email

(4) others: any other message that is not represented above

User message:

"""

text = """
Hello AI enthusiast,

Welcome back to WhatTheAI, your weekly dose of all things artificial intelligence. Ready to explore the latest and greatest in the AI realm this week? Buckle up, because we're gearing up for an exciting journey!

🚀 Get ready to be amazed as we unveil our spotlight tool of the week. Let the AI adventure begin!
"""


class GoogleGemini:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        self.model_name = "gemini"

    def chat_completion(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except ValueError:
            return "Error"
        except Exception as e:
            return f"Error: {e}"


class OpenAIGPT:
    def __init__(self, model: str):
        gpt_3 = "gpt-3.5-turbo-1106"
        gpt_4 = "gpt-4-1106-preview"
        self.model_name = gpt_3 if "gpt-3" in model else gpt_4
        self.client = openai.OpenAI()

    def chat_completion(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt}
                ]
            )
            completion_text = response.choices[0].message.content
            return completion_text
        except Exception as e:
            print(f"Error: {e}")


class LLM:
    def __init__(self, model: str):
        self.model = GoogleGemini() if model == "gemini" else OpenAIGPT(model=model)
        self.score = 0
        self.model_name = self.model.model_name
        self.last_score = 0
        self.answer = ""


def is_not_integer(text: str):
    """ Test if the text cannot be cast as an integer and returns True """
    try:
        _ = int(text) + 1
        return False
    except ValueError:
        return True


def score_answer(answer, ground_truth) -> int:
    """ Gives score based on the ground truth.
        - +1 -> right
        - 0  -> wrong
        - -1 -> gave error or anything other than a single number"""
    if is_not_integer(answer):
        return -1
    if int(answer) == ground_truth:
        return 1
    else:
        return 0


def load_data():
    try:
        # Load JSON data
        data_path = "data.json"
        with open(data_path, 'r') as file:
            json_data = json.load(file)

        return json_data

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def save_result_as_csv(result_data):
    # Specify the file path
    csv_file_path = 'output.csv'

    # Get the header from the first dictionary
    header = list(result_data[0].keys())

    # Write to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)

        # Write the header
        writer.writeheader()

        # Write the data
        writer.writerows(result_data)


def print_score(model_name, model_score, answer, ground_truth, text):
    text_short = text if len(text) <= 17 else text[:17] + "..."
    print(f"""{model_name}: {model_score}
    (Answer given:{answer}| ground truth:{ground_truth}| text: {text_short})""")


def run_test(models: List[LLM], data: dict, store_csv: bool = True):

    result_data = []

    for row in data:
        for model in models:
            model.answer = model.model.chat_completion(prompt=instruction + row.get("text"))
            model.last_score = score_answer(answer=model.answer, ground_truth=row.get("answer"))
            model.score += model.last_score
            print_score(model_name=model.model_name, model_score=model.last_score, answer=model.answer,
                        ground_truth=row.get("answer"), text=row.get("text"))

            # Sleep for five seconds to avoid over-calling the API
            time.sleep(5)

        # Append data to store it as .csv later on
        if store_csv:
            result_data.append({
                'answer': row.get('answer'),
                'text': row.get('text'),
                'gemini': models[0].last_score,
                'gpt-3': models[1].last_score,
                'gpt-4': models[2].last_score,
                'gemini-answer': models[0].answer,
                'gpt-3-answer': models[1].answer,
                'gpt-4-answer': models[2].answer
            })

    print(f"""
    Round one -------
        Gemini: {models[0].score}
        GPT-3: {models[1].score}
        GPT-4: {models[2].score}
    """)

    if store_csv:
        save_result_as_csv(result_data)


if __name__ == "__main__":
    gemini = LLM(model="gemini")
    gpt3 = LLM(model="gpt-3.5-turbo")
    gpt4 = LLM(model="gpt-4.5-turbo")

    # If the order is changed here, it needs to be changed in lines 166, 167, 168, 176, 177 and 178
    models = [gemini, gpt3, gpt4]

    data = load_data()

    run_test(models=models, data=data, store_csv=False)




