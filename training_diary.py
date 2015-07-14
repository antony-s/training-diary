#! /usr/bin/env python3

import argparse
import datetime
import json
import os, errno
import time

class TrainingDiary(object):
    DIARY_DATA_LOC = os.path.expanduser('~/.training_diary')
    DIARY_DATA_FILE = 'data.json'
    SESSION_TYPES = {
        'e': {'name': 'Easy'},
        'i': {'name': 'Interval'},
        't': {'name': 'Tempo'},
        'l': {'name': 'Long'},
        'r': {'name': 'Race'},
        'f': {'name': 'Fartlek'}
    }

    DISTANCE_UNITS = {
        'km': {'name': 'Kilometres'},
        'mi': {'name': 'Miles'}
    }

    def i_get_session_type(self):
        print('\nPlease select a session type from the following:\n')
        for key, session_type in self.SESSION_TYPES.items():
            print('{name} ({key})'.format(key=key, name=session_type['name']))
        return input('Session code: ')

    def i_get_distance_unit(self):
        print('\nPlease select units for distance from the following:\n')
        for key, distance_unit in self.DISTANCE_UNITS.items():
            print('{name} ({key})'.format(key=key, name=distance_unit['name']))
        return input('Distance unit code: ')

    def i_get_distance(self, selected_distance_unit):
        return float(input('\nPlease enter distance ({}): '.format(selected_distance_unit)))

    def i_get_duration(self):
        """Return duration in seconds."""
        duration = time.strptime(input('\nPlease enter your time HH:MM:SS: '), '%H:%M:%S')
        return datetime.timedelta(hours=duration.tm_hour, minutes=duration.tm_min,
            seconds=duration.tm_sec).total_seconds()

    def i_get_note(self):
        """Return a session note."""
        return input('\nPlease enter any session notes: ')

    def save_session(self, session):
        diary_path = os.path.join(self.DIARY_DATA_LOC, self.DIARY_DATA_FILE)
        diary_data = []
        try:
            os.makedirs(self.DIARY_DATA_LOC)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(self.DIARY_DATA_LOC):
                pass
            else:
                raise
        try:
            with open(diary_path) as f:
                try:
                    diary_data = json.load(f)
                except ValueError:
                    if not os.fstat(f.fileno()).st_size:
                        pass
                    else:
                        raise
        except FileNotFoundError as e:
            pass

        diary_data.append(session)

        with open(diary_path, 'w') as f:
            json.dump(diary_data, f)
            print('Session saved')

    def interactive(self):
        selected_session_type = self.i_get_session_type()
        selected_distance_unit = self.i_get_distance_unit()
        distance = self.i_get_distance(selected_distance_unit)
        duration = self.i_get_duration()
        note = self.i_get_note()
        session = {
            'selected_session_type': selected_session_type,
            'selected_distance_unit': selected_distance_unit,
            'distance': distance,
            'duration': duration,
            'note': note
        }
        self.save_session(session)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process training session data')
    parser.add_argument('-i', '--interactive', nargs='?', const=True, default=False, help='Run in interactive mode')
    args = parser.parse_args()
    training_diary = TrainingDiary()
    if args.interactive:
        training_diary.interactive()
    # TODO: Add training-session args
