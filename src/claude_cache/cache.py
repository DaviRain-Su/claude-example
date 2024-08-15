import anthropic
import json

def format_message(message):
    output = []
    output.append(f"Message ID: {message.id}")
    output.append(f"Model: {message.model}")
    output.append(f"Role: {message.role}")
    output.append(f"Stop Reason: {message.stop_reason}")
    output.append("Content:")

    for block in message.content:
        if block.type == 'text':
            output.append(f"  Text: {block.text}")
        elif block.type == 'tool_use':
            output.append(f"  Tool Use:")
            output.append(f"    Tool: {block.name}")
            output.append(f"    Input: {json.dumps(block.input, indent=6)}")

    output.append("Usage:")
    output.append(f"  Input Tokens: {message.usage.input_tokens}")
    output.append(f"  Output Tokens: {message.usage.output_tokens}")
    output.append(f"  Cache Creation Input Tokens: {message.usage.cache_creation_input_tokens}")
    output.append(f"  Cache Read Input Tokens: {message.usage.cache_read_input_tokens}")

    return "\n".join(output)

def main_function():
    client = anthropic.Anthropic()
    response = client.beta.prompt_caching.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2048,
        system="You are a helpful assistant that provides information about weather and time. When asked about weather or time in a specific location, use the appropriate tools to fetch the most up-to-date information. Please provide detailed responses, including any relevant context or additional information that might be useful to the user.",
        tools=[
            {
                "name": "get_weather",
                "description": "Get the current weather in a given location",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
                        }
                    },
                    "required": ["location"]
                },
            },
            {
                "name": "get_time",
                "description": "Get the current time in a given time zone",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": "The IANA time zone name, e.g. America/Los_Angeles"
                        }
                    },
                    "required": ["timezone"]
                },
            }
        ],
        messages=[
            {
                "role": "user",
                "content": "I'm planning a trip to New York City next week and I'm trying to pack appropriately. Could you please give me a detailed overview of the current weather conditions in New York? Also, I'm currently in Los Angeles and I'm trying to coordinate some calls with colleagues in New York. What's the current time difference between these two cities? Please provide as much detail as possible, including any tips or recommendations based on the weather and time information."
            }
        ]
    )
    print(format_message(response))

if __name__ == "__main__":
    main_function()
