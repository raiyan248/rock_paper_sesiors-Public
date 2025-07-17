import random
import json
import os
import time

ACTIONS = ["Rock", "Paper", "Scissors"]
WIN_RULES = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
Q_TABLE_FILE = "q_table.json"

# Q-learning params
alpha, gamma, epsilon = 0.3, 0.9, 0.2
Q = {}

scoreboard = {"Player": 0, "Computer": 0, "Ties": 0}

AI_WIN_REACTIONS = [
    "😎 Haha! Too easy for me!",
    "🔥 I'm on fire! Can't stop me!",
    "💪 Big brain moves!"
]
AI_LOSE_REACTIONS = [
    "😱 Nooo! How did you do that?",
    "😭 Impossible! I was supposed to win!",
    "😤 Okay... lucky shot!"
]
AI_TIE_REACTIONS = [
    "🤔 Huh, we think alike!",
    "😅 Close one!",
    "😐 A tie? Meh."
]

def save_q_table():
    with open(Q_TABLE_FILE, "w") as f:
        json.dump(Q, f)

def load_q_table():
    global Q
    if os.path.exists(Q_TABLE_FILE):
        with open(Q_TABLE_FILE, "r") as f:
            Q = json.load(f)
        for s in Q:
            for a in Q[s]:
                Q[s][a] = float(Q[s][a])

def init_state(state):
    if state not in Q:
        Q[state] = {a: 0 for a in ACTIONS}

def get_best_action(state):
    init_state(state)
    return max(Q[state], key=Q[state].get)

def choose_action(state):
    init_state(state)
    if random.random() < epsilon:
        return random.choice(ACTIONS), "🧪 Random pick!"
    return get_best_action(state), "🎯 Best move!"

def update_q(prev_state, action, reward, next_state):
    init_state(prev_state)
    init_state(next_state)
    best_next = get_best_action(next_state)
    Q[prev_state][action] += alpha * (reward + gamma * Q[next_state][best_next] - Q[prev_state][action])

def get_reward(player, computer):
    if player == computer:
        scoreboard["Ties"] += 1
        return 0
    elif WIN_RULES[player] == computer:
        scoreboard["Player"] += 1
        return -1
    scoreboard["Computer"] += 1
    return 1

def print_intro():
    print("\n🤖 Hey there! I'm your AI opponent.")
    print("😏 Think you can beat me in Rock-Paper-Scissors?")
    print("🔥 Let's find out! (Press 'q' anytime to quit)\n")

def print_score():
    print(f"\n📊 Scores → You: {scoreboard['Player']} | Me: {scoreboard['Computer']} | Ties: {scoreboard['Ties']}")

def get_player_choice():
    while True:
        choice = input("\n🎮 Choose:\n 1️⃣ Rock\n 2️⃣ Paper\n 3️⃣ Scissors\n (or 'q' to quit): ").strip()
        if choice == 'q':
            return None
        if choice in ['1', '2', '3']:
            return ACTIONS[int(choice) - 1]
        print("❌ Invalid input! Try again.")

def play_game():
    load_q_table()
    print_intro()
    prev_state = "Start"

    while True:
        player = get_player_choice()
        if not player:
            print("\n👋 How was the game?")
            if scoreboard["Computer"] > scoreboard["Player"]:
                print("😎 I totally crushed you! Next time will be even worse for you! 💀")
            else:
                print("😤 You were lucky this time... I'll destroy you next time! 🔥")
            print_score()
            save_q_table()
            break

        computer, reason = choose_action(prev_state)
        time.sleep(0.5)
        print(f"\n🤖 {reason}")
        time.sleep(0.5)
        print(f"\n👉 You chose: {player} | I chose: {computer}")

        reward = get_reward(player, computer)
        if reward == 1:
            print(random.choice(AI_WIN_REACTIONS))
        elif reward == -1:
            print(random.choice(AI_LOSE_REACTIONS))
        else:
            print(random.choice(AI_TIE_REACTIONS))

        update_q(prev_state, computer, reward, player)
        prev_state = player
        print_score()
        save_q_table()

if __name__ == "__main__":
    play_game()
