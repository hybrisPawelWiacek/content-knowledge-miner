import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
# Check if the API key is loaded
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

# Initialize the Anthropic client with the API key
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Create a message with Claude
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ]
)

# Output the response from Claude
print(message.content[0].text)