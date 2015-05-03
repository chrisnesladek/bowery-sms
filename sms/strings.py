#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Common abbreviations to help reduce the text message length.
abbreviations = {
    'minutes': 'min',
    'seconds': 'sec',
    'meters': 'm',
    'Chest-to-Bar': 'CTB',
    'Chest to Bar': 'CTB',
    'Pull-Ups': 'PU',
    'Pull Ups': 'PU',
    'as many rounds and reps as possible': 'AMRAP',
    'as many rounds as possible': 'AMRAP',
    'as many reps as possible': 'AMRAP',
    'back squat': 'BS',
    'hang squat clean': 'HSC',
    'hang clean': 'HC',
    'clean and jerk': 'C&J',
    'every minute on the minute': 'EMOM',
    'front squat': 'FS',
    'hand stand push up': 'HSPU',
    'knees to elbow': 'KTE',
    'muscle ups': 'MU',
    'overhead squat': 'OHS',
    'power clean': 'PC',
    'push press': 'PP',
    'push-press': 'PP',
    'push jerk': 'PJ',
    'power snatch': 'PSN',
    'squat clean': 'SC',
    'sumo deadlift high pull': 'SDHP',
    'toes to bar': 'TTB',
    'push-ups': 'PU',
    'snatch': 'SN',
    'squat': 'SQ',
    'kettlebell': 'KB',
    'clean': 'CLN',
    'deadlift': 'DL',
    ' one': ' 1',
    ' two': ' 2',
    ' three': ' 3',
    ' four': ' 4',
    ' five': ' 5',
    'rounds for time of': 'RFT',
    'rounds for time': 'RFT',
    'alternating': 'alt',
    'sit-ups': 'SU',
    'Sit-Ups': 'SU',
    'Double-Unders': 'DU',
    }

# This is ugly. I should do this better.
# Todo: Actually learn about encoding.
special_chars = {
    '’': "'",
    '‘': "'",
    '“': '"',
    '”': '"',
    '…': '...',
    '\xc2\xa0' : ' ',
    }

# Possible headers
headers = {
    'Open Workout:': 'Experienced Workout:',
    'Experienced Level:': 'Open Level:',
    'Experienced/Open': None,
    'Workout:': None,
    }

# List of positive reinforcement salutations
salutations = [
    'Nice work!',
    ]

# List of available commands
commands = {
    'Subscribe': 'Receive the day\'s workout every morning.',
    'Stop': 'Stop receiving the day\'s workout every morning.',
    'WOD': 'Receive the day\'s workout.',
    '+ [result]': 'Log your result from today\'s workout. e.g. "+ 4 rounds"',
    '[activity]: [result]': 'Log a PR for a movement or activity. e.g. "Clean 1RM: 135lbs"',
    '? [activity]': 'Search your history for a given activity or movement. e.g. "Clean 1RM"',
    }