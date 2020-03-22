class CancellationToken:
    cancel_requested: bool = False

    def cancel(self,):
        self.cancel_requested = True