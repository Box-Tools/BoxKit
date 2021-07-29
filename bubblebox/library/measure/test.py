from bubblebox.utilities import Task

import copy

class Action:

    @Task
    def taskA(unit,*args):
        print(id(Action.taskB))
        pass

    @Task
    def taskB(unit,*args):
        pass

    def clone():
        return 


def main():
    unitlist = [None]
    print(id(Action.taskB))
    Action.taskA(unitlist)


    NewAction=Action.__new__(Action)
    print(id(NewAction.taskB))


if __name__ == "__main__":
    main()
