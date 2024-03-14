# Terminal for the cache, RAM, and SSD to access data and find the execution time
# For notification purposes only (Intermediary is only used to notify users how the program is running)
class Intermediary:
    def __init__(self, name, access_time):
        self.name = name
        self.access_time = access_time
        self.execution_time = 0

    
    # Prints the name of the memory type and its execution speed for extracting data from the memory
    def process_request_read(self, data, status):
        self.reset_execution_time() # Reset the exeuction time back to 0 to prevent it from calculating the exeuction time for the entire session

        self.execution_time += self.access_time

        return f'Read: {self.name} - {status} - \'{data}\''

    
    # Prints the name of the memory type and its execution speed for entering data into the memory
    def process_request_write(self, data, status):
        self.reset_execution_time()

        self.execution_time += self.access_time
        
        return f'Write: {self.name} - {status} - \'{data}\''

    
    def return_execution_time(self):
        return self.execution_time

    
     # To prevent the program from calculating the exeuction time of the program in addition to including the past execution times, reset the execution time here:
    def reset_execution_time(self):
        self.execution_time = 0