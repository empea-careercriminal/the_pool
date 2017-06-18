import os
from sys import exit
from glob import glob 
import pickle

from player import *
from styles import *
from agent import *
from mount import *
from trap import *
from chest import *
from item import *
from game_map import *

player = None


class Menu(object):

    def __init__(self, styles):
        self.styles = styles


    def main_menu(self):
        '''Show the start menu to add and load players.'''
        print """
        Neues Spiel   (0)
        Spiel laden   (1)
        Spiel beenden (2)
        """
        action = raw_input("Bitte waehle eine Option: ")
        print "\n"
        styles.flower()
        return action

    def locations_menu(self, location, game_map):
        '''Show the players position and available locations to go to next.'''
        self.location = location
        self.game_map = game_map
        #print "Du bist an diesem Ort: %s " % the_game.player.location
        styles.flower()
        print "Von hier kannst du folgende Orte besuchen: "
        
        #print "Die Map: %s" % self.game_map

        poi_list = []
        for k, v in self.game_map.scenemapper.iteritems():
            if v == self.location:
                poi_list.append(k)

        def poi_format(poi_list):
            for i in poi_list:
                print """    %s""" % i
        
        poi_formatted = poi_format(poi_list)
        styles.flower()
        action = raw_input("Bitte waehle eine Option: ")
        return poi_formatted, action #returns a tuple

    def agents_menu(self, agent):
        '''Show the name and stats of agents at the current location. Update the stats in fights and allow to check on agents by typing [agent_name] + [untersuchen]'''
        self.agent = agent
        print "An diesem Ort befindet sich folgender weitere Spieler: %s" % self.agent.name
        action = raw_input('Wenn du mehr ueber diesen Spieler erfahren moechtest, dann tippe seinen Namen ein: \n >>')



class Navigation(object):
    """Take in Map and the player handle all possible locations, track current location, find next possible location."""
    def __init__(self, gamemap):
        #self.player = player
        self.gamemap = gamemap

    def next_scene(self, last_scene):
        """return a list of possible next scenes"""
        available_locations = {}
        for k, v in the_navigation.gamemap.scenemapper.iteritems():
            available_locations.setdefault(v, []).append(k)
              
        for k, v in available_locations.iteritems():
            if the_game.player.location in v:
                return k
        
        '''
        #noble way to check if string is in dictionary       
        if 'start' in [x for v in available_locations.values() for x in v]:
            #do something
        '''

class Engine(object):
    """Takes in the navigation, plays the game, handles savegames and players."""
    def __init__(self, navigation, the_player, the_menu):
        self.navigation = navigation
        self.player = the_player
        self.menu = the_menu

    def playgame(self):
        """Show Textblock followed by Menu of available options."""
        styles.flower()
        action = str(the_menu.main_menu())
        if action is '0':
            self.player = self.create_player()
            raw_input('Moechtest du diesen Spieler jetzt abspeichern, dann druecke bitte die Enter Taste.')
            self.savegame()
            self.player = self.loadinstant(self.player)
        elif action is '1':
            self.player = self.loadgame()
            print "\nHier beginnt deine Reise, %s. ich oeffne jetzt das Tor zu deinem Abenteuer.\n" % self.player.name
        elif action is '2':
            print 'Auf wiedersehen.'
            exit(1)
        else:
            print "Das habe ich nicht verstanden"
        
        while True:
            # original way to access the_navigation.next_scene(self.player[8])
            #print "Du bist im %s. Hier gibt es folgende Orte, an denen du dich umsehen koenntest." % the_navigation.next_scene(self.player[8])

            #detour to access the same thing via the_menu
            #unpacking return values tuple
            poi_formatted, action = the_menu.locations_menu(the_navigation.next_scene(self.player.location), game_map)

            if action in the_navigation.gamemap.scenemapper:
                '''call player movement if a valid location next location has been picked'''
                self.player.location = self.player.move(action)
                the_navigation.gamemap.locations[self.player.location].enter()

            else:
                print "Diese Eingabe habe ich nicht verstanden. Probiere es noch einmal."

            ''' implement all this:
                #debug: print the_game.player.location            
            elif action in agents_dict
                #move to next location
                pass
            elif action in chests_dict
                #move to next location
                pass
            elif action in doors_dict
                #move to next location
                pass
            elif action in items_dict
                #move to next location
                pass
            elif action in mounts_dict
                #move to next location
                pass
            elif action in traps_dict
                #move to next location
                pass
            else:
                '''

    def create_player(self):
        """define a new player name, gender and generate hitpoints randomly"""
        while True:
            try:
                self.player = Player(raw_input('Dein Name: '), raw_input('Dein Geschlecht: '), float(raw_input('Dein Alter: ')), raw_input('Dein Start: '), None, None)
                print '\nDein Name lautet %s, du bist %s und %s jahre alt.' % (self.player.name, self.player.gender, int(self.player.age))
                print 'Daraus ergibt sich eine Angriffswert von %s und du erhaelts %s Lebenspunkte zu Beginn dieses Spiels.\n' % (int(self.player.strength), int(self.player.hitpoints))
                return self.player
            except ValueError:
                print "Bitte gebe hier nur Zahlen und keine Buchstaben ein."

    def savegame(self):
        """write current state entire game session to a file."""
        pickle_out = open ('savegame_' + str(self.player.name) + '.txt', 'w+')
        pickle.dump(self.player, pickle_out)
        #self.player = pickle.dump(self.player, pickle_out)
        pickle_out.close()
        print "\nSpieler >> %s << gespeichert.\n" % self.player.name

    def loadgame(self):
        """Restore a game session based on a raw input of player name string."""
        while True:
            savegames = glob("savegame*") #creates a list of available savegames on disk
            print "Du moechtest ein Spiel laden? In Ordnung, bitte waehle deinen Spieler:\n"
            shortname_list = []
            for entries in savegames:
                #to do: format the strings to only display the name of the player
                shortname = "%s" % entries.rstrip('.txt').lstrip('savegame_')
                print shortname
                shortname_list.append(shortname)
            action = raw_input('>> ')
            if action in shortname_list:
                print 'savegame_' + action + '.txt'
                pickle_in = open ('savegame_' + action + '.txt', 'r+')
                self.player = pickle.load(pickle_in)
                styles.flower()
                print "In Ordnung, %s. Legen wir los." % self.player.name
                print '''
                Hier siehst du Details ueber deinen Helden:
                
                Name:           %s
                Geschlecht:     %s
                Alter:          %s Jahre
                Angriff:        %s
                Lebenspunkte:   %s
                Reittier:       %s

                Aktueller Ort:  %s
                ''' % (self.player.name, self.player.gender, int(self.player.age), int(self.player.strength), int(self.player.hitpoints), self.player.mount, self.player.location)
                
                return self.player
            else:
                print "Bitte gib den Namen des Spielers richtig ein."  


    def loadinstant(self, player):
        """Restore a game session based on a passed player name string."""
        player = self.player.name
        pickle_in = open ('savegame_' + player + '.txt', 'r+')
        restored_player = pickle.load(pickle_in)
        styles.flower()
        print "In Ordnung, %s. Legen wir los." % restored_player.name
        print '''
        Hier siehst du Details ueber deinen Helden:
        
        Name:           %s
        Geschlecht:     %s
        Alter:          %s Jahre
        Angriff:        %s
        Lebenspunkte:   %s
        Reittier:       %s

        Aktueller Ort:  %s
        ''' % (self.player.name, self.player.gender, int(self.player.age), int(self.player.strength), int(self.player.hitpoints), self.player.mount, self.player.location)

        return restored_player

    def delete_player(self, name):
        """truncate one players data from disk"""
        pass


styles = Styles(None)
the_menu = Menu(styles)
the_menu.styles.flower

the_player = Player(1, 2, 3, 4, 5, 6)
the_navigation = Navigation(game_map)
the_game = Engine(the_navigation, the_player, the_menu)

the_game.playgame()

'''
knockout = Knockout()
knockout.enter()

ende = Ende()
ende.enter()
'''
