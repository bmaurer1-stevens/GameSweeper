# src/ai/learning_manager.py

import json
import os

class LearningManager:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_experience()
    
    def _load_experience(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_experience(self):
        def custom_serializer(obj):
            if isinstance(obj, frozenset):
                return list(obj)  # Convert frozenset to list
            raise TypeError(f"Type {type(obj)} not serializable")
        
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2, default=custom_serializer)


    def record_game(self, game_key, actions, outcome):
        """
        game_key: a simple string describing the game config, e.g. '5x5_5mines'
        actions: list of (state_hash, action) describing each step
        outcome: 'win' or 'lose'
        """
        if game_key not in self.data:
            self.data[game_key] = []

        self.data[game_key].append({
            "steps": actions,
            "outcome": outcome
        })

    def best_action_for_state(self, game_key, state_hash):
        """
        Returns an action that historically led to better outcomes 
        for the given state_hash, or None if no data found.
        This is a naive approach: we look at all records that had this state_hash,
        see the outcome, and pick the best outcome's action.
        """
        if game_key not in self.data:
            return None

        # Collect potential actions
        action_scores = {}
        # Example: if an action leads to a win, give +1, lose => -1
        for game_record in self.data[game_key]:
            for step in game_record["steps"]:
                st_hash, act = step
                if st_hash == state_hash:
                    score = +1 if game_record["outcome"] == 'win' else -1
                    if act not in action_scores:
                        action_scores[act] = 0
                    action_scores[act] += score

        if not action_scores:
            return None

        # Return the action with the highest score
        best_act = max(action_scores, key=action_scores.get)
        return best_act
