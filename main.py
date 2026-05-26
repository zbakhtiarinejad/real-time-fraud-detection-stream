import threading
from producer import start_producer
from consumer import start_consumer

producer_thread = threading.Thread(target=start_producer)
consumer_thread = threading.Thread(target=start_consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()