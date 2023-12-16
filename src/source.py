from gcal import summarize_schedule
from chatgpt import send_user_content

prompt = ""
with open('prompt.md', 'r') as file:
    prompt = file.read()
data = summarize_schedule()
response = send_user_content(prompt + str(data))
print(response.choices[0].message.content)
