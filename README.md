# 🃏 Enhanced Blackjack with Card Counting

A Python-based **Blackjack game** built using `Tkinter` and `Pillow` (PIL) with an interactive GUI.  
The game includes advanced features like **4-deck shoe**, **discard pile display**, and a **card counting system (Hi-Lo)**.

---

## **Features**
- 🎨 **Modern GUI** using `Tkinter` with themed colors and clean layout.
- ♠ **4-deck shoe** with automatic reshuffle when cards are low.
- 🗂 **Discard pile display** (shows last used card).
- 🧮 **Card Counting Panel**:
  - Running Count (Hi-Lo system).
  - True Count (Running Count divided by decks remaining).
  - Advantage & Betting suggestion.
- 💰 **Betting system**:
  - Quick betting tokens ($5, $10, $20).
  - Custom bet entry.
  - Reset balance button.
- 🎯 **Game Actions**: Hit, Stand, Double Down, Insurance (Split pending).
- 🔄 **Auto-reset game** when deck is reshuffled or balance is empty.

---

## **Project Structure**
Blackjack/
│
├── main.py # Entry point
├── blackjack_app.py # Main game logic
│
├── ui/ # UI Components
│ ├── dealer_ui.py
│ ├── player_ui.py
│ ├── betting_ui.py
│ ├── counting_ui.py
│
├── deck.py # Deck creation and card images
├── game_logic.py # Game rules and scoring
├── utils.py # Helper functions
└── README.md # Project documentation


---

## **Requirements**
- Python 3.8+
- **Libraries:**
  ```bash
  pip install pillow
