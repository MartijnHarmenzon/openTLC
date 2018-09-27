#! python3


# import libraries
import time
from k0001func import initialise
from k0001app import open_tlc
from k0001rpifunc import start_func, set_gui_inputs, set_state, finally_func


#
def run():
    #
    start_func()

    #
    step = 0
    # amber_state = False

    #
    initialise()

    #
    while True:
        #
        # if step % 5 == 0:
        #     amber_state ^= True

        #
        set_gui_inputs()

        #
        open_tlc(step)
        # open_tlc(step, amber_state)

        #
        set_state()

        # Delay for a 10th of a second (0.1 seconds)
        time.sleep(0.1)

        #
        step += 1


if __name__ == '__main__':
    try:
        run()
    finally:
        finally_func()
        print('TLC stopped...')
