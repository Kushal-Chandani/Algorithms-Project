import time
import matplotlib.pyplot as plt

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
def measure_compression_time(filename):
    with open(filename, 'r') as file:
        text = file.read()

    start_compress = time.time()
    compressed = lzw_encode(text)  # Change here
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
