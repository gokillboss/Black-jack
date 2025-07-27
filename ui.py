import tkinter as tk
import random
from deck import create_deck, draw_from_top, card_image, card_thumbnail, get_deck_info
from game_logic import calculate_score, is_blackjack
from utils import clear_frame

# Constants
RESHUFFLE_THRESHOLD = 52  # Reshuffle when less than 1 deck remains
DISCARD_SHOW_MAX = 1  # Only show last card
COLORS = {
    'bg_main': '#0f5132',
    'bg_table': '#2d5a3d', 
    'bg_bottom': '#1a1a1a',
    'text_primary': 'white',
    'text_secondary': 'lightgray',
    'text_highlight': 'gold',
    'text_warning': 'yellow'
}

class BlackjackApp:
    def __init__(self, master):
        self.master = master
        self._setup_window()
        self._init_game_state()
        self._setup_ui()
        self.reset_game()
        self.result_label.config(text="💳 Balance reset! Good luck!")

    def _setup_window(self):
        """Initialize main window properties"""
        self.master.title("Enhanced Blackjack - 4 Deck Shoe")
        self.master.geometry("950x700")  # Slightly larger for deck info
        self.master.configure(bg=COLORS['bg_main'])

    def _init_game_state(self):
        """Initialize all game state variables"""
        # Financial state
        self.balance = 1000
        self.bet = 0
        self.insurance_bet = 0
        
        # Game state
        self.can_double_down = False
        self.can_split = False
        self.game_in_progress = False
        
        # Cards
        deck_info = get_deck_info()
        self.total_cards = deck_info['total_cards']
        self.num_decks = deck_info['num_decks']
        
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.discard_pile = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_imgs = []
        self.dealer_imgs = []
        self.discard_imgs = []
        
        # Card counting
        self.running_count = 0
        self.cards_seen = 0

    def _setup_ui(self):
        """Setup all UI components"""
        self._create_header()
        self._create_game_table()
        self._create_action_buttons()
        self._create_betting_section()

    def _create_header(self):
        """Create title and deck info display"""
        tk.Label(self.master, text="🃏 BLACKJACK - 4 DECK SHOE 🃏",
                font=('Arial', 20, 'bold'), fg=COLORS['text_highlight'], 
                bg=COLORS['bg_main']).pack(pady=10)

        # Deck info
        self.deck_info_label = tk.Label(self.master, text=f"📚 Cards Remaining: {len(self.deck)} / {self.total_cards}",
                                       font=('Arial', 12), fg=COLORS['text_secondary'], 
                                       bg=COLORS['bg_main'])
        self.deck_info_label.pack(pady=2)

        self.bet_label = tk.Label(self.master, text="Current Bet: $0",
                                 font=('Arial', 12), fg=COLORS['text_warning'], 
                                 bg=COLORS['bg_main'])
        self.bet_label.pack(pady=2)

    def _create_game_table(self):
        """Create the main game table with dealer and player areas"""
        game_table = tk.Frame(self.master, bg=COLORS['bg_table'], relief='raised', bd=10)
        game_table.pack(pady=20, padx=30, fill='both', expand=True)

        # Dealer section
        self._create_dealer_section(game_table)
        
        # Result display
        self.result_label = tk.Label(game_table, text="", font=('Arial', 18, 'bold'), 
                                    fg=COLORS['text_warning'], bg=COLORS['bg_table'])
        self.result_label.pack(pady=15)

        # Player section
        self._create_player_section(game_table)

    def _create_dealer_section(self, parent):
        """Create dealer area with cards and discard pile"""
        dealer_section = tk.Frame(parent, bg=COLORS['bg_table'])
        dealer_section.pack(pady=15, fill='x')

        tk.Label(dealer_section, text="🎩 DEALER", font=('Arial', 16, 'bold'), 
                fg=COLORS['text_primary'], bg=COLORS['bg_table']).pack()

        self.dealer_score_label = tk.Label(dealer_section, text="Score: ?", font=('Arial', 12), 
                                          fg=COLORS['text_secondary'], bg=COLORS['bg_table'])
        self.dealer_score_label.pack()

        # Dealer row with cards and discard pile
        dealer_row = tk.Frame(dealer_section, bg=COLORS['bg_table'])
        dealer_row.pack(pady=10)

        self.dealer_frame = tk.Frame(dealer_row, bg=COLORS['bg_table'])
        self.dealer_frame.pack(side=tk.LEFT, padx=10)

        self._create_discard_section(dealer_row)

    def _create_discard_section(self, parent):
        """Create discard pile display"""
        discard_panel = tk.Frame(parent, bg=COLORS['bg_table'])
        discard_panel.pack(side=tk.LEFT, padx=30)

        self.discard_title = tk.Label(discard_panel, text="🗂️ Last Card", 
                                     font=('Arial', 12, 'bold'), fg=COLORS['text_primary'], 
                                     bg=COLORS['bg_table'])
        self.discard_title.pack()

        self.discard_count_label = tk.Label(discard_panel, text="(0 cards used)", 
                                           font=('Arial', 10), fg=COLORS['text_secondary'], 
                                           bg=COLORS['bg_table'])
        self.discard_count_label.pack()

        self.discard_frame = tk.Frame(discard_panel, bg=COLORS['bg_table'])
        self.discard_frame.pack(pady=5)

    def _create_player_section(self, parent):
        """Create player area with card counting and balance"""
        player_section = tk.Frame(parent, bg=COLORS['bg_table'])
        player_section.pack(pady=15)

        # Player header with counting info
        player_header = tk.Frame(player_section, bg=COLORS['bg_table'])
        player_header.pack()

        # Left side - Player info with balance
        player_info = tk.Frame(player_header, bg=COLORS['bg_table'])
        player_info.pack(side=tk.LEFT)

        tk.Label(player_info, text="👤 PLAYER", font=('Arial', 16, 'bold'), 
                fg=COLORS['text_primary'], bg=COLORS['bg_table']).pack()

        self.balance_label = tk.Label(player_info, text=f"💰 Balance: ${self.balance}",
                                     font=('Arial', 14, 'bold'), fg=COLORS['text_highlight'], 
                                     bg=COLORS['bg_table'])
        self.balance_label.pack()

        self.player_score_label = tk.Label(player_info, text="Score: 0", font=('Arial', 12), 
                                          fg=COLORS['text_secondary'], bg=COLORS['bg_table'])
        self.player_score_label.pack()

        # Right side - Card counting
        self._create_card_counting_section(player_header)

        self.player_frame = tk.Frame(player_section, bg=COLORS['bg_table'])
        self.player_frame.pack(pady=12)

    def _create_card_counting_section(self, parent):
        """Create card counting display"""
        counting_panel = tk.Frame(parent, bg=COLORS['bg_table'])
        counting_panel.pack(side=tk.LEFT, padx=50)

        tk.Label(counting_panel, text="🧮 CARD COUNTING", font=('Arial', 12, 'bold'), 
                fg=COLORS['text_highlight'], bg=COLORS['bg_table']).pack()

        # Running count
        self.running_count_label = tk.Label(counting_panel, text="Running Count: 0", 
                                           font=('Arial', 11, 'bold'), fg='#00ff00', 
                                           bg=COLORS['bg_table'])
        self.running_count_label.pack()

        # True count (running count / decks remaining)
        self.true_count_label = tk.Label(counting_panel, text="True Count: 0.0", 
                                        font=('Arial', 11, 'bold'), fg='#ffff00', 
                                        bg=COLORS['bg_table'])
        self.true_count_label.pack()

        # Decks remaining
        self.decks_remaining_label = tk.Label(counting_panel, text="Decks Left: 4.0", 
                                             font=('Arial', 10), fg=COLORS['text_secondary'], 
                                             bg=COLORS['bg_table'])
        self.decks_remaining_label.pack()

        # Basic strategy hint
        self.strategy_hint_label = tk.Label(counting_panel, text="Advantage: Neutral", 
                                           font=('Arial', 10, 'bold'), fg='white', 
                                           bg=COLORS['bg_table'])
        self.strategy_hint_label.pack()

        # Betting suggestion
        self.betting_suggestion_label = tk.Label(counting_panel, text="💰 Standard Bet", 
                                                font=('Arial', 9, 'bold'), fg='white', 
                                                bg=COLORS['bg_table'])
        self.betting_suggestion_label.pack()

    def _create_action_buttons(self):
        """Create game action buttons with betting tokens"""
        action_frame = tk.Frame(self.master, bg=COLORS['bg_main'])
        action_frame.pack(pady=15)

        # Top row - Main action buttons
        top_row = tk.Frame(action_frame, bg=COLORS['bg_main'])
        top_row.pack(pady=5)

        buttons_config = [
            ('🎯 Hit', self.hit, '#17a2b8', 0, 0, 12),
            ('✋ Stand', self.stand, '#6f42c1', 0, 1, 12),
            ('⬆️ Double Down', self.double_down, '#fd7e14', 0, 2, 15)
        ]

        self.action_buttons = {}
        for text, command, color, row, col, width in buttons_config:
            btn = tk.Button(top_row, text=text, width=width, command=command, 
                           state='disabled', font=('Arial', 11, 'bold'), 
                           bg=color, fg=COLORS['text_primary'])
            btn.grid(row=row, column=col, padx=5)
            self.action_buttons[text.split()[1].lower()] = btn

        # Second row - Special buttons + Token buttons
        middle_row = tk.Frame(action_frame, bg=COLORS['bg_main'])
        middle_row.pack(pady=5)

        # Insurance and Split on the left
        self.insurance_btn = tk.Button(middle_row, text="🛡️ Insurance", width=12,
                                      command=self.take_insurance, state='disabled',
                                      font=('Arial', 10, 'bold'), bg='#20c997', 
                                      fg=COLORS['text_primary'])
        self.insurance_btn.grid(row=0, column=0, padx=5)

        self.split_btn = tk.Button(middle_row, text="✂️ Split", width=12,
                                  command=self.split_hand, state='disabled',
                                  font=('Arial', 10, 'bold'), bg='#e83e8c', 
                                  fg=COLORS['text_primary'])
        self.split_btn.grid(row=0, column=1, padx=5)

        # Spacer to push tokens to the right
        tk.Label(middle_row, text="", bg=COLORS['bg_main'], width=10).grid(row=0, column=2)

        # Quick bet tokens on the right
        tk.Label(middle_row, text="🎰 Quick Bet:", font=('Arial', 11, 'bold'), 
                fg=COLORS['text_highlight'], bg=COLORS['bg_main']).grid(row=0, column=3, padx=5)

        # Token configuration: (amount, color)
        tokens_config = [(5, '#28a745'), (10, '#007bff'), (20, '#dc3545')]
        self.token_buttons = {}

        for i, (amount, color) in enumerate(tokens_config):
            btn = tk.Button(middle_row, text=f"${amount}", 
                           command=lambda a=amount: self.quick_bet(a),
                           font=('Arial', 11, 'bold'), bg=color, fg=COLORS['text_primary'],
                           width=5, height=2, relief='solid', bd=3,
                           cursor='hand2')
            btn.grid(row=0, column=4+i, padx=8)
            self.token_buttons[amount] = btn

        tk.Frame(self.master, bg=COLORS['bg_main'], height=20).pack(fill='x')

    def _create_betting_section(self):
        """Create control buttons only"""
        bottom_section = tk.Frame(self.master, bg=COLORS['bg_bottom'], relief='sunken', bd=5)
        bottom_section.pack(side='bottom', fill='x', pady=10, padx=20)

        self._create_control_buttons(bottom_section)

    def _create_control_buttons(self, parent):
        """Create game control buttons"""
        control_frame = tk.Frame(parent, bg=COLORS['bg_bottom'])
        control_frame.pack(pady=20)

        control_buttons = [
            ('🔄 New Game', self.new_game, '#007bff'),
            ('💳 Reset Balance', self.reset_balance, '#dc3545')
        ]

        for text, command, color in control_buttons:
            tk.Button(control_frame, text=text, width=15, command=command,
                     font=('Arial', 12, 'bold'), bg=color, 
                     fg=COLORS['text_primary'], height=2).pack(side=tk.LEFT, padx=15)

    # Game Logic Methods (optimized)
    def _draw_card(self):
        """Draw card with automatic reshuffling"""
        if len(self.deck) <= RESHUFFLE_THRESHOLD:
            self.deck = create_deck()
            random.shuffle(self.deck)
            self.discard_pile.clear()
            self.running_count = 0
            self.cards_seen = 0
            self.update_discard_ui()
            self.update_counting_display()
            self.result_label.config(text="🔄 Reshuffled new deck!")
        
        card = draw_from_top(self.deck)
        self._update_card_count(card)
        return card

    def _update_card_count(self, card):
        """Update card counting based on Hi-Lo system"""
        rank = card.split('_')[0]
        self.cards_seen += 1
        
        # Hi-Lo counting system
        if rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif rank in ['10', 'jack', 'queen', 'king', 'ace']:
            self.running_count -= 1
        # 7, 8, 9 are neutral (0)

    def _calculate_true_count(self):
        """Calculate true count (running count / estimated decks remaining)"""
        cards_remaining = len(self.deck)
        decks_remaining = max(cards_remaining / 52, 0.5)  # Minimum 0.5 to avoid division issues
        return self.running_count / decks_remaining

    def _get_advantage_text(self, true_count):
        """Get advantage text based on true count"""
        if true_count >= 3:
            return "Advantage: VERY FAVORABLE", '#00ff00'
        elif true_count >= 2:
            return "Advantage: FAVORABLE", '#33ff33'
        elif true_count >= 1:
            return "Advantage: Slight Edge", '#ffff00'
        elif true_count <= -3:
            return "Advantage: VERY BAD", '#ff0000'
        elif true_count <= -2:
            return "Advantage: UNFAVORABLE", '#ff4444'
        elif true_count <= -1:
            return "Advantage: House Edge", '#ff8800'
        else:
            return "Advantage: Neutral", 'white'

    def _get_betting_suggestion(self, true_count):
        """Get betting suggestion based on true count"""
        if true_count >= 3:
            return "💰 MAX BET!", '#00ff00'
        elif true_count >= 2:
            return "💰 Increase Bet", '#33ff33'
        elif true_count >= 1:
            return "💰 Small Increase", '#ffff00'
        elif true_count <= -2:
            return "⚠️ MIN BET ONLY", '#ff0000'
        else:
            return "💰 Standard Bet", 'white'

    def update_counting_display(self):
        """Update card counting display"""
        true_count = self._calculate_true_count()
        decks_remaining = len(self.deck) / 52
        advantage_text, adv_color = self._get_advantage_text(true_count)
        betting_text, bet_color = self._get_betting_suggestion(true_count)
        
        self.running_count_label.config(text=f"Running Count: {self.running_count:+d}")
        self.true_count_label.config(text=f"True Count: {true_count:+.1f}")
        self.decks_remaining_label.config(text=f"Decks Left: {decks_remaining:.1f}")
        self.strategy_hint_label.config(text=advantage_text, fg=adv_color)
        self.betting_suggestion_label.config(text=betting_text, fg=bet_color)

    def _validate_bet(self, amount):
        """Validate bet amount"""
        if self.game_in_progress:
            self.result_label.config(text="⚠️ Finish current game first!")
            return False
        if amount > self.balance:
            self.result_label.config(text="⚠️ Insufficient funds!")
            return False
        if amount < 1:
            self.result_label.config(text="⚠️ Bet must be > $0!")
            return False
        return True

    def quick_bet(self, amount):
        """Place quick bet with animation feedback"""
        if self._validate_bet(amount):
            self.bet = amount
            self.result_label.config(text=f"Bet placed: ${amount}")
            # Disable betting buttons during deal
            self.disable_betting_buttons()
            self.master.after(500, self.start_new_round)

    def start_new_round(self):
        """Start new game round with card dealing animation"""
        self.game_in_progress = True
        self.insurance_bet = 0
        self.can_double_down = True
        self.can_split = False

        # Clear previous hands
        self.player_hand = []
        self.dealer_hand = []
        self.update_ui()  # Clear the display first

        # Deal cards with animation
        self._deal_initial_cards()

    def _deal_initial_cards(self):
        """Deal initial cards with animation sequence"""
        # Schedule card dealing sequence
        self.master.after(200, self._deal_player_card_1)
        self.master.after(600, self._deal_dealer_card_1)
        self.master.after(1000, self._deal_player_card_2)
        self.master.after(1400, self._deal_dealer_card_2)
        self.master.after(1800, self._finish_initial_deal)

    def _deal_player_card_1(self):
        """Deal first card to player"""
        card = self._draw_card()
        self.player_hand.append(card)
        self.update_ui()
        self.result_label.config(text="Dealing cards...")

    def _deal_dealer_card_1(self):
        """Deal first card to dealer"""
        card = self._draw_card()
        self.dealer_hand.append(card)
        self.update_ui()

    def _deal_player_card_2(self):
        """Deal second card to player"""
        card = self._draw_card()
        self.player_hand.append(card)
        self.update_ui()

    def _deal_dealer_card_2(self):
        """Deal second card to dealer (face down)"""
        card = self._draw_card()
        self.dealer_hand.append(card)
        self.update_ui()

    def _finish_initial_deal(self):
        """Complete the initial deal and check for game conditions"""
        # Check for split possibility
        player_ranks = [c.split('_')[0] for c in self.player_hand]
        self.can_split = player_ranks[0] == player_ranks[1]

        # Check for blackjacks
        if is_blackjack(self.player_hand):
            if is_blackjack(self.dealer_hand):
                self.master.after(500, lambda: self.end_game("Push! Both have Blackjack!"))
            else:
                self.master.after(500, lambda: self._player_blackjack_win())
            return

        # Enable insurance if dealer shows ace
        if self.dealer_hand[0].split('_')[0] == 'ace':
            self.insurance_btn.config(state='normal')

        self.result_label.config(text="")
        self.enable_game_buttons()

    def _player_blackjack_win(self):
        """Handle player blackjack win"""
        self.end_game("🎉 Blackjack! You win!")
        self.balance += int(self.bet * 1.5)

    def hit(self):
        """Player hits with animation"""
        # Disable buttons during animation
        self.disable_game_buttons()
        self.result_label.config(text="Drawing card...")
        
        # Draw card with delay
        self.master.after(300, self._complete_hit)

    def _complete_hit(self):
        """Complete the hit action"""
        card = self._draw_card()
        self.player_hand.append(card)
        self.can_double_down = False
        self.can_split = False
        
        self.update_ui()
        player_score = calculate_score(self.player_hand)
        
        if player_score > 21:
            self.master.after(500, lambda: self._player_bust())
        elif player_score == 21:
            self.master.after(500, self.stand)
        else:
            self.result_label.config(text="")
            self.enable_game_buttons()

    def _player_bust(self):
        """Handle player bust"""
        self.end_game("💥 Bust! You lose!")
        self.balance -= self.bet

    def stand(self):
        """Player stands with dealer animation"""
        self.disable_game_buttons()
        self.result_label.config(text="Dealer's turn...")
        
        # Start dealer play sequence
        self.master.after(800, self._dealer_play_sequence)

    def _dealer_play_sequence(self):
        """Animate dealer playing their hand"""
        dealer_score = calculate_score(self.dealer_hand)
        
        if dealer_score < 17:
            # Dealer needs to hit
            self.result_label.config(text="Dealer hits...")
            card = self._draw_card()
            self.dealer_hand.append(card)
            self.update_ui(reveal_dealer=True)
            
            # Continue dealer sequence after delay
            self.master.after(1000, self._dealer_play_sequence)
        else:
            # Dealer stands, compare hands
            self.master.after(500, self.end_game_comparison)

    def double_down(self):
        """Player doubles down with animation"""
        if not self.can_double_down or self.bet > self.balance:
            self.result_label.config(text="⚠️ Cannot double down!")
            return
        
        self.bet *= 2
        self.disable_game_buttons()
        self.result_label.config(text="Double Down! Drawing one card...")
        
        # Draw card with animation
        self.master.after(500, self._complete_double_down)

    def _complete_double_down(self):
        """Complete double down action"""
        card = self._draw_card()
        self.player_hand.append(card)
        self.can_double_down = False
        self.can_split = False
        
        self.update_ui()
        player_score = calculate_score(self.player_hand)
        
        if player_score > 21:
            self.master.after(500, lambda: self._player_bust())
        else:
            self.master.after(800, self.stand)

    def take_insurance(self):
        """Take insurance bet"""
        insurance_amount = self.bet // 2
        if insurance_amount > self.balance - self.bet:
            self.result_label.config(text="⚠️ Cannot afford insurance!")
            return
        
        self.insurance_bet = insurance_amount
        self.insurance_btn.config(state='disabled')
        
        if is_blackjack(self.dealer_hand):
            self.result_label.config(text="🛡️ Insurance pays! Dealer has Blackjack!")
            self.balance += insurance_amount
        else:
            self.result_label.config(text="❌ Insurance lost.")
            self.balance -= insurance_amount
        
        self.update_ui()

    def split_hand(self):
        """Split hand (placeholder)"""
        self.result_label.config(text="🚧 Split feature coming soon!")

    def end_game_comparison(self):
        """Compare hands and determine winner with reveal animation"""
        self.result_label.config(text="Revealing dealer's hand...")
        
        # Reveal dealer's hand first
        self.update_ui(reveal_dealer=True)
        
        # Wait before showing final result
        self.master.after(1000, self._show_final_result)

    def _show_final_result(self):
        """Show the final game result"""
        player_score = calculate_score(self.player_hand)
        dealer_score = calculate_score(self.dealer_hand)
        
        if dealer_score > 21:
            self.end_game("🎉 Dealer busts! You win!")
            self.balance += self.bet
        elif player_score > dealer_score:
            self.end_game("🎉 You win!")
            self.balance += self.bet
        elif player_score < dealer_score:
            self.end_game("😞 You lose!")
            self.balance -= self.bet
        else:
            self.end_game("🤝 Push! It's a tie!")

    def end_game(self, message):
        """End current game with animation"""
        self.game_in_progress = False
        self.result_label.config(text=message)
        self.disable_game_buttons()
        
        # Update UI and move cards to discard pile
        self.update_ui(reveal_dealer=True)
        self.discard_pile.extend(self.player_hand + self.dealer_hand)
        self.update_discard_ui()

        # Re-enable betting after a short delay
        if self.balance <= 0:
            self.result_label.config(text="💸 Game Over! No money left!")
            self.disable_all_betting()
        else:
            self.master.after(2000, self._ready_for_next_game)

    def _ready_for_next_game(self):
        """Prepare for next game"""
        self.enable_betting_buttons()
        if self.result_label.cget('text') not in ["💸 Game Over! No money left!"]:
            self.result_label.config(text="🎰 Ready for next hand!")

    # UI Update Methods (optimized)
    def _update_button_states(self, buttons, state):
        """Update multiple button states"""
        for button in buttons:
            button.config(state=state)

    def enable_game_buttons(self):
        """Enable game action buttons"""
        self.action_buttons['hit'].config(state='normal')
        self.action_buttons['stand'].config(state='normal')
        
        # Conditional enables
        double_state = 'normal' if (self.can_double_down and self.bet <= self.balance) else 'disabled'
        self.action_buttons['double'].config(state=double_state)
        
        split_state = 'normal' if (self.can_split and self.bet <= self.balance) else 'disabled'
        self.split_btn.config(state=split_state)
        
        # Note: betting buttons managed separately

    def disable_game_buttons(self):
        """Disable game action buttons"""
        game_buttons = [self.action_buttons['hit'], self.action_buttons['stand'], 
                       self.action_buttons['double'], self.insurance_btn, self.split_btn]
        self._update_button_states(game_buttons, 'disabled')
        # Note: betting buttons remain enabled for quick betting during game

    def enable_betting_buttons(self):
        """Enable betting buttons based on balance"""
        for amount, button in self.token_buttons.items():
            state = 'normal' if self.balance >= amount else 'disabled'
            button.config(state=state)

    def disable_betting_buttons(self):
        """Disable betting buttons during gameplay"""
        betting_buttons = list(self.token_buttons.values())
        self._update_button_states(betting_buttons, 'disabled')

    def disable_all_betting(self):
        """Disable all betting when game over"""
        self.disable_betting_buttons()

    def update_discard_ui(self):
        """Update discard pile display - show only last card"""
        clear_frame(self.discard_frame)
        self.discard_imgs = []
        self.discard_count_label.config(text=f"({len(self.discard_pile)} cards used)")
        
        # Show only the last card
        if self.discard_pile:
            last_card = self.discard_pile[-1]
            self._add_card_to_frame(last_card, self.discard_frame, is_thumbnail=True)

    def _add_card_to_frame(self, card, frame, is_thumbnail=False):
        """Add a card to specified frame"""
        img_func = card_thumbnail if is_thumbnail else card_image
        img = img_func(card)
        
        if img:
            lbl = tk.Label(frame, image=img, bg=COLORS['bg_table'])
            lbl.pack(side=tk.LEFT, padx=2 if is_thumbnail else 4)
            if is_thumbnail:
                self.discard_imgs.append(img)
            else:
                return img
        else:
            # Fallback text display
            size_config = (6, 4, 7) if is_thumbnail else (12, 8, 8)
            width, height, font_size = size_config
            
            lbl = tk.Label(frame, text=card.replace('_', ' ').title(),
                          bg='white', fg='black', width=width, height=height,
                          font=('Arial', font_size, 'bold'), relief='raised', bd=3)
            lbl.pack(side=tk.LEFT, padx=2 if is_thumbnail else 4)

    def update_ui(self, reveal_dealer=False):
        """Update main game UI"""
        # Update labels
        self.balance_label.config(text=f"💰 Balance: ${self.balance}")
        self.bet_label.config(text=f"Current Bet: ${self.bet}")
        self.deck_info_label.config(text=f"📚 Cards Remaining: {len(self.deck)} / {self.total_cards}")

        # Clear card frames
        clear_frame(self.dealer_frame)
        clear_frame(self.player_frame)
        self.dealer_imgs = []
        self.player_imgs = []

        # Update dealer cards
        self._update_dealer_cards(reveal_dealer)
        
        # Update player cards
        for card in self.player_hand:
            img = self._add_card_to_frame(card, self.player_frame)
            if img:
                self.player_imgs.append(img)

        # Update scores
        if reveal_dealer:
            self.dealer_score_label.config(text=f"Score: {calculate_score(self.dealer_hand)}")
        else:
            self.dealer_score_label.config(text="Score: ?")
        
        if self.player_hand:
            self.player_score_label.config(text=f"Score: {calculate_score(self.player_hand)}")
        
        # Update card counting display
        self.update_counting_display()

    def _update_dealer_cards(self, reveal_dealer):
        """Update dealer card display"""
        for idx, card in enumerate(self.dealer_hand):
            if idx == 0 or reveal_dealer:
                img = self._add_card_to_frame(card, self.dealer_frame)
                if img:
                    self.dealer_imgs.append(img)
            else:
                # Show card back
                img = card_image("back")
                if img:
                    lbl = tk.Label(self.dealer_frame, image=img, bg=COLORS['bg_table'])
                    lbl.pack(side=tk.LEFT, padx=4)
                    self.dealer_imgs.append(img)
                else:
                    lbl = tk.Label(self.dealer_frame, text="🂠\nCARD\nBACK",
                                  bg='#1a472a', fg=COLORS['text_primary'], width=12, height=8,
                                  font=('Arial', 10, 'bold'), relief='raised', bd=3)
                    lbl.pack(side=tk.LEFT, padx=4)

    def new_game(self):
        """Start new game"""
        if self.balance <= 0:
            self.reset_balance()
            return
        self.reset_game()

    def reset_game(self):
        """Reset game to initial state"""
        self.bet = 0
        self.insurance_bet = 0
        self.game_in_progress = False
        self.can_double_down = False
        self.can_split = False
        self.player_hand = []
        self.dealer_hand = []
        
        self.result_label.config(text="🎰 Use Quick Bet tokens to start!")
        self.disable_game_buttons()
        self.enable_betting_buttons()
        self.update_ui()
        self.update_discard_ui()

    def reset_balance(self):
        """Reset balance to initial amount"""
        self.balance = 1000
        # Reset counting when balance is reset
        self.running_count = 0
        self.cards_seen = 0
        self.discard_pile.clear()
        self.reset_game()