# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted

class ActionDefaultFallback(Action):

    def name(self) -> str:
        return "action_default_fallback"

    async def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Sorry, I didn't understand that. Can you please rephrase?")
        return [UserUtteranceReverted()]

# class Action_Rating(Action):
#     def name(self) -> Text:
#         return "action_rating"

#     def run(self, dispatcher: CollectingDispatcher,
#                 tracker: Tracker,
#                 domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
#                 from yattag import Doc

#                 doc, tag, text, line = Doc().ttl()

#                 with tag('html'):
#                     with tag('body'): 
#                         with tag('style', type='text/css'):
#                             doc.stag('label {font-size: 5vw}')
#                             # doc.stag('link',rel="stylesheet",href="style.css")
#                 line('h1', 'Feedback')
#                 with tag('form', action = ""):
#                     line('p', 'Please select')
#                     for label in ('5', '4', '3', '2', '1'):
#                         doc.input(name = 'rate', type = 'radio', value = label)
#                         text("☆")
#                     doc.stag('input', type = 'submit', value = 'submit')
#                 dispatcher.utter_message(text=doc.getvalue())