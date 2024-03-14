# Used to store data coming from the RAM and SSD
class Hash_Map:
    def __init__(self, array_size):
        self.array_size = array_size
        self.array = [None for i in range(self.array_size)]
    
    
    def hashing(self, key, collisons):
        key_bytes = key.encode()
        hash_code = sum(key_bytes)

        return hash_code + collisons
    

    def compressor(self, hash_code):
        return hash_code % self.array_size
    

    def assign(self, key, value, collisons = 0):
        index = self.compressor(self.hashing(key, collisons))
        array_value = self.array[index]

        if array_value is None:
            self.array[index] = [key, value]
            return
        
        if array_value[0] == key:
            self.array[index] = [key, value]
            return
        
        # Collison
        if array_value is not None and array_value[0] != key:
            self.assign(key, value, collisons + 1)
        

    def retrieve(self, key, collisons = 0):
        index = self.compressor(self.hashing(key, collisons))
        array_value = self.array[index]

        if array_value is None:
            return None

        if array_value[0] == key:
            return array_value[1]
        
        if array_value is not None and array_value[0] != key:
            self.retrieve(key, collisons + 1)
        
        