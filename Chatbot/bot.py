import pyautogui
import time
import pyperclip
from openai import OpenAI

client = OpenAI(
  api_key="<Your Key Here>",
)

def is_last_message_from_sender(chat_log, sender_name="Shahzad Khan"):
    # Split the chat log into individual messages
    messages = chat_log.strip().split("/2024] ")[-1]
    if sender_name in messages:
        return True 
    return False


# Step 1: Click on the chrome icon at coordinates (1639, 1412)
pyautogui.click(1639, 1412)
time.sleep(1)  # Wait for 1 second to ensure the click is registered

while True:
    time.sleep(5)

    # Step 2: Click and hold → move → release
    pyautogui.moveTo(972, 202)       # Move to start of chat
    pyautogui.mouseDown(button='left')
    time.sleep(0.2)
    pyautogui.moveTo(2213, 1278, duration=2.0)  # Drag to bottom
    pyautogui.mouseUp(button='left')

    # Step 3: Copy the selected text to the clipboard
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    pyautogui.click(1994, 281)

    # Step 4: Retrieve the text from the clipboard
    chat_history = pyperclip.paste()

    # Debugging
    print(chat_history)
    print(is_last_message_from_sender(chat_history))

    if is_last_message_from_sender(chat_history):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a person named Naruto who speaks Hindi and English. You are from India and a coder. You analyze chat history and roast people in a funny way. Output should be the next chat response (text message only)."},
                {"role": "system", "content": "Do not start like this [21:02, 12/6/2024] Rohan Das: "},
                {"role": "user", "content": chat_history}
            ]
        )

        response = completion.choices[0].message.content
        pyperclip.copy(response)

        # Step 5: Click at coordinates (1808, 1328)
        pyautogui.click(1808, 1328)
        time.sleep(1)

        # Step 6: Paste the text
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        # Step 7: Press Enter
        pyautogui.press('enter')
