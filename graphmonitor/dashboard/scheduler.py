from threading import Timer, Lock

class Periodic(object):
    """
    A periodic task running in threading.Timers
    https://stackoverflow.com/questions/2398661/schedule-a-repeating-event-in-python-3
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._lock = Lock()
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self._stopped = True
        if kwargs.pop('autostart', True):
            self.start()

    def start(self, from_run=False):
        self._lock.acquire()
        if from_run or self._stopped:
            self._stopped = False
            self._timer = Timer(self.interval, self._run)
            self._timer.start()

        self._lock.release()

    def _run(self):
        self.start(from_run=True)
        self.function(*self.args, **self.kwargs)

    def stop(self):
        self._lock.acquire()
        self._stopped = True
        self._timer.cancel()
        self._lock.release()

    def isRunning(self):
        return not self._stopped


class Processes():
    '''
    Static container class for holding Periodic objects and syncronizing them when accessed.
    '''
    _processes = {}
    _mutex = Lock()


    @staticmethod
    def addProcess(id: int, seconds: int, function):
        Processes._mutex.acquire()
        try:
            if id not in Processes._processes:
                Processes._processes[id] = Periodic(seconds, function, id)
                return True
        finally:
            Processes._mutex.release()
        
        return False


    @staticmethod
    def removeProcess(id: int):
        Processes._mutex.acquire()
        try:
            if id in Processes._processes:
                Processes._processes[id].stop()
                del Processes._processes[id]
                return True
        finally:
            Processes._mutex.release()
        
        return False


    @staticmethod
    def startProcess(id: int):
        Processes._mutex.acquire()
        try:
            if id in Processes._processes:
                Processes._processes[id].start()
                return True
        finally:
            Processes._mutex.release()
        
        return False


    @staticmethod
    def stopProcess(id: int):
        Processes._mutex.acquire()
        try:
            if id in Processes._processes:
                Processes._processes[id].stop()
                return True
        finally:
            Processes._mutex.release()
        
        return False


    @staticmethod
    def updateProcessInterval(id: int, seconds: int):
        Processes._mutex.acquire()
        try:
            if id in Processes._processes:
                Processes._processes[id].interval = seconds
                return True
        finally:
            Processes._mutex.release()
        
        return False

    @staticmethod
    def isProcessRunning(id: int) -> bool:
        Processes._mutex.acquire()
        try:
            if id in Processes._processes:
                return Processes._processes[id].isRunning()
        finally:
            Processes._mutex.release()
        
        return False