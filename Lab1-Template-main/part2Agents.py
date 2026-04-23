from model import (
    Location,
    Portal,
    Wizard,
    Goblin,
    Crystal,
    WizardMoves,
    GoblinMoves,
    GameAction,
    GameState,
)
from agents import ReasoningWizard
from dataclasses import dataclass


class WizardGreedy(ReasoningWizard):
    def evaluation(self, state: GameState) -> float:
        #wizards location
        wizard_loc = state.active_entity_location
        #portal location
        portal_loc = state.get_all_tile_locations(Portal)[0]
        #location of goblins -> list
        goblin_locs = state.get_all_entity_locations(Goblin)

        portal_dist = abs(portal_loc.row - wizard_loc.row) + abs(portal_loc.col - wizard_loc.col)
        #value determined by how far portal is from wizard
        value = state.score - portal_dist

        #make the closest goblin the first goblin for now
        closest_goblin = goblin_locs[0]
        closest_goblin_dist = abs(closest_goblin.col - wizard_loc.col) + abs(closest_goblin.row - wizard_loc.row)
        for goblin in goblin_locs:
            current_goblin_dist = abs(goblin.col - wizard_loc.col) + abs(goblin.row - wizard_loc.row)
            if current_goblin_dist < closest_goblin:
                closest_goblin = goblin
                closest_goblin_dist = current_goblin_dist

        if closest_goblin_dist == 0:
            value -= 1000
        elif 1 <= closest_goblin_dist <= 3:
            value -= 100
        elif 4 <= closest_goblin_dist <= 9:
            value -= 50
        elif 10 <= 15:
            value -= 20
        return float(value)




class WizardMiniMax(ReasoningWizard):
    max_depth: int = 2

    def evaluation(self, state: GameState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def is_terminal(self, state: GameState) -> bool:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        raise NotImplementedError


    def minimax(self, state: GameState, depth: int):
        # TODO YOUR CODE HERE
        raise NotImplementedError


class WizardAlphaBeta(ReasoningWizard):
    max_depth: int = 2

    def evaluation(self, state: GameState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def is_terminal(self, state: GameState) -> bool:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        raise NotImplementedError


    def alpha_beta_minimax(self, state: GameState, depth: int):
        # TODO YOUR CODE HERE
        raise NotImplementedError




class WizardExpectimax(ReasoningWizard):
    max_depth: int = 2

    def evaluation(self, state: GameState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def is_terminal(self, state: GameState) -> bool:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        raise NotImplementedError


    def expectimax(self, state: GameState, depth: int):
        # TODO YOUR CODE HERE
        raise NotImplementedError
