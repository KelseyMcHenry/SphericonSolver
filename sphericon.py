import random


class Sphericon:

    def __init__(self):
        self.single_track = True
        self.marbles = ['b', 'b', 'b', 'b', 'b', 'b', 'r', 'r', 'r', 'r', 'r', 'r', 'g', 'g', 'g', 'g', 'g', 'g', 'y', 'y', 'y', 'y', 'y', 'y']
        random.shuffle(self.marbles)

        # init tracks
        self.track1 = Track(3, 1)
        self.track2 = Track(3, 2)
        self.track3 = Track(6, 3)
        self.track4 = Track(6, 4)
        self.track5 = Track(3, 5)
        self.track6 = Track(3, 6)
        self.track_container = [self.track1, self.track2, self.track3, self.track4, self.track5, self.track6]
        for track in self.track_container:
            contents = [self.marbles.pop(0) for _ in range(track.get_size())]
            track.set_contents(contents)
            # print(f"TRACK: {track.get_contents()}")

        # define orientation of 2 halves
        # definition starts in top right intersection and rotates clockwise
        # the halves are viewed from opposite perspectives, ie one is face towards you, one is face away.
        self.half1 = [(2, "start"), (4, "start"), (6, "start"), (6, "end"), (4, "end"), (2, "end")]
        self.half2 = [(1, "end"), (3, "end"), (5, "end"), (5, "start"), (3, "start"), (1, "start")]

        # init all the pointers
        for address1, address2 in zip(self.half1, self.half2):
            Track.link_two_tracks(self.track_container[address1[0] - 1], address1[1], self.track_container[address2[0] - 1], address2[1])

    def __repr__(self):
        already_printed = []
        ret_val = ""
        for track in self.track_container:
            if track.get_id() not in already_printed:
                ret_val += str(track) + " , "
                already_printed.append(track.get_id())

                head = track
                next_track = track.end_link[0]
                # if you enter at start, leave at end, vice versa
                entered_via = track.end_link[1]
                while next_track is not None and next_track is not head:
                    ret_val += str(next_track) + " , "
                    already_printed.append(next_track.get_id())
                    if entered_via == "start":
                        entered_via = next_track.end_link[1]
                        next_track = next_track.end_link[0]
                    else:
                        entered_via = next_track.start_link[1]
                        next_track = next_track.start_link[0]

                ret_val += '...'
                ret_val += '\n'
        return ret_val

    def is_solved(self):
        return all([all([track.get_contents()[0] == item for item in track.get_contents()]) for track in self.track_container]) and self.track1 == self.track2 and self.track5 == self.track6

    def update_links(self):
        for address1, address2 in zip(self.half1, self.half2):
            Track.link_two_tracks(self.track_container[address1[0] - 1], address1[1], self.track_container[address2[0] - 1], address2[1])

    def rotate_cw(self):
        end = self.half1[-1]
        remainder = self.half1[:-1]
        self.half1.clear()
        self.half1.append(end)
        self.half1.extend(remainder)
        self.update_links()

    def rotate_ccw(self):
        front = self.half1[0]
        remainder = self.half1[1:]
        self.half1.clear()
        self.half1.extend(remainder)
        self.half1.append(front)
        self.update_links()

    def shift_marbles_cw(self, track):
        pass

    def shift_marbles_ccw(self, track):
        pass


class Track:

    def __init__(self, size, track_id, contents=[]):
        self.contents = contents
        self.end_link = None, None
        self.start_link = None, None
        self.track_id = track_id
        self.size = size

    def __eq__(self, other):
        return set(self.contents) == set(other.get_contents())

    def __str__(self):
        # return f"ID: {self.track_id}|| {self.start_link[0].get_id()}:{self.start_link[1]} <-- {self.contents} -- > {self.end_link[0].get_id()}:{self.end_link[1]}"
        return f"{self.contents}"

    def get_size(self):
        return self.size

    def get_id(self):
        return self.track_id

    def set_contents(self, contents):
        self.contents = contents

    @staticmethod
    # attach the pos1 of track1 to the pos2 of track2
    def link_two_tracks(track1, pos1, track2, pos2):
        if pos1 == "end":
            track1.end_link = (track2, pos2)
        else:
            track1.start_link = (track2, pos2)

        if pos2 == "end":
            track2.end_link = (track1, pos1)
        else:
            track2.start_link = (track1, pos1)

    def get_contents(self):
        return self.contents

    def get_reverse_contents(self):
        return self.contents.__reversed__()


def main():
    s = Sphericon()
    print(s)
    s.rotate_cw()
    print(s)
    s.rotate_ccw()
    print(s)
    # print(s.is_solved())

if __name__ == '__main__':
    main()

