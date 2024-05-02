import os
import time
import matplotlib.pyplot as plt

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

# Compress text
def compress(text):
    bwt = bwt_compress(text)
    mtf = mtf_encode(bwt)
    rle = rle_compress(mtf)
    return rle

def measure_compression_time(filename):
    with open(filename, 'r') as file:
        text = file.read()

    start_compress = time.time()
    compressed = compress(text)
    end_compress = time.time()

    compression_time = end_compress - start_compress

    return len(text), compression_time

# Measure compression time for multiple files
def measure_multiple_files(files):
    compression_data = []
    for file in files:
        input_length, compression_time = measure_compression_time(file)
        compression_data.append((input_length, compression_time))
    return compression_data

# Plot compression time vs input length
def plot_compression_time(compression_data):
    input_lengths, compression_times = zip(*compression_data)
    plt.plot(input_lengths, compression_times, marker='o', linestyle='-')
    plt.title('Compression Time vs Input Length')
    plt.xlabel('Input Length')
    plt.ylabel('Compression Time (seconds)')
    plt.grid(True)
    plt.show()

# Example usage
file_names = ["sample10k.txt", "sample20k.txt", "sample30k.txt","sample40k.txt","sample50k.txt","sample60k.txt","sample70k.txt","sample80k.txt","sample90k.txt","sample100k.txt",]  # Provide the paths to your files here
compression_data = measure_multiple_files(file_names)
plot_compression_time(compression_data)
