# deck.py
import os
from PIL import Image, ImageTk

CARD_DIR = os.path.join("assets", "card_images")
CARD_WIDTH = 80
CARD_HEIGHT = 120

# Configuration
NUM_DECKS = 4  # Số bộ bài trong shoe

suits = ['clubs', 'diamonds', 'hearts', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
single_deck_template = [f"{rank}_of_{suit}" for suit in suits for rank in ranks]

def create_deck():
    """Trả về shoe gồm 4 bộ bài (chưa shuffle – để UI tự shuffle 1 lần)."""
    shoe = []
    for _ in range(NUM_DECKS):
        shoe.extend(single_deck_template.copy())
    return shoe

def draw_from_top(deck_list):
    """Lấy lá trên cùng (cuối list). Nếu deck rỗng, UI sẽ tự reshuffle."""
    return deck_list.pop()

def get_deck_info():
    """Trả về thông tin về số bộ bài và tổng số lá."""
    total_cards = len(single_deck_template) * NUM_DECKS
    return {
        'num_decks': NUM_DECKS,
        'cards_per_deck': len(single_deck_template),
        'total_cards': total_cards
    }

def card_image(card_name):
    """Ảnh kích thước chuẩn cho game."""
    img_path = os.path.join(CARD_DIR, f"{card_name}.png")
    try:
        img = Image.open(img_path).resize((CARD_WIDTH, CARD_HEIGHT))
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

def card_thumbnail(card_name, w=40, h=60):
    """Ảnh thumbnail dùng cho discard pile."""
    img_path = os.path.join(CARD_DIR, f"{card_name}.png")
    try:
        img = Image.open(img_path).resize((w, h))
        return ImageTk.PhotoImage(img)
    except Exception:
        return None