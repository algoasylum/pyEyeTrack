from queue import Queue

q = Queue()


class QueueHandling():
    """
    This class is used to handles the queue in real-time.
    Methods:
        add_data(data)
            This function adds the data to the queue.
        get_data()
            This function returns the data elements in the queue.
        is_empty()
            This function checks if the queue is empty.
        search_element(key)
            This function is used to search if a specified element is 
            present in the queue.
    """

    def __init__(self):
        global q

    def add_data(self, data):
        """
        This function adds the data to the queue.

        Args:
            data ([tuple]): The tuple consists of the pupil center coordinates 
            with timestamps.
        """
        q.put(data)

    def get_data(self):
        """
        This function returns the data elements in the queue.

        Returns:
            tuple: The tuple consists of the pupil center coordinates with 
            timestamps.
        """
        return q.get()

    def is_empty(self):
        """
        This function checks if the queue is empty.

        Returns:
            boolean: The function returns True if the queue is empty. 
                     If the queue has data elements, then it returns False.
        """
        if q.empty():
            return True
        else:
            return False

    def search_element(self, key):
        """
        This function is used to search if a specified element is present in 
        the queue.

        Args:
            key ([char/integer/float/string]): The key is a data element of 
            the queue.

        Returns:
            boolean : The function returns true if the key exists in the queue, 
                    else returns false.
        """
        if key in list(q.queue):
            return True
        return False
