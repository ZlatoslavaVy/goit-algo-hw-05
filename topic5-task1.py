class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key) # key_hash - це індекс в таблиці, self.hash_function — це метод класу HashTable, який приймає ключ і повертає ціле число-індекс у таблиці
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key: #pair[0] - key
                    return pair[1] #pair[1] - value
        return None
    
    def delete(self, key):
        key_hash = self.hash_function(key)

        if self.table[key_hash] is None:
            return False
        for i in range (0, len(self.table[key_hash])):
            if self.table[key_hash][i][0] == key:
                self.table[key_hash].pop(i)
                return True
        return False
    
# Тестуємо нашу хеш-таблицю:
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(H.get("apple"))   # Виведе: 10
print(H.get("orange"))  # Виведе: 20
print(H.get("banana"))  # Виведе: 30
print(H.table)
print(H.delete("orange"))
print(H.table)