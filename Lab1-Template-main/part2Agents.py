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
        elif 10 <= closest_goblin_dist <= 15:
            value -= 20
        return float(value)




class WizardMiniMax(ReasoningWizard):
    """
    -In WizardMiniMax you should implement this generalized MiniMax as well as an evaluation function.
     In order to expand the minimax search tree, unlike in part 1 ReasoningAgents get direct access to
      calculating GameState successors using the self.get_successors function.

    -wizard 
    """
    max_depth: int = 2
    #helper function to calculate manhattan distance 
    def manhatt_dist(self, entity1: Location, entity2: Location) -> int:
        distance = abs(entity1.col - entity2.col) + abs(entity1.row - entity2.row)
        return distance

    def evaluation(self, state: GameState) -> float:
        #wizards location
        wizard_loc = state.active_entity_location

        #portal location
        portal_loc = state.get_all_tile_locations(Portal)[0]
        #location of goblins -> list
        goblin_locs = state.get_all_entity_locations(Goblin)

        #location of crystals -> list
        crytsal_locs = state.get_all_entity_locations(Crystal)

        # portal_dist = abs(portal_loc.row - wizard_loc.row) + abs(portal_loc.col - wizard_loc.col)
        portal_dist = self.manhatt_dist(wizard_loc, portal_loc)
        #value determined by how far portal is from wizard
        value = state.score - portal_dist

        #make the closest goblin the first goblin for now
        closest_goblin = goblin_locs[0]
        # closest_goblin_dist = abs(closest_goblin.col - wizard_loc.col) + abs(closest_goblin.row - wizard_loc.row)
        closest_goblin_dist = self.manhatt_dist(closest_goblin, wizard_loc)
        for goblin in goblin_locs:
            # current_goblin_dist = abs(goblin.col - wizard_loc.col) + abs(goblin.row - wizard_loc.row)
            current_goblin_dist = self.manhatt_dist()
            if current_goblin_dist < closest_goblin_dist:
                closest_goblin = goblin
                closest_goblin_dist = current_goblin_dist

       
        #make closest distance to crystal very big
        closest_crystal_dist = 10000
    
        if len(crytsal_locs) != 0:
            for crystal in crytsal_locs:
                # current_crystal_dist = abs(crystal.col - wizard_loc.col) + abs(crystal.row - wizard_loc.row)
                current_crystal_dist = self.manhatt_dist(crystal, wizard_loc)
                if current_crystal_dist < closest_crystal_dist:
                    closest_crystal_dist = current_crystal_dist



        if closest_goblin_dist == 0:
            value -= 1000
        elif 1 <= closest_goblin_dist <= 3:
            value -= 100
        elif 4 <= closest_goblin_dist <= 9:
            value -= 50
        elif 10 <= closest_goblin_dist <= 15:
            value -= 20

        #wizard values life more than death by goblin
        if closest_crystal_dist == 0:
            value += 100
        elif 1 <= closest_crystal_dist <= 3:
            value += 50
        elif 4 <= closest_crystal_dist <= 9:
            value += 20
        elif 10 <= closest_crystal_dist <= 15:
            value += 5

        return float(value)

    def is_terminal(self, state: GameState) -> bool:
        """
        -checks if game is over
        -game is over when wizard reaches portal or is dead
        """
        #active entity might be goblin, so get all entities that are wizards
        wizard_locs = state.get_all_entity_locations(Wizard)
        portal_loc = state.get_all_tile_locations(Portal)[0]

        #if length of wizard locs is 0, then wizard is dead and game is over
        if len(wizard_locs) == 0:
            return True
        else:
            #if wizard is at portal, then the game is over
            wizard_location = wizard_locs[0]
            if wizard_location == portal_loc:
                return True




    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        #get a list of all possible moves
        #moves is a tuple
        #tuple(GameAction, GameState)
        possible_moves = self.get_successors(state)

        #dictionary to hold score. Key is action, and value is the score
        scores: dict[WizardMoves, float] = {}

        #for each possible action, measure the return score
        for action, gamestate in possible_moves:
            #call minimax
            calculated_score = self.minimax(gamestate, 1)
            #place the return score into the dictionary
            scores[action] = calculated_score
        
        #return the highest score
        return max(scores, key=scores.get)


    def minimax(self, state: GameState, depth: int):
        # maximizer = 0
        # minimizer = 0
        #check if we reached terminal
        if self.is_terminal(state) or depth == self.max_depth:
            return self.evaluation(state)
        
        #get active entity
        current_entity = state.get_active_entity 
        #get list of possible nodes or moves to explore
        possible_moves = self.get_successors

        #if active entity is wizard, then we want the highest possible value
        if isinstance(Wizard):
            max_value = float('-inf')
            for move, gamestate in possible_moves:
                possible_values = self.minimax(gamestate, depth + 1)
                max_value = max(max_value, possible_values)
            return max_value
        
        #if active entity is goblin, then we want lowest possible value
        if isinstance(Goblin):
            min_value = float('inf')
            for move, gamestate in possible_moves:
                possible_values = self.minimax(gamestate, depth + 1)
                min_value = min(min_value, possible_values)
            return min_value
        
        return self.evaluation(state)
        
        

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
