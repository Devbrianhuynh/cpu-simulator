from ram_ssd import RAM
from intermediary import Intermediary
from hash_map import Hash_Map
import random


# CPU handles all of the user preferences for storage and policies
# Connects the cache, RAM, and SSD together to make them communicable and transmit data to one another
# Process instructions for: When to inject data into the cache, RAM, and SSD
class CPU:
    def __init__(self, model, clock_speed, cores, cache_blocks, ram_gbs, ssd_gbs, cache_access_time, ram_access_time, ssd_access_time, cache_write_preference):
        self.model = model
        self.clock_speed = clock_speed
        self.cores = cores # Only for show/demonstration purposes; core count will not affect anything in this program

        self.cache_blocks = cache_blocks
        self.ram_gbs = ram_gbs
        self.ssd_gbs = ssd_gbs

        # SIMULATION PURPOSES ONLY; NOT ACCURATE IN REAL LIFE SCANERIOS
        self.cache_access_time = cache_access_time 
        self.ram_access_time = ram_access_time
        self.ssd_access_time = ssd_access_time

        # Define all of the computer component's specs in the cache since they are corresponding and transitive:
        # Cache connects with the RAM, and RAM connects with the SSD
        self.cache = Cache(self.cache_blocks, self.cache_access_time, self.ram_gbs, self.ram_access_time, self.ssd_gbs, self.ssd_access_time)
        self.cache_write_preference = cache_write_preference

    
    # FOR SIMULATION PURPOSES ONLY; NOT ACCURATE IN REAL LIFE SCENARIOS
    # Get 20% of the CPU's clock speed and subtract it from the cache/ram/ssd_access_time(s) (higher the clock speed, the lower the access_time) 
    # This is done to emphasize how a CPU's clock speed can drastically affect a computer's performance
    def clock_speed_fine_tuning(self):
        self.cache_access_time = self.cache_access_time - (self.clock_speed * 0.01)
        self.ram_access_time = self.ram_access_time - (self.clock_speed * 0.05)
        self.ssd_access_time = self.ssd_access_time - (self.clock_speed * 0.10)

        # Redefine self.cache with the new modified parameters
        self.cache = Cache(self.cache_blocks, self.cache_access_time, self.ram_gbs, self.ram_access_time, self.ssd_gbs, self.ssd_access_time)

        return f'Computer specs fine-tuned based on the clock speed'


    # Cache
    def add_cache_data(self, address, data):
        if self.cache_write_preference == 'write back':
            return self.cache.write_cache(address, data, self.cache_write_preference)
        else:
            return self.cache.write_cache(address, data, self.cache_write_preference)

    
    def read_cache_data(self, address):
        return self.cache.read_cache(address)
    

    # RAM
    def save_progress(self):
        return self.cache.ram.save_data()
    
    
    def wipeout_progress(self):
        return self.cache.ram.wipeout_data()


    # SSD
    def add_ssd_data(self, address, data):
        return self.cache.ram.store_data_to_ssd(address, data)
    

    def read_ssd_data(self, address):
        return self.cache.ram.read_data_from_ssd(address)


    # Get the execution time for all three compenents (regardless if they've been read or written yet): Cache + RAM + SSD
    def get_execution_time(self):
        # Convert the cache and RAM nanoseconds to milliseconds by dividing them by 1,000,000
        cache_ram_exeuction_time = (self.cache.get_execution_time() + self.cache.ram.get_execution_time()) / 1000000
        ssd_exeuction_time = self.cache.ram.ssd.get_execution_time()
        total_execution_time = ssd_exeuction_time + cache_ram_exeuction_time
        
        return f'{total_execution_time} milliseconds'
    
        
# Transitive architecture: If data overflows the cache, then it gets sent to the RAM, and if the RAM is overflowed, data is sent to the SSD via paging 
class Cache(Intermediary):
    def __init__(self, blocks, access_time, ram_gbs, ram_access_time, ssd_gbs, ssd_access_time):
        super().__init__('Cache', access_time)
        self.blocks = blocks
        self.cache_block = Hash_Map(blocks) # Each data will be given a 'tag' for identification and 'data' to store the data in: ['tag', 'data']
        self.ram = RAM(ram_gbs, ram_access_time, ssd_gbs, ssd_access_time)
        self.fifo_index = 0


    # Data will be ENTERED into the RAM (and SSD if paging occurs)
    # The user will have a choice of either to write-through or -back
    # Write-through: Add data to the cache and RAM
    # Write-back: Add data to the cache; we only add the data to the memory if it is to be replaced with newer data
    def write_cache(self, address, data, write_preference):
        data_check = self.cache_block.retrieve(address) # Attempt to get this data out of the cache block to check if it exists

        if data_check:
            return f'{data} already exists in the cache'

        else:
            if write_preference == 'write back':
                self.replace_block(address, data, True) 
                return super().process_request_write(address, data, 'Cache storage')

            elif write_preference == 'write through':
                self.replace_block(address, data, False)
                return self.ram.write_ram(address, data) # Enter this data to the RAM along with adding this data to the cache 

    
    def read_cache(self, address) -> str:
        data = self.cache_block.retrieve(address)

        if data:
            return super().process_request_read(address, data, 'Cache read')
        
        else:
            data = self.ram.read_ram(address) # If there isn't any data in the cache, we go to the RAM where the rest of the data is stored
            
            if data is None:
                return f'The topic in cache \'{address}\' doesn\'t exist'
            else:
                self.replace_block(address, data, False) # Replace the oldest cache data with this RAM data
                return super().process_request_write(address, data, 'Cache read')


    # Replace the oldest cache with the newest one (that is to be entered into the cache)
    def replace_block(self, address, data, write_back = False):
        index = self.get_hash_index(address)

        # Take the old data and update it into the RAM 
        if write_back == True:
            block_old = self.cache_block.array[index]

            # If there is data already in the block, we put this old data into the RAM before replacing it with new data
            if block_old is not None:
                address_old, data_old = block_old
                self.ram.write_ram(address_old, data_old)

        try:
            self.cache_block.assign(address, data)
        except: 
            # If an error is given, the hash map is full; replace the old address/data with this new address/data
            # Any present data inside of this hash is wiped out and replaced with this new data
            self.cache_block.array[index] = [address, data]


    # Get the hash index of the address entered to check if it has already been filled with data
    def get_hash_index(self, address):
        address_index = sum(address.encode()) % self.blocks

        return address_index

  
    # Gets the execution time for processing the cache
    def get_execution_time(self):
        return super().return_execution_time()
    

    # To ensure that the cache and RAM are connected, call the commands for RAM here:
        # Inheritence/constructor chaining: Cache is connected to the RAM, and the RAM is connected to the SSD: Cache --> RAM --> SSD
    def store_data_to_ram(self, address, data):
        return self.ram.write_ram(address, data)
    

    def read_data_from_ram(self, address):
        return self.ram.read_ram(address)
    

    
    
