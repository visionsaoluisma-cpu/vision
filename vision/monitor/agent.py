import time
import traceback
from .. import db

class MonitorAgent:
    def __init__(self, interval_seconds: int = 10) -> None:
        self.interval_seconds = interval_seconds
        self._running = False

    def start(self) -> None:
        self._running = True
        while self._running:
            try:
                self._health_check()
            except Exception:
                err = traceback.format_exc()
                db.insert_erro_sistema(err)
            time.sleep(self.interval_seconds)

    def stop(self) -> None:
        self._running = False

    def _health_check(self) -> None:
        # Expanda com verificações reais (captura facial, filas, etc.)
        pass
