import os
import json
import getpass
import requests
from rich.markdown import Markdown
URL = "https://api.groq.com/openai/v1/chat/completions"
# --
def get_api_key():
  key_file = 'api.key'
  key = None
  if os.path.exists(key_file)
  with open(key_file, 'r') as kf:
    key = kf.read()
    else:
        key = getpass.getpass('Enter api-key:')
        # with open(key_file, 'w') as kf:
        #     kf.write(key)
    return key

# Your API key from environment variable
# api_key = os.getenv("GROQ_API_KEY")
api_key = get_api_key()
assert api_key, "Please set the GROQ_API_KEY environment variable."
prompt = ''

# --
def main():
    clear = lambda: os.system('clear')
    while 1:
        query = str(input('Query: '))
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        # --
        if not query:
            break
        clear()
        # Headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        # --
        try:
            response = requests.post(URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            md = Markdown(data['choices'][0]['message']['content'])
            output = md.markup
            print('len:', len(output), '\n', output)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

if __name__ == '__main__':
  main()
# todo: code formatting src/*