import os
import argparse
import pandas as pd
import numpy as np
import sys


# add src to path for local imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# src directory is two levels up from CURRENT_DIR (src/events/<event>)
SRC_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import design


prize_pool = {
    "Tyler Gold Edition stickers (+ special prize)": {
        "n_items": 1,
        "value": 6,
    },
    "Tyler Mode: ON stickers": {
        "n_items": 2,
        "value": 5,
    },
    "⭐ 3000 Starz": {
        "n_items": 1,
        "value": 4,
    },
    "⭐ 1000 Starz": {
        "n_items": 2,
        "value": 3,
    },
    "⭐ 500 Starz": {
        "n_items": 3,
        "value": 2,
    },
    "⭐ 100 Starz": {
        "n_items": 4,
        "value": 1,
    },
}


def _load_data(path):
    df = pd.read_csv(path)

    telegram_id_to_username = {
        row['telegram_id']: row['username'] if not pd.isnull(row['username']) else None
        for _, row in df.iterrows()
    }

    return df, telegram_id_to_username


def _select_winners(df, telegram_id_to_username, seed, save_path):
    tickets = []
    for _, row in df.iterrows():
        tickets.extend([row['telegram_id']] * row['tickets_count'])

    np.random.seed(seed)
    np.random.shuffle(tickets)

    winners = []
    for prize, details in sorted(prize_pool.items(), key=lambda item: item[1]["value"], reverse=True):
        for _ in range(details['n_items']):
            if tickets:
                winner_telegram_id = tickets.pop()
                winner_username = telegram_id_to_username.get(winner_telegram_id, None)
                winners.append({
                    "telegram_id": winner_telegram_id,
                    "username": winner_username,
                    "prize": prize,
                })

    winners_df = pd.DataFrame(winners)
    winners_df.to_csv(save_path, index=False)

    return winners


def _get_stats(df, telegram_id_to_username):
    total_n_participants = df.shape[0]

    top_5_participants_df = df.nlargest(5, "tickets_count")
    top_5_participants = [
        {
            "telegram_id": row["telegram_id"],
            "username": telegram_id_to_username.get(row["telegram_id"], None),
            "tickets_count": row["tickets_count"],
        }
        for _, row in top_5_participants_df.iterrows()
    ]

    return top_5_participants, total_n_participants


def main(seed):
    if seed is None:
        raise ValueError("Seed is required")

    os.system("clear")
    print(design.LOGO)

    print(f"Random seed: {seed}")
    print(f"NumPy version: {np.__version__}")
    print(f"Pandas version: {pd.__version__}")
    input()

    os.system("clear")
    print(design.WINNERS_WILL_BE_SELECTED)
    input()

    os.system("clear")
    print(design.NOW)
    input()

    data_path = os.path.join(CURRENT_DIR, "data.csv")
    df, telegram_id_to_username = _load_data(data_path)

    winners = _select_winners(df, telegram_id_to_username, seed, os.path.join(CURRENT_DIR, "winners.csv"))

    top_5_participants, total_n_participants = _get_stats(df, telegram_id_to_username)

    os.system("clear")
    print(f"Total number of participants [Общее число участников]:", end="")
    input()
    print(f"{total_n_participants}!", end="")
    print()
    input()

    print("Top-5 by tickets [Топ-5 по количеству билетов]:", end="")
    for idx, participant in enumerate(top_5_participants, 1):
        input()

        text = f"{idx}. {participant['telegram_id']}"
        if participant['username']: text += f" @{participant['username']}"
        text += f" – {participant['tickets_count']} tickets"

        print(text, end="")
    print()
    input()

    os.system("clear")
    print("So... Итак...", end="")
    input()

    print("IT'S TIME! ВРЕМЯ ПРИШЛО!", end="")
    input()

    # announce prize count and list all prizes with their counts (no values)
    print(f"Today we will be giving away {len(winners)} prizes [Сегодня мы разыграем {len(winners)} призов]:", end="")
    input()

    for prize_name, details in sorted(prize_pool.items(), key=lambda item: item[1]["value"], reverse=True):
        print(f"{prize_name} — {details['n_items']}")
    print()

    print("Good luck and have fun! [Удачи и давайте повеселимся!]", end="")
    print()
    input()

    os.system("clear")
    print("Here're the luckiest Ballers [Вот они, самые удачливые Боллеры]:", end="")
    print()

    # announce from low to high prize value
    winners_sorted = sorted(winners, key=lambda w: prize_pool[w["prize"]]["value"])
    for winner in winners_sorted:
        input()

        telegram_id, username, prize = (
            winner["telegram_id"],
            winner["username"],
            winner["prize"],
        )

        text = f"🎉 {telegram_id}"
        if username: text += f" @{username}"
        text += f" – wins '{prize}'!"

        print(text, end="")
    print()
    input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='@myballs prize selection')
    parser.add_argument('--seed', type=int, required=True, help='Random seed (from dice)')
    args = parser.parse_args()

    main(args.seed)


