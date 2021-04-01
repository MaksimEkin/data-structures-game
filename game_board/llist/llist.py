import sys

""""handles all the stuff that happens inside the tunnels"""


class LList_Handler():
    def __init__(self):
        self.ants = {}
        self.chambers = []
        self.tunnels = {}
        self.food = {}
        self.under_attack = {}
        self.num_ants = 1
        self.num_chambers = 0
        self.highest_id = 0

    @classmethod
    def from_gamestate(cls, gamestate):
        handler = cls()
        handler.ants = gamestate['ants']
        handler.chambers = gamestate['chambers']
        handler.tunnels = gamestate['tunnels']
        handler.food = gamestate['food']
        handler.under_attack = gamestate['under_attack']
        handler.num_ants = gamestate['num_ants']
        handler.num_chambers = gamestate['num_chambers']
        handler.highest_id = gamestate['highest_id']
        return handler

    def digTunnel(self, chamber, dest=None):
        if chamber not in self.chambers:
            raise ValueError
        if dest is not None and dest not in self.chambers:
            raise ValueError
        if self.tunnels[chamber][0] < 2:
            self.tunnels[chamber] += 1
        self.tunnels[chamber][1][1] = dest

    def digChamber(self, connecting_chbr=None):
        if connecting_chbr is not None:
            if connecting_chbr not in self.chambers:
                raise ValueError
        self.num_chambers += 1
        self.highest_id += 1
        newchamberID = "chamber" + str(self.highest_id)
        self.chambers.append(newchamberID)
        if connecting_chbr is None and self.num_chambers == 1:
            self.tunnels[newchamberID] = [0, ['Head', None]]
        elif self.tunnels[connecting_chbr][0] == 2 or (self.tunnels[connecting_chbr][1][0] == 'Head'
                                                       and self.tunnels[connecting_chbr][0] == 1):
            self.tunnels[newchamberID] = [1, [connecting_chbr, None]]
            self.tunnels[connecting_chbr][1][1] = newchamberID
            self.under_attack[newchamberID] = False
            self.food[newchamberID] = {'crumb': 0, 'berry': 0, 'donut': 0}
            self.ants[newchamberID] = 0

    def fillTunnel(self, chamber):
        if chamber in self.chambers.keys():
            if self.tunnels[chamber][1][1]:
                self.tunnels[chamber] -= 1
                self.tunnels[chamber][1][1] = None
        else:
            raise ValueError

    def fillChamber(self, chamber):
        if chamber in self.chambers.keys():
            if self.num_chambers > 1:
                self.tunnels[self.tunnels[chamber][1][0]][1][1] = None
            self.tunnels.pop(chamber)
            self.chambers.remove(chamber)
            self.food.pop(chamber)
            self.num_chambers -= 1
        else:
            raise ValueError

    def to_gamestate(self):
        outdict = {'ants': self.ants, 'chambers': self.chambers, 'tunnels': self.tunnels, 'food': self.food,
                   'under_attack': self.under_attack, 'num_ants': self.num_ants, 'num_chambers': self.num_chambers,
                   'highest_id': self.highest_id}
        return outdict


"""API callable function, makes a new 'linked list' structure for a game"""


def makeNewGame():
    handler = LList_Handler()
    return handler.to_gamestate()


"""API callable function; given a game state and an action (array), returns the game state
with the action performed"""


def doAction(game, action):
    a = ['dig_tunnel', 'fill_tunnel', 'dig_chamber', 'fill_chamber']
    actionable = LList_Handler.from_gamestate(game)
    if action[0] == a[0]:
        actionable.dig_tunnel(a[1], a[2])
        return actionable.to_gamestate()
    elif action[0] == a[1]:
        actionable.fill_tunnel(a[1])
        return actionable.to_gamestate()
    elif action[0] == a[2]:
        actionable.dig_chamber(a[1])
        return actionable.to_gamestate()
    elif action[0] == a[3]:
        actionable.fill_chamber(a[1])
        return actionable.to_gamestate()
    else:
        raise ValueError
