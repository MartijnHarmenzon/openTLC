#
import time

#
from k0001func import initialise
from k0001app import openTLC
from k0001rpifunc import startFunc, setGuiInputs, setState, finallyFunc

#
def run():
    #
    startFunc()

    #
    step = 0
    amberState = False

    #
    initialise()

    #
    while True:
        #
        if step % 5 == 0:
            amberState ^= True

        #
        setGuiInputs()

        #
        openTLC(step, amberState)

        #
        setState()

        # Delay for a 10th of a second (0.1 seconds)
        time.sleep(0.1)

        #
        step += 1

#
try:
    run()
finally:
    #
    finallyFunc()

    #
    print('TLC stopped...')
