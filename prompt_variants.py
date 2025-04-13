import random

title_prompts = [
  "Choose a title for your note ✏️ :\n>  ",
  "Now you may enter the title 😊 :\n>  ",
  "Enter the title, please 👀 :\n>  ",
  "How would you like to name your note? 🤔 \n>  ",
  "Wrtie the title here ⬇️ :\n>  "
]

text_prompt = [
  "Write your text 🖋️ :\n>  ",
  "You can share your secrets. I promise, I won't tell anyone 🤫 :\n>  ",
  "I am ready to record the text 🫡 :\n>  ",
  "What text would you like to add this time? 🧐 \n>  ",
  "Write your text. I remember things better than your ex 🥸 :\n>  "
]

edit_note_prompt = [
  "Of course 😀 ! Let's change your note. What was the title?\n>  ",
  "Sure 💯 ! What note would you like to update?\n>  ",
  "Did something change? Let's edit the note! Remind me the title 🫥 :\n>  ",
  "Change?.. No problem... What is the title?\n>  ",
  "Please write the title of the note you want to edit 🙂 :\n>  "
]

edit_text_prompt = [
  "Please, write the new text - and make sure it's correct this time! 🙃 \n>  ",
  "And the new text is 😲 :\n>  ",
  "How would you like to change the text? 😑 \n>  ",
  "Tell me the updated version 🫠 :\n>  ",
  "So, what do we change in the text? 😶 \n>  "
]

title_search_prompt = [
  "Let's search by title 🔍 :\n>  ",
  "I'll find it in a second 🔜 ! What is the title?\n>  ",
  "Which note do you want to find? ➡️ \n>  "
]

delete_note_prompt = [
  "Sure! What is the title of the note? 📒 \n>  ",
  "Which note would you like to delete? 🗑️ \n>  ",
  "Oh yes, this is easy 🥱 . WHat is the title?\n>  "
]

def get_prompts(prompt_list):
  return random.choice(prompt_list)