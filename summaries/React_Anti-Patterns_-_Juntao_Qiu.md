# React Anti-Patterns - Comprehensive Summary

**Author:** Juntao Qiu
**Published:** January 2024 (Packt Publishing)
**ISBN:** 978-1-80512-397-2

---

## Overview

This book addresses the common anti-patterns that arise in React applications, particularly as they scale to medium and large sizes. It bridges the gap between established software design principles (SRP, DIP, DRY, layered architecture) and their practical application in the React ecosystem. The author draws from his experience at Atlassian and Thoughtworks to demonstrate how patterns like the Strategy pattern, Anti-Corruption Layer (ACL), and Headless Components can dramatically improve React codebases. The book progresses from fundamentals through testing, refactoring, design patterns, and culminates in two end-to-end projects.

---

## Part 1: Introducing the Fundamentals

### Chapter 1: Introducing React Anti-Patterns

An anti-pattern is code that functions correctly at first but becomes problematic as the codebase expands. This chapter frames the difficulty of building modern frontend applications and catalogs the most common React anti-patterns.

**The difficulty of building UIs:** Web browsers were designed for documents, not rich interactive UIs. Components like accordions, toggle switches, and interactive cards must be simulated with HTML, CSS, and JavaScript. Complex applications like Jira's issue view contain many interactive elements that are not native browser components.

**State management challenges:** Remote states (data fetched from backend servers) introduce significant complexity including asynchronous operations, error handling, loading states, consistency issues, caching, and optimistic UI updates. A simple static rendering component can triple in code size when handling loading states, error states, and data fetching. Local state (like accordion open/close status) adds yet another dimension of complexity.

**Unhappy paths:** Errors thrown from third-party components can crash entire applications if not isolated with error boundaries. Unexpected user behavior (special characters, rapid form submissions) requires additional validation and safeguards.

**Common anti-patterns cataloged:**

1. **Props drilling:** Passing props through multiple intermediate components that do not use them. Solution: Context API.
2. **In-component data transformation:** Embedding data mapping logic directly inside components, reducing reusability and testability. Solution: Extract transformations to utility functions or custom Hooks.
3. **Complicated logic in views:** Placing business logic (filtering, calculations) inside view components. Solution: Separation of concerns with layered architecture.
4. **Lack of tests:** No safety net for verifying correctness or supporting confident refactoring. Solution: TDD.
5. **Duplicated code:** Similar filtering or transformation logic repeated across components. Solution: DRY principle with shared utilities or HOCs.
6. **Long components with too much responsibility:** Monolithic components with huge prop lists (like an `OrderContainer` with 12+ props). Solution: SRP decomposition.

**The book's approach:** Combine render props, HOCs, Hooks, layered architecture, interface-oriented programming, headless components, TDD, and continuous refactoring to systematically address these anti-patterns.

---

### Chapter 2: Understanding React Essentials

This chapter covers the foundational React concepts needed throughout the book.

**Static components and props:** A static component returns fixed JSX. Props make components reusable by accepting dynamic data. Components should ideally have no more than 5-6 props for clarity.

**Breaking down UIs:** A weather application is used as an example of decomposing a complex UI into sub-components (`Heading`, `SearchBox`, `Notification`, `WeatherList`). Each sub-component can manage its own state and behavior independently.

**Internal state with useState:** The `useState` Hook manages local component state. Multiple states can coexist (e.g., a login form with username, password, and rememberMe). State persists across re-renders.

**The rendering process:** React follows: initial render, state/props changes (triggering diffing), reconciliation, re-rendering, and DOM update. The diffing algorithm compares previous and new virtual DOM representations to minimize real DOM manipulations.

**useEffect:** Handles side effects (API calls, DOM manipulation, event listeners, timers). Key concepts:
- Empty dependency array `[]` runs once on mount
- Dependencies array triggers the effect when values change
- Cleanup functions prevent memory leaks (e.g., `clearTimeout`, `AbortController` for fetch cancellation)

**useCallback:** Memoizes callback functions to prevent unnecessary recreation during re-renders. Particularly useful when passing callbacks to child components or as dependencies in other Hooks.

**React Context API:** Provides a way to pass data through the component tree without passing props at every level. Demonstrated with a theme context (`ThemeContext`, `ThemeProvider`) supporting both reading and modifying the context value. Multiple contexts can be nested (interaction, security, logging) to manage different concerns independently.

---

### Chapter 3: Organizing Your React Application

This chapter explores four major project structuring strategies and provides practical guidance for evolving a project's structure as it grows.

**Problems of a less-structured project:** Code disorganization, poor reusability, collaboration difficulties, scalability issues, and maintenance complexity all worsen as a project grows without proper structure.

**Frontend application components:** Source code, assets, configuration, tests, documentation, build artifacts, and development tools must all be organized.

**Feature-based structure:** Organizes by feature (Home, Cart, Checkout, etc.) with each feature containing its own components, services, and state. Benefits: clear separation, modularity, scalability, team collaboration. Drawback: potential duplication across features.

**Component-based structure:** Organizes around reusable components. Benefits: modularity, separation of concerns, code reusability. Drawbacks: project complexity at scale, learning curve, potential duplication.

**Atomic design structure:** Categorizes components as atoms (buttons, inputs), molecules (form fields), organisms (headers, sidebars), templates (page layouts), and pages (complete screens). Benefits: reusability, consistency, scalability. Drawbacks: learning curve, complexity at scale, risk of overengineering.

**MVVM structure:** Separates Model (data/business logic), View (UI), and ViewModel (state management and interaction logic). Benefits: separation of concerns, testability of ViewModels, reusability. Drawbacks: added complexity for smaller projects, learning curve.

**Practical evolution approach:** Start with feature-based structure. As duplication emerges, extract shared components into a separate `components` folder. Add `hooks`, `context`, and `mocks` folders as needed. File naming should be consistent (either explicit component names with `index.tsx` or kebab-case). Use ESLint and FolderLint to enforce conventions.

**The recommended customized structure** includes folders for: `api`, `components` (shared), `context`, `hooks`, `mocks`, and `pages` (feature-specific). As applications grow, shared components may evolve into an internal design system.

---

### Chapter 4: Designing Your React Components

This chapter applies three core design principles to React component design.

**Single Responsibility Principle (SRP):** Each component should have one reason to change. A `BlogPost` component that fetches data, renders content, and handles likes violates SRP. The refactoring extracts:
- `useFetchPost` custom Hook (data fetching)
- `LikeButton` component (like functionality)
- `BlogPost` component (rendering only)

**Don't Repeat Yourself (DRY):** When `ProductList` and `Cart` components share nearly identical rendering logic (image, name, price, action button), extract a shared `LineItem` component. This component accepts `product`, `performAction`, and `label` props, eliminating duplication and creating a single source of truth.

**Composition:** Building complex UIs from simpler components. A monolithic `UserDashboard` is decomposed into `UserProfile`, `FriendList`, and `PostList`, each handling a single concern. Benefits include separation of concerns, readability, reusability, and testability.

**Combining principles with the Page component example:** A `Page` component with seven props (headerTitle, headerSubtitle, sidebarLinks, etc.) violates SRP with its long prop list. The refactoring proceeds in stages:

1. Extract `Header`, `Sidebar`, and `Main` sub-components (SRP)
2. Rename props to remove redundant prefixes (e.g., `headerTitle` becomes `title` inside `Header`)
3. Use composition to accept sub-components as `ReactNode` props instead of configuration props

The final `Page` component accepts just three props (`header`, `sidebar`, `main`), each being a `ReactNode` that can be any JSX element. This maximizes flexibility while minimizing the component's surface area.

---

## Part 2: Embracing Testing Techniques

### Chapter 5: Testing in React

**Why tests matter:** Tests ensure code correctness, prevent regression, facilitate refactoring, boost confidence in code quality, and serve as documentation.

**Test pyramid:** Originally conceived by Mike Cohn -- many fast unit tests at the bottom, fewer integration tests in the middle, and few E2E tests at the top. The modern frontend test pyramid also includes visual regression tests and static checks. The key is a balanced strategy with quick, useful feedback at different levels.

**Unit tests with Jest:** Jest is Facebook's JavaScript testing framework. Tests use `test` or `it` functions with `expect` and matchers. Related tests are grouped with `describe` blocks, which can be nested for systematic organization. The React Testing Library tests components by rendering them and querying the DOM:

```tsx
describe("Section", () => {
  it("renders a section with heading and content", () => {
    render(<Section heading="Basic" content="Hello world" />);
    expect(screen.getByText("Basic")).toBeInTheDocument();
    expect(screen.getByText("Hello world")).toBeInTheDocument();
  });
});
```

**Integration tests:** Test interactions between multiple components. A Terms and Conditions component demonstrates testing the interaction between a checkbox and a "Next" button (button starts disabled, becomes enabled when checkbox is clicked). Uses `userEvent.click` wrapped in `act` and runs in a jsdom environment (in-memory headless browser).

**E2E tests with Cypress:** Cypress operates directly in the browser (not using Selenium). The chapter demonstrates:
- Installing Cypress and creating test specs
- Visiting pages and asserting content with `cy.contains()`
- Querying elements with `data-testid` attributes
- Intercepting network requests with `cy.intercept()` to stub API responses, making tests deterministic and isolated from backend instability

---

### Chapter 6: Exploring Common Refactoring Techniques

Refactoring is a disciplined process of improving code design without changing external behavior. The key distinction: refactoring is small, incremental changes that preserve functionality; restructuring is larger-scale changes that may alter behavior.

**Critical rule:** Always add tests before refactoring to have a safety net. The chapter uses a `ShoppingCart` class with `addItemToCart` and `calculateTotal` methods (including a 10% discount for quantities over 10) as the running example.

**Refactoring techniques demonstrated:**

1. **Rename Variable:** Renaming `cartItems` to `items` for clarity. Simple but powerful for readability.

2. **Extract Variable/Constant:** Extracting the magic number `0.9` into a named constant `DISCOUNT_RATE`.

3. **Replace Loop with Pipeline:** Converting a `for` loop to `reduce`:
```typescript
calculateTotal() {
  return this.items.reduce((total, item) => {
    let subTotal = item.price * item.quantity;
    return total + (item.quantity > 10 ? subTotal * DISCOUNT_RATE : subTotal);
  }, 0);
}
```

4. **Extract Function:** Extracting `applyDiscountIfEligible(item, subTotal)` from `calculateTotal` for modularity and self-documentation.

5. **Introduce Parameter Object:** Grouping related parameters into a single object type (`Item`), reducing function signature complexity.

6. **Decompose Conditional:** Extracting `isDiscountEligible(item)` from the inline conditional, making the intention clearer.

7. **Move Function:** Relocating type definitions to `types.ts` and utility functions to `utils.ts`, improving encapsulation (only `applyDiscountIfEligible` is exported as public API).

After all refactorings, the `ShoppingCart` class is significantly simplified with logic properly distributed across focused modules.

---

### Chapter 7: Introducing Test-Driven Development with React

**TDD fundamentals:** Originated from Extreme Programming (XP), popularized by Kent Beck. The Red-Green-Refactor loop: write a failing test (Red), write minimal code to pass (Green), then improve the code (Refactor). Benefits include focused problem-solving, predictable next steps, simpler design, mental flow, and automatic test coverage.

**TDD styles:**
- **TDD (classic):** Unit test focus on smallest code pieces
- **ATDD:** Starts with user acceptance tests defining "done" from the user's perspective
- **BDD:** Checks system behavior under certain conditions, using descriptive language (Gherkin with Cucumber)

**Tasking:** Breaking features into small, manageable tasks (15-30 minutes each) that serve as the basis for test cases. Steps: review requirements, identify logical components, create a task list, sequence tasks, map tasks to tests.

**Top-down vs. Bottom-up:**
- **Bottom-up:** Start with smallest components (`PizzaItem`), build up to integration. Strong validation of individual units but may face integration challenges.
- **Top-down:** Start with high-level application features, gradually extract smaller components. Ensures primary objectives are established early; may require temporary stubs.

**Practical TDD example -- The Code Oven pizza store:**

The chapter walks through building a pizza ordering application using top-down TDD:

1. **Application headline:** Write test for "The Code Oven" text, make it pass with a static component, refactor to separate file.

2. **Menu list:** Test for 8 list items, make pass with hardcoded `<li>` elements, refactor to use `Array.map`.

3. **Shopping cart:** Test for container with disabled "Place My Order" button. Each test cycle adds more assertions (button text, disabled state).

4. **Adding items:** Test clicking "Add" button shows item in cart and enables order button. Requires `async`/`await` for React state updates to propagate.

5. **Refactoring:** Extract `MenuList` and `ShoppingCart` components from the monolithic `PizzaShopApp`. Rename variables for clarity (`x` to `item`). Add unique keys to list items. Tests remain green throughout.

Key TDD insight: The code does not have to be perfect initially. The iterative Red-Green-Refactor cycle provides continuous improvement with a safety net.

---

## Part 3: Unveiling Business Logic and Design Patterns

### Chapter 8: Exploring Data Management in React

**Business logic leaks:** When data transformation logic (mapping API response fields to frontend-friendly formats) is scattered across components, Hooks, and utility functions, it creates tight coupling, code duplication, and inconsistency. The `UserProfile` component example shows field mapping (`data.user_identification` to `id`, `data.user_full_name` to `name`) embedded inside a `useEffect`.

**Anti-Corruption Layer (ACL):** A centralized translation layer between external systems and the frontend application. Benefits:
- Unified interface for disparate data sources (REST, GraphQL, WebSocket)
- Centralized caching, error transformations, and cross-cutting concerns
- Single place for data shape changes

Implementation involves defining `RemoteUser` and local `User` types, then creating a `transformUser` function in `transformer.ts`. The component becomes agnostic to the remote data structure.

**Fallback/default values:** Instead of scattering null checks and fallback values throughout components (`user && user.name ? user.name : "Loading..."`), centralize this logic in the ACL using optional chaining (`?.`) and nullish coalescing (`??`):

```typescript
export const transformUser = (remoteUser: RemoteUser): User => {
  return {
    id: remoteUser.user_identification ?? 'N/A',
    name: remoteUser.user_full_name ?? 'Unknown User',
    isPremium: remoteUser.is_premium_user ?? false,
    subscription: (remoteUser.subscription_details?.level ?? 'Basic') as UserSubscription,
    expire: remoteUser.subscription_details?.expiry ?? 'Never',
  };
};
```

**Prop drilling deep dive:** Using a `SearchableList` component decomposed into `SearchInput`, `List`, and `ListItem`, the chapter demonstrates how adding analytics callbacks (`onItemClicked`, `onSearch`) forces intermediate components to pass props they do not use. The `List` component must accept and forward `onItemClicked` without using it -- a code smell.

**Context API solution:** Define a `SearchableListContext` with `onSearch` and `onItemClicked` functions. The `SearchableList` wraps children in the context provider. Sub-components access needed functions via `useContext` directly, eliminating prop drilling. The `List` component reverts to its simple form, and `ListItem` accesses `onItemClicked` from the context.

---

### Chapter 9: Applying Design Principles in React

**Revisiting SRP with render props:** Starting from a static `Title` component, the chapter demonstrates progressive abstraction: adding a `title` prop, then a `transformer` higher-order function, then a full render prop that accepts a function returning JSX. Using the `children` prop as a render prop provides a more intuitive API. The pattern enables maximum flexibility -- the parent controls rendering while the child provides structure and data.

**Composition to apply SRP:** An `Avatar` component that internally uses `Tooltip` creates tight coupling. The refactored approach simplifies `Avatar` to focus solely on displaying an image, letting consumers compose it with `Tooltip` when needed. Benefits: leaner `Avatar` bundle, consumer freedom to customize or swap tooltip libraries.

**Dependency Inversion Principle (DIP):** High-level modules should depend on abstractions, not concrete implementations. Demonstrated through:
1. A notification system: `Application` depends on a `Notification` interface, not `EmailNotification` directly. Swapping to `SMSNotification` requires no changes to `Application`.
2. An analytics button: `Button` depends on an `InteractionMeasurement` interface provided via Context. Products wanting analytics wrap the app in a provider; those that do not simply use `Button` directly. This avoids modifying shared components for product-specific features.

**CQRS (Command and Query Responsibility Segregation):** Separate methods that modify state (commands) from methods that read state (queries). Applied to a shopping cart:

- **Commands:** `addItem`, `removeItem` (modify state, return nothing)
- **Queries:** `useTotalPrice` (read state, no modifications)

Implemented using `useReducer` for state management with a `shoppingCartReducer` handling `ADD_ITEM` and `REMOVE_ITEM` actions. The reducer generates unique keys (`uniqKey`) to handle duplicate products correctly. A `ShoppingCartProvider` context exposes commands, while custom Hooks (`useTotalPrice`) expose queries.

---

### Chapter 10: Diving Deep into Composition Patterns

**Higher-order functions (HOFs):** Functions that take or return other functions. A `report` function accepting a `transformer` parameter demonstrates how HOFs enable customization without modifying core logic.

**Higher-order components (HOCs):** Functions that accept a component and return an enhanced version. Examples:
- `withAuthorization`: Wraps components with authentication checks
- `withAutoClose`: Adds auto-dismissal behavior (for notifications, tooltips)
- `withKeyboardToggle`: Adds keyboard navigation (Enter/Space to toggle, Escape to blur)

HOCs can be composed: `withAutoClose(withKeyboardToggle(ExpandablePanel), 2000)` creates an accessible, auto-closing panel. This mirrors the Decorator design pattern.

**React Hooks for composition:** Hooks provide a lighter-weight alternative to HOCs:
- `useAutoClose`: Encapsulates auto-close timer logic
- `useKeyboard`: Encapsulates keyboard event handling
- `useService`: Generic data fetching Hook managing loading, error, and data states

Hooks offer a "plugin mechanism" rather than the "wrapping approach" of HOCs, making them lighter and better managed by React.

**Developing a drop-down list component:** Building a dropdown from scratch reveals the complexity hidden in native select elements. The implementation progresses through:
1. Basic mouse-click open/close with `useState`
2. Extracting `Trigger` and `DropdownMenu` sub-components
3. Adding keyboard navigation (Enter, Space, ArrowUp, ArrowDown, Escape) with `useDropdown` custom Hook
4. Supporting remote data fetching with loading/error states

**Headless Component pattern:** Separates behavior/logic from UI rendering. A headless component (implemented as a Hook) manages all stateful logic but renders nothing. The consumer controls the UI. Benefits: reusability (DRY), separation of concerns, flexibility across different visual representations. Drawbacks: learning curve, potential over-abstraction. Notable libraries using this pattern: React Aria, Headless UI, React Table, Downshift.

The layered architecture visualization shows JSX at the top, headless components (Hooks) in the middle managing stateful logic, and domain models at the bottom handling data transformation.

---

## Part 4: Engaging in Practical Implementation

### Chapter 11: Introducing Layered Architecture in React

**Application evolution stages:**
1. **Single-component:** Everything in one component (suitable only for tiny apps)
2. **Multiple-component:** Decomposed into focused components
3. **State management with Hooks:** Logic extracted into custom Hooks
4. **Extracting business models:** Domain objects with data mapping and business rules
5. **Layered architecture:** Physical separation into folders for views, hooks, and models

**Enhancing the Code Oven application:** The chapter extends the pizza store from Chapter 7 with remote data, prices, ingredients, and discount logic.

**Refactoring through custom Hooks:** The `useMenuItems` Hook extracts data fetching and transformation from the `MenuList` component, restoring its single responsibility.

**Transitioning to class-based models:** The `MenuItem` type becomes a class with:
- Private readonly fields for encapsulation
- Constructor accepting `RemoteMenuItem` for ACL
- Getter methods for controlled access (e.g., `ingredients` returns only first 3 items)

Benefits: encapsulation, method behavior, inheritance/polymorphism, consistent interface, read-only properties.

**Applying discounts with polymorphism:** Different menu item types have different discount rules:
- `IMenuItem` interface defines the contract
- `AbstractMenuItem` base class implements shared logic
- `PizzaMenuItem`: 10% discount for 3+ toppings
- `PastaItem`: 15% discount for large servings

**Strategy pattern:** For flexible, runtime-changeable discounts:
- `IDiscountStrategy` interface with `calculate(price)` method
- `NoDiscountStrategy`, `SpecialDiscountStrategy`, `TenPercentageDiscountStrategy` implementations
- `BaseMenuItem` holds a `discountStrategy` property settable at runtime
- Friday specials or item-type discounts can be applied dynamically without modifying model classes

**The layered structure:**
```
src/
  App.tsx
  hooks/
    useMenuItems.ts
    useShoppingCart.ts
  models/
    BaseMenuItem.ts
    IMenuItem.ts
    PastaItem.ts
    PizzaMenuItem.ts
    RemoteMenuItem.ts
    strategy/
      IDiscountStrategy.ts
      NoDiscountStrategy.ts
      SpecialDiscountStrategy.ts
      TenPercentageDiscountStrategy.ts
  views/
    MenuList.tsx
    ShoppingCart.tsx
```

Key principle: one-directional dependency. Views use Hooks; Hooks use models. Models never import JSX or Hooks. This enables changing or replacing underlying layers without impacting upper layers.

**Advantages of layered architecture:** Enhanced maintainability, increased modularity, improved readability, better scalability, and the ability to migrate the view layer without altering models and logic.

---

### Chapter 12: Implementing an End-To-End Project

This chapter builds a weather application from scratch using ATDD, demonstrating the complete development workflow with OpenWeatherMap API integration.

**Initial acceptance test (Cypress):** Start with a failing test verifying "Weather Application" text, then make it pass with a simple `<h1>` tag.

**City Search feature:**
1. Intercept OpenWeatherMap API calls with `cy.intercept()` using fixture data
2. Implement search input with Enter-key trigger
3. Display search results in a dropdown list

**Enhancing search results with unit tests:** Extract `SearchResultItem` component and add city name, state, and country fields. Unit tests (Jest) are preferred for component-level details because they are faster and more focused than E2E tests.

**Implementing an ACL:** The remote API returns fields like `local_names`, `lon`, `lat` that the UI does not need. A `SearchResultItemType` class transforms remote data:
- Maps `country` codes to full names ("AU" to "Australia")
- Exposes only needed fields via getters
- Unit tests verify the transformation logic independently

**Add to Favorite feature:**
1. Click a search result to fetch weather data from a second API endpoint
2. Display city name and temperature in a favorites list
3. Close the dropdown after selection

**Weather modeling with CityWeather class:**
- Constructor accepts `RemoteCityWeather`
- `temperature` getter returns formatted string ("20 C") with fallback ("-/-" for null)
- `degree` getter rounds up with `Math.ceil`
- `main` getter lowercases the weather category

**Refactoring the application:**
- Extract `useSearchCity` custom Hook (query, search results, dropdown state)
- Extract `SearchCityInput` component (input handling, dropdown rendering)
- Extract `useFetchCityWeather` custom Hook (weather data fetching)
- Extract `Weather` and `WeatherList` components
- Final `App.tsx` is clean and minimal

**Multiple cities in favorites:** Update `useFetchCityWeather` to manage an array of `CityWeather` objects. Test with `renderHook` and `fetchMock`:

```typescript
const { result } = renderHook(() => useFetchCityWeather());
await act(async () => {
  await result.current.fetchCityWeather(searchResultItem);
});
expect(result.current.cities.length).toEqual(1);
```

**Persisting data with localStorage:**
- Extract `fetchCityWeatherData` as a standalone async function (SRP)
- On item click, save to localStorage (deferred with `setTimeout(fn, 0)`)
- On app launch, hydrate from localStorage and fetch fresh weather data with `Promise.all`

**Final project structure** shows clean separation: models (`CityWeather`, `SearchResultItemType`, `RemoteCityWeather`), hooks (`useSearchCity`, `useFetchCityWeather`), and views (`App`, `SearchCityInput`, `Weather`, `WeatherList`).

---

### Chapter 13: Recapping Anti-Pattern Principles

**Anti-patterns revisited:**
- **Props drilling:** Use Context API for central data stores
- **Long props list/big component:** Decompose with SRP; use custom Hooks
- **Business leakage:** Extract logic to Hooks, separate modules, or ACL
- **Complicated logic in views:** Move to Hooks, utilities, or business logic layer
- **Lack of tests:** Adopt TDD with unit, integration, and E2E testing
- **Code duplications:** Apply DRY with shared utilities, components, or Hooks

**Design patterns revisited:**
- **HOCs:** Reuse component logic by wrapping components
- **Render props:** Share code via function props
- **Headless components:** Separate behavior from UI
- **Data modeling:** Organize and define data to simplify component logic
- **Layered architecture:** Segregate concerns into layers with specific responsibilities
- **Context as interface:** Eliminate prop drilling for component communication

**Foundational design principles:**
- **SRP:** One reason to change per component/module -- the most reliable ally when dealing with large components
- **DIP:** Depend on abstractions, not concretions
- **DRY:** Minimize repetition for maintainability
- **ACL:** Create stable interfaces between system boundaries
- **Composition:** Build complex components from simpler, reusable parts

**Techniques and practices:**
- **User acceptance tests:** Write from the end user's perspective, focusing on customer value
- **TDD:** Red-Green-Refactor loop ensures functional, bug-free code
- **Refactoring:** Continuous improvement through small, behavior-preserving changes

**Recommended further reading:**
- *Refactoring* by Martin Fowler
- *Clean Code* by Robert Martin
- *Patterns of Enterprise Application Architecture* by Martin Fowler
- *Test-Driven Development with React and TypeScript* by Juntao Qiu

---

## Key Takeaways

1. **Anti-patterns are not bugs; they are design weaknesses.** Code with anti-patterns often works correctly but becomes unmaintainable as the codebase scales. Recognizing them early is the first step toward fixing them.

2. **The SRP is the most versatile tool in your arsenal.** Whether decomposing a monolithic component, extracting a custom Hook, or creating an ACL, the SRP guides you toward focused, maintainable code.

3. **Always add tests before refactoring.** Without a test safety net, refactoring becomes risky and inefficient. TDD's Red-Green-Refactor loop provides structure and confidence.

4. **The ACL pattern is essential for real-world applications.** Any application interfacing with external APIs needs a translation layer. Centralizing data transformation, fallback values, and field mapping prevents business logic from leaking into views.

5. **Composition over configuration.** Instead of components with long prop lists for every possible customization, accept sub-components as `ReactNode` props. This maximizes flexibility while minimizing the component's API surface.

6. **Context as an interface solves prop drilling elegantly.** Define context types that expose commands (state modifiers) and let consumers access them via `useContext`. This eliminates the need for intermediate components to forward props they do not use.

7. **CQRS with useReducer brings clarity to state management.** Separate commands (dispatch actions that modify state) from queries (custom Hooks that read state). This pattern scales well for complex state interactions.

8. **The Headless Component pattern is the pinnacle of separation of concerns.** By encapsulating all behavior and state logic in Hooks while leaving rendering to the consumer, you achieve maximum reusability and flexibility.

9. **Layered architecture scales with your application.** Views depend on Hooks; Hooks depend on models; models depend on nothing UI-related. This one-directional dependency enables independent evolution of each layer.

10. **Small, incremental improvements compound over time.** Neither refactoring nor TDD is about grand, sweeping changes. Each small step (renaming a variable, extracting a function, writing one test) builds toward a significantly healthier codebase.

11. **Design patterns from other domains apply directly to React.** The Strategy pattern, Decorator pattern, DIP, and layered architecture -- all proven in backend and enterprise contexts -- solve the same problems in frontend applications.

12. **Think from the user's perspective when writing tests.** As Kent C. Dodds says: "The more your tests resemble the way your software is used, the more confidence they can give you." User acceptance tests should drive feature development, with unit tests filling in the details.
