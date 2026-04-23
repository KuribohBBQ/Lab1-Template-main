from model import (
    Location,
    Portal,
    EmptyEntity,
    Wizard,
    Goblin,
    Crystal,
    WizardMoves,
    GoblinMoves,
    GameAction,
    GameState,
)
from agents import WizardSearchAgent
import heapq
from dataclasses import dataclass


class WizardDFS(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location #location of wizard
        portal_loc: Location #location of portal

    paths: dict[SearchState, list[WizardMoves]] = {} 
    search_stack: list[SearchState] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState: 
        initial_wizard_loc = self.initial_game_state.active_entity_location #initial location of wizard
        initial_wizard = self.initial_game_state.get_active_entity()    

        #creates new game state with a new location of the wizard
        
        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity() #replace the initial location of wizard with an empty entity
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = []
        self.search_stack = [initial_search_state]

    #probably checks if current state is goal
    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc
    

    """
    if the agent does not have a live plan the game will request a next_search_expansion and then pass 
    all of the successors of the returned node to process_search_expansion and repeat this until a plan 
    is determined or no next_search_expansion is returned. It is up to the agent to use this information to maintain their search
    """


    def next_search_expansion(self) -> GameState | None:
        # TODO: YOUR CODE HERE
        """
        -check if search stack is none
        -pop last element from search stack
        -looks like game.py already does the looping through neighbors
        
                successors = GameTransitions.get_successors(search_expansion_node)
                self.number_search_expansions += 1
                for action, target in successors:
                    if not isinstance(action, WizardMoves):
        """

        if not self.search_stack:
            return None

        next_search = self.search_stack.pop()
        
        #check if the next search is the goal
        #if true, add it to plan
        if self.is_goal(next_search):
            self.plan = self.paths[next_search]
            return None

        return self.search_to_game(next_search)



    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        """
        -convert source and target to search state
        -add action to path
        -add to stack the target

        """
        current_source = self.game_to_search(source)
        current_target = self.game_to_search(target)

        #if target is already in paths, ignore it
        if current_target in self.paths:
            return None
        
        #current_target is a key in dictionary
        #add action to list  
        #current source is current node we are currently expanding
        #+ action to current_source makes path to reach current target 
        self.paths[current_target] = [action] + self.paths[current_source] 
        self.search_stack.append(current_target)




class WizardBFS(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, list[WizardMoves]] = {}
    search_stack: list[SearchState] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = []
        self.search_stack = [initial_search_state]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def next_search_expansion(self) -> GameState | None:
        # TODO: YOUR CODE HERE
        """
        -BFS is FIFO, so pop the first element in stack instead of last
        -if search is not none, pop first elemement in stack
        """
        if not self.search_stack:
            return None
        
        next_search = self.search_stack.pop(0)

        if self.is_goal(next_search):
            self.plan = self.paths[next_search]
            return None
        
        return self.search_to_game(next_search)



    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:

        current_source = self.game_to_search(source)
        current_target = self.game_to_search(target)

        if current_target in self.paths:
            return None
        
        self.paths[current_target] = [action] + self.paths[current_source]
        self.search_stack.append(current_target)





class WizardAstar(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    
    #key is searchState, value is tuple
    paths: dict[SearchState, tuple[float, list[WizardMoves]]] = {}
    #list of tuples (heuristic distance, SearchState)
    search_pq: list[tuple[float, SearchState]] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = 0, []
        self.search_pq = [(0, initial_search_state)]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def cost(self, source: GameState, target: GameState, action: WizardMoves) -> float:
        return 1

    def heuristic(self, target: GameState) -> float:
        """
        -given gamestate
        -convert gamestate to searchstate to get wizard and portal locations
        -use manhattan distance
        -returns a float
        """
        #convert target gamestate to searchstate
        searchState = self.game_to_search(target)


        #wizard location
        wiz_loc = searchState.wizard_loc
        #portal location
        port_loc = searchState.portal_loc

        #row distance between portal and wizard
        row_dist = abs(port_loc.row - wiz_loc.row)
        #col distance between portal and wizard
        col_dist = abs(port_loc.col - wiz_loc.col)

        manhat_dist = float(row_dist + col_dist)

        return manhat_dist

        

    def next_search_expansion(self) -> GameState | None:
        """
        -get the highest priority item from search_pq
        -probably do mostly same thing as DFS and BFS

        """
        if not self.search_pq:
            return None
        
        #pop item with highest priority in search_pq
        priority, curr_searchState = heapq.heappop(self.search_pq)

        if self.is_goal(curr_searchState):

            #self.paths[curr_searchState][0] = priority
            #self.paths[curr_searchState][1] = list of paths
            self.plan = self.paths[curr_searchState][1]
            return None

        return self.search_to_game(curr_searchState)

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        """
        -convert source and target to gamestate
        -f(n) = g(n) + h(n)
        -g(n) is cost from start to target node
        -h(n) is how far target node is from destination

        """

        current_source = self.game_to_search(source)
        current_target = self.game_to_search(target)

        #current cost to get to current position
        source_cost = self.paths[current_source][0]
        #path so far to get to current position
        source_path = self.paths[current_source][1]
        #moving to target adds 1 to cost.
        g_n = source_cost + self.cost(source, target, action)

        #heuristic cost to reach target
        h_n = self.heuristic(target)

        #priority
        f_n = g_n + h_n

        #check if target is already in paths
        if current_target in self.paths:
            #if true, check if new path is worse than old path
            old_path_cost = self.paths[current_target][0]

            #if new path cost is worse than old path, skip this node
            #because if we can get to this same node with less cost, then new path is better
            #otherwise, don't add to path
            if g_n >= old_path_cost:
                return None
            
        #path to reach target
        path_to_target = [action] + source_path
        #add path to target to paths
        #value is tuple (cost, path)
        self.paths[current_target] = (g_n, path_to_target)

        #add to heap
        #tuple(priority, SearchState)
        heapq.heappush(self.search_pq, (f_n, current_target))




class CrystalSearchWizard(WizardSearchAgent):
    # TODO: YOUR CODE HERE
    """
    -use A star
    -now have multiple crystals
    -collect crystals and then go to portal
    -search order by closest crystals?
    -use manhatten distance to determine which crystal is closer to wizard
    """
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location
        crystals_loc: tuple[Location,...]

    #key is searchState, value is tuple
    paths: dict[SearchState, tuple[float, list[WizardMoves]]] = {}
    #list of tuples (heuristic distance, SearchState)
    search_pq: list[tuple[float, SearchState]] = []
    initial_game_state: GameState

    
    def search_to_game(self, search_state: SearchState) -> GameState:
        """
        -get all crystal locations from initial game state
        -go through crystals locations in initial game state and remove them
        -go through crystals_loc and put the crystals back in new_game_state
        """

        #get all intial crystal locations
        initial_crystals_loc = self.initial_game_state.get_all_entity_locations(Crystal)
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = self.initial_game_state

        #remove wizard from the initial location
        new_game_state = new_game_state.replace_entity(
            initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
        )

        #remove all initial crystal locations
        for init_crystal in initial_crystals_loc:
            new_game_state = new_game_state.replace_entity(
                init_crystal.row, init_crystal.col,EmptyEntity()
            )

        #put crystals back in depending on crystals_loc
        for remaining_crystal in search_state.crystals_loc:
            new_game_state = new_game_state.replace_entity(remaining_crystal.row, 
                remaining_crystal.col, Crystal())
            
        #place the wizard in the search state's location
        new_game_state = new_game_state.replace_entity(
            search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
        ).replace_active_entity_location(search_state.wizard_loc)


        return new_game_state
        

    #adjust for crystal location 
    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        crystal_locs = tuple(sorted(game_state.get_all_entity_locations(Crystal)))
        return self.SearchState(wizard_loc, portal_loc, crystal_locs)


    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def is_goal(self, state: SearchState) -> bool:
        return len(state.crystals_loc) == 0 and state.wizard_loc == state.portal_loc
    
    def is_crystal(self, state: SearchState) -> bool:
        return state.wizard_loc in state.crystals_loc
    
    def cost(self, source: GameState, target: GameState, action: WizardMoves) -> float:
        return 1


    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = 0, []
        self.search_pq = [(0, initial_search_state)]

    def heuristic(self, target: GameState) -> float:
        """
        -given gamestate
        -convert gamestate to searchstate to get wizard and portal locations
        -use manhattan distance
        -returns a float
        """
        #convert target gamestate to searchstate
        searchState = self.game_to_search(target)


        #wizard location
        wiz_loc = searchState.wizard_loc
        #portal location
        port_loc = searchState.portal_loc
        #crystal locations
        crystals_loc = searchState.crystals_loc

        #return the manhat dist to the nearest crystal
        if crystals_loc:
            nearest_crystal_dist = min(
            abs(crystal.row - wiz_loc.row) + abs(crystal.col - wiz_loc.col)
            for crystal in crystals_loc
        )
            return float(nearest_crystal_dist)

        #row distance between portal and wizard
        row_dist = abs(port_loc.row - wiz_loc.row)
        #col distance between portal and wizard
        col_dist = abs(port_loc.col - wiz_loc.col)

        manhat_dist = float(row_dist + col_dist)

        return manhat_dist
    

    def next_search_expansion(self) -> GameState | None:
        # TODO YOUR CODE HEREs
        """
        -get the highest priority item from search_pq
        -probably do mostly same thing as DFS and BFS

        """
        if not self.search_pq:
            return None
        
        #pop item with highest priority in search_pq
        priority, curr_searchState = heapq.heappop(self.search_pq)

        
        if self.is_crystal(curr_searchState):
            self.plan = self.paths[curr_searchState][1]
            return None

        if self.is_goal(curr_searchState):
            #self.paths[curr_searchState][0] = priority
            #self.paths[curr_searchState][1] = list of paths
            self.plan = self.paths[curr_searchState][1]
            return None

        return self.search_to_game(curr_searchState)

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        """
        -convert source and target to gamestate
        -f(n) = g(n) + h(n)
        -g(n) is cost from start to target node
        -h(n) is how far target node is from destination

        """

        current_source = self.game_to_search(source)
        current_target = self.game_to_search(target)

        #current cost to get to current position
        source_cost = self.paths[current_source][0]
        #path so far to get to current position
        source_path = self.paths[current_source][1]
        #moving to target adds 1 to cost.
        g_n = source_cost + self.cost(source, target, action)

        #heuristic cost to reach target
        h_n = self.heuristic(target)

        #priority
        f_n = g_n + h_n

        #check if target is already in paths
        if current_target in self.paths:
            #if true, check if new path is worse than old path
            old_path_cost = self.paths[current_target][0]

            #if new path cost is worse than old path, skip this node
            #because if we can get to this same node with less cost, then new path is better
            #otherwise, don't add to path
            if g_n >= old_path_cost:
                return None
            
        #path to reach target
        path_to_target = [action] + source_path
        #add path to target to paths
        #value is tuple (cost, path)
        self.paths[current_target] = (g_n, path_to_target)

        #add to heap
        #tuple(priority, SearchState)
        heapq.heappush(self.search_pq, (f_n, current_target))



class SuboptimalCrystalSearchWizard(CrystalSearchWizard):

    def heuristic(self, target) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError
