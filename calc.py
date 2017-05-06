#!/usr/bin/env python
"""
SYNOPSIS

    calc [-h, --help] [-m, --maxcups N]

DESCRIPTION
    This script calculates the optimum upgrade purchase path
    in the Office Space minigame.

EXAMPLES

    TODO: Show some examples of how to use this script.


AUTHOR

    TODO: Tony Nelson <hhubris@gmail.com>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

import sys
import os
import traceback
import optparse
import math

"""Thermos upgrade values in the format (thermos_count, upgrade_percent)"""
thermos_upgrades_available = [
    (100, 100),
    (200, 200)
]

"""Briefcae upgrade values in the format (briefcase_count, upgrade_percent)"""
briefcase_upgrades_available = [
    (150, 150),
    (250, 250)
]


def thermos_bonus():
    """This method returns the bonus for each thermos crafted"""
    return 0.01


def briefcase_bonus():
    """This method returns the bonus for each briefcase crafted"""
    return 0.12


def create_state(thermos_count=0, briefcase_count=0,
                 thermos_upgrades=[], briefcase_upgrades=[],
                 curr_bonus=0):
    """This method creates a state tuple from the given inputs"""
    return (thermos_count, briefcase_count,
            thermos_upgrades, briefcase_upgrades,
            curr_bonus)


def thermos_count(state):
    """This method returns the number of thermoses in the given state"""
    return state[0]


def briefcase_count(state):
    """This method returns the number of briefcases in the given state"""
    return state[1]


def current_bonus(state):
    """This method returns the bonus of the given state"""
    return state[4]


def calc_bonus(thermos_count, briefcase_count,
               thermos_upgrades, briefcase_upgrades):

    # print("{},{}".format(thermos_count, briefcase_count))

    if (thermos_count < 0):
        return 0

    return (1 + (thermos_count * thermos_bonus())) * \
        (1 + (briefcase_count * briefcase_bonus())) - 1


def next_state(state):
    """This method determines the next best state, given the input state"""
    (thermos_count, briefcase_count,
        thermos_upgrades, briefcase_upgrades, curr_bonus) = state

    new_briefcase_bonus = calc_bonus(thermos_count - 8, briefcase_count + 1,
                                     thermos_upgrades, briefcase_upgrades)

    new_thermos_bonus = calc_bonus(thermos_count + 1, briefcase_count,
                                   thermos_upgrades, briefcase_upgrades)

    # print("{}, {}, curr: {:.2f} thermos: {:.2f} briefcase: {:.2f}".format(
    #     thermos_count, briefcase_count, curr_bonus * 100,
    #     new_thermos_bonus * 100,
    #     new_briefcase_bonus * 100))

    if (new_briefcase_bonus <= curr_bonus and
            new_thermos_bonus > new_briefcase_bonus):
        return next_state(create_state(thermos_count + 1, briefcase_count,
                                       thermos_upgrades, briefcase_upgrades,
                                       new_thermos_bonus))
    else:
        return create_state(thermos_count - 8, briefcase_count + 1,
                            thermos_upgrades, briefcase_upgrades, 
                            new_briefcase_bonus)


def main(options, args):
    """main loop of the progam"""

    # for i in range(38, 50):
    #     print("{},{},{:.2f},{},{},{:.2f}".format(
    #           i, 8, calc_bonus(i, 8, [], []) * 100,
    #           i - 8, 9, calc_bonus(i - 8, 9, [], []) * 100))

    # sys.exit(0)

    state = create_state()

    while (thermos_count(state) < options.max):
        state = next_state(state)
        if (thermos_count(state) < options.max):
            print("{:6d},{:6d} => {:.2f}".format(
                thermos_count(state), briefcase_count(state),
                round(calc_bonus(thermos_count(state), briefcase_count(state),
                                 [], []) * 100, 2)))


if __name__ == '__main__':
    try:
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'], version='$Id$')
        parser.add_option('-m', '--max', action='store',
                          type='int', default=10000,
                          help='Maximum thermos count [10000 default]')
        parser.add_option('-v', '--verbose', action='store_true',
                          default=False, help='verbose output')
        (options, args) = parser.parse_args()
        main(options, args)
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)
