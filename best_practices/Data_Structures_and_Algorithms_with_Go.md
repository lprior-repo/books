# Data Structures and Algorithms with Go — Deep Dive

**Author:** Dušan Stojanović
**Topic tags:** `#general` `#go` `#performance` `#concurrency`
**Language focus:** Go-first
**Sources:** `markdown_output/Data_Structures_and_Algorithms_with_Go_-_Dusan_Stojanovic/Data_Structures_and_Algorithms_with_Go_-_Dusan_Stojanovic.md` · `summaries/Data_Structures_and_Algorithms_with_Go_-_Dusan_Stojanovic.md`

## TL;DR
A practical, from-scratch tour of every core data structure (arrays, slices, lists, stacks, queues, maps, trees, graphs) and the canonical algorithms over them (search, sort, traversal, MST, shortest paths, max-flow, topological sort, critical path, heap sort). Go's standard library is used where it exists (`container/list`, `container/ring`, `container/heap`, `sort`) and the rest is hand-rolled in idiomatic Go. Apply when implementing any foundational data structure, when choosing between array/slice/list/map, or when wiring graph algorithms into Go services.

---

## Best Practices by Topic

### Algorithmic Complexity & Big-O

**Principle:** Complexity is calculated on two resources — *time* (CPU) and *space* (memory). When choosing among multiple algorithms, pick the one with the lowest complexity class.

**Do:**
- State the complexity of every algorithm you write (the book does this consistently).
- Remember the ordering of classes when picking algorithms.

**Don't:**
- Don't compare algorithms only by wall-clock — measure asymptotic class first.

Complexity ordering (least to most expensive):

```
O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(n^k), k>2 < O(k^n), k>1
```

Class summary used throughout the book:

| Class            | Example in book                     |
|------------------|-------------------------------------|
| `O(1)` constant  | Insert at head of unordered list    |
| `O(log n)`       | Binary search                       |
| `O(n)` linear    | Sequential search                   |
| `O(n log n)`     | Quick sort, heap sort, Kruskal's    |
| `O(n^2)` square  | Insertion / selection / bubble sort |
| `O(n^3)`         | Warshall, Floyd                     |
| `O(VE^2)`        | Ford-Fulkerson                      |

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Algorithmic complexity and O-notation"*

---

### Pointers — the Building Block for Linked Structures

**Principle:** A pointer holds the memory address of another variable. Linked representations (lists, trees, graphs) are impossible in Go without pointers.

**Do:**
- Use `*T` to declare a pointer to `T`.
- Use `&i` to take an address and `*p` to read/write through it.
- Pass pointers when a function must mutate the caller's value.

**Code:**
```go
var pi *int
```

```go
i := 27
pi = &i
*pi = 18
fmt.Println(*pi)
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Memory representation"*

---

### Custom Structs — Foundation for All Data Structures

**Principle:** When the standard library does not provide a structure, model it with a `struct` — a collection of fields.

**Do:**
- Use zero-value-friendly field types.
- Omitted fields in a struct literal get their zero value.

**Don't:**
- Don't reach for interfaces before you need polymorphism — start with structs.

**Code:**
```go
type Point struct {
 X int
 Y int
}
```

```go
var (
  p1 = Point{27, 5}
  p2 = Point{X: 18}
  p3 = Point{}
)
```

Access fields with `.`; take a pointer with `&`:

```go
p := Point{27, 5}
p.X = 18
pp := &p
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Structures in Go"*

---

### Functions in Go

**Principle:** Every algorithm in this book lives inside a function. Go functions support multiple return values, named returns, naked returns, and pointer arguments.

**Do:**
- Group same-typed params: `func sum(i, j int) int`.
- Use named returns for documentation and naked returns in short functions.
- Use pointer args when the caller's value must be mutated in place.

**Don't:**
- Don't return multiple values without documenting their meaning.

**Code:**
```go
func hello() {
 fmt.Println("Hello World")
}
func inc(i int) int {
 return i + 1
```

```go
}
func sum(i int, j int) int {
 return i + j
}
```

Same-type parameter shorthand:

```go
func sum(i, j int) int {
 return i + j
}
```

Multiple return values:

```go
func calc(i int) (int, int) {
 return i*i, i+i
}
```

Named (naked) return:

```go
func inc(i int) (res int) {
 res = i + 1
 return
}
```

Pointer argument — caller-visible mutation:

```go
func inc(i *int) {
 *i = *i + 1
}
```

```go
func main() {
 i := 5
 pi := &i
 inc(pi)
 fmt.Println(i)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Functions in Go"*

---

### Arrays in Go

**Principle:** Arrays are linear, homogeneous, fixed-size, sequentially stored. The length is part of the type — `[8]int` and `[5]int` are different types.

**Do:**
- Use arrays only when capacity is known and fixed.
- Reach for slices (below) for almost everything else.

**Code:**
```go
var a [8]int
```

```go
var a = [8]int{1, 18, 5, 27, 25, 8, 21, 9}
```

```go
var b = a[3]
```

```go
a[3] = 7
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Arrays in Go"*

---

### Slices — Go's Dynamic Array

**Principle:** A slice is a pointer into an underlying array, with `length` and `capacity` attributes. `append()` grows the slice; if capacity is exceeded a new underlying array is allocated.

**Do:**
- Default low bound is `0`, default high bound is `len(s)` — omit them when you can.
- Preallocate with `make([]T, 0, n)` when the final size is known.
- Remember that slices *share* the underlying array — writes through one slice are visible to others.

**Don't:**
- Don't forget that mutating a sub-slice mutates the underlying array.
- Don't assume capacity — check `cap(s)`.

**Code:**
```go
s[low:high]
```

```go
a := [8]int{1, 18, 5, 27, 8, 25, 9, 21}
var s []int = a[1:4]
fmt.Println(s[0])
```

```go
fmt.Println(len(s))
fmt.Println(s[len(s)–1]) // last element
```

Slice from another slice (shares underlying array):

```go
s1 := []int{1, 18, 5, 27, 8, 25, 9, 21}
s2 := s1[1:4]
```

`append()`:

```go
s := []int{1, 18, 5, 27, 8, 25, 9, 21}
s = append(s, 3, 21, 12, 30)
```

Preallocate with `make`:

```go
s := make([]int, 0, 5)
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Slices in Go"*

---

### Multidimensional Arrays (Matrices)

**Principle:** Matrices are stored sequentially by row. Declare with `[rows][cols]T`. When dimensions are omitted you must use `append()` to add rows.

**Code:**
```go
var matrix [3][3]int
```

```go
var matrix = [3][3]int{{1, 18, 5}, {27, 25, 8}, {21, 9, 12}}
```

```go
var n = matrix[1][2]
```

```go
a[2][0] = 7
```

Dynamically-sized matrices use `append()` per row:

```go
var matrix [][]int
matrix = append(matrix, []int{1, 18, 5}, []int{27, 8, 25})
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Multidimensional arrays"*

---

### Methods on Types

**Principle:** A method is a function with a receiver argument. Pointer receivers mutate the caller; value receivers do not.

**Do:**
- Use pointer receivers when the method must mutate state or the struct is large.

**Code:**
```go
type Rectangle struct {
 a, b int
}
```

```go
func (r Rectangle) Area() int {
  return r.a * r.b
}
```

```go
func (r Rectangle) Perimeter() int {
return 2*r.a + 2*r.b
 }
```

```go
func main() {
r := Rectangle{2, 3}
 fmt.Println("Area: ", r.Area())
 fmt.Println("Perimeter: ", r.Perimeter())
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Methods"*

---

### Interfaces — Implicit Implementation

**Principle:** A type implements an interface by implementing all its methods — no `implements` keyword, no explicit declaration.

**Do:**
- Define small interfaces (`Shape`, `sort.Interface`).
- Accept interfaces at function boundaries; return concrete types.

**Code:**
```go
type Shape interface {
 Area() int
 Perimeter() int
}
```

```go
type Rectangle struct {
  a, b int
 }
 func (r Rectangle) Area() int {
  return r.a * r.b
}
 func (r Rectangle) Perimeter() int {
return 2*r.a + 2*r.b
 }
 type Square struct {
  a int
 }
```

```go
func (s Square) Area() int {
 return s.a * s.a
}
func (s Square) Perimeter() int {
 return 4 * s.a
}
```

```go
func main() {
 r := Rectangle{2, 3}
 fmt.Println("Area: ", r.Area())
 fmt.Println("Perimeter: ", r.Perimeter())
```

```go
s := Square{4}
 fmt.Println("Area: ", s.Area())
 fmt.Println("Perimeter: ", s.Perimeter())
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Interface"*

---

### Sequential (Linear) Search — O(n)

**Principle:** Compare each element to the key until a match is found. For unordered arrays this is the *only* option; for ordered arrays you can bail early when elements exceed the key.

**Code:**
```go
func SeqSearch(array []int, key int) int {
    for I := 0; i < len(array); i++ {
      if key == array[i] {
         return i
      }
    }
    return -1
}
```

Idiomatic `for range` variant:

```go
func SeqSearch(array []int, key int) int {
 for i, elem := range array {
      if key == elem {
         return i
      }
    }
    return -1
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Sequential search"*

---

### Binary Search — O(log n)

**Principle:** Divide-and-conquer on a *sorted* array. Halve the search space each iteration by comparing the key to the middle element.

**Code:**
```go
func BinSearch(array []int, key int) int {
   low := 0
   high := len(array) - 1
   for low <= high {
      mid := (low + high) / 2
      if key == array[mid] {
        return mid
      } else if key < array[mid] {
        high = mid - 1
      } else {
        low = mid + 1
      }
```

```go
}
    return -1
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Binary search"*

---

### Standard Library `sort.Search*` — Use the Binary Search Wrappers

**Principle:** The `sort` package exposes `SearchInts`, `SearchFloat64s`, `SearchStrings`, all wrappers around the generic `Search(n, f)`.

**Code:**
```go
func Search(n int, f func(int) bool) int
```

```go
func SearchInts(a []int, x int) int {
```

```go
return Search(len(a), func(I int) bool { return a[i] >= x})
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Searching algorithms in Go"*

---

### Insertion Sort — O(n²)

**Principle:** Maintain a sorted prefix; insert each next element into its correct position within the prefix.

**Code:**
```go
func InsertionSort(array []int) []int {
 for i := 1; i < len(array); i++ {
  k := array[i]
  j := i - 1
```

```go
for j >= 0 && array[j] > k {
    array[j+1] = array[j]
    j = j - 1
  }
  array[j+1] = k
 }
 return array
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Insertion sort"*

---

### Selection Sort — O(n²)

**Principle:** Repeatedly find the minimum of the unsorted suffix and swap it to the end of the sorted prefix.

**Code:**
```go
func SelectionSort(array []int) []int {
 for i := 0; i < len(array)-1; i++ {
  min := array[i]
  pos := i
  for j := i + 1; j < len(array); j++ {
    if array[j] < min {
     min = array[j]
     pos = j
    }
  }
```

```go
array[pos] = array[i]
  array[i] = min
 }
 return array
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Selection sort"*

---

### Bubble Sort — O(n²)

**Principle:** Iterate repeatedly, swapping adjacent out-of-order elements. Largest unsorted element "bubbles" to its final position each pass.

**Code:**
```go
func BubbleSort(array []int) []int {
 n := len(array)
```

```go
for i := 0; i < n-1; i++ {
  for j := 0; j < n-i-1; j++ {
    if array[j] > array[j+1] {
     array[j], array[j+1] =
     array[j+1], array[j]
    }
  }
 }
 return array
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Bubble sort"*

---

### Quick Sort — O(n log n) avg, O(n²) worst

**Principle:** Divide-and-conquer: pick a pivot, partition elements into ≤ pivot and > pivot, recurse on each partition.

**Code:**
```go
func QuickSort(array []int, low, high int) []int {
 if low < high {
  array, j := partition(array, low, high)
  QuickSort(array, low, j-1)
  QuickSort(array, j+1, high)
 }
```

```go
return array
}
```

The `partition` helper uses two indices `i` and `j` walking toward each other:

```go
func partition(array []int, low, high int) ([]int, int) {
 pivot := array[low]
 i := low
 j := high
 for i < j {
```

```go
for array[i] <= pivot && i < j {
  i++
}
for array[j] > pivot {
  j--
}
if i < j {
  array[i], array[j] =
  array[j], array[i]
}
```

```go
}

array[low], array[j] = array[j], pivot
 return array, j
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Quick sort"*

---

### Standard Library `sort.Ints` / `sort.Sort` — O(n log n) Optimized Quick Sort

**Principle:** The `sort` package wraps an optimized quick sort behind `sort.Interface`. Stable sorts preserve equal-element order via `sort.Stable`.

**Code:**
```go
func Ints(x []int) { Sort(IntSlice(x)) }
```

The interface you must implement:

```go
type Interface interface {
  Len() int
  Less(i, j int) bool
  Swap(i, j int)
 }
```

`IntSlice` reference implementation:

```go
type IntSlice []int
 func (x IntSlice) Len() int { return len(x) }
 func (x IntSlice) Less(i, j int) bool { return x[i] < x[j] }
 func (x IntSlice) Swap(i, j int) { x[i], x[j] = x[j], x[i] }
```

Typical call site:

```go
array = []int{18, 1, 5, 27, 8, 25, 9, 21}
sort.Ints(array)
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Sorting algorithms in Go"*

---

### Single-Linked List — Built From Scratch

**Principle:** Lists use linked memory representation; each node holds a value and a pointer to the next node. The `head` pointer references the first node; `len` tracks node count.

**Do:**
- Handle empty-list edge case first in every mutator.
- Use a `temp` pointer for traversal; never reassign `head` mid-traversal.
- Set the removed node's `next` to `nil` so the GC can reclaim it.

**Code:**
```go
type Node struct {
 next *Node
 value int
}
```

```go
type List struct {
 head *Node
```

```go
len int
}
```

```go
func New() List {
 return List{
  head: nil,
  len: 0,
 }
}
```

Unordered insert — prepend in O(1):

```go
func (l *List) Insert(v int) {
 node := Node{
  next: nil,
  value: v,
 }
 if l.head != nil {
  node.next = l.head
 }
 l.head = &node
```

```go
l.len++
}
```

Ordered insert — walk to the correct position:

```go
func (l *List) InsertOrdered(v int) {
  node := Node{
   next: nil,
   value: v,
  }
  if l.head == nil {
```

```go
l.head = &node
 l.len++
 return
}
temp := l.head
for temp.next != nil && temp.next.value < v {
 temp = temp.next
}
node.next = temp.next
temp.next = &node
l.len++
```

```go
}
```

Remove — handle empty and single-node cases first:

```go
func (l *List) Remove(v int) {
  if l.head == nil {
   return
  }
```

```go
if l.len == 1 {
 l.head = nil
 l.len--
 return
}
for temp := l.head; temp != nil; temp = temp.next {
 if temp.next.value == v {
  node := temp.next
  temp.next = node.next
  node.next = nil
  l.len--
  return
```

```go
}
 }
}
```

Find:

```go
func (l *List) Find(v int) *Node {
 for temp := l.head; temp != nil; temp = temp.next {
  if temp.value == v {
   return temp
  }
 }
```

```go
return nil
}
```

Concatenate — link tail of first list to head of second:

```go
func (l *List) Concatenate(l2 List) {
  temp := l.head
  for temp.next != nil {
   temp = temp.next
  }
  temp.next = l2.head
  l2.head = nil
```

Print:

```go
func (l *List) Print() {
  fmt.Print("[")
  for temp := l.head; temp != nil; temp = temp.next {
   if temp.next != nil {
     fmt.Printf("%v, ", temp.value)
   } else {
     fmt.Print(temp.value)
   }
  }
```

```go
fmt.Println("]")
}
```

Getters:

```go
func (l *List) Len() int {
  return l.len
 }
 func (l *List) Head() *Node {
  return l.head
```

```go
}
```

End-to-end usage:

```go
func main() {
  l1 := linkedlist.New()
  l1.Insert(1)
  l1.Insert(18)
  l1.Insert(9)
  l1.Insert(21)
  l1.Print()
  l1.Remove(9)
  l1.Print()
```

```go
l2 := linkedlist.New()
  l2.InsertOrdered(5)
  l2.InsertOrdered(27)
  l2.InsertOrdered(25)
  l2.InsertOrdered(8)
  l2.Print()
  n1 := l1.Find(18)
  fmt.Println(n1)
  n2 := l1.Find(27)
fmt.Println(n2)
  l1.Concatenate(l2)
l1.Print()
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Implementation of single-linked list"*

---

### Lists vs Arrays — Choosing the Right Linear Structure

**Principle:** Use arrays/slices when capacity is known in advance and indexed access dominates. Use lists when insertions and removals at arbitrary positions dominate.

**Do:**
- Pick slices for cache-friendly, index-based access (`a[i]` is O(1)).
- Pick lists when middle-of-collection insert/remove is the hot path.

**Don't:**
- Don't insert into the middle of a large slice — every insert shifts O(n) elements.
- Don't index-walk a linked list — there is no O(1) random access.

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Lists versus arrays"*

---

### Double-Linked List via `container/list`

**Principle:** The standard library's `container/list` provides a ready-made doubly-linked list. Each node has `next`, `prev`, `Value`, and a back-pointer to its `*List`.

**Do:**
- Use `PushFront`, `PushBack`, `InsertBefore`, `InsertAfter`, `Remove`.
- Iterate with `Front()/Next()` or `Back()/Prev()`.

**Code:**
```go
type List struct {
 root Element
 len int
}
```

```go
type Element struct {
 next, prev *Element
```

```go
list *List
  Value any
 }
```

Usage:

```go
l := list.New()
head := l.PushFront(5)
tail := l.PushBack(27)
```

```go
l.InsertBefore(1, tail)
```

```go
l.InsertAfter(18, head)
```

```go
l.Remove(tail)
```

```go
l.Len()
```

Iterate forward:

```go
for node := l.Front(); node != nil; node = node.Next() {
```

```go
fmt.Print(node.Value)
 }
```

Iterate backward:

```go
for node := l.Back(); node != nil; node = node.Prev() {
  fmt.Print(node.Value)
 }
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Double-linked list"*

---

### Circular List via `container/ring`

**Principle:** The `container/ring` package implements a circular (ring) list. A ring has no start or end; any node references the whole.

**Code:**
```go
type Ring struct {
 next, prev *Ring
 Value any
}
```

```go
r := ring.New(4)
```

```go
r.Len()
```

Initialize node values:

```go
for i := 0; i < r.Len(); i++ {
 r.Value = i
 r = r.Next()
}
```

Concatenate two rings:

```go
r3 := r1.Link(r2)
```

Apply a function to every node:

```go
r.Do(func(p any) {
 fmt.Println(p.(int))
})
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Circular list"*

---

### Stack — LIFO Using a Slice

**Principle:** A stack is a LIFO structure. In Go, model the top of the stack as the end of a slice; `append` is push, slice-off-the-end is pop.

**Code (conceptual):**
```go
func Push(v int) {
 sp = sp + 1
 stack[sp] = v
}
```

```go
func Pop() int {
 if sp == 1 {
  return -1
 }
 v := stack[sp]
 sp = sp - 1
 return v
}
```

Go struct implementation:

```go
type Stack struct {
 stack []int
 stackPointer int
}
```

```go
func (s *Stack) Push(v int) {
 s.stack = append(s.stack, v)
 s.stackPointer = len(s.stack) - 1
}
```

```go
func (s *Stack) Pop() int {
 if s.stackPointer == -1 {
  return -1
 }
 element := s.stack[s.stackPointer]
```

```go
s.stack = s.stack[:s.stackPointer]
 s.stackPointer--
 return element
}
```

```go
func main() {
 var s stack.Stack
 s.Push(27)
 s.Push(5)
 s.Push(1)
```

```go
s.Push(18)
 fmt.Println(s)
 fmt.Println(s.Pop())
 fmt.Println(s.Pop())
 fmt.Println(s.Pop())
 fmt.Println(s.Pop())
 fmt.Println(s.Pop())
 fmt.Println(s)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Stack implementation"*

---

### Stack Discipline in Go — `defer` Uses LIFO

**Principle:** Go has no exposed stack type, but it uses an internal stack for `defer` statements. Deferred calls are popped and executed in LIFO order when the surrounding function returns.

**Code:**
```go
func main() {
 defer fmt.Print("a")
 fmt.Print("b")
}
```

Multiple defers print `1234`:

```go
func main() {
 defer fmt.Print(4)
 defer fmt.Print(3)
 defer fmt.Print(2)
 defer fmt.Print(1)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Stack in Go"*

---

### Queue — FIFO Using `container/list`

**Principle:** A queue is a FIFO structure. Use `container/list` so the head/tail pointers come for free. `PushFront` enqueues; `Back()+Remove()` dequeues.

**Code (conceptual):**
```go
func Enqueue(v int) {
 front = front – 1
 queue[front] = v
}
```

```go
func Dequeue() int {
 if front == rear {
  return -1
 }
 v := queue[rear]
 rear = rear – 1
 return v
}
```

Go implementation:

```go
type Queue struct {
 queue *list.List
}
```

```go
func New() *Queue {
```

```go
return &Queue{queue: list.New()}
}
```

```go
func (q *Queue) Enqueue(v int) {
q.queue.PushFront(v)
 }
```

```go
func (q *Queue) Dequeue() int {
 if q.queue.Len() == 0 {
  return -1
```

```go
}
  element := q.queue.Back()
  q.queue.Remove(element)
  return element.Value.(int)
 }
```

```go
func (q *Queue) Print() {
  fmt.Print("[")
  for e := q.queue.Front(); e != nil; e = e.Next() {
   if e.Next() != nil {
     fmt.Printf("%v, ", e.Value)
```

```go
} else {
    fmt.Print(e.Value)
  }
 }
 fmt.Println("]")
}
```

```go
func main() {
  q := queue.New()
q.Enqueue(27)
  q.Enqueue(5)
```

```go
q.Enqueue(1)
  q.Enqueue(18)
  q.Print()
  fmt.Println(q.Dequeue())
  fmt.Println(q.Dequeue())
  fmt.Println(q.Dequeue())
  fmt.Println(q.Dequeue())
  fmt.Println(q.Dequeue())
q.Print()
 }
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Queue implementation"*

---

### Priority Queue via `container/heap`

**Principle:** Go has no built-in priority queue but provides `container/heap` for any type that implements `heap.Interface` (`sort.Interface` + `Push`/`Pop`). The `Less` method determines ordering. **You must call `heap.Push`/`heap.Pop`** — direct calls bypass heap maintenance.

**Do:**
- For a min-priority queue use `<` in `Less`; for max use `>`.
- Always use `heap.Push(&pq, x)` and `heap.Pop(&pq)`, not `pq.Push(x)` / `pq.Pop()`.

**Code:**
```go
type Interface interface {

sort.Interface

```
```go
Push(x any)
 Pop() any
}
```

Element & queue types:

```go
type Element struct {
 value int
}
```

```go
type PriorityQueue []Element
```

```go
func (pq PriorityQueue) Len() int {
 return len(pq)
}
```

```go
func (pq PriorityQueue) Less(i, j int) bool {
 return pq[i].value < pq[j].value
}
```

```go
func (pq PriorityQueue) Swap(i, j int) {
 if pq.Len() == 0 {
  return
 }
 pq[i], pq[j] = pq[j], pq[i]
}
```

```go
func (pq *PriorityQueue) Push(v any) {
 element := Element{
```

```go
value: v.(int),
 }
 *pq = append(*pq, element)
}
```

```go
func (pq *PriorityQueue) Pop() any {
  if pq.Len() == 0 {
   return -1
  }
  queue := *pq
n := pq.Len() - 1
```

```go
element := queue[n]
*pq = queue[0:n]
  return element
 }
```

Usage — must go through `heap.Push`/`heap.Pop`:

```go
func main() {
 pq := make(priorityqueue.PriorityQueue, 0)
 heap.Push(&pq, 27)
```

```go
heap.Push(&pq, 5)
 heap.Push(&pq, 1)
 heap.Push(&pq, 18)
 fmt.Println(pq)
 fmt.Println(heap.Pop(&pq))
 fmt.Println(heap.Pop(&pq))
 fmt.Println(heap.Pop(&pq))
 fmt.Println(heap.Pop(&pq))
 fmt.Println(heap.Pop(&pq))
 fmt.Println(pq)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Priority queue in Go"*

---

### Hash Functions — Choosing a Distribution

**Principle:** A hash function `h(k)` maps a key to a table index. It should be *simple* (cheap to compute) and *uniform* (spread keys evenly to minimize collisions).

**Methods covered:**
- **Division:** `h(k) = k mod n` (n = table size; choice of n matters).
- **Multiplication:** `h(k) = floor(n * (c*k mod 1))`, 0<c<1, ideally c ≈ golden ratio ≈ 0.618.
- **Mid-square:** square the key, extract middle digits.
- **Digit folding:** split key into equal parts, sum.
- **Radix conversion:** reinterpret the key in a different base.
- **Perfect hash:** minimal, collision-free; rarely achievable.
- **Digit analysis:** for known key distributions, pick digit positions with least variation.

**Example computations from the book:**

```
h(27) = 27 mod 10 = 7                                  (division)
h(27) = floor(10 * (0.518 * 27 mod 1)) = 9             (multiplication)
1989^2 = 3956121  →  middle digits "561"                (mid-square)
27051989 → 27+05+19+89 = 140 → 140 mod 100 = 40        (digit folding)
k=275 in base 10 treated as base 12: 2*12^2 + 7*12 + 5 = 377 → 77  (radix)
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Hash function"*

---

### Collision Resolution — Open Addressing vs Separate Chaining

**Principle:** When two keys hash to the same slot, you either probe for another slot (open addressing) or chain synonyms in a list (separate chaining).

**Open addressing variants:**

```
Linear probe:    h(k, i) = (h(k) + i) mod n
Quadratic probe: h(k, i) = (h(k) + i^2) mod n
Random probe:    pseudo-random sequence in [0, n-1]
Double hashing:  h(k, i) = (h1(k) + i * h2(k)) mod n
```

**Load factor α** = elements / table_size; keep α bounded to control collision rate.

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Hash collision"*

---

### Maps in Go — Hash Table Primitives

**Principle:** The built-in `map[K]V` is a hash table. Keys must be comparable. A nil map cannot be written to — always initialize with `make` or a struct literal.

**Do:**
- Use the comma-ok idiom to test key presence.
- Use `delete(m, k)` for removal; `for k, v := range m` to iterate.
- Use custom struct types as values (and as keys if comparable).

**Code:**
```go
var m map[string]int
```

```go
m := make(map[string]int)
```

```go
var m = map[string]int{
 "Monday": 1,
 "Tuesday": 2,
 "Wednesday": 3,
 "Thursday": 4,
 "Friday": 5,
 "Saturday": 6,
 "Sunday": 7,
}
```

```go
m["Monday"] = 0
```

```go
day := m["Monday"]
```

```go
delete(m, "Thursday")
```

Comma-ok key presence:

```go
day, ok := m["Monday"]
```

Iteration:

```go
for key, element := range m {
 fmt.Println(key, element)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Maps in Go"*

---

### Binary Tree — Node With Parent, Left, Right

**Principle:** A binary tree node stores a value plus pointers to left child, right child, and (optionally) parent. The parent pointer simplifies deletion.

**Code:**
```go
type Node struct {
 value int
 left *Node
 right *Node
 parent *Node
}
```

```go
type BinaryTree struct {
 root *Node
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Trees in Go"*

---

### Tree Insert — Leaf or Internal

**Principle:** Insertion handles three cases: empty tree (becomes root), leaf insert (parent's left/right pointer is nil), internal insert (new node inherits the parent's existing child).

**Code:**
```go
func (bt *BinaryTree) Insert(node *Node, side string,
 value int) *Node {
```

```go
newNode := &Node{value, nil, nil, nil}
// inserting to empty tree
if bt.root == nil {
 bt.root = newNode
 return bt.root
}
if side == "left" {
 if node.left == nil {
  // inserting a leaf
  node.left = newNode
 } else {
  // inserting internal node
```

```go
newNode.left = node.left
  node.left = newNode
 }
} else {
 if node.right == nil {
  // inserting a leaf
  node.right = newNode
 } else {
  // inserting internal node
  newNode.right = node.right
  node.right = newNode
```

```go
}
 }
 newNode.parent = node
 return newNode
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Insert operation"*

---

### Tree Delete — Reduce Internal Node Deletion to Leaf Deletion

**Principle:** Leaf deletion is trivial; internal-node deletion reduces to leaf deletion by replacing the internal node's value with its leftmost descendant's value and then deleting that leaf.

**Code:**
```go
func (n *Node) DeleteLeaf() {
 if n.parent.left == n {
  n.parent.left = nil
 } else {
  n.parent.right = nil
 }
}
```

```go
func (n *Node) findLeftmost() *Node {
 node := n
 next := n
 for next != nil {
  node = next
  if next.left != nil {
   next = next.left
      } else {
   next = next.right
  }
 }
```

```go
return node
```

```go
}

func (bt *BinaryTree) Delete(node *Node) {
 // delete leaf
 if node.left == nil && node.right == nil {
```

```go
// delete root when the root is the only node

```
```go
if node == bt.root {
   bt.root = nil
  } else {
   node.DeleteLeaf()
  }
 // delete internal node
 } else {
  leftmostNode := node.FindLeftmost()
  node.value = leftmostNode.value
  leftmostNode.DeleteLeaf()
 }
}
```

```go
func (bt *BinaryTree) GetRoot() *Node {
 return bt.root
}
```

```go
func main() {
 var bt binarytree.BinaryTree
 node18 := bt.Insert(nil, "left", 18)
 node8 := bt.Insert(node18, "left", 8)
 node25 := bt.Insert(node18, "rigth", 25)
```

```go
node5 := bt.Insert(node8, "left", 5)
 bt.Insert(node8, "right", 9)
 bt.Insert(node25, "left", 21)
 bt.Insert(node25, "right", 27)
 bt.Delete(node25)
 bt.Delete(node5)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Delete operation"*

---

### Tree Traversal — Preorder, Inorder, Postorder (Recursive)

**Principle:** The three depth-first traversals differ only in *when* the root is visited relative to its subtrees.

| Traversal | Visit order      | Recursive skeleton                         |
|-----------|------------------|--------------------------------------------|
| Preorder  | Root, Left, Right | print → recurse left → recurse right      |
| Inorder   | Left, Root, Right | recurse left → print → recurse right      |
| Postorder | Left, Right, Root | recurse left → recurse right → print      |

Inorder on a BST produces sorted output.

**Code:**
```go
func Preorder(node *Node) {
 if node != nil {
  fmt.Println(node.value)
  Preorder(node.left)
  Preorder(node.right)
 }
}
```

```go
func Inorder(node *Node) {
 if node != nil {
```

```go
Inorder(node.left)
  fmt.Println(node.value)
  Inorder(node.right)
 }
}
```

```go
func Postorder(node *Node) {
 if node != nil {
```

```go
Postorder(node.left)
  Postorder(node.right)
  fmt.Println(node.value)
 }
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Preorder" / "Inorder" / "Postorder"*

---

### Level-Order Traversal — BFS With a Queue

**Principle:** Level-order visits the tree breadth-first: root, then root's children, then grandchildren, etc. Use a queue; dequeue a node, process it, enqueue its children.

**Code:**
```go
func Levelorder(node *Node) {
  next := node
  queue := New()
  queue.Enqueue(node)
  for !queue.IsEmpty() {
```

```go
next = queue.Dequeue()
fmt.Println(next.value)
   if next.left != nil {
     queue.Enqueue(next.left)
   }
   if next.right != nil {
     queue.Enqueue(next.right)
   }
  }
 }
```

Node-storing queue used by level-order:

```go
func New() *Queue {
  return &Queue{queue: list.New()}
 }
 func (q *Queue) Enqueue(node *Node) {
  q.queue.PushFront(node)
 }
 func (q *Queue) Dequeue() *Node {
if q.queue.Len() == 0 {
   return nil
  }
  element := q.queue.Back()
```

```go
q.queue.Remove(element)
  return element.Value.(*Node)
 }
 func (q *Queue) IsEmpty() bool {
  return q.queue.Len() == 0
 }
```

End-to-end traversal demo:

```go
func main() {
  // Create a tree
  var bt binarytree.BinaryTree
  node18 := bt.Insert(nil, "left", 18)
  node8 := bt.Insert(node18, "left", 8)
```

```go
node25 := bt.Insert(node18, "rigth", 25)
bt.Insert(node8, "left", 5)
bt.Insert(node8, "right", 9)
bt.Insert(node25, "left", 21)
bt.Insert(node25, "right", 27)
fmt.Println("Preorder")
binarytree.Preorder(bt.GetRoot())
fmt.Println("Inorder")
binarytree.Inorder(bt.GetRoot())
```

```go
binarytree.Postorder(bt.GetRoot())

```

```go
fmt.Println("Levelorder")
 binarytree.Levelorder(bt.GetRoot())
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Level-order"*

---

### Sorting an Array With a Tree (BST Sort) — O(n log n)

**Principle:** Insert each array element into a BST (smaller → left, larger → right), then inorder-traverse the tree to read values back in sorted order.

**Code:**
```go
func ArrayToTree(array []int) *Node {
```

```go
var bt BinaryTree
root := bt.Insert(nil, "left", array[0])
for i := 1; i < len(array); i++ {
 side, node := find(array[i], root)
 bt.Insert(node, side, array[i])
}
return root
```

```go
}
```

```go
func find(value int, root *Node) (side string, node *Node) {
 next := root
```

```go
for next != nil {
 node = next
 if value <= next.value {
  side = "left"
  next = next.left
 } else {
  side = "right"
  next = next.right
 }
}
return
```

```go
}
```

```go
func main() {
 array := []int{18, 27, 5, 21, 1, 9}
 root := binarytree.ArrayToTree(array)
 binarytree.Inorder(root)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Sorting an array with a tree"*

---

### Heap Sort via `container/heap` — O(n log n)

**Principle:** A max-heap keeps the largest element at the root. Heap sort: heapify, then repeatedly pop the root into the back of an array.

**Code:**
```go
type IntHeap []int
```

```go
func (h IntHeap) Len() int {
  return len(h)
 }
 func (h IntHeap) Less(i, j int) bool {
return h[i] > h[j]
}
 func (h IntHeap) Swap(i, j int) {
h[i], h[j] = h[j], h[i]
 }
```

```go
func (h *IntHeap) Push(v any) {
*h = append(*h, v.(int))
 }
 func (h *IntHeap) Pop() any {
  old := *h
  n := len(old)
  v := old[n-1]
  *h = old[0 : n-1]
  return v
 }
```

```go
func Heapsort(array *IntHeap) []int {
 heap.Init(array)
 n := array.Len()
 sortedArray := make([]int, n)
 for i := n - 1; array.Len() > 0; i-- {
  sortedArray[i] = heap.Pop(array).(int)
 }
 return sortedArray
}
```

```go
func main() {
 array := &binarytree.IntHeap{18, 27, 5, 21, 1, 9}
 fmt.Println(binarytree.Heapsort(array))
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Sorting an array with a tree" (heap sort section)*

---

### Graph — Modeled as Two Sets (Nodes, Edges)

**Principle:** A graph G = (V, E). In Go, simulate sets with `map[T]struct{}` — empty struct consumes zero bytes.

**Code:**
```go
type Node struct {
 value int
}
type Edge struct {
 u, v Node
```

```go
}
func NewNode(value int) Node {
 return Node{value}
}
```

```go
type Graph struct {
 nodes map[Node]struct{}
 edges map[Edge]struct{}
}
func New() *Graph {
```

```go
return &Graph{
  nodes: make(map[Node]struct{}),
  edges: make(map[Edge]struct{}),
 }
}
```

```go
func (g *Graph) AddNode(n Node) {
 g.nodes[n] = struct{}{}
}
func (g *Graph) AddEdge(u, v Node) {
```

```go
e := Edge{u, v}
 g.edges[e] = struct{}{}
}
```

```go
func (g *Graph) RemoveNode(n Node) {
  delete(g.nodes, n)
for e := range g.edges {
if e.u == n || e.v == n {
     delete(g.edges, e)
}
```

```go
} }
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Graphs in Go"*

---

### Breadth-First Search (BFS) — O(n + e) With a Queue

**Principle:** Visit the start node, then all its neighbors, then their unvisited neighbors, level by level. A `visit` map prevents revisiting; a queue drives the order.

**Code:**
```go
func BFS(g *Graph, start *Node) {
  visit := make(map[int]bool)
  for n := range g.nodes {
   visit[n.value] = false
  }
  visit[start.value] = true
  queue := NewQueue()
  queue.Enqueue(start)
for !queue.IsEmpty() {
   u := queue.Dequeue()
```

```go
fmt.Println(u.value)
   for edge := range g.edges {
     if edge.u.value == u.value &&
      !visit[edge.v.value] {
      visit[edge.v.value] = true
n := edge.v
      queue.Enqueue(&n)
}
   }
  }
 }
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Breadth-first search"*

---

### Depth-First Search (DFS) — Recursive, O(n + e)

**Principle:** Follow one path as far as possible, backtrack when stuck. Naturally recursive.

**Code:**
```go
func DFS(g *Graph, start *Node) {
```

```go
visit := make(map[int]bool)
 for n := range g.nodes {
  visit[n.value] = false
 }
 dfsVisit(g, start, visit)
}
```

```go
func dfsVisit(g *Graph, u *Node, visit map[int]bool) {
 visit[u.value] = true
 fmt.Println(u.value)
```

```go
for edge := range g.edges {
  if edge.u.value == u.value &&
   !visit[edge.v.value] {
   dfsVisit(g, &edge.v, visit)
  }
 }
}
```

Driver:

```go
main() {
 node27 := graph.NewNode(27)
 node18 := graph.NewNode(18)
```

```go
node21 := graph.NewNode(21)
  node9 := graph.NewNode(9)
  node5 := graph.NewNode(5)
  node25 := graph.NewNode(25)
  g := graph.New()
g.AddNode(node27)
  g.AddNode(node18)
  g.AddNode(node21)
  g.AddNode(node9)
  g.AddNode(node5)
  g.AddNode(node25)
g.AddEdge(node27, node18)
```

```go
g.AddEdge(node27, node21)
g.AddEdge(node27, node9)
g.AddEdge(node18, node5)
g.AddEdge(node21, node5)
g.AddEdge(node21, node25)
g.AddEdge(node9, node25)
g.AddEdge(node5, node25)
```

```go
fmt.Println("BFS")
graph.BFS(g, &node27)
fmt.Println("DFS")
graph.DFS(g, &node27)
```

```go
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Depth-first search"*

---

### Weighted Graph and MST Type

**Principle:** Add a `weight` field to edges for MST and shortest-path algorithms.

**Code:**
```go
type WeightedEdge struct {
 u, v Node
 weight int
}
type WeightedGraph struct {
 nodes map[Node]struct{}
 edges map[WeightedEdge]struct{}
}
func NewWeightedGraph() *WeightedGraph {
 return &WeightedGraph{
  nodes: make(map[Node]struct{}),
  edges: make(map[WeightedEdge]struct{}),
```

```go
}
}
func (wg *WeightedGraph) AddNode(n Node) {
 wg.nodes[n] = struct{}{}
}
func (wg *WeightedGraph) AddEdgee(u, v Node, w int) {
 e := WeightedEdge{u, v, w}
 wg.edges[e] = struct{}{}
}
func (wg *WeightedGraph) RemoveNode(n Node) {
 delete(wg.nodes, n)
 for e := range wg.edges {
```

```go
if e.u == n || e.v == n {
      delete(wg.edges, e)
}
  }
 }
```

MST container:

```go
type MST struct {
 nodes map[Node]struct{}
 edges map[WeightedEdge]struct{}
}
func (m MST) Print() {
```

```go
fmt.Println("Nodes:")
 for n := range m.nodes {
  fmt.Printf("%v ", n.value)
 }
 fmt.Println()
 fmt.Println("Edges: ")
 for e := range m.edges {
  fmt.Printf("%v ", e)
 }
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Spanning tree"*

---

### Prim's Algorithm — MST, O(n²) Greedy Incremental

**Principle:** Start from any node; repeatedly add the minimum-weight edge that connects a tree node to a non-tree node. Originally Jarnik's algorithm.

**Code:**
```go
func Prim(wg *WeightedGraph, start *Node) *MST {
  treeNodes := make(map[Node]struct{})
  treeEdges := make(map[WeightedEdge]struct{})
  treeNodes[*start] = struct{}{}
  for len(treeNodes) != len(wg.nodes) {
   node, minEdge := minEdge(wg, treeNodes)
   treeNodes[node] = struct{}{}
   treeEdges[minEdge] = struct{}{}
```

```go
}
  return &MST{treeNodes, treeEdges}
 }
```

```go
func minEdge(wg *WeightedGraph,
nodes map[Node]struct{}) (n Node, we WeightedEdge) {
  min := 1000
  for e := range wg.edges {
   _, ok1 := nodes[e.u]
   _, ok2 := nodes[e.v]
   if ok1 && !ok2 && e.v.value < min {
```

```go
n = e.v

we = e
}
return
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Prim's algorithm"*

---

### Kruskal's Algorithm — MST, O(e log n) Forest Merge

**Principle:** Start with a forest of isolated nodes. Repeatedly add the minimum-weight edge connecting two different components, merging them. Uses a priority queue of edges by weight.

**Code (priority queue of weighted edges):**
```go
type Element struct {
 value WeightedEdge
}
type PriorityQueue []Element
func (pq PriorityQueue) Len() int {
 return len(pq)
}
func (pq PriorityQueue) Less(i, j int) bool {
 return pq[i].value.weight < pq[j].value.weight
}
func (pq PriorityQueue) Swap(i, j int) {
```

```go
if pq.Len() == 0 {
  return
 }
 pq[i], pq[j] = pq[j], pq[i]
}
func (pq *PriorityQueue) Push(v any) {
 element := Element{
  value: v.(WeightedEdge),
 }
 *pq = append(*pq, element)
}
```

```go
func (pq *PriorityQueue) Pop() any {
  if pq.Len() == 0 {
       return -1
  }
  queue := *pq
n := pq.Len() - 1
  element := queue[n]
*pq = queue[0:n]
  return element
 }
```

Kruskal proper:

```go
func Kruskal(wg *WeightedGraph) *MST {
 treeEdges := make(map[WeightedEdge]struct{})
 pq := make(PriorityQueue, 0)
 for edge := range wg.edges {
  heap.Push(&pq, edge)
 }
```

```go
// forest
forest := make(map[int][]Node)
i := 0
for node := range wg.nodes {
 forest[i] = append(forest[i], node)
 i++
}
for n := 0; n < len(wg.nodes)-1 || pq.Len() == 0; {
 edge := heap.Pop(&pq).(Element).value
 i := findInForest(forest, edge.u.value)
 j := findInForest(forest, edge.v.value)
```

```go
if i != j {
   treeEdges[edge] = struct{}{}
   forest[i] = append(forest[i],
   forest[j]...)
   delete(forest, j)
   n++
  }
 }
 return &MST{wg.nodes, treeEdges}
}
```

```go
func findInForest(forest map[int][]Node, node int) int {
 for i, v := range forest {
  // Check all nodes in the tree
  for _, n := range v {
   if n.value == node {
     return i
   }
  }
 }
 return -1
}
```

Driver for both MST algorithms:

```go
func main() {
 node27 := graph.NewNode(27)
 node18 := graph.NewNode(18)
 node21 := graph.NewNode(21)
 node9 := graph.NewNode(9)
 node5 := graph.NewNode(5)
 node25 := graph.NewNode(25)
 wg := graph.NewWeightedGraph()
 wg.AddNode(node21)
 wg.AddNode(node27)
```

```go
wg.AddNode(node18)
 wg.AddNode(node5)
 wg.AddNode(node9)
 wg.AddEdgee(node21, node27, 5)
 wg.AddEdgee(node21, node18, 10)
 wg.AddEdgee(node27, node18, 25)
 wg.AddEdgee(node27, node5, 15)
 wg.AddEdgee(node18, node9, 20)
 wg.AddEdgee(node5, node9, 30)
 mstPrim := graph.Prim(wg, &node21)
 mstPrim.Print()
 mstKruskal := graph.Kruskal(wg)
```

```go
mstKruskal.Print()
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Kruskal's algorithm"*

---

### Transitive Closure — Warshall's Algorithm, O(n³)

**Principle:** From an adjacency matrix, compute the reachability matrix. For every intermediate node `k`, check if `i` can reach `j` via `k`.

**Code:**
```go
func Warshall(a [][]bool) (p [][]bool) {
 p = a
 for k := 0; k < len(p); k++ {
```

```go
for i := 0; i < len(p); i++ {
    for j := 0; j < len(p); j++ {
     p[i][j] = p[i][j] ||
       (p[i][k] && p[k][j])
    }
   }
 }
 return
}
```

```go
func main() {
 a := [][]bool{
```

```go
{false, true, false, true, false},
  {false, false, false, false, true},
  {false, false, false, true, true},
  {false, false, false, false, false},
  {false, false, false, true, false},
 }
 p := graph.Warshall(a)
 fmt.Println(p)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Transitive closure"*

---

### All-Pairs Shortest Paths — Floyd's Algorithm, O(n³)

**Principle:** Relaxation: maintain an upper-bound distance matrix; on each iteration try to improve `d[i][j]` by going through intermediate `k`.

**Code:**
```go
func Floyd(w [][]int) (d [][]int) {
 d = w
 for k := 0; k < len(d); k++ {
  for i := 0; i < len(d); i++ {
    for j := 0; j < len(d); j++ {
     if d[i][j] > d[i][k]+d[k][j] {
```

```go
d[i][j] = d[i][k] + d[k][j]
       }
     }
    }
  }
  return
 }
```

```go
func main() {
 const INF = 99999
 w := [][]int{
```

```go
{0, 5, INF, 7, INF},
  {INF, 0, INF, INF, 10},
  {INF, INF, 0, 3, 6},
  {INF, INF, INF, 0, INF},
  {INF, INF, INF, 9, 0},
 }
 d := graph.Floyd(w)
 fmt.Println(d)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Floyd's algorithm"*

---

### Single-Source Shortest Path — Dijkstra's Algorithm, O(n²)

**Principle:** Maintain set `S` (confirmed shortest paths) and set `V` (remaining nodes with estimates). Move the min-estimate node from `V` to `S`, then relax its neighbors. **No negative weights supported.**

**Code:**
```go
func Dijkstra(start int, w [][]int) (d map[int]int) {
 n := len(w)
 s := make(map[int]struct{})
 s[start] = struct{}{}
 v := make(map[int]struct{})
```

```go
d = make(map[int]int)
for i := 0; i < n; i++ {
 if i != start {
  v[i] = struct{}{}
  d[i] = w[start][i]
 }
}
for len(v) != 0 {
 i := findMin(d, v)
 s[i] = struct{}{}
 delete(v, i)
 for j := range v {
```

```go
if d[i]+w[i][j] < d[j] {
     d[j] = d[i] + w[i][j]
    }
  }
 }
 return
}
```

```go
func findMin(d map[int]int, v map[int]struct{}) (node int) {
```

```go
min := INF
for i := range d {
```

```go
_, ok := v[i]
   if d[i] <= min && ok {
node = i
     min = d[i]
}
  }
  return
 }
```

```go
func main() {
  w := [][]int{
```

```go
{0, 5, INF, 7, INF},

```
```go
{INF, 0, INF, INF, 10},
  {INF, INF, 0, INF, INF},
  {INF, INF, 3, 0, INF},
  {INF, INF, 6, 9, 0},
 }
 d := graph.Dijkstra(0, w)
 fmt.Println(d)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Dijkstra's algorithm"*

---

### Flow Network — Edge With Capacity and Flow

**Principle:** A flow network is a directed graph where each edge has non-negative `capacity`. The flow function satisfies capacity, symmetry, and conservation constraints.

**Code:**
```go
type Node struct {
 value int
}
type FlowEdge struct {
 u, v Node
 capacity int
 flow int
}
type FlowGraph struct {
 nodes map[Node]struct{}
 edges map[FlowEdge]struct{}
}
```

```go
func NewFlowGraph() *FlowGraph {
 return &FlowGraph{
  nodes: make(map[Node]struct{}),
  edges: make(map[FlowEdge]struct{}),
 }
}
func (fg *FlowGraph) AddNode(n Node) {
 fg.nodes[n] = struct{}{}
}
func (fg *FlowGraph) AddEdge(u, v Node, c int) {
 e := FlowEdge{u, v, c, 0}
 fg.edges[e] = struct{}{}
```

```go
}
 func (fg *FlowGraph) RemoveNode(n Node) {
  delete(fg.nodes, n)
  for e := range fg.edges {
if e.u == n || e.v == n {
     delete(fg.edges, e)
}
  }
 }
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Ford-Fulkerson algorithm" (graph setup)*

---

### Maximum Flow — Ford-Fulkerson, O(VE²)

**Principle:** Start with zero flow. Repeatedly find an augmenting path (residual capacity > 0 on every edge), push the minimum residual capacity along that path, accumulate into `maxFlow`. Stop when no augmenting path remains.

**Code:**
```go
func FordFulkerson(graph *FlowGraph, source,
target *Node) (maxFLow int) {
```

```go
for e := range graph.edges {
 e.flow = 0
}
ok, path := AugmentingPath(graph, source, target)
for ok {
 cf := pathFLow(path)
 for _, edge := range path {
  delete(graph.edges, edge)
  edge.flow += cf
  graph.edges[edge] = struct{}{}
 }
 maxFLow += cf
```

```go
ok, path = AugmentingPath(graph, source, target)
  }
  return
 }
```

```go
func pathFlow(path []FlowEdge) (flow int) {
  flow = INF
  for _, edge := range path {
   cf := edge.capacity - edge.flow
   if cf < flow {
    flow = cf
```

```go
}
 }
 return
}
```

Augmenting-path search (modified BFS that reconstructs the path):

```go
func AugmentingPath(g *FlowGraph, source *Node,
 target *Node) (ok bool, path []FlowEdge) {
 ok = false
```

```go
visit := make(map[int]bool)
for n := range g.nodes {
   visit[n.value] = false
  }
  visit[source.value] = true
queue := NewQueue()
  queue.Enqueue(source)
  for !queue.IsEmpty() {
   u := queue.Dequeue()
  for edge := range g.edges {
    if edge.u.value == u.value &&
      !visit[edge.v.value] &&
      edge.capacity != edge.flow {
```

```go
if len(path) == 0 ||
      !inPath(edge.u.value, path) &&
      inPathDest(edge.u.value, path) {
      visit[edge.v.value] = true
      path = append(path, edge)
n := edge.v
      queue.Enqueue(&n)
if edge.v.value == target.value {
       ok = true
       return
        }
      }
```

```go
}
   }
  }

```
```go
return
 }
func inPath(node int, path []FlowEdge) bool {
  for _, edge := range path {
   if edge.u.value == node {
     return true
   }
  }
  return false
```

```go
}
 func inPathDest(node int, path []FlowEdge) bool {
  for _, edge := range path {
   if edge.v.value == node {
     return true
   }
  }
  return false
 }
```

Driver:

```go
func main() {
  node0 := graph.NewNode(0)
```

```go
node1 := graph.NewNode(1)
  node2 := graph.NewNode(2)
  node3 := graph.NewNode(3)
  node4 := graph.NewNode(4)
  g := graph.NewFlowGraph()
  g.AddNode(node0)
g.AddNode(node1)
  g.AddNode(node2)
  g.AddNode(node3)
  g.AddNode(node4)
g.AddEdge(node0, node1, 5)
g.AddEdge(node0, node3, 7)
```

```go
g.AddEdge(node1, node4, 10)
 g.AddEdge(node3, node2, 3)
 g.AddEdge(node4, node2, 6)
 g.AddEdge(node4, node3, 9)
 maxFlow := graph.FordFulkerson(g, &node0, &node2)
 fmt.Println(maxFlow)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Ford-Fulkerson algorithm"*

---

### Topological Sort — O(n + e) on DAGs

**Principle:** Repeatedly pick a node with indegree 0, append it to the order, remove it and its outgoing edges. Output is not unique. The DAG property guarantees at least one zero-indegree node exists.

**Code:**
```go
func TopSort(graph *Graph) []Node {
```

```go
nodes := graph.nodes

```
```go
edges := graph.edges
  n := len(nodes)
  t := make([]Node, n)
for i := 0; i < n; i++ {
   zeroIndegreeNode :=
   findZeroIndegreeNode(nodes, edges)
   t[i] = zeroIndegreeNode
   delete(nodes, zeroIndegreeNode)
for edge := range edges {
     edge.u.value == zeroIndegreeNode.value {
      delete(edges, edge)
    }
```

```go
}
 }
 return t
}
```

```go
func findZeroIndegreeNode(nodes map[Node]struct{},
 edges map[Edge]struct{}) Node {
 for node := range nodes {
  isZeroDegree := true
  for edge := range edges {
   if edge.v.value == node.value {
    isZeroDegree = false
```

```go
}
   }
   if isZeroDegree {
    return node
   }
  }
  return Node{}
 }
```

```go
func main() {
  node0 := graph.NewNode(0)
  node1 := graph.NewNode(1)
```

```go
node2 := graph.NewNode(2)
  node3 := graph.NewNode(3)
  node4 := graph.NewNode(4)
  tsGraph := graph.New()
  tsGraph.AddNode(node0)
  tsGraph.AddNode(node1)
  tsGraph.AddNode(node2)
  tsGraph.AddNode(node3)
tsGraph.AddNode(node4)
  tsGraph.AddEdge(node0, node1)
  tsGraph.AddEdge(node0, node3)
  tsGraph.AddEdge(node1, node4)
```

```go
tsGraph.AddEdge(node3, node2)
 tsGraph.AddEdge(node4, node2)
 tsGraph.AddEdge(node4, node3)
 t := graph.TopSort(tsGraph)
 fmt.Println(t)
}
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Topological sorting"*

---

### Critical Path — EST, LST, Latency on a DAG

**Principle:** In a DAG modeling a project (edge weights = activity durations), the **critical path** is the longest source-to-target path. Activities on it cannot be delayed. Compute Earliest Start Time (EST) forward through topological order, Latest Start Time (LST) backward; latency `L[i] = LST[i] - EST[i]`. Nodes with `L[i] == 0` are critical.

**Code (weighted-graph topological sort — copies the maps to avoid mutating caller state):**
```go
func TopSortWG(graph WeightedGraph) []Node {

nodes := make(map[Node]struct{})

```
```go
edges := make(map[WeightedEdge]struct{})
  for k, v := range graph.nodes {
   nodes[k] = v
  }
  for k, v := range graph.edges {
edges[k] = v
  }
  n := len(nodes)
t := make([]Node, n)
  for i := 0; i < n; i++ {
   zeroIndegreeNode :=
     findZeroIndegreeNodeWG(nodes, edges)
```

```go
t[i] = zeroIndegreeNode
delete(nodes, zeroIndegreeNode)
for edge := range edges {
    if edge.u.value == zeroIndegreeNode. value {
      delete(edges, edge)
    }
   }
  }
  return t
 }
```

```go
func CriticalPath(graph WeightedGraph) ([]int, []int, []int) {
  t := TopSortWG(graph)
  n := len(t)
  est := make([]int, n)
  est[0] = 0
  for i := 1; i < n; i++ {
   k := t[i].value
   est[k] = findMax(k, est, graph.edges)
  }
  lst := make([]int, n)
  lst[n-1] = est[n-1]
```

```go
for i := n - 2; i >= 0; i-- {
   k := t[i].value
   lst[k] = findMinLST(k, lst, graph.edges)
  }
  l := make([]int, n)
  for i := 0; i < n; i++ {
   l[i] = lst[i] - est[i]
  }
  return est, lst, l
}
```

```go
func findMax(nodeValue int, est []int,
  edges map[WeightedEdge]struct{}) int {
  max := -1
  // find predecessors
  predecessors := make(map[int]int)
  for edge := range edges {
   if edge.v.value == nodeValue {
predecessors[edge.u.value] = edge.weight
   }
  }
  // find maximum
```

```go
for p, v := range predecessors {
   if est[p]+v > max {
    max = est[p] + v
   }
 }
 return max
}
```

```go
func findMinLST(nodeValue int, lst []int,
 edges map[WeightedEdge]struct{}) int {
 min := INF
```

```go
// Find successors
successors := make(map[int]int)
for edge := range edges {
 if edge.u.value == nodeValue {
  successors[edge.v.value] = edge.weight
 }
}
// Find minimum
for p, v := range successors {
 if lst[p]-v < min {
  min = lst[p] - v
 }
```

```go
}
  return min
 }
```

```go
func main() {
  node0 := graph.NewNode(0)
  node1 := graph.NewNode(1)
  node2 := graph.NewNode(2)
  node3 := graph.NewNode(3)
  node4 := graph.NewNode(4)
  node5 := graph.NewNode(5)
```

```go
wg := graph.NewWeightedGraph()
wg.AddNode(node0)
  wg.AddNode(node1)
  wg.AddNode(node2)
  wg.AddNode(node3)
  wg.AddNode(node4)
  wg.AddNode(node5)
  wg.AddEdgee(node0, node1, 5)
  wg.AddEdgee(node0, node2, 7)
  wg.AddEdgee(node1, node3, 2)
  wg.AddEdgee(node1, node4, 6)
  wg.AddEdgee(node2, node3, 4)
```

```go
wg.AddEdgee(node2, node4, 9)
 wg.AddEdgee(node3, node4, 3)
 wg.AddEdgee(node3, node5, 8)
 wg.AddEdgee(node4, node5, 6)
 est, lst, l := graph.CriticalPath(wg)
 fmt.Println(est, lst, l)
}
```

Allowed per-edge latency, derived from EST/LST:

```
l(i, j) = LST[j] - EST[i] - w(i, j)
```

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Critical path"*

---

## Complexity Reference Table (All Algorithms in the Book)

| Algorithm          | Category                | Complexity   | Key idea                                  |
|--------------------|-------------------------|--------------|-------------------------------------------|
| Sequential search  | Search                  | O(n)         | Linear scan                              |
| Binary search      | Search                  | O(log n)     | Divide-and-conquer on sorted data        |
| Insertion sort     | Sorting                 | O(n²)        | Sorted/unsorted partitioning             |
| Selection sort     | Sorting                 | O(n²)        | Find min of unsorted suffix              |
| Bubble sort        | Sorting                 | O(n²)        | Compare and swap adjacent                |
| Quick sort         | Sorting                 | O(n log n) avg | Divide-and-conquer with pivot          |
| Heap sort          | Sorting                 | O(n log n)   | Max-heap + extract root                  |
| Preorder/Inorder/Postorder | Tree traversal | O(n)         | Recursive DFS                            |
| Level-order        | Tree traversal          | O(n)         | Queue-based BFS                          |
| BFS                | Graph traversal         | O(n + e)     | Queue, level-by-level                    |
| DFS                | Graph traversal         | O(n + e)     | Stack/recursive, depth-first             |
| Prim's             | MST                     | O(n²)        | Greedy incremental connected component   |
| Kruskal's          | MST                     | O(e log n)   | Forest merge with priority queue         |
| Warshall           | Transitive closure      | O(n³)        | Reachability matrix from adjacency       |
| Floyd              | All-pairs shortest path | O(n³)        | Distance matrix from cost matrix         |
| Dijkstra           | Single-source shortest  | O(n²)        | Distance vector from cost matrix         |
| Ford-Fulkerson     | Max flow                | O(VE²)       | Residual network with augmenting paths   |
| Topological sort   | Dependency ordering     | O(n + e)     | Repeatedly pick zero-indegree node       |
| Critical path      | Project scheduling      | O(n + e)     | EST/LST vectors from topological order   |

*Ref: Data_Structures_and_Algorithms_with_Go.md — "Table 7.3: Graph algorithms" (and per-section complexity notes)*

---

## Anti-Patterns & Common Mistakes

- **Calling `pq.Push` / `pq.Pop` directly on a `heap.Interface` type:** Bypasses heap invariants; you get a regular queue, not a priority queue. → *fix:* Always call `heap.Push(&pq, x)` and `heap.Pop(&pq)`.
- **Returning a nil slice from a "not found" search:** Conflates "not found" with "found zero". → *fix:* Return a sentinel index (`-1`) or `(value, bool)` like the comma-ok idiom.
- **Mutating a slice that aliases an underlying array:** A sub-slice `s[1:4]` *shares* storage; writes leak. → *fix:* Copy with `copy()` when independence is required.
- **Writing to a nil map:** `var m map[string]int; m["x"] = 1` panics. → *fix:* Initialize with `make(map[string]int)` or a literal.
- **Inserting into the middle of a slice:** Shifts O(n) elements. → *fix:* Use a linked list if middle-insert is hot.
- **Walking a tree with iteration instead of recursion:** Three DFS traversals are 4 lines each recursively; iterative variants are far longer. → *fix:* Use recursion unless tree depth is unbounded.
- **Forgetting to set parent pointers in tree insert:** Simplifies delete later; missing it forces costly re-traversal. → *fix:* Always set `newNode.parent = node`.
- **Modifying the caller's graph maps inside `TopSort`:** Side-effects corrupt the graph for subsequent calls. → *fix:* Copy the maps first (the book's `TopSortWG` shows the pattern).
- **Assuming Dijkstra handles negative weights:** It does not. → *fix:* Use Bellman-Ford (not covered in this book) for graphs with negative edges.
- **Indexing past slice length:** `s[len(s)]` panics. Use `s[len(s)-1]` for the last element (book uses this pattern).
- **Using an even `n` for division hash:** Even keys collide into even slots. → *fix:* Pick `n` prime, or use multiplication/mid-square methods.

*Ref: Data_Structures_and_Algorithms_with_Go.md — multiple sections (Priority queue, Slices, Maps, Tree delete, Topological sort)*

---

## Decision Heuristics / Checklists

### When to use array vs slice vs list vs map

| Need                                | Pick            |
|-------------------------------------|-----------------|
| Fixed size, indexed access          | Array `[n]T`    |
| Dynamic size, indexed access        | Slice `[]T`     |
| Many middle inserts/removes         | Linked list     |
| Bidirectional traversal             | `container/list` |
| Circular iteration                  | `container/ring` |
| Key → value lookup                  | `map[K]V`       |

### When to use which traversal

| Goal                                | Traversal              |
|-------------------------------------|------------------------|
| Sorted output from BST              | Inorder                |
| Expression-tree prefix expression   | Preorder               |
| Expression-tree postfix expression  | Postorder              |
| Level-by-level processing           | Level-order (BFS)      |
| Shortest path in unweighted graph   | BFS                    |
| Cycle detection / topological order | DFS                    |

### When to use which MST algorithm

| Condition                          | Algorithm  |
|------------------------------------|------------|
| Dense graph                        | Prim's     |
| Sparse graph                       | Kruskal's  |
| Need forest-style union-find       | Kruskal's  |

### When to use which shortest-path algorithm

| Need                              | Algorithm        |
|-----------------------------------|------------------|
| Single source, non-negative       | Dijkstra         |
| All pairs                         | Floyd            |
| Reachability only (no weight)     | Warshall         |
| Single source, negative weights   | Bellman-Ford (not in book) |

### When to use which sort algorithm

| Condition                         | Sort           |
|-----------------------------------|----------------|
| Small or nearly sorted            | Insertion sort |
| Small, simplicity matters         | Selection sort |
| Teaching / never in production    | Bubble sort    |
| General-purpose, average fast     | Quick sort     |
| Production Go code                | `sort.Ints` / `sort.Sort` / `sort.Stable` |
| Priority-queue-driven             | Heap sort      |

### Hashing checklist

- [ ] Hash function simple and uniform?
- [ ] Table size chosen to minimize collisions (prime for division method)?
- [ ] Load factor α bounded (typically < 0.75)?
- [ ] Collision strategy chosen (linear/quadratic/double probing or chaining)?
- [ ] For Go maps, initialized with `make` (not nil)?

*Ref: Data_Structures_and_Algorithms_with_Go.md — synthesis of all chapters*

---

## Key Takeaways

1. **Use the standard library first.** Go ships `container/list`, `container/ring`, `container/heap`, `sort`, and `map` — reach for these before hand-rolling.
2. **`heap.Push` / `heap.Pop` are the only way to use `container/heap`.** Direct method calls bypass heap invariants.
3. **Slices alias underlying arrays.** Treat them as views; use `copy()` for independence, `make([]T, 0, n)` to preallocate.
4. **Map zero-value is nil and unwritable.** Always `make` it.
5. **Prefer recursion for the three DFS tree traversals** (4 lines each); prefer a queue for level-order.
6. **Inorder traversal of a BST produces sorted output** — that's the basis of tree sort.
7. **`map[T]struct{}` simulates a set with zero-byte values** — the Go idiom for graph node/edge sets.
8. **Pointer receivers mutate the caller; value receivers don't.** Choose deliberately.
9. **Always handle the empty-collection edge case first** in every list/stack/queue/tree operation.
10. **Garbage collection reclaims unlinked nodes**, but explicitly setting removed pointers to `nil` makes intent clear and avoids lingering references.
11. **Dijkstra does not support negative weights** — choose your algorithm based on graph properties.
12. **Critical path = longest source-to-target path** in a weighted DAG; activities with `LST - EST == 0` are critical.
13. **Big-O ordering is invariant:** `O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n^k) < O(k^n)`.
14. **Data structure precedes algorithm** — data must exist before it can be manipulated. Pick the structure based on the operations you'll perform most.

---

## Cross-References

- Related: [[../Efficient_Go.md]] — pre-allocation, allocation profiling, slice/list performance.
- Related: [[../Concurrency_in_Go.md]] — channels, goroutines, sync primitives.
- Related: [[../100_Go_Mistakes.md]] — map nil-write panic, slice-sharing traps, pointer-receiver pitfalls.
- Related: [[../Domain_Driven_Design_with_Golang.md]] — struct design, value objects.
- Topic index: [[../INDEX.md]]
