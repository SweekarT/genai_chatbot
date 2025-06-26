from dataframe_agent import db_fn
from no_db_response import no_db_fn
from inference import recommendation
from database_operation import inference_ip

from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI
from openai import AzureOpenAI

import json


endpoint = "https://aihub2565181539.openai.azure.com/"
model_name = "gpt-4o"
deployment = "gpt-4o"

subscription_key = "CnrQXBv16oAlU7kXdE8lXbeKVRlytn8bg55ae4fFm2wUjpz432FLJQQJ99BEAC77bzfXJ3w3AAAAACOG2x9F"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

def fn_call(user_input):
        messages = [
            {"role": "user",
             "content": user_input
             }
        ]

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "db_fn",
                    "description": "Queries the database for specific information and answers the user question",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_input": {
                                "type": "string",
                                "description": "user's question"
                            }
                        },
                        "required": ["user_input"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "no_db_fn",
                    "description": "Answers the user question in general",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_input": {
                                "type": "string",
                                "description": "user's question"
                            }
                        },
                        "required": ["user_input"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "recommendation",
                    "description": "It has a trained model which recommends financial products to customers based on their life events, which it'll get from querying the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "client_id": {
                                "type": "string",
                                "description": "client_id extracted from user question"
                            }
                        },
                        "required": ["client_id"]
                    }
                }
            }

        ]
        response = client.chat.completions.create(
            model=deployment,  # Use deployment name, not model name
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=2000
        )



        response_message = response.choices[0].message
        print(response_message)
        tool_calls = response_message.tool_calls



        if tool_calls: 
            for toolcall in tool_calls: # Check if there are any tool calls
                tool_call = toolcall # only consider the first tool call, as requested
                function_name = tool_call.function.name
                print(function_name)
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "db_fn":
                    function_response = db_fn(user_input=function_args["user_input"])
                elif function_name == "no_db_fn":
                    function_response = no_db_fn(user_input=function_args["user_input"])
                elif function_name == "recommendation":
                    function_response = recommendation(inference_ip('C001'))
                else:
                    function_response = "Error: Unknown function"

                # function_response = function_name(user_input=function_args["user_input"])

                print('1'+str(messages))
                
                messages.append(response_message)  # Append the assistant message
                print('2 '+ str(messages))
                messages.append(

                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response),
                    }
                )  # Append the tool response
                print('3 '+str(messages))
                # Get a new response from the model to incorporate the tool results
            second_response = client.chat.completions.create(
                    model=deployment,
                    messages=messages,
                )
            resp = second_response.choices[0].message.content.strip()
            print("Chatbot:", resp)
            return resp

        else:
            resp =response_message.content.strip()
            print("Chatbot:", resp)
            return resp
              # print the direct response if no tool call
