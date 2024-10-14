import random

class PokerGame:
    def __init__(self, user_name, difficulty):
        self.user_name = user_name
        self.difficulty = difficulty
        self.community_cards = []
        self.user_hand = []
        self.ai_hand = []
        self.user_tokens = 200
        self.ai_tokens = 200

    def play(self):
        self.deal_hands()
        print(f"{self.user_name}'s hand: {self.user_hand}")
        print(f"{self.user_name} has {self.user_tokens} tokens.")
        print(f"AI has {self.ai_tokens} tokens.")
        
        # Initial betting round
        if not self.betting_round():
            return

        # Reveal the flop (first 3 community cards)
        self.reveal_community_cards(3)
        if not self.betting_round():
            return

        # Reveal the turn (4th community card)
        self.reveal_community_cards(1)
        if not self.betting_round():
            return

        # Reveal the river (5th community card)
        self.reveal_community_cards(1)
        if not self.betting_round():
            return

        # Determine winner (simplified for this example)
        self.determine_winner()

    def betting_round(self):
        action = int(input("1: Fold\n2: Check/Call\n3: Raise\n4: All-in\nChoose an action (1-4): "))

        if action == 1:
            print(f"{self.user_name} folds. AI wins!")
            self.ai_tokens += self.user_tokens
            self.user_tokens = 0
            return False

        if self.difficulty == "Easy":
            ai_action = self.ai_decision_easy()
        elif self.difficulty == "Medium":
            ai_action = self.ai_decision_medium()
        else:
            ai_action = self.ai_decision_hard()

        print(f"AI (Difficulty: {self.difficulty}) chooses to: {ai_action}")

        if ai_action == "fold":
            print("AI folds. You win!")
            self.user_tokens += self.ai_tokens
            self.ai_tokens = 0
            print(f"{self.user_name} has {self.user_tokens} tokens.")
            print(f"{self.user_name}'s hand: {self.user_hand}")
            print(f"AI has {self.ai_tokens} tokens.")
            print("AI's hand: ", self.ai_hand)
            return False

        # Check if either player has run out of tokens
        if self.user_tokens <= 0 or self.ai_tokens <= 0:
            self.determine_winner()
            return False

        return True

    def reveal_community_cards(self, number):
        for _ in range(number):
            card = self.community_cards.pop(0)
            print(f"Revealed community card: {card}")

    def ai_decision_easy(self):
        actions = ["fold", "check", "raise"]
        return random.choice(actions)

    def ai_decision_medium(self):
        # Simplified logic for Medium difficulty (AI evaluates the strength of its hand)
        hand_strength = self.evaluate_hand(self.ai_hand + self.community_cards)
        if hand_strength[0] > 5:
            return "raise"
        elif hand_strength[0] > 3:
            return "check"
        else:
            return "fold"

    def ai_decision_hard(self):
        # More sophisticated logic for Hard difficulty
        hand_strength = self.evaluate_hand(self.ai_hand + self.community_cards)
        user_hand_strength = self.evaluate_hand(self.user_hand + self.community_cards)
        
        if hand_strength[0] > user_hand_strength[0]:
            return "raise"
        elif hand_strength[0] == user_hand_strength[0]:
            if hand_strength[1] > user_hand_strength[1]:
                return "raise"
            else:
                return "check"
        else:
            return "fold"

    def evaluate_hand(self, hand):
        # Evaluate the hand and return a tuple (rank, high_card)
        ranks = '23456789TJQKA'
        suits = 'HDCS'
        rank_dict = {r: i for i, r in enumerate(ranks, start=2)}
        suit_dict = {s: i for i, s in enumerate(suits)}

        # Count occurrences of each rank and suit
        rank_counts = {r: 0 for r in ranks}
        suit_counts = {s: 0 for s in suits}
        for card in hand:
            rank_counts[card[0]] += 1
            suit_counts[card[1]] += 1

        # Check for flush
        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break

        # Check for straight
        sorted_ranks = sorted([rank_dict[card[0]] for card in hand], reverse=True)
        straight = False
        for i in range(len(sorted_ranks) - 4):
            if sorted_ranks[i] - sorted_ranks[i + 4] == 4:
                straight = True
                high_card = sorted_ranks[i]
                break

        # Check for straight flush
        if flush_suit:
            flush_cards = [card for card in hand if card[1] == flush_suit]
            sorted_flush_ranks = sorted([rank_dict[card[0]] for card in flush_cards], reverse=True)
            for i in range(len(sorted_flush_ranks) - 4):
                if sorted_flush_ranks[i] - sorted_flush_ranks[i + 4] == 4:
                    return (9, sorted_flush_ranks[i])  # Straight flush

        # Check for four of a kind, full house, three of a kind, two pair, and pair
        rank_count_values = sorted(rank_counts.values(), reverse=True)
        if rank_count_values[0] == 4:
            return (8, max(rank_dict[card[0]] for card in hand if rank_counts[card[0]] == 4))  # Four of a kind
        if rank_count_values[0] == 3 and rank_count_values[1] >= 2:
            return (7, max(rank_dict[card[0]] for card in hand if rank_counts[card[0]] == 3))  # Full house
        if flush_suit:
            return (6, max(rank_dict[card[0]] for card in hand if card[1] == flush_suit))  # Flush
        if straight:
            return (5, high_card)  # Straight
        if rank_count_values[0] == 3:
            return (4, max(rank_dict[card[0]] for card in hand if rank_counts[card[0]] == 3))  # Three of a kind
        if rank_count_values[0] == 2 and rank_count_values[1] == 2:
            return (3, max(rank_dict[card[0]] for card in hand if rank_counts[card[0]] == 2))  # Two pair
        if rank_count_values[0] == 2:
            return (2, max(rank_dict[card[0]] for card in hand if rank_counts[card[0]] == 2))  # Pair

        return (1, max(rank_dict[card[0]] for card in hand))  # High card

    def deal_hands(self):
        # Create a deck of cards
        suits = ['H', 'D', 'C', 'S']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        deck = [(rank, suit) for suit in suits for rank in ranks]
        
        # Shuffle the deck
        random.shuffle(deck)
        
        # Deal hands
        self.user_hand = [deck.pop(), deck.pop()]
        self.ai_hand = [deck.pop(), deck.pop()]
        
        # Deal community cards
        self.community_cards = [deck.pop() for _ in range(5)]

    def determine_winner(self):
        # Evaluate hands
        user_hand_strength = self.evaluate_hand(self.user_hand + self.community_cards)
        ai_hand_strength = self.evaluate_hand(self.ai_hand + self.community_cards)
        
        # Determine winner
        if user_hand_strength > ai_hand_strength:
            print(f"{self.user_name} wins!")
            print(f"{self.user_name}'s hand: {self.user_hand}")
            print("AI's hand: ", self.ai_hand)
        elif user_hand_strength < ai_hand_strength:
            print("AI wins!")
            print("AI's hand: ", self.ai_hand)
        else:
            print("It's a tie!")

# Start game
user_name = input("Enter your name: ")
difficulty = input("Select difficulty (Easy, Medium, Hard): ")
game = PokerGame(user_name, difficulty)
game.play()
