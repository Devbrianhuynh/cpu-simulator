from hash_map import Hash_Map 
from intermediary import Intermediary
from datetime import datetime


# Memory that is fast but temporary (progress will be lost if not saved)
class RAM(Intermediary):
    def __init__(self, gbs, access_time, ssd_gbs, ssd_access_time):
        super().__init__('RAM', access_time) # Instance of Intermediary with self.name and self.access_time defined here
        self.ram_memory = Hash_Map(gbs) # Hash map used to store RAM's data
        self.ssd = SSD(ssd_gbs, ssd_access_time)
        

    def write_ram(self, address, data):
        # We will know that a hash map is full when a RecursionError appears
        try:
            self.ram_memory.assign(address, data)
            return super().process_request_write(data, 'RAM storage')
        
        # When the RAM is full, use paging: Store data from the SSD for later use in the RAM
        except RecursionError:
            return self.paging_ram(address, data, 'write')

    
    # Retrieve the data from this address
    def read_ram(self, address):
        # If paging occurs, a RecursionError will appear
        # Access the SSD for the corresponding address
        try:
            data = self.ram_memory.retrieve(address)

            # Edge case scenario: User attempts to retrieve an address that doesn't exist in the RAM 
            if data is None:
                print(f'The topic in RAM \'{address}\' doesn\'t exist')
                return None
            else:
                return super().process_request_read(data, 'RAM read')

        except RecursionError:
            return self.paging_ram(address, None, 'read') # data parameter is None since data is not needed when retrieving; only the address is needed

    
    # Edge case scenario: When the RAM needed exceeds the available amount of RAM (paging: use the SSD to store the data that exceeds the RAM's gbs)
    # Access the SSD's storage and inject the data there
    # Paging has two uses: Storing data and retrieving data
    def paging_ram(self, address, data, data_method): 
        if data_method == 'write':
            self.ssd.write_ssd(address, data, True)
            return super().process_request_write(data, 'SSD storage (paging)')

        elif data_method == 'read':
            data = self.ssd.read_ssd(address, True) # Take the returned data to print the data and its message
            return super().process_request_read(data, 'SSD read (paging)')


    def get_execution_time(self):
        return super().return_execution_time()
    

    # Edge case scenario: If the user fails to save their progress, all data stored in the RAM is wiped out
    def wipeout_data(self):
        ram_memory = self.ram_memory.array

        for i in range(len(ram_memory)):
            ram_memory[i] = None

        return f'RAM data wipeout at {datetime.now().strftime("%H:%M:%S")}'

    
    # If the user saves their progress before shutting down, all data stored in the RAM is transfered to the SSD
    def save_data(self):
        ram_memory = self.ram_memory.array

        for i in range(len(ram_memory)):
            address, data = ram_memory[i]
            self.ssd.write_ssd(address, data, False)

        return f'RAM data saved into SSD (flash drive) at {datetime.now().strftime("%H:%M:%S")}'
    

    def check_for_none(self):
        ram_memory = self.ram_memory.array

        none_count = 0

        for i in range(len(ram_memory)):
            if ram_memory[i] == None:
                none_count += 1
        
        if none_count == 0:
            return False
        else:
            return True 
        
    
    # Since there may be some data that is paged into the SSD, keep the RAM and SSD connected by storing data to the SSD through the RAM class
    # Store data to the SSD
    def store_data_to_ssd(self, address, data):
        return self.ssd.write_ssd(address, data, False)
    

    # Retrieve and read data from the SSD
    def read_data_from_ssd(self, address):
        return self.ssd.read_ssd(address, False)


# Memory that is slow but permanent (progress will only be stored if saved)
class SSD(Intermediary):
    def __init__(self, gbs, access_time):
        super().__init__('SSD (flash drive)', access_time)
        self.flash_drive = Hash_Map(gbs)


    def read_ssd(self, address, paging = False):
        data = self.flash_drive.retrieve(address)

        # Edge case scenario: User attempts to search for an address that doesn't exist 
        if data is None:
            return f'The topic in SSD (flash drive) \'{address}\' doesn\'t exist'
        
        else:
            if paging == True:
                return data # Return the data back to the paging_ram() 
            elif paging == False:
                return super().process_request_read(data, 'SSD read')

    
    def write_ssd(self, address, data, paging = False):
        self.flash_drive.assign(address, data)

        if paging == True:
            return
        elif paging == False:
            return super().process_request_write(data, 'SSD storage')

    
    def get_execution_time(self):
        return super().return_execution_time()
    

    # Edge case scenario: User wants to factory reset their data
    def factory_reset(self):
        flash_drive = self.flash_drive.array

        for i in range(len(flash_drive)):
            flash_drive[i] = None

        return f'SSD (flash drive) factory reset at {datetime.now().strftime("%H:%M:%S")}'


