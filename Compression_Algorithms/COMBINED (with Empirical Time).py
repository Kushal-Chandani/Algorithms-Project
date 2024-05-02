import os
import time
import matplotlib.pyplot as plt

class Node:
    def __init__(self, frequency, value):
        self.frequency = frequency
        self.value = value
        self.left = None
        self.right = None

# Burrows-Wheeler Transform (BWT) compression
def bwt_compress(text):
    # Add end of text marker
    text += '$'
    # Generate suffix array
    suffix_array = sorted(range(len(text)), key=lambda i: text[i:])
    # Construct BWT by taking the last character of each suffix
    bwt = ''.join(text[i-1] for i in suffix_array)
    return bwt

# Move-to-Front (MTF) encoding
def mtf_encode(text):
    alphabet = list(sorted(set(text)))
    encoded_text = []
    for char in text:
        idx = alphabet.index(char)
        encoded_text.append(idx)
        # Move the character to the front of the alphabet
        del alphabet[idx]
        alphabet.insert(0, char)
    return encoded_text

# Run-Length Encoding (RLE) compression
def rle_compress(data):
    compressed_data = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            compressed_data.append((data[i - 1], count))
            count = 1
    compressed_data.append((data[-1], count))
    return compressed_data

def run_length_encode(st):
    n = len(st)
    i = 0
    encoded_string = ""
    while i < n:
        count = 1
        if st[i].isdigit() == True:
            while i < n - 1 and st[i] == st[i + 1]:
                count += 1
                i += 1
            encoded_string += "(" + st[i] + ")" + str(count) 
            i += 1
        else:
            while i < n - 1 and st[i] == st[i + 1]:
                count += 1
                i += 1
            encoded_string += st[i] + str(count)
            i += 1
    return encoded_string

# Compress text
def compress(text, algorithm):
    if algorithm == "bwt":
        bwt = bwt_compress(text)
        mtf = mtf_encode(bwt)
        rle = rle_compress(mtf)
        return rle
    elif algorithm == "huffman":
        character_freq = {char: text.count(char) for char in set(text)}
        root_node = huffman(character_freq)
    elif algorithm == "lzw":
        compressed = lzw_encode(text)
        return compressed
    elif algorithm == "rle":
        rle = run_length_encode(text)
        return rle

# Huffman encoding functions
def huffman(c):
    n = len(c)
    Q = [Node(frequency, value) for value, frequency in c.items()]

    for i in range(1, n):
        temp = Node(0, None)

        # Get two nodes with minimum frequencies
        left = get_min(Q)
        right = get_min(Q)

        # Assign left and right children
        temp.left = left
        temp.right = right

        # Calculate frequency of parent node
        temp.frequency = left.frequency + right.frequency

        # Insert new node back to the queue
        insert(Q, temp)

    return get_min(Q)

def get_min(Q):
    min_node = Q[0]
    min_index = 0
    for i in range(1, len(Q)):
        if Q[i].frequency < min_node.frequency:
            min_node = Q[i]
            min_index = i
    return Q.pop(min_index)

def insert(Q, node):
    Q.append(node)
    Q.sort(key=lambda x: x.frequency)

# LZW encoding function
def lzw_encode(data):
    """LZW encoding for the input data."""
    dictionary = {chr(i): i for i in range(256)}
    p = ""
    compressed = []
    for c in data:
        pc = p + c
        if pc in dictionary:
            p = pc
        else:
            compressed.append(dictionary[p])
            dictionary[pc] = len(dictionary)
            p = c
    if p:
        compressed.append(dictionary[p])
    return compressed

# Measure time taken for compression
def measure_compression_time(filename, algorithm):
    with open(filename, 'r') as file:
        text = file.read()

    start_compress = time.time()
    if algorithm in ["bwt", "rle"]:
        compressed = compress(text, algorithm)
    elif algorithm == "huffman":
        character_freq = {char: text.count(char) for char in set(text)}
        root_node = huffman(character_freq)
    elif algorithm == "lzw":
        compressed = lzw_encode(text)
    end_compress = time.time()

    compression_time = end_compress - start_compress

    return len(text), compression_time

# Measure compression time for multiple files
def measure_multiple_files(files, algorithm):
    compression_data = []
    for file in files:
        input_length, compression_time = measure_compression_time(file, algorithm)
        compression_data.append((input_length, compression_time))
    return compression_data

# Plot compression time vs input length for multiple algorithms
def plot_compression_time(compression_data_dict):
    plt.figure(figsize=(10, 6))
    markers = ['o', 's', '^', 'D']
    colors = ['r', 'g', 'b', 'm']
    for i, (algorithm, compression_data) in enumerate(compression_data_dict.items()):
        input_lengths, compression_times = zip(*compression_data)
        plt.plot(input_lengths, compression_times, marker=markers[i], linestyle='-', color=colors[i], label=algorithm)

    plt.title('Compression Time vs Input Length')
    plt.xlabel('Input Length')
    plt.ylabel('Compression Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
file_names = ["sample10k.txt", "sample20k.txt", "sample30k.txt","sample40k.txt","sample50k.txt","sample60k.txt","sample70k.txt","sample80k.txt","sample90k.txt","sample100k.txt",]  # Provide the paths to your files here

compression_data_dict = {}
for algo in ["bwt", "huffman", "lzw", "rle"]:
    compression_data = measure_multiple_files(file_names, algo)
    compression_data_dict[algo] = compression_data

plot_compression_time(compression_data_dict)
