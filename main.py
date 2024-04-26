from blobs import Blobservation


# Simple test to check how a simulation works
generation0 = [
    {'x': 0, 'y': 4, 'size': 3},
    {'x': 0, 'y': 7, 'size': 5},
    {'x': 2, 'y': 0, 'size': 2},
    {'x': 3, 'y': 7, 'size': 2},
    {'x': 4, 'y': 3, 'size': 4},
    {'x': 5, 'y': 6, 'size': 2},
    {'x': 6, 'y': 7, 'size': 1},
    {'x': 7, 'y': 0, 'size': 3},
    {'x': 7, 'y': 2, 'size': 1}]
blobs = Blobservation(8)
blobs.populate(generation0)
blobs.print_state()
blobs.move()
blobs.print_state()
blobs.move()
blobs.print_state()
blobs.move(1000)
blobs.print_state()
