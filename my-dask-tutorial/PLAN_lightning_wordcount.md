# Plan: Lightning Notebook for Word Count with Dask

## Objective
Create a concise, quick-to-complete notebook that demonstrates word counting by:
1. Generating a file with 1,000,000 English words
2. Counting words using a straightforward sequential approach
3. Counting words using Dask and the MapReduce approach

This notebook teaches the classic MapReduce pattern and demonstrates the performance benefits of parallel processing.

**Style**: Lightning-fast introduction. Code cells minimal and focused. Markdown cells brief but clear. Aim for ~10-15 minutes total execution time.

## Notebook Structure
**File**: `my-dask-tutorial/07_lightning_wordcount.ipynb`

### Section 1: Introduction (2 cells)
- **Cell 1 (Markdown)**: Title and overview
  - What is word count?
  - Why it's a classic distributed computing example (MapReduce)
  - What we'll do: Generate 1M words, count sequentially, count with Dask
  - Learning objectives: Sequential vs parallel processing, MapReduce pattern
  
- **Cell 2 (Code)**: Setup and imports
  ```python
  import dask.bag as db
  from collections import Counter
  import random
  import time
  import os
  
  # Optional: Start client with 10 CPUs for diagnostics
  from dask.distributed import Client
  client = Client()
  client
  ```

### Section 2: Generate 1,000,000 English Words (3-4 cells)
- **Cell 3 (Markdown)**: Generating test data
  - Need a large dataset to demonstrate parallel processing benefits
  - Will generate a text file with 1,000,000 words
  - Use a word list (common English words) and randomly sample
  
- **Cell 4 (Code)**: Create word list
  ```python
  # Common English words for generating test data
  common_words = [
      "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
      "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
      "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
      "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
      # Add more words to get variety
      "up", "out", "many", "then", "them", "these", "so", "some", "her", "would",
      "make", "like", "into", "him", "time", "has", "look", "two", "more", "write",
      "go", "see", "number", "no", "way", "could", "people", "my", "than", "first",
      "water", "been", "call", "who", "oil", "sit", "now", "find", "down", "day",
      "did", "get", "come", "made", "may", "part", "over", "new", "sound", "take",
      "only", "little", "work", "know", "place", "year", "live", "me", "back", "give",
      "most", "very", "after", "thing", "our", "just", "name", "good", "sentence", "man",
      "think", "say", "great", "where", "help", "through", "much", "before", "line", "right",
      "too", "mean", "old", "any", "same", "tell", "boy", "follow", "came", "want",
      "show", "also", "around", "form", "three", "small", "set", "put", "end", "does",
      "another", "well", "large", "must", "big", "even", "such", "because", "turn", "here",
      "why", "ask", "went", "men", "read", "need", "land", "different", "home", "us",
      "move", "try", "kind", "hand", "picture", "again", "change", "off", "play", "spell",
      "air", "away", "animal", "house", "point", "page", "letter", "mother", "answer", "found",
      "study", "still", "learn", "should", "America", "world", "high", "every", "near", "add",
      "food", "between", "own", "below", "country", "plant", "last", "school", "father", "keep",
      "tree", "never", "start", "city", "earth", "eye", "light", "thought", "head", "under",
      "story", "saw", "left", "don't", "few", "while", "along", "might", "close", "something",
      "seem", "next", "hard", "open", "example", "begin", "life", "always", "those", "both",
      "paper", "together", "got", "group", "often", "run", "important", "until", "children", "side",
      "feet", "car", "mile", "night", "walk", "white", "sea", "began", "grow", "took",
      "river", "four", "carry", "state", "once", "book", "hear", "stop", "without", "second",
      "later", "miss", "idea", "enough", "eat", "face", "watch", "far", "Indian", "really",
      "almost", "let", "above", "girl", "sometimes", "mountain", "cut", "young", "talk", "soon",
      "list", "song", "leave", "family", "it's"
  ]
  
  print(f"Word list contains {len(common_words)} unique words")
  ```

- **Cell 5 (Code)**: Generate 1,000,000 words and save to file
  ```python
  # Generate 1,000,000 words
  num_words = 1_000_000
  output_file = "words_1million.txt"
  
  print(f"Generating {num_words:,} words...")
  words = [random.choice(common_words) for _ in range(num_words)]
  
  # Save to file (one word per line, or space-separated)
  with open(output_file, 'w') as f:
      # Write words in chunks (e.g., 100 words per line for readability)
      words_per_line = 100
      for i in range(0, len(words), words_per_line):
          line = ' '.join(words[i:i+words_per_line])
          f.write(line + '\n')
  
  file_size = os.path.getsize(output_file)
  print(f"File created: {output_file}")
  print(f"File size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
  print(f"Number of lines: {len(words) // words_per_line}")
  ```

### Section 3: Sequential Word Count (2-3 cells)
- **Cell 6 (Markdown)**: Sequential approach
  - Most straightforward way: read file, split into words, count
  - Simple and easy to understand
  - Single-threaded, processes one word at a time
  
- **Cell 7 (Code)**: Sequential word counting
  ```python
  # Sequential word count
  print("Counting words sequentially...")
  start_time = time.time()
  
  word_counts = {}
  with open(output_file, 'r') as f:
      for line in f:
          words = line.strip().split()
          for word in words:
              word_counts[word] = word_counts.get(word, 0) + 1
  
  sequential_time = time.time() - start_time
  
  # Display results
  sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
  print(f"\nSequential counting completed in {sequential_time:.2f} seconds")
  print(f"Total unique words: {len(word_counts)}")
  print(f"Total word count: {sum(word_counts.values()):,}")
  print("\nTop 10 most frequent words:")
  for word, count in sorted_counts[:10]:
      print(f"  {word}: {count:,}")
  ```

- **Cell 8 (Code)**: Alternative sequential approach using Counter
  ```python
  # Alternative: Using Counter (also sequential but more Pythonic)
  print("Counting words using Counter...")
  start_time = time.time()
  
  word_counts_counter = Counter()
  with open(output_file, 'r') as f:
      for line in f:
          words = line.strip().split()
          word_counts_counter.update(words)
  
  counter_time = time.time() - start_time
  
  print(f"Counter approach completed in {counter_time:.2f} seconds")
  print(f"Top 10 most frequent words:")
  for word, count in word_counts_counter.most_common(10):
      print(f"  {word}: {count:,}")
  ```

### Section 4: Dask MapReduce Word Count (4-5 cells)
- **Cell 9 (Markdown)**: MapReduce approach with Dask
  - MapReduce pattern: Map (split into words) → Shuffle → Reduce (count)
  - Dask Bag handles this automatically
  - Parallel processing across partitions
  - Can process large files that don't fit in memory
  
- **Cell 10 (Code)**: Dask Bag word count
  ```python
  # Dask Bag word count (MapReduce)
  print("Counting words with Dask (MapReduce)...")
  start_time = time.time()
  
  # Read text file with Dask Bag
  bag = db.read_text(output_file)
  
  # Map: Split into words
  words = bag.str.split().flatten()
  
  # Reduce: Count frequencies
  word_counts_dask = words.frequencies()
  
  # Compute (triggers execution)
  result = word_counts_dask.compute()
  
  dask_time = time.time() - start_time
  
  # Display results
  sorted_dask = sorted(result, key=lambda x: x[1], reverse=True)
  print(f"\nDask counting completed in {dask_time:.2f} seconds")
  print(f"Total unique words: {len(result)}")
  print(f"Total word count: {sum(count for _, count in result):,}")
  print("\nTop 10 most frequent words:")
  for word, count in sorted_dask[:10]:
      print(f"  {word}: {count:,}")
  ```

- **Cell 11 (Code)**: Visualize the computation graph
  ```python
  # Show the computation graph
  word_counts_dask.visualize()
  ```

- **Cell 12 (Code)**: Inspect partitions and execution plan
  ```python
  # Inspect how Dask partitions the data
  bag = db.read_text(output_file)
  print(f"Number of partitions: {bag.npartitions}")
  print(f"Partition size (approximate): {len(bag) // bag.npartitions if bag.npartitions > 0 else 'N/A'}")
  
  # Show the computation plan
  words = bag.str.split().flatten()
  word_counts_dask = words.frequencies()
  print("\nComputation graph structure:")
  print(word_counts_dask)
  ```

### Section 5: Comparison and Performance (2-3 cells)
- **Cell 13 (Markdown)**: Performance comparison
  - Compare execution times
  - Discuss when to use sequential vs parallel
  - Memory considerations
  
- **Cell 14 (Code)**: Performance comparison
  ```python
  # Compare performance
  print("=" * 50)
  print("PERFORMANCE COMPARISON")
  print("=" * 50)
  print(f"Sequential approach: {sequential_time:.2f} seconds")
  print(f"Counter approach:   {counter_time:.2f} seconds")
  print(f"Dask approach:      {dask_time:.2f} seconds")
  print()
  
  if sequential_time > 0:
      speedup = sequential_time / dask_time
      print(f"Speedup: {speedup:.2f}x")
  
  # Verify results match
  sequential_dict = dict(sorted_counts)
  dask_dict = dict(sorted_dask)
  
  if sequential_dict == dask_dict:
      print("\n✓ Results match perfectly!")
  else:
      print("\n⚠ Results differ (this shouldn't happen)")
      print(f"Sequential unique words: {len(sequential_dict)}")
      print(f"Dask unique words: {len(dask_dict)}")
  ```

- **Cell 15 (Code)**: Memory usage comparison (optional)
  ```python
  # Memory considerations
  print("\nMemory considerations:")
  print("- Sequential: Loads entire file into memory (or processes line by line)")
  print("- Dask: Processes in partitions, can handle files larger than memory")
  print(f"- File size: {file_size / 1024 / 1024:.2f} MB")
  print(f"- Dask partitions: {bag.npartitions}")
  ```

### Section 6: Summary (1 cell)
- **Cell 16 (Markdown)**: Key takeaways
  - Sequential: Simple, straightforward, single-threaded
  - Dask MapReduce: Parallel, scalable, handles large files
  - MapReduce pattern: Map (transform) → Shuffle → Reduce (aggregate)
  - When to use each approach
  - Dask Bag is perfect for text processing tasks

## Key Concepts to Emphasize

1. **MapReduce Pattern**:
   - Map: Transform data (split text into words)
   - Shuffle: Group by key (words)
   - Reduce: Aggregate (count occurrences)

2. **Sequential vs Parallel**:
   - Sequential: One operation at a time, simple to understand
   - Parallel: Multiple operations simultaneously, better for large data

3. **Dask Bag Operations**:
   - `read_text()`: Read text files
   - `str.split()`: Split strings
   - `flatten()`: Flatten nested structures
   - `frequencies()`: Count occurrences (MapReduce)

4. **Performance Considerations**:
   - For small files, sequential may be faster (less overhead)
   - For large files, parallel processing shines
   - Memory efficiency with Dask partitions

## Notes

- The 1M words file should be large enough to show performance differences
- Use realistic English words to make results meaningful
- Keep code simple and focused on the core concepts
- Emphasize the MapReduce pattern as a fundamental distributed computing concept
