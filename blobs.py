from copy import copy


class Blobservation:

    def __init__(self, h, w=None):
        self.h = h
        if w is None:
            self.w = h
        else:
            self.w = w
        # The smaller the number, the higher the priority
        self.dir_prior = {
            (0, -1):    1,
            (1, -1):    2,
            (1, 0):     3,
            (1, 1):     4,
            (0, 1):     5,
            (-1, 1):    6,
            (-1, 0):    7,
            (-1, -1):   8
        }
        self.blobs = []

    def populate(self, blobs_list):
        """Creates blobs according given list with dict elements.
        Element format: {'x': Int, 'y': Int, 'size': Int}"""
        for new_blob in blobs_list:
            if not self.check_new_blob(new_blob["x"], new_blob["y"], new_blob["size"]):
                raise Exception("Invalid population data")

        for new_blob in blobs_list:
            if not self.check_new_blob(new_blob["x"], new_blob["y"], new_blob["size"]):
                # If at least one given blob includes incorrect data - all blobs are rejected
                break
            for blob in self.blobs:
                # x and y are swapped because of assumptions of the author of this exercise (x-vertical, y-horizontal)
                if new_blob["y"] == blob.x and new_blob["x"] == blob.y:
                    # If a new blob is creating at position any other blob exists, then they are merged.
                    blob.size += new_blob['size']
                    break
            else:
                self.blobs.append(Blob(new_blob))

    def move(self, turns=1):
        """Executes a given number of movements turns.
        In each turn all blobs move simultaneously (after all moves, their states are checked)."""
        if turns < 1 or isinstance(turns, bool):
            raise Exception("Invalid value")
        for i in range(turns):
            smallest_size = self.smallest_blob_size()
            # Find next moves for each blob (except the smallest ones)
            for blob in self.blobs:
                if blob.size == smallest_size:
                    blob.update_move([0, 0])
                    continue
                # find target blob and movement
                target_blob, movement = self.find_target(blob)
                blob.update_move(movement)
            # Execute movements for each blob (except the smallest ones)
            for blob in self.blobs:
                blob.move()
            # Check for blobs fusions
            for blob in self.blobs:
                self.check_fusion(blob)

    def check_fusion(self, blob):
        """Checks if a given blob fuzes with any other blob.
        It happens when they are at the same position."""
        enemies_list = self.blobs.copy()
        enemies_list.remove(blob)
        for enemy in enemies_list:
            # Check if 2 blobs are at the same position
            if blob.x == enemy.x and blob.y == enemy.y:
                new_size = blob.size + enemy.size
                blob.size = new_size
                self.blobs.remove(enemy)

    def find_target(self, blob):
        """Finds the nearest target according to other assumptions for a given blob.
        Returns a found target blob object and the next movement towards it."""
        enemies_list = self.blobs.copy()
        enemies_list.remove(blob)
        target_blob = copy(blob)
        # initial target blob's size has the lowest priority
        target_blob.size = 0
        # initial min distance is random but high enough to be greater than possible to reach
        distance_min = self.w * self.h
        # initial movement value has the lowest priority
        movement = [-1, -1]
        for enemy in enemies_list:
            # Check size condition
            if enemy.size < blob.size:
                # Enemy size is smaller
                enemy_distance, first_move = self.calc_dist_first_move(blob, enemy)
                # Check if distance is the smallest so far
                if enemy_distance < distance_min:
                    # New smallest distance, new target
                    distance_min = enemy_distance
                    target_blob = copy(enemy)
                    movement = first_move
                elif enemy_distance == distance_min and enemy.size > target_blob.size:
                    # The same distance but bigger size so far
                    target_blob = copy(enemy)
                    movement = first_move
                elif enemy_distance == distance_min and enemy.size == target_blob.size:
                    # The same distance and size
                    if self.dir_prior[tuple(first_move)] < self.dir_prior[tuple(movement)]:
                        # Higher direction priority
                        target_blob = copy(enemy)
                        movement = first_move
        return target_blob, movement

    @staticmethod
    def calc_dist_first_move(blob, target):
        """Calculates distance (number of movements) and first move as [x, y]."""
        blob_moving = copy(blob)
        movements = 0   # counting movements
        is_first_move = True
        first_move = None
        movement_x, movement_y = 0, 0
        while blob_moving.x != target.x or blob_moving.y != target.y:
            # Calculating number of movements to the target and the first move.
            # Each loop iteration the blob_moving moves towards the target.
            move_done = False
            if blob_moving.x != target.x:
                distance_x = target.x - blob_moving.x
                movement_x = int(distance_x / abs(distance_x))  # define direction (always 1 or -1)
                blob_moving.x += movement_x
                move_done = True
                movements += 1
            if blob_moving.y != target.y:
                distance_y = target.y - blob_moving.y
                movement_y = int(distance_y / abs(distance_y))  # define direction (always 1 or -1)
                blob_moving.y += movement_y
                if not move_done:
                    movements += 1
            if is_first_move:
                first_move = [movement_x, movement_y]
            is_first_move = False
        return movements, first_move

    def print_state(self):
        """Prints sorted list of current blobs' states in format: [x, y, size]."""
        # x and y are swapped because of assumptions of the author of this exercise (x-vertical, y-horizontal)
        print(sorted([[blob.y, blob.x, blob.size] for blob in self.blobs]))

    def check_new_blob(self, x, y, size):
        """Checks if blob attributes (x, y, size) are correct types and within valid ranges."""
        if not (isinstance(x, int) and isinstance(y, int) and isinstance(size, int)):
            raise Exception("Invalid data type. Expected Integers only.")
        if isinstance(x, bool) or isinstance(y, bool) or isinstance(size, bool):
            raise Exception("Invalid data type. Boolean instead of Integer.")
        if x >= self.h or x < 0:
            raise Exception("Invalid x coordinate of a blob.")
        if y >= self.w or y < 0:
            raise Exception("Invalid y coordinate of a blob.")
        if size < 1 or size > 20:
            raise Exception("Invalid blob's size.")
        return True

    def smallest_blob_size(self):
        """Calculates the smallest size among all blobs."""
        if not self.blobs:
            return 0
        smallest_size = self.blobs[0].size
        for blob in self.blobs:
            if blob.size < smallest_size:
                smallest_size = blob.size
        return smallest_size


class Blob:

    def __init__(self, blob_properties):
        # x and y are swapped because of assumptions of the author of this exercise (x-vertical, y-horizontal)
        self.x = blob_properties["y"]
        self.y = blob_properties["x"]
        self.size = blob_properties["size"]
        self.next_move = [0, 0]

    def update_move(self, movement):
        """Updates values [x, y] for the next movement to be executed for a blob."""
        # movement = [x, y]
        self.next_move = movement

    def move(self):
        """Executes a blob's movement with the last updated values [x, y]."""
        self.x += self.next_move[0]
        self.y += self.next_move[1]
