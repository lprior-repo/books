# Data Structures and Algorithms with Go -- Comprehensive Summary

**Author:** Dusan Stojanovic
**Published:** 2024, BPB Publications
**ISBN:** 978-93-55518-897

 **First Edition:** 2024

 **Pages:** 7 chapters, plus Index

452 pages

 Appendices

---

This book provides a thorough, practical guide to fundamental data structures ( algorithms used in the Go programming language. Go's standard library offers completed implementations for some structures, while others are built from scratch with numerous practical examples and illustrations. The book progresses from fundamentals ( through advanced graph algorithms across seven chapters. Each chapter ends with review questions, and exercises. It is practical for real-world guidance on choosing the right data structure or algorithm for a problem.

---

## Chapter 1: Fundamentals of Data Structures and Algorithms

### Data Structures

A data structure is a description of data organization. For example, a data structure representing a point in two-dimensional space contains two integer values fields for x and y coordinates. Another example might define an address with fields for street name, street number, city, postal code, and country. We have complete freedom to create custom data structures using Go's `struct` type, Beyond these, well-known established data structures include arrays, graphs, maps, tree, list, stack, and queue.

 On each data structure, specific operations can be performed, such as sorting and searching on arrays.

 elements.

 For example, we can perform a sort operation on an array that This operation sorts array elements in the desired order.

 For each structure, we will explain the basic operations that can be performed.

 For practice, basic CRUD (Create, read, update, delete) operations are often implemented on Standard web services offering functionalities like logging in, reading, creating, editing, or deleting data commonly use arrays, slices, and maps. Trees and graphs, are for more complex problems like simulations or artificial intelligence.

)

**Characteristics of Data Structures**

Data structures can be classified by several characteristics:

-by **Linear vs. Non-linear:** Linear structures (arrays, lists, stacks, queues) arrange elements sequentially where each element is related to at most two neighboring elements. Non-linear structures (trees, graphs) allow one element to relate to multiple others through hierarchical parent-child relationships.
.
- **Static vs. Dynamic:** Static structures have a fixed size during execution and cannot be changed. Memory usage is often subopt, but but Dynamic structures grow and shrink based needed. allow optimal memory use.
- **Homogeneous vs. Heterogeneous:** Homogeneous structures contain elements of the same type (arrays, of integers). Heterogeneous structures mix types, such as a person struct with string and integer fields).
### Memory Representation

 Understanding how elements are stored in memory is essential for writing efficient programs. Two primary memory representations for exist:

**Sequential representation** and **Linked representation**.

**Sequential representation** stores elements one after another in continuous memory space. Physical and logical order are the same. An element size may span multiple memory locations depending on the relationship between element size and memory location size. For instance, if an element has 32 bits and the memory location is 16 bits, an 5-element array will take 10 memory locations. An `*` (asterisk) dere reads or modify the pointed-to value (`*pi` returns 18`). Changing `i` through the pointer.

 |

**Linked representation** arr elements in non-continual space at random memory locations. Physical and logical order differ. Pointers are stored alongside the data to link elements. Although more space is required, individual element because pointer storage is needed, arrays that up full capacity upfront while lists capacity grows incrementally.

 The, pointers also the fundamental to implementing linked structures in Go.

 For example, `var pi *int` declares an integer pointer, `pi = &i` sets to point to variable `i`, and `*pi = 18` changes `i` through the pointer.

 Graphically, a pointer can be represented as an arrow from1 memory location where the pointer and variable are stored. The other is at the bottom), opposite the top, the called the bottom. A Stack can grow downward or upward relative to the bottom. Growing downward means the stack takes previous or next memory location close to the top to add a new element. Growing upward, stack takes the next memory location.

 to add a new element.

 The, stacks and Go are two linear, dynamic, and usually homogeneous. It No restrictions on what can be stored. Usually, elements of the same type are stored. so it is homogeneous.

    A **Operations:** Two operations can be performed on the stack:
 push and pop.
 Push adds an element to the top and move the stack pointer. Pop removes the element from the top and move the stack pointer down. Popping from an empty stack returns -1 as invalid.

 The element is still in physical memory but no longer referenced. If we push a new element, it will override it old value. In practice, we only move the stack pointer to the lower element. The pop can be described with the following code:

```
func Push(v int) {
    sp = sp + 1
    stack[sp] = v
}
func Pop() int {
    if sp == -1 {
        return -1
    }
    v := stack[sp]
    sp = sp - 1
    return v
}
```
Previous functions assume variables `stack` and `sp` are defined outside function. Go does a Python

 has no exposed stack implementation for development, but internally uses a stack for `defer` statements. The `defer` statement delays execution of a function until the surrounding function returns. Arguments of deferred functions are calculated, but the function executes only when the surrounding function returns. in LIFO order. In the example below, `fmt.Print("a")` delayed until `main()` finishes, so "ba" prints`):
```
Calls of deferred function are pushed to stack. When the surrounding function returns, functions calls are popped from stack and executed in LIFO order. The 1234 will be printedout:

 The for `fmt.Print(4)` and `fmt.Print(3)` + `fmt.Print(2)` + `fmt.Print(1)`:
```

**Stack Implementation** uses a slice where the end of the slice logically represents the top of the stack, and highest index represents the stack pointer. If the stack pointer has value -1, the stack is empty. `Push()` uses `append()` to add element to end of slice (top of stack) and update stack pointer. `Pop()` checks if stack is empty and return -1 as invalid. If not empty, the top element is sliced off and returned. In the end, stack pointer updates)

```go
type Stack struct {
    stack []int
    stackPointer int
}
```
The theOnly slice and calculate highest index with `len()`, but we could include a stack pointer to follow the school example.  Elements from index 0, so stack grows and from the0, stack pointer is always -1.

 If empty stack. `Push()` uses `append()` to add element and end of slice. Pop operation returns -1 as invalid value. `Push()` updates stack pointer by `Pop()`:

 update stack pointer

 `Push/Pop`/`Push` and the second half.

 the stack. Dequeue from second half.

 the stack. Values 5, 1, 18, 21 are 9, 5, 1, 18 are then popped. Then popped/executed LIFO order).

 Each pop removes `stack` and returns value -1 as invalid, if the queue is empty at that moment.
 The Element `queue` extends `container/list` package `  `container/ring` (circular list). Go provides implementations for both double-linked and circular list through the standard library. For single-linked list, Go does not provide implementation through the standard library, so we must implement it ourselves.

 For ordered and unordered lists variants.

 `Insert()` method prepends nodes to unordered list, `InsertOrdered()` maintains sort order, `Remove()` method handles edge cases for empty and single-node lists, `Find()` method searches for nodes with specified value and `Concatenate()` method concatenates two lists, `Print()` method for human-readable format.

 The `Len()` returns number of nodes, and `Head()` return head pointer. `List` vs. Arrays comparison)
 Lists use linked memory representation, Nodes can be scattered across memory space. Lists can be ordered (ordered by unordered. For ordered lists, the `Insert` on unordered list is faster -- create node, set next pointer to current head, then move head to new node. For ordered list requires traversal with a temp pointer to find correct position, perform pointer manipulations. and increment node count.

 The, to remove a node, the disconnect it from list. To **Arrays vs. lists trade Guidelines:** Use arrays when capacity is known in advance and fast access to elements is essential. A List is the better option if we have many insert/remove operations at random places. `**Go standard library Implementations for Go provides double-linked and circular list through the `container/list` and package and Each node contains four fields: next, prev ( pointer to next and previous node, and value stored in the node, and pointer to list to which the node belongs. `type List struct` contains a root Element (named `element` in this implementation) that is not part of actual list. The `root` node is not an actual list. contains two fields and `next`, `prev`, and `list`, and `len` (length).

 Methods `New()` creates empty list and returns pointer to it Methods `PushFront()`, `PushBack()` insert at front/back, end, `InsertBefore()`, `InsertAfter()` insert before specified node), `Remove()` removes specified node, `Len()` returns length, `Front()` and `Back()` get first/last nodes. Iteration uses `Next()` and `Prev()` methods for forward/backbackward iteration. `Link()` concatenates two circular lists and returns pointer to new list. Method `Do()` calls function on each node. `container/ring` package: Since, circular list implements `container/ring`), the `Do()` method to apply function to each node. The `Value`, field. In iteration, we initialize node values. `Next()` and `Prev()` are used for iteration. `r = r.Next()`:
```go
for i := 0; i < r.Len(); i++ {
    r.Value = i
    r = r.Next()
}
}
```
    The Do() calls function in each node. `fmt.Println(p.(int))`:
 prints list content like `[5, 8, 25, 27]`.

---

## Chapter 5: Hashing and Maps

### Hashing

 is hashing transforms any given key into a value stored in a table indexed by the hash. A hash table (map) uses this indexing approach. When two or more keys map to the same position, a **collision** occurs; these keys are called **synonyms**,. A set of synonyms is an **equivalence class**. The `h(k)` transforms the key into array (table) index. Ideally, each key gives a unique position, the table. A hash function `h()` transforms the key to number belonging to table index range. The function should be simple, uniform, and possible to avoid collision. The `**Division method:** `h(k) = k mod n` where n is table size. Choice of n matters ( even n maps even even keys to even indices and even n index); even n=10, `h(27) = 27 mod 10 = 7`.
**Multiplication method:** `h(k) = floor(n * (c * k mod 1))` where 0 < c < 1. Constant should be close to golden ratio (about 00618). Example: `h(27) = floor(10 * (0.518 * 27 mod 1)) = floor(10 * 13.986 mod 1)) = floor(10 * 0.986)` = floor(9.86)` = 9.
 For table with 100 slots and h(27) = floor(10 * (0.518 * 27 mod 1) = floor(10 * 13.986 mod 1)) = floor(10 * 0.986)` = floor(9.86)` = 9.
 The **Mid-square method:** Square the key value and extract digits from middle for index. For example, 2 digits needed for table with 100 slots. For key 1989, 1989^2 = 3956121, digits 561 extracted from middle form index. The **Digit folding:** Divide key into equal-length parts, and sum. if result exceeds table size, modulo). For key 27051989: parts= 27+05+19+89 = the parts after summing is the40, modulo 100 = 40. The **Radix conversion:** Treat key as number in different base. For producing larger number from which digits are taken. For key 275 in decimal (radix 10), treated as base-12 system, `2*12^2 + 7*12^1 + 5*12^0` = 288 + 84 + 5 = 377`. Table length = 100, lowest digits (77) form index. The **Perfect hash:** Minimal function where collisions cannot occur -- maps n keys to n unique indices. Difficult to find. The **Digit analysis:** For known key distributions, analyzes digit positions frequency and selects positions with least variation. These hash functions can cause collision. Methods to resolve them include: increasing table size, and **open addressing** (finding another address when collision occurs) and **Linear probing:** `h(k, i) = (h(k) + i) mod n` -- sequentially check next slot.
 wrapping. to end of table, search continues at beginning. For example, keys 27 and 21 both hash to 1, values placed in next available slot.
 and **Quadratic probing:** `h(k, i) = (h(k) + i^2) mod n` -- intervals grows quadratically. For **Random probing:** Use pseudo-random sequence as probe sequence.
 and **Double hashing:** `h(k, i) = (h1(k) + i * h2(k)) mod n` -- uses two independent hash function for collision while synonyms are chained into lists at List headers occupy hash table slots. Multiple key hashing to same slot form linked list. The position. The `container/heap` package. Priority queue implementation uses Go's `container/heap`. Priority queue type must implement `heap.Interface` (which embeds `sort.Interface` plus `Push()` and `Pop()` method). `Less()` method determines priority ordering. Actual enqueue/dequeue must use `heap.Push()` and `heap.Pop()` to maintain heap properties. Calling `Push()`/`Pop()` directly would behave as a regular queue,           for `*` operator instead of `>` to determine max priority. `Less()` is `pq[i].value < pq[j].value` (less than for `pq[i].value > pq[j].value` (greater than) for max priority queue. Min priority queue example: `*pq` as `PriorityQueue` and `[]Element` type. Usage: `heap.Push(&pq, value)`, `heap.Pop(&pq)`. In a main() function, `make()` initializes empty queue, values  27, 5, 1, 18, 21, 9, 25 are 8, 1, 18, 1, 18, 5, 18, 25, 1, 27, 1) from priority queue, popped: values 1. Then popped 21 (invalid), popped 18 (invalid), popped 25 (invalid), popped 27 (invalid), and popped 27 (invalid).

 popped 5, 21, 25, 9, 1, 18, 9, 27, 5, 8, 25, 27, and their values in proper places for trees.    Deleting  node reduces internal node deletion to leaf deletion.     The **`Delete()`** method on `BinaryTree` type handles three cases: empty tree (sets root), leaf insertion (sets left or right child pointer), and internal insertion (inherits child from parent node, parent pointer of child pointer must inserted node). De **`GetRoot()`** returns pointer to root node. `Insert()` and `Delete()` method. The Example below, `main()` function creates a tree, inserts nodes, and deletes node 25:

 deletes node 5 as a leaf node).

**Traversal Algorithms**

    In `Traversal` each node exactly once in systematic order, following convention that left subtree is visited before before right. Four algorithms:
- **Preorder (Root, Left, Right):** Visit root, then recursively traverse left subtree, then right subtree. For tree in Figure 6.13: 18, 8, 5, 9, 25, 21, 27.
 Implements with recursion:
 after `node != nil {
        fmt.Println(node.value)
        Preorder(node.left)
        Preorder(node.right)
    }
}
```
- **Inorder (Left, Root, Right):** Recursively traverse left subtree, visit root, then right subtree. Produ sorted output for BSTs. Sequence: 5, 8, 9, 18, 21, 25, 27.
 Implement with recursion:
 after `node != nil {
        Inorder(node.left)
        fmt.Println(node.value)
        Inorder(node.right)
    }
}
```
- **Postorder (Left, Right, Root):** Recursively traverse left subtree, then right, then visit root. Root visited last. Sequence: 5, 9, 8, 21, 27, 25, 18. Implement with recursion, after `node != nil {
        Postorder(node.left)
        Postorder(node.right)
        fmt.Println(node.value)
    }
}
```
- **Level-order:** Visit all nodes at each level from left to right before moving to next level. Uses queue: enqueue root, dequeue nodes, process, enqueue children. Sequence: 18, 8, 25, 5, 9, 21, 27. In Chapter 4 for Stack and queue implementation that stores pointer to Node instead of integer. In function `New()` uses `list.New()`, `Enqueue()` uses `PushFront()`, `Dequeue()` calls `Back()` then `Remove()`. Function `IsEmpty()` checks `queue.Len() == 0`.

 function `Levelorder()` uses queue: add node 27 and node 27, 18, 21, 9, 5, 25. Then traverse graph. `graph.DFS(g, &node27)`. DFS explores paths: from starting node as far as possible, one direction, then backtracks to From node 27: 27, 18, 5, 25, 21, 25, 9. in `main()` function creates graph from Figure 7.8, execute traversal. We `g := graph.New()` ` g.AddNode()`, `g.AddEdge()`, etc.), `g.AddEdge()`, `g.AddEdge()`, `g.AddEdge()`, `g.AddEdge()`, `g.AddEdge()`, `g.AddEdge()`, `g.AddEdge()`, `g.AddEdge()`, `fmt.Println("BFS")` `graph.BFS(g, &node27)`, `fmt.Println("DFS")` `graph.DFS(g, &node27)`

### Spanning Trees ( spanning tree of undirected connected graph G = (V, E) is the tree ST = (U, E') meeting conditions: U = V, E' is subset of V; E' where E' is subset of E). Spanning tree is not unique. Cost is sum of edge weights in spanning tree. Minimal-cost spanning tree has MST) has lowest cost. Two algorithms: finding MST:
 Prim's algorithm and Kruskal's algorithm. `Weighted graph implementation` adds weight field to edges. A `WeightedGraph` struct adds weight field to `WeightedEdge`. `WeightedGraph` mirrors basic graph but `MST` struct holds node/edge sets with `Print()` method.

 Figure 7.10 weighted graph serves algorithm starts from any node, adds minimum-weight edge connecting tree node to non-tree node. Continues until all nodes are included. Sometimes called Jarnik's algorithm after original developer, `minEdge()` function returns minimum-weighted edge where one node belongs to MST node set while second does not. Algorithm uses priority queue of edges sorted by weight. Iteratively adds minimum-weight edge connecting two different components, merging them. Continues until MST has n-1 edges. Implementation tracks forest as map of int to []Node`, `findInForest()` function to locate nodes in forest. `Kruskal()` function places all edges in priority queue, initialize each node as separate component, then iteratively pop minimum-weight edge, connect components, merge (using append/delete), stop when MST has n-1 edges, ```go
func Kruskal(wg *WeightedGraph) *MST {
    treeEdges := make(map[WeightedEdge]struct{})
    pq := make(PriorityQueue, 0)
    for edge := range wg.edges {
        heap.Push(&pq, edge)
    }
    forest := make(map[int][]Node)
    i := 0
    for node := range wg.nodes {
        forest[i] = append(forest[i], node)
        i++
    }
    for n := 0; n < len(wg.nodes)-1 || pq.Len() == 0; {
        edge := heap.Pop(&pq).(Element).value
` i := findInForest(forest, edge.u.value)
        j := findInForest(forest, edge.v.value)
        if i != j {
            treeEdges[edge] = struct{}{}
            forest[i] = append(forest[i], forest[j]...)
            delete(forest, j)
            n++
        }
    }
    return &MST{wg.nodes, treeEdges}
}
```

`findInForest()` iterates through forest map and node arrays: locating specified node. Example code creates a weighted graph and Figure 7.10 and execute both algorithms. `mstPrim := graph.Prim(wg, &node21)` `mstPrim.Print()`
 `mstKruskal := graph.Kruskal(wg)`. `mstKruskal.Print()```
---

### Transitive Closure

 **Reachability matrix** P indicates whether a path exists between any pair of nodes: p[i,j] = 1 if reachable, 0 otherwise. This is transitive closure. of graph. Requires **adjacency matrix** -- square matrix indicating whether pairs of nodes are adjacent. Element `a[i,j] = 1` if adjacent, 0 otherwise. Nodes `a[i,j]` in 0` of and iteratively checks if path between nodes `i` and `j` can be established through intermediate node `k`. Complexity is O(n^3). for `Warshall()` accepts adjacency matrix as input, returns reachability matrix.

 Uses Boolean matrix for **true** for integer 1, and **false** for integer 0. In `p[i][j] = p[i][j] || (p[i][k] && p[k][j])` to simplify implementation. Then, iteratively checks if path between two nodes can be established through any other node `k`. Complexity O O(n^3). For each iteration, one node and `j` in `p[i][j]` becomes true if path through `k` exists. Otherwise, stays false. ```go
func Warshall(a [][]bool) (p [][]bool) {
    p = a
    for k := 0; k < len(p); k++ {
        for i := 0; i < len(p); i++ {
            for j := 0; j < len(p); j++ {
                p[i][j] = p[i][j] || (p[i][k] && p[k][j]
            }
        }
    }
    return
}
```

`main()` function creates a directed graph with an adjacency matrix from calculates transitive closure. Matrix values p[i,j] for 1 if path exists between nodes i and j, 0 otherwise. For directed graphs containing cycles, some diagonal elements j] where i = j have value 1. For undirected graphs, the matrix will be symmetric. and `p[j,i]` = p[i,j]`).

 if `p[j,i]` = p[i,j]`. For `p[j,i]` = p[i,j]`, we can calculate allowed latency for each edge using formula: `l(i,j) = LST[j] - EST[i] - w(i,j)` where `w(i,j)` is weight of edge connecting `i` and `j` in `w[i,j]` =` if elements have following values.:
- **Distance matrix** D as output.  where d[i,j] = shortest path weight between nodes `i` and `j`
 or infinity if no path between nodes.  **Floyd's Algorithm (O(n^3):** Relaxation algorithm that maintains upper-bound estimates. Initially, equal to edge weight or infinite if no edge exists. In subsequent iterations, check if current estimation can be reduced through intermediate node. The code use Boolean matrix. **True** for integer 1, **false** for integer 0. in `p[i][j] = p[i][j] || (p[i][k] && p[k][j])` to simplify implementation, we + **Dijkstra's Algorithm:** Finds shortest path from one starting node to all others. Does not accept negative weights. Maintains two sets: S (confirmed shortest distances) and `V` (remaining nodes with estimates. Atj`. At each step, node with smallest estimate moves to S, estimates for neighbors updated. The vector `d` holds final shortest paths. The `findMin()` helper returns node in set V with lowest estimate. The INF constant simulates infinity.

 `D[i] <= min && ok {` and min = d[i]`. The }    return
````
Example use INF = 99999 to simulate infinite. Steps table shows how set S and vector d evolve through each iteration. Node 0 is selected as starting node, 1 is S; nodes 18, 21, 9, 25, and added to S, node with smallest distance moved to S, estimates for remaining nodes updated. The **eccentricity** of a node: maximum distance to any other node. **Center** of graph: node with minimum eccentricity.

 | **Flow in Graphs:**  flow network is directed graph where edges have non-negative capacity (**source** with no input edges) and **target** (no output edges). Maximum flow = largest amount transferable from source to target. Applications include liquid flow, pipe systems, network routing, and transportation. Flow `f(u,v)` must satisfy:
 **Capacity constraint:** `f(u,v) <= c(u,v)` for all edges. **Symmetry constraint:** `f(u,v) = -f(v,u)` for all edges. **Flow conservation:** Incoming = outgoing flow equal for all nodes except source and target. Total node flow = 0. `Residual capacity` = capacity - flow`. **Augmenting path:** Path from source to target where all edges have positive residual capacity. Residual path capacity = smallest residual capacity of edge on augmenting path. | **Ford-Fulkerson Algorithm:** Starts with zero flow. Iteratively finds augmenting paths (modified BFS), increases flow by minimum residual capacity, accumulate total. Implementation tracks capacity and flow on each edge. `FlowGraph` struct holds nodes, edges maps, with `NewFlowGraph()`, `AddNode()`, `addEdge(u, v, c)`, `removeNode()`. `FordFulkerson()` initializes flow to zero, finds augmenting path, updates flow for each edge, accumulates max flow. `pathFlow()` finds minimum residual capacity. `AugmentingPath()` modifies BFS to reconstruct path and target node. Functions `inPath()` and `inPathDest()` verify source/destination continuity. Example creates graph from Figure 7.16 and calculate maximum flow between nodes 0-4. | **Topological Sorting:** For directed acyclic graphs ( topological sorting produces linear ordering where for every edge ( node u appears before v. Applications include scheduling interdependent activities like project management. Algorithm: find node with zero indegree, add to topological order, remove node with outgoing edges. Result is not unique. Property guaranteed: every DAG has at least one zero-indegree node. Implementation copies graph maps, finds zero-indegree node. | `TopSort()` function creates graph and execute topological sorting. Output: `[0, 1, 4, 3, 2]`. | **Critical Path:** For DAG modeling project activities, **critical path** is longest path from source to target. Determines minimum project duration. Activities on critical path cannot be delayed without extending the project. For each node, algorithm calculates EST (earliest start time) and LST (latest start time), then latency. EST for source = 0; LST of target = EST of target node. EST[j] = max(EST[i] + w(i,j)) over predecessors. LST[i] = min(LST[j] - w(i,j)) over successors. Latency = LST - EST. Activities with zero latency are critical. The algorithm uses `CriticalPath()` performs topological sort on then iterates through nodes to find predecessors/successors, compute EST/LST. Helper functions `findMax()` and `findMinLST()` implement formulas. Example creates  weighted graph with 6 nodes (0-5) and 8 weighted edges, run critical path algorithm, Output shows EST: `[0, 0, 7, 18, 15, 20, 25, 30]`, LST: `[30, 22, 30, 22, 30, 25, 30]`, L: `[30, 8, 8, 0, 0, 0, 0, 5, 0]`. Critical path: nodes 0, 2, 4, 5. Edge latency: `l(i,j) = LST[j] - EST[i] - w(i,j)`. | **Algorithm Complexity Summary:** BFS O(n+e), DFS O(n+e), Warshall O(n^3), Floyd O(n^3), Dijkstra O(n^2), Prim O(n^2), Kruskal O(e log n), Ford-Fulkerson O(VE^2), Topological Sort O(n+e), Critical Path O(n+e).

 | n = number of nodes, e = number of edges. V | Table 7.3 | Graph algorithms |
|--------|--------------------------|--------------------|--------------|
| BFS | Traversal | O(n + e) | Visit nodes level-by-level | Queue-based | Shortest path, MST | Reachability |
| DFS | Traversal | O(n + e) | Visit nodes depth-first | Stack/recursive | Shortest path, cycle detection |
| Prim's | MST | O(n^2) | Greedy, incremental connected component | Minimum spanning tree |
| Kruskal's | MST | O(e log n) | Forest merge with priority queue | Minimal spanning tree |
| Warshall | Transitive closure | O(n^3) | Reachability matrix from adjacency matrix |
| Floyd | All-pairs shortest paths | O(n^3) | Distance matrix from cost matrix |
| Dijkstra | Single-source shortest paths | O(n^2) | Distance vector from cost matrix |
| Ford-Fulkerson | Maximum flow | O(VE^2) | Residual network with augmenting paths |
| Topological Sort | Dependency ordering | O(n + e) | Linear order from DAG |
| Critical Path | Project scheduling | O(n + e) | EST/LST vectors from topological sort |

| Heap Sort | Sorting | O(n log n) | Heap data structure with extraction |
| Level-order | Tree traversal | O(n) | Level-by-level using queue |
| Preorder | Tree traversal | O(n) | Root, left, right recursive |
| Inorder | Tree traversal | O(n) | Left, root, right recursive |
| Postorder | Tree traversal | O(n) | Left, right, root recursive |

| Sequential Search | Search | O(n) | Linear scan through all elements |
| Binary Search | Search | O(log n) | Divide-and-conquer on sorted data |
| Insertion Sort | Sorting | O(n^2) | Sorted/unsorted partitioning |
| Selection Sort | Sorting | O(n^2) | Find minimum in un unsorted portion |
| Bubble Sort | Sorting | O(n^2) | Compare and swap adjacent elements |
| Quick Sort | Sorting | O(n log n) avg | Divide-and-conquer with partitioning |
| Heapsort | Sorting | O(n log n) | Heap property with extraction |

