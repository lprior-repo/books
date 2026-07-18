# Grokking Functional Programming -- Summary

**Author:** Michal Plachta
**Published:** 2022, Manning Publications
**Language used:** Scala (with Java comparisons throughout)

---

## Overview

*Grokking Functional Programming* is a practical, step-by-step introduction to functional programming for programmers with experience in imperative object-oriented languages like Java. The book teaches FP concepts through concrete examples and exercises, using Scala as its teaching language. It is organized into three parts: (1) the functional toolkit (pure functions, immutable values, functions as values), (2) functional programs (sequential programs, error handling, type-driven design, IO, streams, concurrency), and (3) applied functional programming (designing and testing a real-world application using Wikidata).

The central thesis is that functional programming is programming using **pure functions** that manipulate **immutable values**, and that this approach leads to code that is more readable, testable, and maintainable. The book repeatedly demonstrates that treating everything -- including errors, side effects, streams, and concurrent state -- as immutable values yields programs that are easier to reason about and compose.

---

## Part 1: The Functional Toolkit

### Chapter 1: Learning Functional Programming

This introductory chapter sets the stage. It addresses three potential reader profiles: the curious, the previously frustrated learner, and the skeptic on the fence. The book promises a practical, example-driven approach with minimal mathematical jargon.

**Key concepts introduced:**

- **Functions as boxes**: A function takes inputs, does something in its body, and returns outputs. The signature is what other programmers see; the body is hidden inside.
- **Signatures vs. bodies**: In FP, programmers focus more on signatures than bodies. A good signature tells the whole story without needing to read the implementation.
- **Functions that lie**: Several common functions have signatures that do not tell the full truth. For example, `getFirstCharacter` promises to return a `char` for any `String`, but throws an exception on an empty string. `divide` promises an `int` but crashes when dividing by zero. These are "lying" functions, and FP aims to write functions that do not lie.
- **Imperative vs. declarative programming**: Imperative code focuses on *how* to compute a result (step-by-step instructions). Declarative code focuses on *what* needs to be done. The declarative version of calculating a word score is `word.length()` instead of a for-loop that manually counts characters.
- **Scala as the teaching language**: The book uses Scala but is not a Scala book. Readers need no prior Scala or FP knowledge. The book guides readers through installing Scala and using the REPL (Read-Eval-Print Loop) to experiment with code.

The chapter establishes the book's pedagogical approach: learn through experimentation, practice with exercises ("coffee breaks"), and always start from the function signature.

### Chapter 2: Pure Functions

This chapter introduces the foundational concept of the entire book: pure functions. It uses a shopping cart discount calculation example to demonstrate the problems with imperative code and how pure functions solve them.

**The shopping cart evolution:**

The chapter starts with an imperative `ShoppingCart` class that stores items in a mutable `ArrayList` and tracks whether a book was added via a `bookAdded` boolean. Bugs emerge because external callers can modify the internal list, and the stored boolean can become stale.

Three refactoring techniques are introduced to transform imperative code into pure functions:

1. **Recalculating instead of storing**: Rather than caching `bookAdded` as a field, recalculate whether the list contains a book each time the discount is needed.
2. **Passing the state as an argument**: Instead of using instance fields, pass the list of items as a function parameter.
3. **Passing copies of data**: When mutable data is shared, create defensive copies to prevent external modification.

**Three rules of pure functions:**

1. The function always returns a single value.
2. The function calculates the return value based only on its arguments.
3. The function does not mutate any existing values.

**Pure functions and mathematical functions:**

Pure functions in programming are inspired by mathematical functions, which are always pure. In mathematics, `f(x) = x * 95 / 100` will always return the same result for the same input. Most programming languages allow impure implementations (e.g., adding a side effect inside the function body), which is why discipline is required.

**Additional properties of pure functions:**

- **Single responsibility**: When a function returns only one value and cannot mutate, it can only do one thing.
- **No side effects**: The function's only observable result is its return value. Side effects include HTTP calls, database writes, logging, throwing exceptions, and modifying global state.
- **Referential transparency**: Calling the function multiple times with the same arguments always returns the same result. You could substitute a call like `f(20)` with its result `19` without changing program behavior.

**Testing pure functions:**

Pure functions are straightforward to test because they depend only on their inputs. You call them with specific arguments and assert on the return value. No setup or teardown of external state is needed.

### Chapter 3: Immutable Values

This chapter introduces the second pillar of FP: immutable values. It uses a travel planner example to demonstrate the dangers of mutable data.

**The replan problem:**

The chapter starts with a `replan` function that inserts a new city into a travel itinerary. The initial Java implementation mutates the input list by calling `add(index, element)`, which causes problems when the caller's original list is unexpectedly modified.

**Shared mutable state:**

The core problem is **shared mutable state** -- a variable shared between different parts of the codebase that can be mutated by any of them. This makes it impossible to reason about a function in isolation because its behavior depends on the current state of shared data.

**Fighting mutability:**

- **Working with copies**: The first defense is to create a copy of incoming mutable data and work only on the copy. This protects callers from unexpected mutations.
- **Immutable values**: A more powerful approach is to use data structures that cannot be mutated at all. Java's `String` is already immutable (methods like `substring` return new Strings rather than modifying the original). Scala provides immutable collections as part of its standard library.

**Immutable Scala List:**

Scala's `List` is immutable. Operations like `slice`, `appended`, and `appendedAll` return new lists rather than modifying the original:

```scala
def replan(plan: List[String], newCity: String, beforeCity: String): List[String] = {
  val beforeCityIndex = plan.indexOf(beforeCity)
  val citiesBefore = plan.slice(0, beforeCityIndex)
  val citiesAfter = plan.slice(beforeCityIndex, plan.size)
  citiesBefore.appended(newCity).appendedAll(citiesAfter)
}
```

**Performance considerations:**

The book addresses the common concern that copying is slow. While it is slower than in-place mutation, it is usually not a bottleneck in most applications. When it does become a problem, techniques like using `prepended` (constant-time prepend instead of copy-heavy append) can help. The key insight is that readability and maintainability should take priority, and performance optimization should be done only after profiling.

**The functional approach to relations between values:**

Immutability forces programmers to think in terms of *relations between values* rather than sequences of mutations. You define what the result *is* in terms of the inputs, not how to construct it step by step. This naturally leads to more declarative code.

**Core definition:**

> Functional programming is programming using *pure functions* that manipulate *immutable values*.

### Chapter 4: Functions as Values

This is the longest and most important chapter in Part 1. It demonstrates that functions themselves can be treated as immutable values -- stored, passed around, and returned from other functions.

**The word ranking example:**

The chapter uses a word-scoring game to build up the concept of functions as values. The `score` function calculates points for a word:

```java
static int score(String word) {
    return word.replaceAll("a", "").length();
}
```

**Evolution of the `rankedWords` function:**

1. **Version 1 -- Imperative with mutation**: Uses `Comparator` and `List.sort()`, which mutates the input list.
2. **Version 2 -- Java Streams**: Uses `words.stream().sorted(comparator).collect(Collectors.toList())`, which does not mutate the input.
3. **Version 3 -- Passing algorithms as arguments**: The comparator is passed as a parameter to make the function pure. The signature now tells the whole story.
4. **Version 4 -- Changing requirements**: When the scoring algorithm changes (adding a bonus for words containing 'c'), the `rankedWords` function does not need to change at all -- only the comparator passed to it changes.

**Java's `Function` type:**

Java provides `Function<String, Integer>` to represent a function from String to Integer. Functions can be stored as values and passed around:

```java
Function<String, Integer> scoreFunction = w -> w.replaceAll("a", "").length();
```

**Scala's function syntax:**

Scala provides much more concise syntax. The key higher-order functions introduced:

- **`sortBy`**: Takes a function that extracts a sorting key from each element.
  ```scala
  def rankedWords(wordScore: String => Int, words: List[String]): List[String] = {
    words.sortBy(wordScore).reverse
  }
  ```

- **`map`**: Applies a function to every element of a list, returning a new list.
  ```scala
  def wordScores(wordScore: String => Int, words: List[String]): List[Int] = {
    words.map(wordScore)
  }
  ```

- **`filter`**: Returns only elements satisfying a boolean condition.
  ```scala
  def highScoringWords(wordScore: String => Int, words: List[String]): List[String] = {
    words.filter(word => wordScore(word) > 1)
  }
  ```

**Functions returning functions:**

When the high-score threshold needs to vary, instead of creating separate functions for each threshold, the function returns another function:

```scala
def highScoringWords(wordScore: String => Int, words: List[String]): Int => List[String] = {
  higherThan => words.filter(word => wordScore(word) > higherThan)
}
```

This allows partial application: the scoring function and word list are provided once, and the threshold is supplied later.

**Currying:**

Using multiple parameter lists in Scala is called currying. A curried function takes its arguments one at a time, each in its own parameter list:

```scala
def highScoringWords(wordScore: String => Int, words: List[String])(higherThan: Int): List[String]
```

**`foldLeft`:**

The chapter introduces `foldLeft`, which reduces a list to a single value by applying a function cumulatively:

```scala
List[A].foldLeft(z: B)(f: (B, A) => B): B
```

Examples include summing a list, finding the longest word, or counting elements satisfying a condition.

**Product types (`case class`):**

Scala's `case class` is used to couple several pieces of data into an immutable bundle:

```scala
case class TravelGuide(attraction: Attraction, subjects: List[PopCultureSubject])
```

---

## Part 2: Functional Programs

### Chapter 5: Sequential Programs

This chapter introduces `flatMap` and for comprehensions, the primary tools for building sequential programs in FP.

**flatten and flatMap:**

When `map` produces a list of lists (e.g., mapping each book to its list of authors), `flatten` joins them into a single list. `flatMap` combines `map` and `flatten` in one step:

```scala
books.flatMap(_.authors).flatMap(bookAdaptations)
```

**Key insight about flatMap**: Unlike `map`, `flatMap` can change the *size* of the resulting list because the mapping function returns a list that gets flattened.

**Nested flatMaps:**

When values depend on other values, flatMaps are nested:

```scala
books.flatMap(book =>
  book.authors.flatMap(author =>
    bookAdaptations(author).map(movie =>
      s"You may like ${movie.title}, because you liked ${author}'s ${book.title}"
    )
  )
)
```

**For comprehensions:**

Nested flatMaps become hard to read. Scala's for comprehensions provide syntactic sugar:

```scala
for {
  book <- books
  author <- book.authors
  movie <- bookAdaptations(author)
} yield s"You may like ${movie.title}, because you liked ${author}'s ${book.title}"
```

**How for comprehensions work:**

- Every line with `<-` (except the last) is translated into a `flatMap` call.
- The last `<-` line is translated into a `map` call.
- Guard expressions (`if`) are translated into `filter` calls.
- The `yield` expression defines the result.

**Option type and flatMap:**

`Option` (Some/None) also has `flatMap`. When parsing data with validation:

```scala
def parse(name: String, start: Int, end: Int): Option[Event] =
  for {
    validName <- validateName(name)
    validEnd <- validateEnd(end)
    validStart <- validateStart(start, end)
  } yield Event(validName, validStart, validEnd)
```

If any validation returns `None`, the entire for comprehension short-circuits to `None`. This is the same mechanism as with lists, where returning an empty list from flatMap filters out that element.

### Chapter 6: Error Handling

This chapter teaches how to handle errors functionally using `Option` and `Either`, without exceptions or nulls.

**The TV show parsing example:**

The chapter builds a TV show parsing engine that must handle many potential errors (missing names, invalid years, various formats).

**From exceptions to Option:**

Instead of throwing exceptions or returning null, functions return `Option`:

```scala
def parseShow(rawShow: String): Option[TvShow]
```

**Small functions that compose:**

The parsing is broken into small, independently testable functions:

```scala
def extractName(rawShow: String): Option[String]
def extractYearStart(rawShow: String): Option[Int]
def extractYearEnd(rawShow: String): Option[Int]
def extractSingleYear(rawShow: String): Option[Int]
```

**Error recovery with `orElse`:**

`orElse` provides fallback behavior: if the first Option is None, try the second:

```scala
extractYearStart(rawShow).orElse(extractSingleYear(rawShow))
```

**Error propagation with for comprehensions:**

When parsing multiple fields, if any fails, the whole thing fails:

```scala
def parseShow(rawShow: String): Option[TvShow] = for {
  name <- extractName(rawShow)
  yearStart <- extractYearStart(rawShow).orElse(extractSingleYear(rawShow))
  yearEnd <- extractYearEnd(rawShow).orElse(extractSingleYear(rawShow))
} yield TvShow(name, yearStart, yearEnd)
```

**Two error-handling strategies for lists:**

1. **Best-effort**: Parse as many items as possible, ignoring failures. Uses `map`, `toList`, `flatten`:
   ```scala
   def parseShows(rawShows: List[String]): List[TvShow] =
     rawShows.map(parseShow).flatMap(_.toList)
   ```

2. **All-or-nothing**: Fail the entire operation if any item fails. Uses `foldLeft`:
   ```scala
   def parseShows(rawShows: List[String]): Option[List[TvShow]] =
     rawShows.map(parseShow).foldLeft(Some(List.empty): Option[List[TvShow]]) {
       (acc, show) => for {
         shows <- acc
         s <- show
       } yield shows.appended(s)
     }
   ```

**Either for descriptive errors:**

`Option` tells you *that* something failed but not *why*. `Either` carries error information:

```scala
def extractName(rawShow: String): Either[String, String]
def extractYearStart(rawShow: String): Either[String, Int]
```

`Left` holds the error description; `Right` holds the successful value. `Either` supports the same combinators (`map`, `flatMap`, `orElse`) as `Option`, so for comprehensions work identically.

**Key principle**: In FP, handling errors means taking an error value and returning a different value. Errors are values, not control flow disruptions.

### Chapter 7: Requirements as Types

This chapter focuses on functional data design -- using types to make invalid states unrepresentable.

**The music artists search example:**

The chapter redesigns an Artist data model and search function, showing five problems with primitive-type-based modeling and solving each one.

**Problem 1 -- Misplaced parameters (solved by newtypes):**

When multiple parameters share the same type (e.g., `String` for both genre and origin), they can be swapped accidentally. **Newtypes** wrap a primitive in a distinct type:

```scala
opaque type Location = String
object Location {
  def apply(name: String): Location = name
  extension (l: Location) def name: String = l
}
```

This is a zero-cost wrapper -- at runtime it is still a String, but the compiler enforces type safety.

**Problem 2 -- Interconnected parameters (solved by Option):**

Instead of `isActive: Boolean` plus `yearsActiveEnd: Int` (where the end year is meaningless when active), use a single `Option[Int]`:

```scala
case class Artist(name: String, genre: String, origin: Location,
  yearsActiveStart: Int, yearsActiveEnd: Option[Int])
```

`None` means still active; `Some(year)` means inactive since that year.

**Higher-order functions on Option:**

- `forall`: Returns true if the condition holds for the contained value, or if the Option is None.
- `exists`: Returns true if the condition holds for the contained value (None returns false).
- `contains`: Checks if the Option contains a specific value.

**Problem 3 -- Finite possibilities (solved by sum types/enums):**

When a parameter should only accept a limited set of values (e.g., genres), use an enum:

```scala
enum Genre {
  case Pop, Rock, HeavyMetal, HardRock
}
```

**Algebraic Data Types (ADTs):**

Combining product types (case classes) and sum types (enums) creates ADTs. For example, a search criterion can be modeled as:

```scala
enum SearchCriterion {
  case ByGenre(genres: List[Genre])
  case ByOrigin(locations: List[Location])
  case ByActiveYears(period: ActiveYears)
  case ByActiveLength(howLong: Int, until: Int)
}
```

**Pattern matching:**

ADTs are processed using pattern matching:

```scala
def matchesCriterion(artist: Artist, criterion: SearchCriterion): Boolean =
  criterion match {
    case ByGenre(genres) => genres.contains(artist.genre)
    case ByOrigin(locations) => locations.contains(artist.origin)
    case ByActiveYears(period) => wasArtistActive(artist, period)
    case ByActiveLength(howLong, until) => activeLength(artist, until) >= howLong
  }
```

The compiler ensures all cases are covered, providing compile-time safety.

**Modeling behaviors as data:**

Search criteria themselves are modeled as data (ADTs) and passed to functions. This makes invalid search combinations unrepresentable and eliminates nested if-else chains.

### Chapter 8: IO as Values

This chapter addresses the "elephant in the room" -- real programs must interact with the outside world (API calls, databases, user input), which is inherently impure.

**The meeting scheduler example:**

The task is to build a meeting scheduler that calls external calendar APIs. The imperative Java version has three problems: (1) entangled concerns (business logic mixed with IO handling), (2) no error recovery (API failures crash the whole function), and (3) the signature lies (claims to return a value but may throw an exception or return null).

**The IO type:**

`IO[A]` is an immutable value that *represents* a potentially side-effectful computation that, when executed, produces an `A`. Crucially, creating an IO value does not execute anything:

```scala
def castTheDie(): IO[Int] = IO.delay(castTheDieImpure())
```

`IO.delay` takes a block of code and wraps it without executing it. `IO.pure` wraps a known value eagerly.

**IO has the same combinators as Option, Either, and List:**

- `map`: Transform the result.
- `flatMap`: Chain sequential IO actions.
- `orElse`: Provide fallback behavior on failure.

**Pushing impurity out:**

The pure business logic works with IO values as descriptions of programs. Only one place in the codebase calls `unsafeRunSync()` to actually execute side effects. This creates a **functional core** of pure functions surrounded by a thin impure shell.

**The functional solution:**

```scala
def schedule(attendees: List[String], lengthHours: Int): IO[Option[MeetingTime]] = {
  for {
    existingMeetings <- scheduledMeetings(attendees)
    possibleMeeting = possibleMeetings(existingMeetings, 8, 16, lengthHours).headOption
    _ <- possibleMeeting match {
      case Some(meeting) => createMeeting(attendees, meeting)
      case None => IO.unit
    }
  } yield possibleMeeting
}
```

**Lazy vs. eager evaluation:**

`IO.delay` is lazy (the wrapped code is not executed until `unsafeRunSync` is called). `IO.pure` is eager (the value is computed immediately). This distinction matters for side-effectful code: you want to delay execution until the right moment.

**Configurable retry strategies:**

The `retry` function demonstrates treating retries as values:

```scala
def retry[A](action: IO[A], maxRetries: Int): IO[A] = {
  List.range(0, maxRetries)
    .map(_ => action)
    .foldLeft(action)((program, retryAction) => program.orElse(retryAction))
}
```

**The `sequence` function:**

Transforms `List[IO[A]]` into `IO[List[A]]` -- sequencing a list of programs into a single program that runs them all.

**Functional architecture:**

The chapter introduces the concept of separating concerns into:
- **Essential concerns**: Business logic (pure functions in the functional core).
- **Accidental concerns**: IO actions, retries, caching (handled by passing IO values to the functional core).

### Chapter 9: Streams as Values

This chapter introduces functional streams for dealing with unknown or potentially infinite amounts of data.

**The currency exchange example:**

The task is an online currency exchange that should only execute when exchange rates are trending (each of the last n rates is higher than the previous). The number of API calls needed is initially unknown.

**Immutable Maps and Tuples:**

Before tackling streams, the chapter introduces Scala's immutable `Map` (key-value pairs with `updated`, `removed`, `get` operations) and tuples (fixed-size collections of heterogeneous values). Both are immutable and return new values on modification.

**Bottom-up design:**

The chapter demonstrates a bottom-up approach: start with small functions and compose them into larger ones.

**Recursive functions for unknown quantities:**

When the number of API calls is unknown, recursion is the first solution:

```scala
def exchangeIfTrending(amount: BigDecimal, from: Currency, to: Currency): IO[BigDecimal] = {
  for {
    rates <- lastRates(from, to, 3)
    result <- if (trending(rates)) IO.pure(amount * rates.last)
              else exchangeIfTrending(amount, from, to)
  } yield result
}
```

Problems with the recursive approach: (1) It fetches rates in fixed batches, missing trends that span batch boundaries, and (2) it runs as fast as possible without delay between API calls.

**Functional Stream type:**

`Stream[IO, A]` is an immutable value representing a lazily evaluated, potentially infinite sequence of side-effectful computations producing values of type `A`.

```scala
val infiniteDieCasts: Stream[IO, Int] = Stream.eval(castTheDie()).repeat
```

**Stream operations:**

- `eval`: Wraps an IO value into a single-element stream.
- `repeat`: Repeats the stream infinitely.
- `take(n)`: Takes only n elements.
- `filter`: Keeps only elements satisfying a condition.
- `map`: Transforms each element.
- `compile.toList`: Compiles the stream into an IO that produces a List.
- `compile.drain`: Compiles the stream into an IO[Unit], executed only for side effects.

**Sliding windows:**

Streams make sliding window calculations natural:

```scala
rates.sliding(n).filter(window => trending(window.toList))
```

**Rate limiting with `metered`:**

```scala
Stream.eval(exchangeTable(from)).metered(1.second).repeat
```

This creates a stream that produces values at a fixed rate of one per second.

**Separation of concerns in streams:**

The stream-based approach separates the *producer* (data generation via API calls) from the *consumer* (business logic using the data). The producer does not know how many values the consumer needs; the consumer does not know how values are produced.

### Chapter 10: Concurrent Programs

This chapter shows how to write safe concurrent programs using purely functional techniques.

**The city check-ins example:**

The task is to process an incoming stream of city check-ins and maintain a live ranking of the most popular cities.

**Sequential vs. concurrent:**

Sequential programs run one step after another. Concurrent programs can run multiple steps in parallel, but this introduces the challenge of shared mutable state.

**Imperative concurrency problems:**

Traditional approaches use locks, synchronized blocks, or atomic references. These are error-prone: deadlocks, race conditions, and forgotten locks are common.

**Functional concurrency with Ref:**

`Ref[IO, A]` is an immutable value representing a concurrently accessible mutable reference to an immutable value of type `A`:

```scala
for {
  counter <- Ref.of[IO, Int](0)
  _ <- counter.update(_ + 1)
  result <- counter.get
} yield result
```

`update` takes a pure function `A => A` and safely applies it using compare-and-swap semantics. If another thread modifies the value in the meantime, the function is retried automatically.

**parSequence:**

Just as `sequence` runs IO values sequentially, `parSequence` runs them in parallel:

```scala
List(io1, io2, io3).parSequence  // Runs all three concurrently
```

**Fibers:**

Functional programming uses **fibers** (lightweight logical threads) instead of OS-level threads. Many fibers can execute on a single thread. They are created implicitly by `parSequence`.

**The concurrent check-ins processor:**

```scala
def processCheckIns(checkIns: Stream[IO, City]): IO[Unit] = for {
  storedCheckIns <- Ref.of[IO, Map[City, Int]](Map.empty)
  storedRanking <- Ref.of[IO, List[CityStats]](List.empty)
  rankingProgram = updateRanking(storedCheckIns, storedRanking)
  checkInsProgram = checkIns.evalMap(storeCheckIn(storedCheckIns)).compile.drain
  _ <- List(rankingProgram, checkInsProgram).parSequence
} yield ()
```

Two programs run concurrently: one stores incoming check-ins, the other continuously recalculates the ranking. Both safely access shared state through Ref values.

**Asynchronous programming:**

The chapter also touches on asynchronous programming, where operations do not block threads but instead use callbacks or fibers. This is more efficient than blocking because threads can do other work while waiting.

---

## Part 3: Applied Functional Programming

### Chapter 11: Designing Functional Programs

This chapter applies all previously learned techniques to build a real-world application: a "pop culture travel guide" that uses Wikidata as a data source.

**The "make it work, make it right, make it fast" approach:**

The chapter follows this iterative design philosophy, first building a working solution, then improving its correctness, and finally optimizing performance.

**Requirements:**

Given a tourist attraction name, the application should:
1. Search for the attraction and its location.
2. Find artists from that location (sorted by followers).
3. Find movies set in that location (sorted by box office).
4. Score the resulting guide and return the best one.
5. Be extensible to support more pop culture subjects in the future.

**Modeling the data:**

The design uses ADTs extensively:

```scala
enum PopCultureSubject:
  case Artist(name: String, followers: Int)
  case Movie(name: String, boxOffice: Long)

case class Attraction(name: String, description: Option[String], location: Location)
case class TravelGuide(attraction: Attraction, subjects: List[PopCultureSubject])
```

**The DataAccess trait -- a bag of functions:**

Data access is modeled as a trait (interface) containing three pure functions that return IO values:

```scala
trait DataAccess {
  def findAttractions(name: String, ordering: AttractionOrdering, limit: Int): IO[List[Attraction]]
  def findArtistsFromLocation(locationId: LocationId, limit: Int): IO[List[Artist]]
  def findMoviesAboutLocation(locationId: LocationId, limit: Int): IO[List[Movie]]
}
```

This design allows the business logic to be completely independent of the data source.

**The functional core:**

The `travelGuide` function is a pure function that takes a `DataAccess` value:

```scala
def travelGuide(data: DataAccess, attractionName: String): IO[Option[TravelGuide]]
```

**Integrating with Wikidata via SPARQL:**

The data access layer is implemented using Apache Jena (a Java library) to query Wikidata's SPARQL endpoint. Imperative library calls are wrapped in `IO.blocking` or `IO.delay`.

**Inversion of control:**

Rather than passing connections around, the design passes *behaviors* (functions) as parameters:

```scala
def findAttractions(execQuery: String => IO[List[QuerySolution]])
  (name: String, ordering: AttractionOrdering, limit: Int): IO[List[Attraction]]
```

**Resource management:**

The `Resource` type ensures that connections and query executions are properly acquired and released, even in the presence of errors:

```scala
val executionResource: Resource[IO, QueryExecution] =
  Resource.make(createExecution(connection, query))(closeExecution)
```

**Making it right -- scoring guides:**

A pure `guideScore` function implements the scoring algorithm. The `travelGuide` function fetches multiple attractions, creates guides for each, scores them, and returns the best one.

**Making it fast -- concurrency:**

Sequential `sequence` calls are replaced with `parSequence` to fetch artists and movies for each attraction in parallel:

```scala
guides <- attractions.map(attraction =>
  List(
    data.findArtistsFromLocation(attraction.location.id, 2),
    data.findMoviesAboutLocation(attraction.location.id, 2)
  ).parSequence.map(_.flatten)
    .map(popCultureSubjects => TravelGuide(attraction, popCultureSubjects))
).parSequence
```

**Caching:**

A `Ref`-based cache stores query results to avoid redundant API calls:

```scala
def cachedExecQuery(connection: RDFConnection, cache: Ref[IO, Map[String, List[QuerySolution]]])
  (query: String): IO[List[QuerySolution]]
```

### Chapter 12: Testing Functional Programs

The final chapter covers testing functional programs, demonstrating that testing pure functions is fundamentally simpler than testing impure code.

**Tests are just functions:**

No new concepts are needed. Tests are pure functions that call other pure functions with specific inputs and assert on outputs.

**Testing by providing examples (example-based testing):**

```scala
test("guideScore should return 30 for a guide with description only") {
  val guide = TravelGuide(attractionWithDesc, List.empty)
  assert(guideScore(guide) == 30)
}
```

**Testing by providing properties (property-based testing):**

Instead of specific examples, test properties that should hold for all inputs:

```scala
test("guideScore should always be non-negative") {
  forAll { (guide: TravelGuide) =>
    assert(guideScore(guide) >= 0)
  }
}
```

**Custom generators:**

Property-based testing requires generators that produce valid test data. The book shows how to create custom generators for ADTs.

**Data usage tests (testing IO-based functions):**

When testing functions that use IO, external dependencies are stubbed by passing alternative `DataAccess` implementations:

```scala
val dataAccess = new DataAccess {
  def findAttractions(name: String, ordering: AttractionOrdering, limit: Int) =
    IO.pure(List(yellowstone))
  def findArtistsFromLocation(locationId: LocationId, limit: Int) =
    IO.pure(List.empty)
  def findMoviesAboutLocation(locationId: LocationId, limit: Int) =
    IO.pure(List.empty)
}
```

No mocking libraries are needed because functions are passed as values.

**Integration tests with real servers:**

A local SPARQL server is started using `Resource` to test the actual data access layer against a real (but local) service:

```scala
def localSparqlServer: Resource[IO, FusekiServer] = {
  val start: IO[FusekiServer] = IO.blocking { /* start server */ }
  Resource.make(start)(server => IO.blocking(server.stop()))
}
```

**Test-driven development (TDD):**

The chapter concludes with a TDD example for a new feature: returning a `SearchReport` when no good-enough guide is found. The process follows red-green-refactor:

1. **Red**: Write a failing test for the new behavior.
2. **Green**: Implement the simplest code that makes the test pass.
3. **Refactor**: Improve the code while keeping tests green.
4. Repeat until all requirements are satisfied.

The new signature uses `Either`:

```scala
def travelGuide(dataAccess: DataAccess, attractionName: String): IO[Either[SearchReport, TravelGuide]]
```

**Choosing the right testing approach:**

The book provides a decision framework:
- Pure functions without IO: example-based or property-based tests.
- Functions using IO with stubbed dependencies: data usage tests.
- Integration layer: real server integration tests (example-based or property-based).
- The testing pyramid: many fast unit tests, fewer integration tests.

---

## Key Takeaways

1. **FP is programming with pure functions and immutable values.** Pure functions always return a single value, use only their arguments, and do not mutate existing values. Immutable values cannot be changed after creation.

2. **Functions are values.** Functions can be stored, passed as arguments, and returned from other functions. This enables higher-order functions like `map`, `filter`, `flatMap`, `foldLeft`, and `sortBy`, which are the building blocks of functional programs.

3. **Signatures should tell the whole story.** A function's signature should communicate everything about its behavior. Functions that "lie" (throwing exceptions, returning null, relying on hidden state) are the source of many bugs.

4. **Errors are values, not control flow.** Use `Option` for possible absence, `Either` for descriptive errors, and combinators like `orElse`, `map`, and `flatMap` to compose error-handling logic. This replaces try-catch blocks with declarative value transformations.

5. **Model data using types to prevent invalid states.** Newtypes prevent parameter misuse, `Option` models absence in data, sum types (enums) model finite possibilities, and product types (case classes) couple related data. Together they form Algebraic Data Types.

6. **Side effects are described by IO values, not executed inline.** `IO[A]` is a value representing a side-effectful computation. Pure functions return IO values without executing them. Execution happens in a single controlled location via `unsafeRunSync`.

7. **For comprehensions are the primary control flow mechanism.** They are syntactic sugar for nested `flatMap`/`map` calls and work uniformly across `List`, `Option`, `Either`, `IO`, and `Stream`.

8. **Streams handle infinite or unknown quantities of data.** Functional streams are immutable, lazy, and composable. They integrate seamlessly with IO, enabling declarative processing of real-time or infinite data sources.

9. **Concurrency is declarative.** Use `Ref` for safe shared mutable state, `parSequence` to run IO programs in parallel, and fibers instead of OS threads. The type system ensures thread safety.

10. **Testing pure functions requires no mocking frameworks.** Pure functions are tested by calling them with inputs and asserting on outputs. IO-based functions are tested by passing stub implementations as function arguments. Everything is just values.

11. **Functional architecture separates essential concerns from accidental ones.** The functional core contains only pure functions and immutable values. Impure details (IO actions, external APIs) are pushed to the edges and passed in as parameters.

12. **The same patterns recur everywhere.** `map`, `flatMap`, `filter`, `foldLeft`, `orElse`, for comprehensions -- these combinators work identically on Lists, Options, Eithers, IOs, Streams, and Refs. Learning them once pays dividends across every domain.
