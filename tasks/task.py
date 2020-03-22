from dispatcher import Dispatcher
from tasks.cancellation_token import CancellationToken
from loguru import logger
import typing
import threading
import time

class MyTask(threading.Thread):
    task: typing.Callable[['Client', Dispatcher], None]
    cancelation_source: CancellationToken
    task_id: int
    timeout: int
    client: 'Client'
    dp: Dispatcher

    def __init__(
        self, 
        task: typing.Callable[['Client', Dispatcher], None], 
        task_id: int,
        timeout: int,
        client: 'Client',
        dp: Dispatcher
    ):
        threading.Thread.__init__(self)

        self.timeout = timeout
        self.task = task
        self.task_id = task_id
        self.client = client
        self.dp = dp

        self.cancelation_source = CancellationToken()
    
    def cancel(self,):
        self.cancelation_source.cancel()

    def run(self,):
        logger.debug(f'Task {self.task_id} started')
        while (self.cancelation_source.cancel_requested == False):
            if (self.client.is_connected == False):
                logger.debug('Client is not connected waiting for next tick...')
                time.sleep(self.timeout)
                continue
            self.task(self.client, self.dp)
            time.sleep(self.timeout)