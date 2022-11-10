# qlearningAgents.py
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update
      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        self.QValues = util.Counter() #indexed by state and action

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        return self.QValues[state, action]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        values = [self.getQValue(state, action) for action in self.getLegalActions(state)]
        if (values):
            return max(values)
        else:
            return 0.0

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legal_actions = self.getLegalActions(state) #all the legal actions

        value = self.getValue(state)
        for action in legal_actions:
            if (value == self.getQValue(state, action)):
                return action


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None

        if (util.flipCoin(self.epsilon)):
            action = random.choice(legalActions)
        else:
            action = self.getPolicy(state)
        """
        What is the best action to take in the state. Note that because
        we might want to explore, this might not coincide with getAction
        Concretely, this is given by

        policy(s) = arg_max_{a in actions} Q(s,a)

        If many actions achieve the maximal Q-value,
        it doesn't matter which is selected.
        """

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        
    # def getValue(self, state):
    #     What is the value of this state under the best action?
    #     Concretely, this is given by

    #     V(s) = max_{a in actions} Q(s,a)
        newQValue = (1 - self.alpha) * self.getQValue(state, action) #new Qvalue
        newQValue += self.alpha * (reward + (self.discount * self.getValue(nextState)))
        # file = open("QLearning.txt", "a")
        # file.write("current state")
        # file.write("\n")
        # file.write(str(state))
        # file.write("\n")
        # file.write("action taken")
        # file.write("\n")
        # file.write(str(action))
        # file.write("\n")
        # file.write("\n")
        # file.write("next state")
        # file.write("\n")
        # file.write(str(nextState))
        # file.write("\n")
        # file.write("\n")
        # file.write("reward given current action and next state")
        # file.write("\n")
        # file.write(str(reward))
        # file.write("\n")
        # file.write("\n")
        # file.write("current state value, next state value")
        # file.write("\n")
        # file.write(str(self.getValue(state)))
        # file.write(", ")
        # file.write(str(self.getValue(nextState)))
        # file.write("\n")
        # file.write("\n")
        # file.write("current Q, Next Q")
        # file.write("\n")
        # file.write(str(self.QValues[state, action]))
        # file.write(", ")
        self.QValues[state, action] = newQValue 
        # file.write(str(self.QValues[state, action]))
        # file.write("\n")
        # file.write("============================")
        # file.write("\n")
        # file.close()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        # print(state)
        # print(action)
        return action
      

class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
          # Returns simple features for a basic reflex Pacman:
          # - whether food will be eaten
          # - how far away the next food is
          # - whether a ghost collision is imminent
          # - whether a ghost is one step away
        features = self.featExtractor.getFeatures(state,action)
        QValue = 0.0
        # print(action)
        # print("entered get q value")
        for feature in features:
          # file = open("ApproxQLearning.txt", "a")
          # file.write("feature: " +str(features[feature]))
          # file.write("\n")
          # file.write("weight: "+str(self.weights[feature]))
          QValue += self.weights[feature] * features[feature]
        #   file.write("\n")
        #   file.write(str(QValue))
        #   file.write("\n")
        #   file.write("======================================")
        #   file.write("\n")
        # file.write("END OF CALCULATING QVALUE FOR ONE STATE, ACTION PAIR")
        # file.write("\n")
        # print(QValue)
        return QValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        QValue = 0
        # file = open("ApproxQLearning.txt", "a")
        # file.write(str(state))
        # file.write("\n")
        # file.write("action taken: " + str(action))
        # file.write("\n")
        # file.write(str(nextState))
        # file.write("\n")
        # file.write("reward: " + str(reward))
        # file.write("\n")
        # file.write("V-value of current state: " + str(self.getValue(state)))
        # file.write("\n")
        # file.write("V-value of next state: " + str(self.getValue(nextState)))
        # file.write("\n")
        # file.write("Q value of the action and state pair: " + str(self.getQValue(state, action)))
        # file.write("\n")
        # min_dist = 1000000.0
        # cap = state.getCapsules()
        # x, y = state.getPacmanPosition()
        # return_cap_coor = (0,0)
        # for i in cap:
        #   dist_loc = (((x-i[0])**2)+((y-i[1])**2))**(1/2)
        #   if dist_loc < min_dist:
        #     min_dist = dist_loc
        #     return_cap_coor = i
        #   else:
        #     return_cap_coor = return_cap_coor
        # min_dist_x, min_dist_y = return_cap_coor
        # if min_dist_x != 0 and min_dist_y != 0:
        #   reward = reward/(((min_dist_x-x)**2)+((min_dist_y-y)**2))**(1/2)
        # file.write("updated reward: " + str(reward))
        # file.write("\n")
        difference = reward + (self.discount * self.getValue(nextState) - self.getQValue(state, action))
        # file.write("difference: " + str(difference))
        # file.write("\n")
        features = self.featExtractor.getFeatures(state, action)
        for feature in features:
          # file.write(feature)
          # file.write("\n")
          # file.write("current weight: " + str(self.weights[feature]))
          # file.write("\n")
          # file.write("value of feature: " + str(features[feature]))
          # file.write("\n")
          self.weights[feature] += self.alpha * features[feature] * difference
        #   file.write("updated weight: " + str(self.weights[feature]))
        #   file.write("\n")
        # file.close()


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
