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

"""Tier1 upgrade values in the format (tier1_count, upgrade_percent)"""
tier1_upgrades_available = [
    (100, 100),
    (200, 200)
]

"""Tiers upgrade values in the format (tier2_count, upgrade_percent)"""
tier2_upgrades_available = [
    (150, 150),
    (250, 250)
]


def tier1_bonus():
    """This method returns the bonus for each tier1 crafted"""
    return 0.01


def tier2_bonus():
    """This method returns the bonus for each tier2 crafted"""
    return 0.18


def create_state(tier1_count=0, tier2_count=0,
                 tier1_upgrades=[], tier2_upgrades=[],
                 curr_bonus=0):
    """This method creates a state tuple from the given inputs"""
    return (tier1_count, tier2_count,
            tier1_upgrades, tier2_upgrades,
            curr_bonus)


def tier1_count(state):
    """This method returns the number of tier1s in the given state"""
    return state[0]


def tier2_count(state):
    """This method returns the number of tier2s in the given state"""
    return state[1]


def current_bonus(state):
    """This method returns the bonus of the given state"""
    return state[4]


def calc_bonus(tier1_count, tier2_count,
               tier1_upgrades, tier2_upgrades):

    # print("{},{}".format(tier1_count, tier2_count))

    if (tier1_count < 0):
        return 0

    return (1 + (tier1_count * tier1_bonus())) * \
        (1 + (tier2_count * tier2_bonus())) - 1


def next_state(state):
    """This method determines the next best state, given the input state"""
    (tier1_count, tier2_count,
        tier1_upgrades, tier2_upgrades, curr_bonus) = state

    new_tier2_bonus = calc_bonus(tier1_count - 8, tier2_count + 1,
                                 tier1_upgrades, tier2_upgrades)

    new_tier1_bonus = calc_bonus(tier1_count + 1, tier2_count,
                                 tier1_upgrades, tier2_upgrades)

    # print("{}, {}, curr: {:.2f} tier1: {:.2f} tier2: {:.2f}".format(
    #     tier1_count, tier2_count, curr_bonus * 100,
    #     new_tier1_bonus * 100,
    #     new_tier2_bonus * 100))

    if (new_tier2_bonus <= curr_bonus and
            new_tier1_bonus > new_tier2_bonus):
        return next_state(create_state(tier1_count + 1, tier2_count,
                                       tier1_upgrades, tier2_upgrades,
                                       new_tier1_bonus))
    else:
        new_state = create_state(tier1_count - 8, tier2_count + 1,
                                 tier1_upgrades, tier2_upgrades,
                                 new_tier2_bonus)

        print("At {:>4} T1, new counts {:>4} T1, {:>4} T2, bonus {:.2f}%"
              .format(tier1_count, tier1_count - 8,
                      tier2_count + 1, new_tier2_bonus * 100))

        return new_state


def main(options, args):
    """main loop of the progam"""

    # for i in range(38, 50):
    #     print("{},{},{:.2f},{},{},{:.2f}".format(
    #           i, 8, calc_bonus(i, 8, [], []) * 100,
    #           i - 8, 9, calc_bonus(i - 8, 9, [], []) * 100))

    # sys.exit(0)

    state = create_state()

    while (tier1_count(state) < options.max):
        state = next_state(state)
        # if (tier1_count(state) < options.max):
        #     print("{:6d},{:6d} => {:.2f}".format(
        #         tier1_count(state), tier2_count(state),
        #         round(current_bonus(state) * 100, 2)))


if __name__ == '__main__':
    try:
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'], version='$Id$')
        parser.add_option('-m', '--max', action='store',
                          type='int', default=10000,
                          help='Maximum tier1 count [10000 default]')
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
