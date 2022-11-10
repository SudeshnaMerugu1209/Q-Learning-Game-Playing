# featureExtractors.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"Feature extractors for Pacman game states"

from os import stat
from game import Directions, Actions
from ghostAgents import GhostAgent
import util

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state,action)] = 1.0
        return feats

class CoordinateExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closestFood(pos, food, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    - how far away ghost is
    - if ghost is scared
    - how far is a scared ghost
    """
    # def getFeatures(self, state, action):
    # # extract the grid of food and wall locations and get the ghost locations
    #     food = state.getFood()
    #     walls = state.getWalls()
    #     ghosts = state.getGhostPositions()
    #     capsulesLeft = len(state.getCapsules())
    #     scaredGhost = []
    #     activeGhost = []
    #     features = util.Counter()
    #     for ghost in state.getGhostStates():
    #         if not ghost.scaredTimer:
    #             activeGhost.append(ghost)
    #         else:
    #             #print (ghost.scaredTimer)
    #             scaredGhost.append(ghost)
        
    #     pos = state.getPacmanPosition()
    #     def getManhattanDistances(ghosts): 
    #         return map(lambda g: util.manhattanDistance(pos, g.getPosition()), ghosts) 
            
    #     distanceToClosestActiveGhost = distanceToClosestScaredGhost = 0
    #     '''
    #     if activeGhost:
    #         distanceToClosestActiveGhost = min(getManhattanDistances(activeGhost))
    #     else: 
    #         distanceToClosestActiveGhost = float("inf")
    #     distanceToClosestActiveGhost = max(distanceToClosestActiveGhost, 5)
    #     '''
        
    #     '''else:
    #         distanceToClosestScaredGhost = 0 # I don't want it to count if there aren't any scared ghosts
    #         features["dist-to-closest-scared-ghost"] = -2*distanceToClosestScaredGhost
    #     '''
        
    #     features["bias"] = 1.0
        
    #     # compute the location of pacman after he takes the action
    #     x, y = state.getPacmanPosition()
    #     dx, dy = Actions.directionToVector(action)
    #     next_x, next_y = int(x + dx), int(y + dy)
        
    #     # count the number of ghosts 1-step away
    #     features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)
        
    #     # if there is no danger of ghosts then add the food feature
    #     if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
    #         features["eats-food"] = 1.0
        
    #     dist = closestFood((next_x, next_y), food, walls)
    #     if dist is not None:
    #     # make the distance a number less than one otherwise the update
    #     # will diverge wildly
    #         features["closest-food"] = float(dist) / (walls.width * walls.height) 
    #         if scaredGhost: # and not activeGhost:
    #             distanceToClosestScaredGhost = min(getManhattanDistances(scaredGhost))
    #             if activeGhost:
    #                 distanceToClosestActiveGhost = min(getManhattanDistances(activeGhost))
    #             else:
    #                 distanceToClosestActiveGhost = 10	
    #             features["capsules"] = capsulesLeft
    #         #features["dist-to-closest-active-ghost"] = 2*(1./distanceToClosestActiveGhost)
    #         if distanceToClosestScaredGhost <=8 and distanceToClosestActiveGhost >=2:#features["#-of-ghosts-1-step-away"] >= 1:
    #             features["#-of-ghosts-1-step-away"] = 0
    #             features["eats-food"] = 0.0
    #             #features["closest-food"] = 0
        
    #     #print(features)
    #     features.divideAll(10.0)
    #     return features
    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()
        features = util.Counter()
        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        cap = state.getCapsules()
        for i in cap:
            if (next_x,next_y) == i:
                isScared = True
                features["both_ghosts_scared"] = 1.0

        #if ghost scared then params
        numAgents = state.getNumAgents()
        for i in range(1,numAgents):
            ghostState = state.getGhostState(i)
            # g_p = state.getGhostPosition(i)
            isScared = ghostState.scaredTimer > 0.0
            if isScared:
                features["g_scared" + str(i)] = 1.0
                food[int(ghosts[i-1][0])][int(ghosts[i-1][1])] = True
                ghosts[i-1] = (19.0,10.0)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)

        # distance between capsules decreased?
        cap = state.getCapsules()
        indices = []
        for i in cap:
            food[i[0]][i[1]] = True
        def scanner_for_power_pellets():
            min_dist = 1000000.0
            cap = state.getCapsules()
            for i in cap:
                dist_loc = (((next_x-i[0])**2)+((next_y-i[1])**2))**(1/2)
                if dist_loc < min_dist:
                    min_dist = dist_loc
            return min_dist

        check_for_closest_pellet = scanner_for_power_pellets()
        if check_for_closest_pellet < 4:
            features["capsule_close_by?"] = 1.0
        #     for i in range(walls.width):
        #         for j in range(walls.height):
        #             food[i][j] = False
        #     food[x][y] = True

            
        features.divideAll(10.0)                

        return features
