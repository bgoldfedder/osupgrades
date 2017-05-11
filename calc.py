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
    {'type': 'tier1', 'count': 150, 'bonus': 100},
    {'type': 'tier1', 'count': 375, 'bonus': 100},
    {'type': 'tier1', 'count': 450, 'bonus': 100}
]

"""Tiers upgrade values in the format (tier2_count, upgrade_percent)"""
tier2_upgrades_available = [
    {'type': 'tier2', 'count': 65, 'bonus': 200},
    {'type': 'tier2', 'count': 112, 'bonus': 200},
    {'type': 'tier2', 'count': 150, 'bonus': 300},
    {'type': 'tier2', 'count': 282, 'bonus': 300}
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


def calc_bonus(tier1_count, tier2_count):

    # print("{},{} {} --- {}".format(tier1_count, tier2_count,
    #                                tier1_upgrades, tier2_upgrades))

    if (tier1_count < 0 or tier2_count < 0):
        return 0

    base_bonus = (1 + (tier1_count * tier1_bonus())) * \
        (1 + (tier2_count * tier2_bonus()))

    return base_bonus - 1


def calc_upgraded_state(state, upgrade_list):
    if (len(upgrade_list) == 0):
        return None

    (tier1_count, tier2_count,
        tier1_upgrades, tier2_upgrades, curr_bonus) = state

    price = upgrade_list[0]

    if (price['type'] == 'tier1'):
        tier1_count = tier1_count - price['count']
        if (tier1_count < 0):
            return None

        tier1_upgrades = list(tier1_upgrades)
        tier1_upgrades.append(price)
    elif(price['type'] == 'tier2'):
        tier2_count = tier2_count - price['count']
        if (tier2_count < 0):
            return None

        tier2_upgrades = list(tier2_upgrades)
        tier2_upgrades.append(price)
    else:
        raise "Unknown type: " + price.type

    new_bonus = (1 + calc_bonus(tier1_count, tier2_count)) * \
        ((price['bonus'] / 100) + 1) - 1

    if (new_bonus > curr_bonus):

        del upgrade_list[0]

        return create_state(tier1_count, tier2_count,
                            tier1_upgrades, tier2_upgrades, new_bonus)

    return None


def display_action(action,
                   old_tier1_count, old_tier2_count,
                   new_tier1_count, new_tier2_count,
                   new_bonus):

    print(("At {:>4},{:>4}, {:>15}, new counts {:>4} T1, " +
          " {:>4} T2, new bonus {:.2f}%")
          .format(old_tier1_count, old_tier2_count,
                  action,
                  new_tier1_count, new_tier2_count,
                  new_bonus * 100))


def next_state(state):
    """This method determines the next best state, given the input state"""

    upgraded_state = calc_upgraded_state(state, tier1_upgrades_available)

    if (upgraded_state):
        display_action("Buy T1 Upgrade",
                       state[0], state[1],
                       upgraded_state[0], upgraded_state[1],
                       upgraded_state[4])

        return upgraded_state

    upgraded_state = calc_upgraded_state(state, tier2_upgrades_available)

    if (upgraded_state):

        display_action("Buy T2 Upgrade",
                       state[0], state[1],
                       upgraded_state[0], upgraded_state[1],
                       upgraded_state[4])

        return upgraded_state

    (tier1_count, tier2_count,
        tier1_upgrades, tier2_upgrades, curr_bonus) = state

    new_tier2_bonus = calc_bonus(tier1_count - 8, tier2_count + 1)

    new_tier1_bonus = calc_bonus(tier1_count + 1, tier2_count)

    # print("{}, {}, curr: {:.2f} tier1: {:.2f} tier2: {:.2f}".format(
    #     tier1_count, tier2_count, curr_bonus * 100,
    #     new_tier1_bonus * 100,
    #     new_tier2_bonus * 100))

    if (new_tier2_bonus <= curr_bonus and
            new_tier1_bonus > new_tier2_bonus):

        bonus_to_beat = max(new_tier1_bonus, curr_bonus)
        return next_state(create_state(tier1_count + 1, tier2_count,
                                       tier1_upgrades, tier2_upgrades,
                                       bonus_to_beat))
    else:
        new_state = create_state(tier1_count - 8, tier2_count + 1,
                                 tier1_upgrades, tier2_upgrades,
                                 new_tier2_bonus)

        # print("At {:>4},{:>4} T1, new counts {:>4} T1, {:>4} T2, bonus {:.2f}%"
        #       .format(tier1_count, tier2_count, tier1_count - 8,
        #               tier2_count + 1, new_tier2_bonus * 100))

        display_action("Buy 1 T2",
                       tier1_count, tier2_count,
                       tier1_count - 8, tier2_count + 1,
                       new_tier2_bonus)

        return new_state


def main(options, args):
    """main loop of the progam"""

    # for i in range(38, 50):
    #     print("{},{},{:.2f},{},{},{:.2f}".format(
    #           i, 8, calc_bonus(i, 8 * 100,
    #           i - 8, 9, calc_bonus(i - 8, 9) * 100))

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
