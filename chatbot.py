import random
import re

class SupportBot:
    negative_res = ("no", "nope", "na", "not a chance")
    exit_command = ("quit", "pause", "bye")

    def __init__(self):
        self.support_responses = {
            'ask_about_product': r'.*\bproduct\b.*',
            'technical_support': r'.*\btechnical\b.*\bsupport\b.*',
            'about_returns': r'.*\breturn.*policy\b.*',
            'general_query': r'.*\bhow\b.*\bhelp\b.*'
        }

    def greet(self):
        self.name = input("Hello! Welcome to our customer support. What's your name? ")
        will_help = input(f"{self.name}, how can I assist you today? ").lower()
        if will_help in self.negative_res:
            print("Alright, have a great day!")
            return
        self.chat()

    def make_exit(self, reply):
        for command in self.exit_command:
            if command in reply:
                print("Thanks for reaching out. Have a great day!")
                return True
        return False

    def chat(self):
        reply = input("Please tell your query: ").lower()
        while not self.make_exit(reply):
            reply = input(self.match_reply(reply).strip())

    def match_reply(self, reply):
        for intent, regex_pattern in self.support_responses.items():
            found_match = re.search(regex_pattern, reply)
            if found_match:
                if intent == 'ask_about_product':
                    return self.ask_about_product()
                elif intent == 'technical_support':
                    return self.technical_support()
                elif intent == 'about_returns':
                    return self.about_returns()
                elif intent == 'general_query':
                    return self.general_query()
        return self.no_match_intent()

    def ask_about_product(self):
        responses = (
            "You can find all product details on our website.",
            "You can contact us anytime at: 7899088565."
        )
        return random.choice(responses)

    def technical_support(self):
        responses = (
            "You can visit our technical support page for detailed assistance.",
            "We can assist you with technical issues. Don’t hesitate to call us."
        )
        return random.choice(responses)

    def about_returns(self):
        responses = (
            "We have a 30-day return policy.",
            "Please ensure that the product is in its original condition."
        )
        return random.choice(responses)

    def general_query(self):
        responses = (
            "I'm sorry, I didn't quite understand that. Can you please rephrase?",
            "My apologies, can you provide more details?"
        )
        return random.choice(responses)

    def no_match_intent(self):
        return "I'm sorry, I didn't understand that. Could you try rephrasing?"

bot = SupportBot()
bot.greet()
