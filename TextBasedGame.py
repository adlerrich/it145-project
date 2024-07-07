# Richard Adler - IT140 Final Project
# I took a class based approach primarily because I had written a skeleton
# of the app a while before module 6, and didn't make the connection between
# dictionaries and game logic before the module. I also thought to use classes primarily to keep
# track of items for both the rooms and the player, and to handle how
# state changes for the player would interact with the room logic. Having a
# list of valid rooms makes generating lists such as hte inventory to compare
# to at the end of the game or the player's valid movements means I just have
# to reference the list of rooms, and ensures that so long as a room is
# initialized using the class and added to the list, I don't need to write any
# additional code to handle it. Using class methods allows for modification
# of information directly to the class as well, meaning I don't need to draw
# on external variables beyond finding the current room.

# define a player class to handle inventory, current position, valid movements,
# what options are available, and the movement function
# valid movements is empty as it will be filled using a list comprehension later
class Player:

    def __init__(self):
        self.inventory = []
        self.coordinates = [0, 1]
        self.has_key = False
        self.valid_movements = []

    # print the available options to the player, formatted using the current room later in the code
    @staticmethod
    def display_options(room):
        return input('You are in the {}\nCurrently, your inventory is {}\nYou can move in the following directions: '
                     '{}\nPick Up Item: Item\nExit Game: Quit\nEnter Movement or Option:\n'.format(room.room_name,
                                                                                                   Player.inventory,
                                                                                                   room.valid_movements))

    # movement function we copy the coordinates into a movement buffer to avoid moving to an illegal room even after
    # checking that the direction inputted is valid, I still found another check necessary to avoid this issue add or
    # subtract 1 from the x or y coordinate based on the given direction, with a special check to ensure the room at
    # (2,2) functions correctly as long as the movement buffer is found to be valid by comparing the movement buffer
    # to the list of valid coordinates set the players coordinates equal to the movement buffer else we print the
    # list of available directions and go back to the top of the game loop
    def move(self, movement_option, room):
        movement_buffer = self.coordinates.copy()

        if movement_option == 'north':
            if movement_buffer == [0, 2] and self.has_key:
                movement_buffer[0] += 2
                return movement_buffer
            else:
                movement_buffer[0] += 1
        elif movement_option == 'south':
            movement_buffer[0] -= 1
        elif movement_option == 'west':
            movement_buffer[1] += 1
        elif movement_option == 'east':
            movement_buffer[1] -= 1
        else:
            print("Please input one of the following directions: {}".format(room.valid_movements))

        # coordinates are in tuples, and briefly converted out of a list to ensure that the check returns a correct
        # answer, as comparing lists does not necessarily check for ordering
        if tuple(movement_buffer) in self.valid_movements:
            return movement_buffer
        else:
            print("Please input one of the following directions: {}".format(room.valid_movements))
            return self.coordinates

    # option handling
    def option_handling(self, player_option, room):

        # first, check for a movement option to pass directly into the above movement function
        if player_option.lower() in ['north', 'south', 'west', 'east']:
            if player_option.capitalize() in room.valid_movements:
                Player.coordinates = self.move(player_option.lower(), room)

        # next, check for other valid options, item will pick the item up if the room currently has an item,
        # else it will state that the room does not have an item
        elif player_option.lower() == 'item' and room.has_item:
            self.inventory.append(room.item)
            print("You picked up the {}!".format(room.item))
            room.has_item = False
        elif not room.has_item and player_option.lower() == 'item':
            print("{} has no item".format(room.room_name))

        # tell the player their option is invalid if it does not match with a valid option
        else:
            print("Please enter a valid option")

        # format output to be a little cleaner, adding a bit of whitespace in between game menus
        print("\n\n")


# initialize a room class, containing the room name, movements available from that room, the item the room contains,
# if the item has been picked up, and the room's coordinates
class Room:

    def __init__(self, room_name, valid_movements, item, room_coordinates):
        self.room_name = room_name
        self.valid_movements = valid_movements
        self.item = item
        self.has_item = True
        self.room_coordinates = room_coordinates


# child class of room for the locked room, inherits everything from the room class
class LockedRoom(Room):

    def __init__(self, room_name, valid_movements, item, room_coordinates):
        super().__init__(room_name, valid_movements, item, room_coordinates)

    # adds the will_unlock method, which will be called upon entry to the room
    # checks if the player has the appropriate item, and appends north to the valid room directions,
    # and (2,2) to the player's valid movements
    def will_unlock(self, player_object):
        if "Rusty Key" in player_object.inventory:
            player_object.has_key = True
            player_object.valid_movements.append((2, 2))
            self.valid_movements.append('North')


# method to determine what room the player is currently in, uses a for loop to iterate over a list of rooms,
# checking the coordinates against the players, and returning the appropriate room None is returned if the function
# does not find a room, but with the above contingencies, we cannot go out of out bounds and in theory, there should
# be no way of returning None
def find_room(room_list, player_list):
    player_tuple = tuple(player_list)
    for room in room_list:
        if room.room_coordinates == player_tuple:
            return room
        else:
            continue
    return None


# initialize the individual rooms using the Room class, the locked room with the LockedRoom class, Entryway and
# Cathedral have there has_item flag set to false, as these are the start and end points of the game respectively
Entryway = Room('Entryway', ['North', 'East', 'West'], None, (0, 1))
Entryway.has_item = False
Sanctuary = Room('Sanctuary', ['North', 'West'], 'Human Vestige', (0, 0))
Confessional = Room('Confessional', ['North', 'South', 'West'], 'Rusty Key', (1, 0))
Vestibule = Room('Vestibule', ['North', 'South', 'East'], 'Divine Blessing', (1, 1))
Lobby = Room('Lobby', ['North', 'South', 'East'], 'Human Vestige', (2, 1))
Commons = LockedRoom('Church Commons', ['East'], 'Cloranthy Leaves', (0, 2))
Quarters = Room('Archbishop Quarters', ['East'], 'Ancient Tome', (2, 2))
Storage_Area = Room('Storage Area', ['North', 'South', 'West'], 'Sword', (2, 0))
Choir_Loft = Room('Choir Loft', ['South', 'West'], 'Shield', (3, 0))
Cathedral = Room("Cathedral", None, None, (3, 1))
Cathedral.has_item = False

# organize rooms into a list for easy iteration later, that way we can make a single pass through the list
# and obtain whatever information we need using only the current room
rooms = [
    Entryway,
    Sanctuary,
    Confessional,
    Vestibule,
    Lobby,
    Commons,
    Quarters,
    Choir_Loft,
    Storage_Area,
    Cathedral
]

# generate a list of game items, to compare with the player inventory at the end of the game,
# excluding None type items as it's only a placeholder for rooms without an item
items = [room.item for room in rooms if room.item is not None]

# initialize a player
Player = Player()
# generate a list of valid movements by using the coordinates of each room
# excluding (2, 2) as that room is locked and handled by other logic
Player.valid_movements = [room.room_coordinates for room in rooms if room.room_coordinates != (2, 2)]

# boolean flag to determine if we should stop the game
game_running = True

# checking to make sure this python script is meant to be run
if __name__ == "__main__":
    # while loop using the game_running bool to determine if the iteration should execute
    while game_running:
        # find the current room using the list of rooms and the player's coordinates
        current_room = find_room(rooms, Player.coordinates)
        # check to see if we're in the boss room, if we are we set game_running to false stopping the loop,
        # and compare the current inventory to the item list by sorting both and checking for equality
        # gives one of two endings based on whether the player has successfully picked up all items
        # then breaks the loop to ensure the game quits and does not execute the remaining code in the loop
        if current_room == Cathedral:
            game_running = False
            items.sort()
            Player.inventory.sort()
            if items == Player.inventory:
                print("With the lord vessel full of humanity, the curse does not affect you. Feeling invigorated from "
                      "the chloranty leaves,\nyou speak the passages of the ancients. Your blade glows brightly. As "
                      "you drive it into the Archbishop, the darkness lifts.\nFinally, the dark soul is no more.")
                break
            else:
                print("Without all of the items in the church, you cannot withstand the dark souls power this close "
                      "to it.\nYour journey ends here.")
                break
        # check to see if we're in the locked room, will_unlock is called here to determine if the new movements
        # should be added on sets the player.has_key to true, ensuring that once the new movements have been
        # appended, they will not get reattached repeatedly
        if current_room == Commons and not Player.has_key:
            Commons.will_unlock(Player)
            current_room = find_room(rooms, Player.coordinates)

        # if we are not in the boss room, incur the standard option handling
        # built into the player class
        option = Player.display_options(current_room)
        if option.lower() == 'quit':
            game_running = False
        else:
            Player.option_handling(option, current_room)
