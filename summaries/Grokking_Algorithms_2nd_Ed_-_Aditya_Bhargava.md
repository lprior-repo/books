# Grokking Algorithms, 2nd Edition - Comprehensive Summary

**Author:** Aditya Y. Bhargava
**Publisher:** Manning Publications, 2024
**Prerequisites:** Basic algebra and familiarity with one programming language (Python used throughout)

---

## Overview

*Grokking Algorithms* is a visually-driven, example-rich introduction to algorithms and data structures designed for readers who can code but want to understand algorithms without heavy mathematics. The book uses over 400 illustrations, memorable analogies, and practical Python 3 code examples throughout. It covers 13 chapters spanning fundamental algorithms (binary search, sorting), core data structures (arrays, linked lists, hash tables, trees), graph algorithms (BFS, Dijkstra's), problem-solving paradigms (divide and conquer, greedy, dynamic programming), and an introduction to machine learning via k-nearest neighbors. The second edition adds two entirely new chapters on trees (Chapters 7 and 8), expanded coverage of NP-completeness in a dedicated appendix, and all code updated to Python 3.

The book is organized to build progressively: Chapters 1-3 lay foundations (binary search, big O, arrays, linked lists, recursion), Chapters 4-8 introduce more advanced data structures and algorithms (quicksort, hash tables, BFS, trees, balanced trees), Chapters 9-11 cover graph algorithms and optimization (Dijkstra's, greedy, dynamic programming), and Chapters 12-13 introduce machine learning and survey additional algorithms. Each chapter includes exercises with solutions in Appendix C.

---

## Chapter 1: Introduction to Algorithms

An algorithm is a set of instructions for accomplishing a task. This book focuses on algorithms that are fast, solve interesting problems, or both.

### Binary Search

Binary search is an algorithm that finds an element in a **sorted** list by repeatedly halving the search space. The book introduces it through a number-guessing game: if you guess 1, 2, 3, 4... sequentially (simple search), it takes up to 100 guesses for numbers 1-100. But if you always guess the middle number and use the "too high/too low" feedback to eliminate half the remaining numbers, you need at most 7 guesses for 1-100, and at most 32 guesses for 4 billion numbers.

**How it works:** Given a sorted array, maintain `low` and `high` indices. Compute `mid = (low + high) // 2`. Check the element at `mid`. If it matches the target, return `mid`. If the guess is too low, set `low = mid + 1`. If too high, set `high = mid - 1`. Repeat until found or the range is exhausted (return `None`).

Binary search only works on **sorted** lists. It runs in **O(log n)** time, compared to simple search's O(n).

### Logarithms

Logarithms are the inverse of exponentials. log2(8) = 3 because 2^3 = 8. log2(256) = 8 because 2^8 = 256. In this book, "log" always means log base 2. Understanding logarithms is essential because log time appears throughout the book.

### Big O Notation

Big O notation describes how the runtime of an algorithm grows as the input size increases. It does not measure speed in seconds -- it measures the **growth rate of the number of operations**. This is critical because algorithms grow at different rates. The book illustrates this with Bob's NASA rocket landing scenario: binary search on 100 elements takes 7ms, but on 1 billion elements takes only 30ms, while simple search takes 11 days on 1 billion elements.

**Five common runtimes (fastest to slowest):**
- **O(log n)** -- Log time. Example: binary search. Eliminates half the data each step.
- **O(n)** -- Linear time. Example: simple search. Touches every element once.
- **O(n log n)** -- Example: fast sorting algorithms like quicksort and merge sort.
- **O(n^2)** -- Example: slow sorting algorithms like selection sort. Touches each element roughly n times.
- **O(n!)** -- Factorial time. Example: the traveling salesperson problem.

Big O describes the **worst-case** scenario and establishes a guarantee that the algorithm will never be slower. Constants like O(2n) are simplified to O(n), and coefficients are dropped because they become irrelevant as n grows large.

### The Traveling Salesperson Problem

A classic O(n!) problem. A salesperson must visit n cities and find the shortest route visiting each exactly once. The only known approach is checking every permutation. For 5 cities, there are 120 permutations; for 30 cities, the number is approximately 2.65 x 10^32. This is one of the unsolved problems in computer science -- no fast algorithm is known, and some believe no fast algorithm exists. The best approach is approximation (covered in Chapter 10).

---

## Chapter 2: Selection Sort

### How Memory Works

Computer memory works like a giant set of drawers, each with a unique address. When storing multiple items, two fundamental approaches exist: arrays and linked lists.

### Arrays vs. Linked Lists

The book uses the analogy of sitting with friends at a movie theater to explain the tradeoffs.

**Arrays** store elements contiguously (right next to each other) in memory. This enables **random access** -- you can jump to any element instantly using its index (O(1) read). But insertion is slow (O(n)) because adding an element may require shifting all subsequent elements or, if there is no adjacent free space, copying the entire array to a new location. A common optimization is "holding seats" -- requesting extra slots upfront -- but this wastes memory if unused, and may still require relocation if exceeded.

**Linked lists** store elements anywhere in memory, with each element storing a pointer (address) to the next element. This makes **insertion and deletion** fast (O(1)) -- you just change a pointer. But reading is slow (O(n)) because you must traverse from the first element, following pointers to reach any specific element (sequential access only).

| Operation  | Arrays     | Linked Lists |
|------------|------------|--------------|
| Reading    | O(1)       | O(n)         |
| Insertion  | O(n)       | O(1)         |
| Deletion   | O(n)       | O(1)         |

Insertion and deletion for linked lists are O(1) only if you have immediate access to the element's location. In practice, the first and last elements are tracked, making operations at those positions O(1).

**Why arrays are more commonly used:**
1. **Random access** is needed for many algorithms (e.g., binary search requires jumping to the middle element).
2. **CPU caching** makes sequential reads of contiguous array memory faster than following scattered linked list pointers.
3. **Memory efficiency** -- linked lists use extra memory for pointers; arrays waste memory only if you over-allocate.

Array elements are numbered starting from 0 (index 0). The position of an element is called its **index**.

### Selection Sort

Selection sort works by repeatedly scanning the unsorted portion to find the smallest (or largest) element and adding it to a new sorted list. Each scan takes O(n), and you perform n scans. Even though you check n-1, n-2, ... elements on subsequent passes, the constant factor is dropped in Big O notation, giving O(n^2) total. The book provides Python code with a `findSmallest` helper function and a `selectionSort` function that copies the array, repeatedly finds and removes the smallest element, and appends it to a new array.

---

## Chapter 3: Recursion

### What Is Recursion?

Recursion is a coding technique where a function calls itself. The book uses the analogy of finding a key in nested boxes: a loop-based approach maintains a pile of boxes to search, while the recursive approach simply says "if you find a box, search inside it." The recursive approach is often clearer, though there is no performance benefit. As Leigh Caldwell noted on Stack Overflow: "Loops may achieve a performance gain for your program. Recursion may achieve a performance gain for your programmer. Choose which is more important in your situation!"

### Base Case and Recursive Case

Every recursive function has two essential parts:
- **Base case:** The condition where the function stops calling itself (prevents infinite loops).
- **Recursive case:** The condition where the function calls itself with a modified input that moves toward the base case.

Without a base case, a recursive function runs forever, filling the call stack until a stack overflow error occurs.

### The Call Stack

The **call stack** is a stack data structure used internally by the computer to manage function calls. When you call a function, a box of memory (containing variable values) is pushed onto the stack. When the function returns, that box is popped off. When you call a function from within another function, the calling function is **paused in a partially completed state** -- all its variables remain on the stack until it resumes.

The book walks through the factorial function `fact(x)` in detail:
- `fact(3)` calls `fact(2)`, which calls `fact(1)`.
- The base case `fact(1)` returns 1.
- Then `fact(2)` returns 2 * 1 = 2.
- Then `fact(3)` returns 3 * 2 = 6.
- Each call has its own copy of the variable `x`.

The stack plays a crucial role in recursion: it acts as the "pile of boxes" that a recursive function needs to track. Using the stack is convenient but costs memory. When the stack grows too tall, you have two options: rewrite using a loop, or use tail recursion (an advanced technique not supported by all languages).

A **stack** has two operations: push (add to top) and pop (remove from top). It is a LIFO (last in, first out) data structure.

---

## Chapter 4: Quicksort

### Divide and Conquer (D&C)

D&C is a well-known recursive problem-solving technique. It is not a specific algorithm but a way of thinking about problems. The strategy:
1. Figure out a simple **base case** (the simplest possible case).
2. **Divide or decrease** the problem until it becomes the base case.

**Example 1: The farmer's plot.** A farmer has a 1680m x 640m plot and wants to divide it into the largest possible equal squares. Using D&C: mark out 640x640 squares (two fit), leaving a 640x400 remainder. Apply the same algorithm to the 640x400 remainder (marking 400x400 squares), leaving 400x240. Continue: 240x160, then 160x80. At 160x80, 80 divides evenly -- that is the base case. The answer is 80m x 80m squares. This is Euclid's algorithm for finding the greatest common denominator.

**Example 2: Summing an array.** Base case: empty array returns 0, single-element array returns that element. Recursive case: `sum([2,4,6]) = 2 + sum([4,6])`. You decrease the problem by removing the first element and recursing on the rest.

D&C builds toward **inductive proofs**: prove the base case works, then prove that if it works for size n, it works for size n+1. This gives you confidence that the algorithm works for all sizes.

### Quicksort

Quicksort uses D&C to sort arrays:
1. Pick a **pivot** element from the array.
2. **Partition** the array into two sub-arrays: elements less than the pivot and elements greater than the pivot.
3. Recursively call quicksort on both sub-arrays.
4. Combine: `quicksort(less) + [pivot] + quicksort(greater)`.

Base case: arrays of 0 or 1 elements are already sorted (return as-is).

The book provides clean Python code:
```python
def quicksort(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i <= pivot]
        greater = [i for i in array[1:] if i > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)
```

### Big O Revisited and Quicksort Performance

Quicksort's performance depends on pivot choice:
- **Worst case:** O(n^2) -- occurs when the pivot always creates maximally unbalanced partitions. Example: always choosing the first element on an already-sorted array means one sub-array is always empty. The call stack has O(n) levels, each doing O(n) work.
- **Best/Average case:** O(n log n) -- occurs when the pivot roughly divides the array in half. The call stack has O(log n) levels, each doing O(n) work.

**The constant factor matters:** Big O notation hides a constant `c` (e.g., 10ms * n vs 1sec * n). For different Big O classes (O(n) vs O(log n)), the constant does not matter for large n. But for the same Big O class, it can matter. Quicksort is faster than merge sort in practice because quicksort has a smaller constant factor, even though merge sort is always O(n log n).

**Choosing a random pivot** ensures you hit the average case most of the time. The only exception: if all elements are identical, you always get worst-case performance without additional logic.

---

## Chapter 5: Hash Tables

### Hash Functions

A hash function is a function that takes a string and returns a number (index). Requirements:
1. **Consistency** -- same input always maps to the same output.
2. **Good distribution** -- different keys should map to different indices as much as possible.

Combining a hash function with an array produces a **hash table** (also called hash map, dictionary, map, or associative array). In Python, hash tables are called **dictionaries** and are created with `{}`.

The hash function tells you exactly where to store and find data, eliminating the need to search. This gives O(1) average-case lookup time.

### Use Cases

**1. Lookups:** Mapping names to phone numbers, domain names to IP addresses (DNS resolution). A DNS cache can be built as a hash table for fast lookups.

**2. Preventing duplicate entries:** A voting system checks whether someone has already voted by looking up their name in a hash table. Hash tables make duplicate checking O(1) instead of O(n) with a list.

**3. Caching/memoization:** Websites like Facebook cache pages that are the same for all logged-out users. Instead of regenerating the page each time, check the hash table for a cached version. The book provides caching pseudocode that checks a hash first, and only fetches from the server on a miss, storing the result in the cache for future requests.

### Collisions

In reality, hash functions cannot perfectly map every key to a unique slot. A **collision** occurs when two keys hash to the same index. Collisions are resolved by using a **linked list** at each slot. If many keys collide at one slot, searching that linked list degrades to O(n).

Two lessons:
- The hash function is critical -- a good one distributes keys evenly.
- Long linked lists kill performance.

**Worst-case scenario illustrated:** If you work at a grocery store that only sells produce starting with 'A' (apples, avocados, apricokes, artichokes...) and your hash function uses the first letter as the index, every single item maps to the same slot. The entire hash table is empty except for one giant linked list -- effectively no better than a linked list. This shows why choosing a good hash function that maps keys broadly is essential.

A perfect hash function (injective function) where every key maps to a unique slot is called an **injective function**. In practice, perfect hash functions are rare. The hash function must also only return valid indexes for the array size -- it cannot return 100 if the array only has 5 slots.

### Performance and Tuning

| Operation | Average Case | Worst Case |
|-----------|-------------|------------|
| Search    | O(1)        | O(n)       |
| Insert    | O(1)        | O(n)       |
| Delete    | O(1)        | O(n)       |

To avoid worst-case performance:
- **Load factor** = number of items / number of slots. Keep it below 0.7. When exceeded, **resize** the hash table (typically double the array) and reinsert all items. Resizing is expensive but averages out to O(1).
- **Good hash function:** Distributes values evenly across slots. You rarely need to implement one yourself -- use your language's built-in hash table. Google's CityHash (used in their Abseil library) is a good reference.

---

## Chapter 6: Breadth-First Search (BFS)

### Introduction to Graphs

A **graph** models a set of connections. Graphs consist of **nodes** (vertices) and **edges** (connections between nodes). If an edge points from node A to node B, A is B's **in-neighbor** and B is A's **out-neighbor**.

- **Directed graph:** Edges have direction (one-way relationships, shown with arrows).
- **Undirected graph:** Edges have no direction (two-way relationships, shown with lines).

Graphs are implemented in code using hash tables: each node maps to a list (array) of its neighbors.

### Breadth-First Search

BFS answers two questions:
1. Is there a path from node A to node B?
2. What is the shortest path (fewest edges) from A to B?

BFS works by exploring all first-degree connections, then all second-degree connections, and so on -- radiating outward from the start. It finds the shortest path because it checks all closer connections before farther ones.

**The mango seller example:** You want to find the nearest mango seller in your social network. Check your friends first (first-degree). If none are sellers, check their friends (second-degree). Add each person's friends to the search list as you go.

**Queues:** To guarantee the correct search order (first-degree before second-degree), you must use a **queue** (FIFO: first in, first out). People added to the list first are searched first. A **stack** (LIFO) would search in the wrong order and might find a distant match before a closer one.

### Implementing BFS

1. Keep a queue of people to search.
2. Dequeue a person and check if they match the target.
3. If not, add all their out-neighbors to the queue.
4. Track already-searched people in a **set** to avoid infinite loops (especially important in graphs with cycles or mutual friendships).
5. Repeat until target found or queue empty.

**Graph representation:** Graphs are implemented using hash tables where each node maps to an array of its neighbors. Example:
```python
graph = {}
graph["you"] = ["alice", "bob", "claire"]
graph["bob"] = ["anuj", "peggy"]
graph["alice"] = ["peggy"]
graph["claire"] = ["thom", "jonny"]
```

**Directed vs. undirected graphs:** In the example, Anuj, Peggy, Thom, and Jonny have empty neighbor lists -- they are endpoints. This is a directed graph (relationships go one way). An undirected graph has no arrows; both nodes in an edge are mutual neighbors. With undirected graphs, the simpler term "neighbor" replaces "in-neighbor" and "out-neighbor."

**Why checking duplicates is critical:** If you do not track searched people, two problems arise: (1) unnecessary duplicate work (Peggy gets added to the queue multiple times through different paths), and (2) infinite loops in cyclic graphs. The book shows a graph where you and Peggy point to each other -- without deduplication, the algorithm bounces between them forever.

**Running time:** O(V + E) where V = number of vertices and E = number of edges. You follow each edge at most once, and each vertex is processed at most once.

### Topological Sort

A **topological sort** produces an ordered list from a graph such that dependencies come before the tasks that depend on them. Example: a morning routine graph where "eat breakfast" depends on "brush teeth." Topological sort is useful for task scheduling (e.g., planning a wedding).

### Trees

A **tree** is a special type of graph that is **connected and acyclic** (no edges point back). In trees, nodes have at most one parent. The root has no parent; leaf nodes have no children. Trees are important enough to warrant their own chapters (7 and 8).

---

## Chapter 7: Trees

### Your First Tree

Trees are a type of graph -- specifically, connected acyclic graphs. The book works with **rooted trees** (trees with one designated root node). Key terminology: root, leaf, parent, child.

**File directories as trees:** A file system is a tree structure. BFS can traverse it to list all files. A key advantage: since trees have no cycles, you never need to track visited nodes (no risk of infinite loops). Each node has at most one parent, so there is no way to revisit a folder. This makes tree traversal code simpler than general graph traversal. Symbolic links can introduce cycles, breaking the tree property, but Python handles this with an error.

### Depth-First Search (DFS)

DFS is another tree/graph traversal algorithm. Unlike BFS (which uses a queue and explores level by level), DFS uses **recursion** and goes deep immediately -- when it finds a subdirectory, it immediately looks inside rather than adding it to a queue.

**BFS vs DFS output:** For the same file tree, BFS and DFS produce different file orderings because they traverse in different patterns. BFS visits nodes level by level; DFS follows each branch to its depth before backtracking.

**Critical difference:** DFS **cannot** find the shortest path. Because DFS goes deep immediately, it may find a target node that is far away before finding one that is closer. BFS guarantees finding the closest match by checking all first-degree connections before second-degree.

**Use cases:** DFS can be used for topological sort. Both BFS and DFS work as general traversal algorithms for tasks like listing all files.

### Binary Trees

A **binary tree** is a tree where each node has **at most two children**, traditionally called the left child and right child. Binary trees appear throughout computer science. An ancestry tree is a natural example (two biological parents per person).

### Huffman Coding

Huffman coding is a text compression algorithm that makes clever use of binary trees. It is the foundation for modern compression algorithms.

**Background on character encoding:**
- **ASCII** (1960s): 7-bit encoding, 128 characters. Limited to English/European characters.
- **ISO-8859-1**: 8-bit encoding, 256 characters. Each character = 1 byte (8 bits). Still limited, and countries began creating their own encodings (Japan alone has several). A messy situation.
- **Unicode/UTF-8**: Variable-length encoding (1-4 bytes per character), 149,000+ characters (including 1,000+ emojis). The modern standard, introduced to unify all encodings. UTF-8 is the recommended default for any project.

**How binary encodes characters:** In ISO-8859-1, each character is 8 bits. The letter 'a' is 01100001 (97 in decimal). The null character is 00000000 and the Latin small letter y with diaeresis (y) is 11111111. With 8 bits, there are 256 possible combinations, supporting 256 characters. You can verify encoding with the `xxd -b` command on Unix to see binary contents.

In ISO-8859-1, the word "tilt" is: 01110100 01101001 01101100 01110100 (4 bytes = 32 bits).

**How Huffman coding works:**
1. Build a binary tree where characters only appear at **leaf nodes**.
2. To find a character's code, trace the path from root to that leaf: left branch = 0, right branch = 1.
3. Characters that appear **more frequently** get **shorter codes** (placed closer to the root). Rare characters get longer codes.

**Simple example -- "tilt":** The word uses only 3 unique letters (t, i, l), so we do not need 8 bits per character. A Huffman tree gives: t=1, i=00, l=01. The encoded word "tilt" becomes 1 00 01 1 (just 7 bits instead of 32). That is a 78% compression.

**More complex example -- "paranoid android":** This phrase has many different characters with varying frequencies. The Huffman tree generates codes of different lengths: frequently appearing 'd' (3 occurrences) gets a short 2-digit code (10), while rare 'p' (1 occurrence) gets a longer 4-digit code (0001). The code for 'i' is 3 digits (011).

**Decoding variable-length codes:** Because codes have different lengths (2, 3, or 4 digits), you cannot chunk the binary data into fixed-size pieces like ISO-8859-1. Instead, you read one bit at a time and traverse the tree: starting at root, 0 means go left, 1 means go right. When you reach a leaf node, you have decoded a character. Return to the root and continue. Example: decoding 01101010 yields "rad" by following the tree path 0-11 (r), 0-1 (a), 1-0 (d).

For "paranoid android": the letter 'd' appears 3 times and gets a short 2-bit code, while 'p' appears once and gets a 4-bit code.

**Decoding:** Read one bit at a time, traversing the tree from root. When you reach a leaf, output that character and return to root. Since codes have variable lengths, you cannot use fixed-width chunking like ISO-8859-1.

**Why trees are essential for Huffman coding:**
- No cycles guarantees you always reach a letter (no infinite loops).
- Letters only at leaf nodes prevents code overlap/ambiguity.
- Unique paths from root to each leaf guarantee unique codes.
- Rooted trees provide a known starting point.
- Binary trees match binary's two-digit system (0 = left, 1 = right).

---

## Chapter 8: Balanced Trees

### Binary Search Trees (BSTs)

A BST is a binary tree with a special property: for every node, all values in the left subtree are smaller, and all values in the right subtree are greater. This enables fast O(log n) search by eliminating half the tree at each step -- exactly like binary search.

**The problem with arrays:** Binary search on a sorted array gives O(log n) search, but **insertion** requires shifting elements (O(n)). Linked lists give O(1) insertion but O(n) search. We want O(log n) for both.

**The problem with unbalanced BSTs:** If elements are inserted in sorted order, the tree degenerates into a linked list shape with O(n) height. Searching takes O(n) -- no better than a linked list.

### Tree Height and Performance

- A **perfectly balanced tree** with 7 nodes has height 2 (O(log n)), giving O(log n) search.
- A **worst-case tree** (linear chain) with 7 nodes has height 6 (O(n)), giving O(n) search.

The goal is to **guarantee** O(log n) height.

### AVL Trees

AVL trees are **self-balancing BSTs** that maintain O(log n) height through **rotations**. Named after Adelson-Velsky and Landis.

**Rotations** rearrange nodes to reduce height. A left rotation takes a right-heavy subtree and makes the right child the new root. A right rotation does the opposite. AVL trees require at most one rotation per insertion.

**Detailed rotation example:** Start with root 10. Insert 20 (goes right, balance factor of 10 becomes -1, still valid). Insert 30 (goes right of 20, balance factor of 10 becomes -2, triggering rebalance). Left rotation makes 20 the new root with 10 as left child and 30 as right child. All balance factors return to 0. Insert 40 (goes right of 30, no rotation needed since 20's balance is -1). Insert 25 (goes left of 30). Node 10's balance drops to -2, triggering rotation. The key insight: you only need to rotate the unbalanced ancestor closest to the inserted node, not the entire tree.

**Balance factor:** Each node stores either its height or a balance factor (left subtree height minus right subtree height). Valid values: -1, 0, or 1. If a node's balance factor drops below -1 or exceeds 1 after insertion, the tree rebalances through rotation. After inserting a node, you set its height/balance factor, then walk up the tree updating ancestors. You only need to store one of these -- the balance factor can be computed from heights. Leaf nodes always have balance factor 0 (no children to be unbalanced). An important property: AVL trees require at most one rebalancing operation after an insert.

**Performance:** AVL trees guarantee O(log n) for both search and insertion. Insertion is just a search to find the right position plus pointer manipulation (like a linked list), plus at most one rotation. The book shows a detailed trace of inserting 55 into a tree and updating height (H) and balance factor (BF) values for all ancestors going up to the root.

| Data Structure | Search   | Insert   |
|----------------|----------|----------|
| Sorted Array   | O(log n) | O(n)     |
| Linked List    | O(n)     | O(1)     |
| Balanced BST   | O(log n) | O(log n) |

### Splay Trees

Splay trees are a different take on balanced BSTs. When you look up a node, it is moved to the root through rotations. Recently accessed nodes cluster near the top, making subsequent lookups faster. The tree is not guaranteed to be balanced at all times -- individual searches may exceed O(log n). However, n searches are guaranteed to take O(n log n) total, averaging O(log n) per operation. This makes splay trees ideal for workloads with locality of reference.

### B-Trees

B-trees are a generalized form of BST where each node can have **multiple keys and multiple children** (not limited to two). The number of children is always one more than the number of keys. The BST ordering property still holds: for each key, all keys in left subtrees are smaller, and all keys in right subtrees are larger.

**Why B-trees matter -- minimizing seek time:** The key optimization is physical. On disk, **seek time** (the time to physically move to the data) is the bottleneck. B-trees store more data per node, so you read larger chunks per seek, reducing the total number of expensive seeks. Instead of seeking to disk for every small binary tree node, B-trees read a bigger chunk each time. This is why B-trees are the standard data structure for databases.

The ordering within B-trees follows a "snaking" pattern starting from the lower-left node, traversing across the entire tree while maintaining sorted order.

---

## Chapter 9: Dijkstra's Algorithm

### Weighted Graphs

Edges in a **weighted graph** have numbers (weights) representing cost, distance, or time. A graph without weights is **unweighted**.
- Use **BFS** for shortest path in unweighted graphs (fewest segments).
- Use **Dijkstra's algorithm** for shortest path in weighted graphs with non-negative weights.

A **cycle** in a graph means you can start at a node and return to it. Following a cycle never helps find the shortest path because it adds weight. Undirected graphs inherently create cycles (each edge is two-way).

### How Dijkstra's Algorithm Works

Four steps:
1. Find the **cheapest** unprocessed node (the one you can reach with the least total cost).
2. For each out-neighbor, calculate the cost to reach it **through** this node.
3. If that cost is lower than previously known, **update** the cost and set this node as the parent.
4. Repeat until all nodes are processed. Trace back through parents to reconstruct the path.

**Key insight:** The cheapest node is guaranteed to have its final shortest-path cost. There is no cheaper way to reach it because any other path would have to go through a more expensive node first.

**Detailed walkthrough -- the travel time example:** Start node connects to node A (6 minutes) and node B (2 minutes). Node B connects to node A (3 minutes) and Finish (5 minutes). Node A connects to Finish (1 minute). Initial costs: A=6, B=2, Finish=infinity.

- Step 1: B is cheapest (2 min). Update A through B: 2+3=5 (cheaper than 6, update cost and parent). Update Finish through B: 2+5=7 (cheaper than infinity, update). B is processed.
- Step 2: A is cheapest unprocessed (5 min). Update Finish through A: 5+1=6 (cheaper than 7, update). A is processed.
- Final costs: B=2, A=5, Finish=6. Path: Start -> B -> A -> Finish (6 minutes total).
- Note: BFS would have found Start -> A -> Finish (two segments, 7 minutes) as "shortest" since it ignores weights. Dijkstra's found a cheaper 3-segment path.

**The trading example:** Rama wants to trade a music book for a piano, minimizing money spent. The graph has items as nodes and trade costs as edge weights. Alex offers a poster ($0) or LP ($5) for the book. Amy offers guitar ($30 from poster, $15 from LP) or drums ($35 from poster, $25 from LP). Beethoven offers piano ($40 from guitar, $35 from drums). Dijkstra's processes nodes in order of cheapest cost and finds the path: Book -> LP ($5) -> Drums ($25 more) -> Piano ($5 more) = $35 total.

**Path reconstruction:** After the algorithm finishes, trace back through the parents hash table. Piano's parent is drums. Drums' parent is LP. LP's parent is book. The complete cheapest trading sequence costs Rama only $35.

### Implementation

Uses three hash tables:
- **graph:** Adjacency list with weights (nested hash tables). Each node maps to a hash table of its out-neighbors and their edge weights. Example: `graph["start"]["a"] = 6`.
- **costs:** Current cheapest cost to each node. Initialize with known direct costs from the start node; unknown nodes set to infinity (`math.inf` in Python).
- **parents:** Maps each node to the node that provides the cheapest known path to it. Used for reconstructing the final path by tracing back from the target to the source.

A `processed` set tracks completed nodes. The `find_lowest_cost_node` function scans all nodes to find the cheapest unprocessed one. The main loop processes nodes until none remain, at each step checking all out-neighbors and updating costs/parents when cheaper paths are found. The code walks through each node: getting its cost, iterating over out-neighbors, computing new costs through the current node, and updating when improvements are found.

**More efficient implementation:** Using a priority queue (min-heap) instead of scanning all nodes for the cheapest one. This improves the overall running time. Priority queues are built on heaps (covered in Chapter 13).

### Negative-Weight Edges

Dijkstra's algorithm **does not work** with negative-weight edges. The algorithm's core assumption -- that processing the cheapest node means no cheaper path exists to it -- is violated by negative weights. For graphs with negative weights, use the **Bellman-Ford algorithm** instead.

---

## Chapter 10: Greedy Algorithms

### The Greedy Strategy

A greedy algorithm makes the **locally optimal** choice at each step, hoping to find a globally optimal solution. They are simple to write and fast to run.

**Classroom scheduling (works optimally):** Pick the class that ends soonest, remove conflicting classes, repeat. This produces the maximum number of non-overlapping classes -- the optimal solution.

**The knapsack problem (suboptimal):** A thief with a 4 lb knapsack wants to maximize stolen value. The greedy strategy (always take the most expensive item that fits) fails: taking a $3000 stereo (4 lb) prevents taking a $1500 guitar + $2000 laptop ($3500 total). The greedy answer ($3000) is suboptimal.

**Takeaway:** "Sometimes perfect is the enemy of good." Greedy algorithms get you close to optimal quickly.

### The Set-Covering Problem

You want to reach listeners in all 50 US states with the minimum number of radio stations. The exact solution requires checking all 2^n subsets -- impossibly slow. For 100 stations, checking all subsets would take 4 x 10^21 years.

**Greedy approximation:** Repeatedly pick the station covering the most uncovered states. Runs in O(n^2) time (much faster than O(2^n)).

The book provides complete Python code using **sets** -- collections that cannot have duplicates. Set operations: union (`|`), intersection (`&`), difference (`-`). The code maintains `states_needed` as a set, iterates through stations to find the one with the largest intersection of uncovered states, adds it to `final_stations`, and removes those states from `states_needed`.

### NP-Hard Problems

The set-covering problem is **NP-hard** -- no known fast algorithm exists. For such problems, approximation algorithms (often greedy) are the practical approach, judged by how fast they run and how close they get to optimal.

---

## Chapter 11: Dynamic Programming

### The Knapsack Problem Revisited

The exact solution (checking all 2^n subsets) is too slow for any reasonable number of items. Dynamic programming (DP) solves this by breaking the problem into discrete subproblems and building up.

**The grid:** Rows are items, columns are knapsack capacities from 1 lb to the full capacity.

**Cell formula:**
```
cell[i][j] = max(
  previous_max (cell[i-1][j]),
  value_of_current_item + cell[i-1][j - item_weight]
)
```

The book walks through a detailed example with a guitar ($1500, 1 lb), stereo ($3000, 4 lb), and laptop ($2000, 3 lb) in a 4 lb knapsack:
- **Guitar row:** Guitar fits in all capacities (1-4 lb), so every cell gets $1500.
- **Stereo row:** Stereo only fits at 4 lb. Previous max was $1500, but stereo alone is worth $3000. Cell (stereo, 4) = $3000.
- **Laptop row:** Laptop fits at 3 lb ($2000 > $1500 previous max). At 4 lb: laptop ($2000) + remaining 1 lb space. The 1 lb subproblem was solved in the guitar row ($1500). Total = $3500 > $3000 (previous max). Final answer: $3500 (guitar + laptop).

This is why you solve subproblems -- to know the value of remaining space when combining items.

**Adding a fourth item -- iPhone ($2000, 1 lb):** A new row is added. The iPhone alone at 1 lb is worth $2000, beating the guitar's $1500. At 2 lb, iPhone + guitar = $3500, beating the previous $1500. At 3 lb, iPhone + guitar = $3500, beating the laptop's $2000. At 4 lb, iPhone + remaining 3 lb of space = $2000 + $2000 (from the laptop row at 3 lb) = $4000, beating the previous $3500. The new optimal answer is $4000 (iPhone + laptop). This demonstrates the power of DP -- adding an item just requires adding one row, with no recalculation of previous rows.

**London travel itinerary example:** You have 2 days in London and want to maximize sightseeing. Attractions: Westminster Abbey (0.5 day, rating 7), Globe Theater (0.5 day, 6), National Gallery (1 day, 9), British Museum (2 days, 9), St. Paul's Cathedral (0.5 day, 8). This is the knapsack problem: the "knapsack" is your 2 days, and "items" are attractions with weights (time) and values (ratings). The DP grid has 0.5-day columns from 0.5 to 2, and rows for each attraction. The optimal answer maximizes your total rating within the time constraint.

**DP limitations:**
- Cannot handle fractions of items (use greedy instead -- take as much as possible of the most valuable item per unit weight).
- Cannot handle items that depend on each other (subproblems must be independent). For example, if visiting Paris makes London attractions "cheaper" (less travel time), DP cannot model this dependency.
- The optimal solution may not fill the knapsack completely (e.g., a $1M diamond weighing 3.5 lb in a 4 lb knapsack leaves 0.5 lb unused, but nothing fits there).
- Smaller items require finer grid columns (a 0.5 lb item needs 0.5 lb increments).
- Column values never decrease -- each cell stores the best estimate so far, which can only improve or stay the same.

### Knapsack FAQ

- **Adding an item:** Just add a new row. No recalculation of previous rows.
- **Row/column order:** Does not affect the final answer.
- **Column values never decrease** -- each cell stores the best estimate so far, which can only improve.
- **Smaller items (fractional weights):** Require finer-grained columns (e.g., 0.5 lb increments).
- **Stealing fractions of items:** DP cannot handle this; use a greedy algorithm instead (take the most valuable item per pound first).
- **Dependent items:** DP requires subproblems to be **independent**. If choosing one item affects another's cost/value, DP does not apply.
- **Multiple sub-knapsacks:** Sub-knapsacks can have their own sub-knapsacks, allowing any number of items to be combined.
- **Incomplete fill:** The optimal solution may not fill the knapsack completely.

### Longest Common Substring

DP can find the longest substring shared by two strings. The grid axes are the characters of each string. Each cell represents the length of the longest common substring ending at those character positions.

**Formula:**
```
if word_a[i] == word_b[j]:
    cell[i][j] = cell[i-1][j-1] + 1
else:
    cell[i][j] = 0
```
The answer is the **largest value anywhere in the grid** (not necessarily the last cell). If characters match, extend the streak; if not, reset to 0.

**Detailed walkthrough -- "hish" vs "fish":** The grid has rows h-i-s-h and columns f-i-s-h.

|   | F | I | S | H |
|---|---|---|---|---|
| H | 0 | 0 | 0 | 1 |
| I | 0 | 1 | 0 | 0 |
| S | 0 | 0 | 2 | 0 |
| H | 0 | 0 | 0 | 3 |

Cell (I, I) = 1 because both are 'i', and the diagonal cell was 0. Cell (S, S) = 2 because both are 's', and the diagonal cell (I, I) was 1. Cell (H, H) in the last row = 3 because both are 'h', and diagonal cell (S, S) was 2. The maximum is 3, representing "ish."

For "hish" vs "vista," the longest common substring is only 2 ("is"), showing how the algorithm distinguishes between similar and dissimilar strings. For "blue" vs "clues," the answer is 3 ("lue").

**The Feynman algorithm:** The book jokes about the Feynman approach to finding DP formulas: (1) write down the problem, (2) think real hard, (3) write down the solution. The truth is there is no single formula -- you must experiment and reason about what each cell should represent.

### Longest Common Subsequence

Similar but allows **gaps**. Used in diff tools (git diff), DNA comparison, and spell-checking (Levenshtein distance).

**Formula:**
```
if word_a[i] == word_b[j]:
    cell[i][j] = cell[i-1][j-1] + 1
else:
    cell[i][j] = max(cell[i-1][j], cell[i][j-1])
```
Example: "fosh" vs "fish" has a common substring of 2 ("sh") but a common subsequence of 3 (f, s, h).

### DP Tips
- Picture the problem as a grid.
- Cell values are what you are optimizing.
- Each cell is a subproblem -- figure out how to divide the problem to determine the axes.
- There is no single formula -- you must experiment.
- DP works when you are optimizing something given a constraint, and subproblems are discrete and independent.

---

## Chapter 12: K-Nearest Neighbors (KNN)

### Classification

KNN classifies items by looking at the k nearest labeled data points. Example: classifying a fruit as orange or grapefruit based on size and color features. The majority class among the k nearest neighbors determines the classification.

### Building a Recommendations System

Users are represented as **vectors** (arrays of numbers) -- feature values like genre ratings. The **distance** between two users is calculated using the generalized Pythagorean formula for n dimensions:

```
distance = sqrt((a1-a2)^2 + (b1-b2)^2 + ... + (n1-n2)^2)
```

Close users in feature space have similar tastes. The book walks through a Netflix example where Priyanka and Justin have a distance of 2 (similar taste), while Priyanka and Morpheus are far apart. To recommend movies, find a user's k nearest neighbors and recommend what those neighbors liked.

### Feature Extraction

Converting an item into a list of comparable numbers. For fruit: size and color. For Netflix users: genre ratings. For OCR: lines, points, and curves extracted from images.

### Regression

While classification predicts a category, **regression** predicts a numerical value. Example: predicting bakery sales based on weather, holiday, and game features. Take the k nearest neighbors and average their values.

**Cosine similarity** is an alternative to the distance formula that compares vector angles rather than magnitude. It handles users who rate on different scales (e.g., one person rates everything 5 stars, another reserves 5 for the best).

### Picking Good Features

Good features:
- Directly correlate with what you are predicting.
- Do not introduce bias.
- The right number of neighbors (k): too low risks skew from outliers; too high includes irrelevant users. A rule of thumb is sqrt(N) for N total users.

### Introduction to Machine Learning

- **OCR (optical character recognition):** Extract features from character images, classify using KNN. Google uses OCR to digitize books.
- **Spam filters:** Use Naive Bayes classifier -- calculate the probability of spam based on word frequencies in training data.
- **Training an ML model:** Gather data -> clean data (remove bad/junk data) -> extract features -> train model on 90% of data -> validate on remaining 10% -> evaluate predictions against known answers -> tune parameters (e.g., try different k values) -> deploy.

---

## Chapter 13: Where to Go Next

Brief introductions to additional algorithms:

1. **Linear Regression:** Fits a line to data points for predicting continuous values. Plot data, fit a line, use the line for predictions. A foundational ML technique.

2. **Inverted Indexes:** Maps words to the documents containing them. The core data structure behind search engines. Hash table where keys are words and values are lists of pages.

3. **The Fourier Transform:** Decomposes a signal into component frequencies. Analogy: given a smoothie, it tells you the ingredients. Used in MP3 compression (remove inaudible frequencies), JPG compression, earthquake prediction, DNA analysis, and Shazam.

4. **Parallel Algorithms:** Use multiple CPU cores. Challenges: overhead of managing parallelism, Amdahl's law (speedup limited by the non-parallelized portion -- optimizing the "sketch" doesn't help if "painting" takes most of the time), and load balancing across cores.

5. **MapReduce:** Distributed algorithm pattern running across many machines. Map applies a function to each item; reduce aggregates results. Used for massive datasets (billions of rows).

6. **Bloom Filters:** Probabilistic set membership testing. Possible false positives ("already crawled" when not), impossible false negatives. Uses minimal memory compared to hash tables. Used by Google, Reddit, and URL shorteners.

7. **HyperLogLog:** Approximates unique element count in massive datasets using minimal memory. Used for counting unique searches or page views.

8. **HTTPS and Diffie-Hellman Key Exchange:** Enables secure communication. Each party generates a private key, creates a public key by combining with a shared public pattern, then each combines the other's public key with their own private key to derive the same shared secret -- without ever sending the secret. HTTPS uses ephemeral Diffie-Hellman (fresh keys per connection) for forward secrecy. TLS is the modern protocol; SSL is the deprecated predecessor.

9. **Locality-Sensitive Hashing (Simhash):** Produces similar hashes for similar inputs (opposite of cryptographic hashes like SHA-256). Used for duplicate detection (Google web crawling), plagiarism detection, and copyright enforcement.

10. **Min Heaps and Priority Queues:** A tree structure where the root is always the minimum value. O(1) peek at minimum, O(log n) extract-min. Enables **heapsort** (repeatedly extract minimum). **Max heaps** have the largest value at root. **Priority queues** (built on heaps) return the highest-priority item, useful for to-do lists and efficient Dijkstra's implementation.

11. **Linear Programming:** Maximizes an objective function given linear constraints. The Simplex algorithm solves it. This is the most general optimization framework -- all graph algorithms in the book are subsets of linear programming.

---

## Appendix B: NP-Hard Problems

### Decision Problems

NP-complete problems are always **decision problems** (yes/no answers). The traveling salesperson optimization problem ("find the shortest route") becomes a decision problem: "Is there a route of length <= k?"

### The SAT (Satisfiability) Problem

Given a boolean formula, can you assign values to variables so the formula evaluates to true? The book uses a Seinfeld pizza-ordering example. SAT was the first NP-complete problem, identified in 1971. With n variables, there are 2^n possible assignments. Verifying a solution is easy (just plug in values and evaluate), but finding one requires potentially checking all 2^n possibilities.

### Key Definitions

- **P:** Problems solvable and verifiable in polynomial time (fast in both directions).
- **NP:** Problems verifiable in polynomial time. May or may not be efficiently solvable. P is a subset of NP.
- **P vs. NP:** The famous unsolved question -- does every problem that is quick to verify also have a fast solution? If P = NP, it would transform computing.
- **Reduction:** Transforming one problem into another you already know how to solve (e.g., converting binary multiplication to decimal). A fundamental technique in computer science.
- **NP-hard:** Every problem in NP can be reduced to this problem in polynomial time. These are at least as hard as the hardest problems in NP.
- **NP-complete:** A problem that is both in NP and NP-hard. Examples: SAT, set-covering, traveling salesperson (decision versions). Finding a polynomial-time algorithm for any single NP-complete problem would prove P = NP.

---

## Key Takeaways

1. **Binary search** eliminates half the remaining elements each step, running in O(log n) time. It requires sorted data and is dramatically faster than O(n) simple search for large datasets.

2. **Arrays** provide O(1) random access but O(n) insertion; **linked lists** provide O(1) insertion but O(n) access. Arrays are generally preferred due to caching benefits and random access.

3. **Big O notation** measures growth rate of operations, not speed in seconds. Constants are dropped. Know the five common runtimes: O(log n) < O(n) < O(n log n) < O(n^2) < O(n!).

4. **Recursion** requires both a base case and a recursive case. The call stack manages state automatically but can overflow. Loops are sometimes more performant; recursion is often clearer.

5. **Quicksort** uses divide and conquer with O(n log n) average-case performance. Choose a random pivot to avoid the O(n^2) worst case. It is faster than merge sort in practice due to a smaller constant factor.

6. **Hash tables** are the most useful complex data structure, providing O(1) average-case search, insert, and delete. Essential for lookups, deduplication, and caching. Maintain load factor below 0.7 and use a good hash function.

7. **BFS** finds the shortest path (fewest edges) in unweighted graphs using a queue. Always track visited nodes to prevent infinite loops in cyclic graphs.

8. **Trees** are acyclic graphs. Binary trees have at most two children. **Huffman coding** uses binary trees for lossless compression by assigning shorter codes to more frequent characters. Trees guarantee no code ambiguity because characters are only at leaves and paths are unique.

9. **Balanced BSTs** (AVL trees) provide O(log n) search and insertion through self-balancing rotations. **B-trees** generalize BSTs with multiple keys per node, optimizing disk seek time for databases. **Splay trees** cache recently accessed nodes at the root.

10. **Dijkstra's algorithm** finds the shortest weighted path in graphs with non-negative edges by always processing the cheapest node first. Use Bellman-Ford for negative-weight edges.

11. **Greedy algorithms** make locally optimal choices. They are simple and fast but not always optimal. They serve as effective approximation algorithms for NP-hard problems like set-covering.

12. **Dynamic programming** solves optimization problems by building a grid of subproblem solutions. It requires discrete, independent subproblems. Applications include the knapsack problem, longest common substring, and longest common subsequence.

13. **KNN** is a simple but powerful ML algorithm for both classification and regression. Performance depends critically on feature extraction and choosing good, unbiased features. It introduces core ML concepts like training, validation, and parameter tuning.

14. **NP-complete problems** (SAT, set-covering, traveling salesperson) have no known polynomial-time exact solution. When you encounter one, use an approximation algorithm. Understanding P, NP, NP-hard, and NP-complete helps you recognize when a problem is fundamentally hard.

---

## Appendix A: Performance of AVL Trees

Both a perfectly balanced tree and an AVL tree with 15 nodes offer O(log n) search performance, but their heights differ. A perfectly balanced tree has height 3 with O(log n) where the log base is 2. An AVL tree allows height differences of 1, so the same 15 nodes produce height 4. The AVL tree still achieves O(log n), but the base of the logarithm is the golden ratio (phi, approximately 1.618) rather than 2. This means AVL tree performance is slightly worse than a perfectly balanced tree, but both are O(log n) and the difference is small.

---

## Additional Patterns and Code Examples

### Key Python Patterns Used Throughout the Book

**Binary search implementation:**
```python
def binary_search(arr, item):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = arr[mid]
        if guess == item:
            return mid
        elif guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None
```

**Quicksort implementation:**
```python
def quicksort(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i <= pivot]
        greater = [i for i in array[1:] if i > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)
```

**BFS implementation pattern:**
```python
from collections import deque
def search(name):
    search_queue = deque()
    search_queue += graph[name]
    searched = set()
    while search_queue:
        person = search_queue.popleft()
        if not person in searched:
            if person_is_seller(person):
                print(person + " is a mango seller!")
                return True
            else:
                search_queue += graph[person]
                searched.add(person)
    return False
```

**Dijkstra's algorithm implementation:**
Uses three hash tables (graph with weights, costs, parents) plus a processed set. The `find_lowest_cost_node` function scans for the cheapest unprocessed node. The main loop processes nodes, updates neighbor costs and parents when cheaper paths are found, and traces back through parents to reconstruct the shortest path.

**Set-covering greedy algorithm:**
```python
while states_needed:
    best_station = None
    states_covered = set()
    for station, states in stations.items():
        covered = states_needed & states
        if len(covered) > len(states_covered):
            best_station = station
            states_covered = covered
    states_needed -= states_covered
    final_stations.add(best_station)
```

### Recurring Themes

**Data structure selection guide:**
- Need fast random access? Use an **array**.
- Need fast insertion/deletion at ends? Use a **linked list**.
- Need fast key-value lookup? Use a **hash table**.
- Need fast search AND insertion on sorted data? Use a **balanced BST** (AVL tree).
- Need to minimize disk seeks? Use a **B-tree**.
- Need to model connections? Use a **graph**.
- Need to process by priority? Use a **priority queue** (min/max heap).

**Algorithm selection guide:**
- Searching a sorted array? **Binary search** (O(log n)).
- Finding shortest path in unweighted graph? **BFS** (O(V + E)).
- Finding shortest weighted path? **Dijkstra's** (O(V^2) or O((V+E) log V) with heap).
- Sorting efficiently? **Quicksort** (O(n log n) average).
- NP-hard optimization? **Greedy approximation** or **dynamic programming**.
- Classification/regression? **KNN**.
- Compression? **Huffman coding**.

**Inductive proofs** appear repeatedly: prove the base case works, then prove that if the algorithm works for size n-1, it works for size n. This pattern applies to quicksort, recursive sum, D&C algorithms, and dynamic programming.
