import ollama
import requests
import json

# TODO: Define your agent's behavior and capabilities here
SYSTEM_PROMPT = "You are a helpful assistant"

# TODO: Write necessary tool functions
# THis fetches real data from your API
# The agent calls this when it needs information

def get_data(query: str) -> str: 
    # TODO: Make an API call using requests and return the result as a string
    # hint: use requests.get() to fetch data from an API endpoint, and then process the response to return the relevant information as a string.
    # Ex: url = "https://your-api-url-here"
    # params = {"search": query}
    # response = requests.get(url, params=params)
    # return json.dumps(response.json())
    pass

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_data",
            "description": "TODO: Describe what your tool fetches", # TODO
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "TODO: Describe what the input should be" # TODO
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# DO NOT EDIT BELOW THIS LINE

chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

print("Agent is ready! Type 'quit' to exit. \n")

while True:
    user_input = input("User:")

    if user_input.lower() == "quit":
        break

    chat_history.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model = "llama3.2:3b",
        messages = chat_history,
        tools = tools,
    )

    if response.message.tool_calls:
        for tool_call in response.message.tool_calls:
            if tool_call.function.name == "get_data":
                args = tool_call.function.arguments
                result = get_data(args["query"])
                chat_history.append({"role": "tool", "content": result})
        
        final_response = ollama.chat(
            model = "llama3.2:3b",
            messages = chat_history,
            tools = tools
        )
        assistant_message = final_response.message.content
    else:
        assistant_message = response.message.content

    chat_history.append({"role": "assistant", "content": assistant_message})
    print(f"Assistant: {assistant_message}\n")
