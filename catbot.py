

import json
import os
from difflib import get_close_matches
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings

DATA_FILE = "data.json"

# Load database
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data_list = json.load(f)
else:
    data_list = []

# Simpan data
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data_list, f, indent=4)

# Matching jawaban
def keyword_match(user_input):
    user_words = set(user_input.lower().split())
    best_score = 0
    best_answer = None
    
    for item in data_list:
        question_words = set(item["Tanya"].lower().split())
        score = len(user_words & question_words)
        if score > best_score:
            best_score = score
            best_answer = item["jawab"]
    
    if best_score == 0:
        all_questions = [item["Tanya"] for item in data_list]
        matches = get_close_matches(user_input, all_questions, n=1, cutoff=0.6)
        if matches:
            for item in data_list:
                if item["Tanya"] == matches[0]:
                    best_answer = item["jawab"]
    return best_answer

def get_response(user_input):
    for item in data_list:
        if item["Tanya"].lower() == user_input.lower():
            return item["jawab"]
    return keyword_match(user_input)

# Setup prompt_toolkit
history = InMemoryHistory()
bindings = KeyBindings()

@bindings.add('c-c')
def _(event):
    event.app.exit()

# Main loop
def main():
    print("=== 😎 CatBot Super Aman 🤖 ===")
    print("Ketik 'exit' untuk keluar\n")
    
    while True:
        try:
            user_input = prompt("😎 Ketik: ",
                                history=history,
                                key_bindings=bindings).strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("🤖 CatBot: Sampai jumpa!")
                break
            
            response = get_response(user_input)
            
            if response:
                print("🤖 CatBot:", response)
            else:
                print("🤖 CatBot: Maaf, saya belum tahu jawaban itu 😅")
                teach = prompt("🤖 CatBot: Mau ajari saya jawaban? (y/n): ").strip().lower()
                if teach == "y":
                    new_answer = prompt("🤖 CatBot: Masukkan jawaban: ").strip()
                    data_list.append({"Tanya": user_input, "jawab": new_answer})
                    save_data()
                    print("🤖 CatBot: Terima kasih! Saya sudah belajar jawaban baru 👍")
        except KeyboardInterrupt:
            print("\n🤖 CatBot: Input dibatalkan, coba lagi 😅")

if __name__ == "__main__":
    main()


