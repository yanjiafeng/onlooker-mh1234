import threading

from episode import Episode

timerInterval = 15

def fun_timer():
    ep.closePage()
    ep.getNextPage()
    global timer
    timer = threading.Timer(timerInterval, fun_timer)
    timer.start()


if __name__ == '__main__':
    ep = Episode()
    timer = threading.Timer(timerInterval, fun_timer)
    timer.start()

    # while 1:
    #     input()
    #     ep.closePage()
    #     ep.getNextPage()
