import multiprocessing as mp
import time
import queue
from .logger import get_logger
from .job_item import *

_logger = get_logger(__name__)


class WorkerPool:
    def __init__(self, num_process: int, jobs):
        self.num_process = num_process
        self.queue = mp.Queue()
        self.processes = [mp.Process(target=self._worker_job, args=(self.queue,)) for _ in range(num_process)]
        self.watchdog = mp.Process(target=self._watchdog)

        if not isinstance(jobs, (list, tuple)):
            self.queue.put(jobs)
        else:
            for j in jobs:
                self.queue.put(j)

    def _watchdog(self):
        while True:
            queue_size = self.queue.qsize()
            _logger.info(f'current queue size = {queue_size}')
            time.sleep(1)

    @staticmethod
    def _worker_job(jobs_queue: mp.Queue):
        _logger.debug(f"Worker started here")
        try:
            while True:
                job = jobs_queue.get(timeout=1)
                _logger.debug(f"action = job = {job}")

                if result := job.run():
                    for s in result:
                        jobs_queue.put(s)

                time.sleep(1)

        except queue.Empty:
            _logger.debug(f"Nothing more")

        except Exception as e:
            _logger.warn(f"Error = {e}")

        _logger.debug(f"End, exit here")

    def start(self):
        self.watchdog.start()
        for p in self.processes:
            p.start()

    def join(self):
        for p in self.processes:
            p.join()

    def handle(self):
        self.start()
        self.join()
