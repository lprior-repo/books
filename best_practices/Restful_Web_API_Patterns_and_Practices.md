# RESTful Web API Patterns and Practices Cookbook
**Author:** Mike Amundsen
**Topic tags:** `#api` `#architecture`
**Language focus:** Language-agnostic; HTTP, HTML, Collection+JSON, SIREN, HAL, JSON, XML, ALPS, and JavaScript examples
**Sources:** `markdown_output/Restful Web API Patterns and Practices Cookbook/Restful Web API Patterns and Practices Cookbook.md` · `summaries/Restful_Web_API_Patterns_and_Practices_Cookbook.md`

## TL;DR
Design network interfaces for strangers, unknown future uses, and decades of independent change. Keep protocol, representation format, vocabulary, and runtime actions separate; bind clients to stable abstractions and let messages carry volatile details. Make writes idempotent and reversible, publish machine-readable semantics and operational metadata, hide storage and service internals, and model long work as observable hypermedia resources.
---
## Best Practices by Topic

### 1. Optimize for REST Architectural Properties
`#api` `#architecture`

**Principle:** Apply constraints as a whole to induce performance, scalability, simplicity, modifiability, visibility, portability, and reliability.

**Do:**
- Separate concerns and generalize interfaces to produce simplicity.
- Support large numbers of components and interactions without central knowledge.
- Put caches, proxies, and mediators where they can observe or improve interactions.
- Allow components to deploy independently.
- Design for failures of individual machines and services.
- Evaluate both network efficiency and user-perceived latency.

**Don't:**
- Call an interface RESTful because it merely uses HTTP.
- Select constraints independently of the system properties they should induce.
- Optimize one component while making the complete network brittle.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "Fielding's REST"*
---
### 2. Separate the Four Communication Layers
`#api` `#architecture`

**Principle:** Keep protocol, message format, vocabulary, and runtime actions independent so each can change without forcing the others to change.

**Do:**
- Use HTTP as the protocol-level agreement.
- Use registered structured media types as the representation agreement.
- Publish domain terms separately from representation structure.
- Carry URLs, methods, encodings, and inputs in links and forms at runtime.
- Translate between internal terms and external vocabulary at the boundary.
- Treat meaning as independent of the message that carries it.

**Don't:**
- Encode domain meaning into transport mechanics.
- Treat a storage schema as a representation format.
- Force a vocabulary to depend on a particular protocol or serialization.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "Hypermedia Design"*
---
### 3. Design for Global Reach, Strangers, and Decades
`#api` `#architecture`

**Principle:** Build services that unknown people can combine for uses you did not predict, long after the initial release.

**Do:**
- Lower adoption barriers with open protocols, standard formats, and published semantics.
- Make interfaces understandable without private meetings or oral history.
- Carry enough context in each interaction for stateless use.
- Prefer longevity and independent evolution over short-term convenience.
- Assume a temporary service may survive for decades.
- Expect every implementation detail to change eventually.

**Don't:**
- Design only for the first known consumer.
- Assume you can coordinate every future change with every caller.
- Treat undocumented context as part of the contract.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "Shared Principles for Scalable Services on the Web" / "Guiding Principles of RESTful Web APIs"*
---
### 4. Use the Rule of Least Power
`#api` `#architecture`

**Principle:** Choose the least powerful language or mechanism that can solve the interaction problem safely.

**Do:**
- Prefer links and simple forms over embedded general-purpose programs.
- Prefer simple name/value HTTP queries for common information retrieval.
- Use constrained workflow affordances before inventing a programming language.
- Keep message exchange generic and local implementations specialized.
- Favor formats and protocols with low barriers to implementation.

**Don't:**
- Expose a database query engine when a named form solves the use case.
- invent a custom language merely to avoid using established standards.
- Add imperative branching to a declarative workflow document.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "The Web of Tim Berners-Lee" / "The Rule of Least Power"*
---
### 5. Treat Links and Forms as Affordances
`#api` `#architecture`

**Principle:** Express what a consumer can do through controls embedded in the current representation.

**Do:**
- Use links to afford navigation.
- Use forms to afford data submission.
- Return controls with results so the next valid actions are visible.
- Vary controls by resource, service, user, and request state.
- Let clients follow controls rather than reconstruct undocumented transitions.
- Design the connection between resources as carefully as the resources themselves.

**Don't:**
- Publish data without the actions needed to use it.
- Make clients infer permissions or state transitions from prose.
- Assume a fixed workflow is the only path through a service.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "Hypermedia: A Definition" / "James J. Gibson"*
---
### 6. Model Ontology, Taxonomy, and Choreography
`#api` `#architecture`

**Principle:** Describe properties, aggregate structures, and valid actions as separate but connected parts of the information architecture.

**Do:**
- Define ontology terms with stable meanings.
- Define taxonomies that group terms into recognizable resource states.
- Define choreography as links, forms, and valid transitions.
- Publish all three dimensions in a semantic profile.
- Use the same semantic identifiers consistently across representations.
- Keep implementation URLs and methods out of the problem-space model.

**Don't:**
- Publish only a data dictionary and call it a complete service vocabulary.
- Define actions without the states they return.
- confuse a semantic profile with an API definition document.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "Morville's Information Architecture" / "3.4 Describing Problem Spaces with Semantic Profiles"*
---
### 7. Bind Clients to Stable Abstractions
`#api` `#architecture`

**Principle:** Bind clients to protocol, media type, and semantic profile rather than volatile URLs, object schemas, or one service implementation.

**Do:**
- Bind HTTP behavior to an HTTP-aware client layer.
- Bind representation parsing to media-type handlers.
- Bind domain understanding to a published vocabulary profile.
- Resolve URLs, methods, encodings, and fields at runtime.
- Keep goal logic and transient state on the client.
- Use one starting URL when the service supplies hypermedia.

**Don't:**
- Generate a captive client whose identity is one endpoint tree.
- Bind application logic directly to response object layout.
- Treat a service definition document as the best client contract.

**Code:**
```
function onboardCustomer() {
 results = http.read("/onboarding/work-in-progress", "GET");
 while(results.actions) {
 var action = results.actions.pop();
 http.send(action.url, action.method, map(action.parameters,local.data));
 }
 return "200 OK";
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "Binding to Protocols and Formats" / "Supporting Client-Centric Workflows"*
---
### 8. Combine Orchestration and Choreography with Hypermedia Workflow
`#api` `#architecture`

**Principle:** Coordinate independent services through a small declarative interface instead of centralizing all decisions or hardwiring point-to-point dependencies.

**Do:**
- Use orchestration for a few simple, stable steps.
- Use choreography for many independent, asynchronous steps.
- Use hypermedia workflow to combine parallel independence with shared job control.
- Require task actions for Execute, Repeat, Revert, and Cancel.
- Require job actions for Continue, Restart, and Cancel.
- Put shared state in addressable documents.
- Observe each job through a progress resource.

**Don't:**
- Hide a single fatal workflow engine behind every interaction.
- Make every service know the complete business process.
- Share a database as the workflow protocol.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "Choreography, Orchestration, and Hypermedia Workflow"*
---
### 9. Use Registered Media Types (Recipe 3.1)
`#api` `#architecture`

**Principle:** Select open, registered formats so independently built consumers can bind to stable message rules.

**Do:**
- Start with the IANA Media Types Registry.
- Support more than one registered media type when practical.
- Include HTML for broad tooling, browser testing, and long-term support.
- Prefer formats that support both hypermedia and safe extension.
- Document supported types and runtime selection.
- Register and maintain a custom type as a public, long-lived commitment if you create one.

**Don't:**
- Create a custom media type without a limited audience, massive audience, or vertical leadership.
- Treat plain JSON or XML as structured merely because parsers exist.
- Abandon community tooling or documentation for a published format.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.1 Creating Interoperability with Registered Media Types"*
---
### 10. Separate Well-Formedness from Validity (Recipe 3.2)
`#api` `#architecture`

**Principle:** Keep representation structure stable while allowing domain content and validation rules to evolve.

**Do:**
- Validate the media-type structure before domain content.
- Use invariant containers such as HTML lists or Collection+JSON data arrays.
- Let added properties remain structurally well formed.
- Treat validity as a separate, evolving semantic concern.
- Keep content loosely coupled to representation structure.

**Don't:**
- Reject a structurally sound message solely because it contains an added field.
- Equate a JSON object's current keys with a permanent message type.
- require a new client parser whenever domain content grows.

**Code:**
```
<ul name="Person">
 <li name="givenName">Marti</li>
 <li name="familyName">Contardi</li>
</ul>
 ...
<ul name="Person">
 <li name="givenName">Marti</li>
 <li name="familyName">Contardi</li>
```

```
 <li name="emailAddress">mcontardi@example.org</li>
</ul>
```

```
{"Person" : {
 "givenName": "Marti",
 "familyName": "Contardi"
 }
}
 ...
{"Person" : {
 "givenName": "Marti",
 "familyName": "Contardi",
 "emailAddress": "mcontardi@example.org",
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.2 Ensuring Future Compatibility with Structured Media Types"*
---
### 11. Publish Domain Vocabularies (Recipe 3.3)
`#api` `#architecture`

**Principle:** Use well-documented public terms and publish every remaining magic string.

**Do:**
- Prefer Schema.org, then declared backup sources such as Microformats.org and Dublin Core.
- Consider established vertical vocabularies such as PSD2, FHIR, and ACORD.
- Publish every input, output, action, relation, name, ID, class, and tag with its definition.
- Link terms to authoritative definitions.
- Limit synonyms and choose one external term consistently.
- Mix sources when necessary but document governance priority.
- Use an anti-corruption layer instead of renaming internal data.

**Don't:**
- Require consumers to understand proprietary internal abbreviations.
- Tie vocabulary terms to a software platform, SDK, or hardware dependency.
- Assume data properties alone form the complete vocabulary.

**Code:**
```
{ "alps" : {
 "descriptor": [
 {"id": "givenName", "def": "https://schema.org/givenName",
 "title": "Given name. In the U.S., the first name of a Person.",
 "tag": "ontology"},
 {"id": "familyName", "def": "https://schema.org/givenName"
 "title": "Family name. In the U.S., the last name of a Person.",
 "tag": "ontology"},
 {"id": "telephone", "def": "https://schema.org/telephone",
 "title": "The telephone number.",
 "tag": "ontology"
 },
 {"id": "country", "def": "http://microformats.org/wiki/hcard#country-name",
 "title": "Name of the country associated with this person.",
 "tag": "ontology"
 }
 ]
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.3 Sharing Domain Specifics via Published Vocabularies"*
---
### 12. Publish ALPS Semantic Profiles (Recipe 3.4)
`#api` `#architecture`

**Principle:** Publish a machine-readable description of the complete problem space, not one implementation.

**Do:**
- List every property, aggregate object, and action.
- Tag descriptors as ontology, taxonomy, or choreography.
- Type actions as safe, unsafe, or idempotent.
- Use `rt` to identify the returned semantic state.
- Aim for broad reuse by keeping profiles general.
- Advertise the profile URI with every response.
- Host profiles in a central discoverable location.
- Publish a new URI for a breaking profile change.

**Don't:**
- Put concrete URLs, MQTT topics, HTTP methods, or status codes in ALPS.
- Mutate a published profile in place when consumers depend on it.
- Confuse profile description with OpenAPI, AsyncAPI, WSDL, or schema validation.

**Code:**
```
{ "$schema": "https://alps-io.github.io/schemas/alps.json",
 "alps" : {
 "title": "Person Semantic Profile Document",
 "doc": {"value":
 "Simple SPD example for http://webapicookbook.com[Web API Cookbook]."},
 "descriptor": [
 {"id": "href", "def": "https://schema.org/url",
 "tag": "ontology"},
 {"id": "identifier", "def": "https://schema.org/identifier",
 "tag": "ontology"},
 {"id": "givenName", "def": "https://schema.org/givenName",
 "tag": "ontology"},
 {"id": "familyName", "def": "https://schema.org/familyName",
 "tag": "ontology"},
 {"id": "telephone", "def": "https://schema.org/telephone",
 "tag": "ontology"},
 {"id": "Person", "tag": "taxonomy",
 "descriptor": [
 {"href": "#href"},
 {"href": "#identifier"},
 {"href": "#givenName"},
 {"href": "#familyName"},
 {"href": "#telephone"}
 ]
 },
 {"id": "Home", "tag": "taxonomy",
 "descriptor": [
 {"href": "#goList"},
 {"href": "#goHome"}
 ]
 },
 {"id": "List", "tag": "taxonomy",
 "descriptor": [
 {"href": "#Person"},
 {"href": "#goFilter"},
 {"href": "#goItem"},
 {"href": "#doCreate"},
 {"href": "#goList"},
 {"href": "#goHome"}
 ]
 },
 {"id": "Item", "tag": "taxonomy",
 "descriptor": [
 {"href": "#Person"},
 {"href": "#goFilter"},
 {"href": "#goItem"},
 {"href": "#doUpdate"},
 {"href": "#doRemove"},
 {"href": "#goList"},
 {"href": "#goHome"}
 ]
 },
 {"id": "goHome", "type": "safe", "tag": "choreography", "rt": "#Home"},
 {"id": "goList", "type": "safe", "tag": "choreography", "rt": "#List"},
 {"id": "goFilter", "type": "safe", "tag": "choreography", "rt": "#List"},
 {"id": "goItem", "type": "safe", "tag": "choreography", "rt": "#Item"},
 {"id": "doCreate", "type": "unsafe", "tag": "choreography", "rt": "#Item"},
 {"id": "doUpdate", "type": "idempotent", "tag": "choreography",
 "rt": "#Item"},
 {"id": "doRemove", "type": "idempotent", "tag": "choreography",
 "rt": "#Item"}
 ]
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.4 Describing Problem Spaces with Semantic Profiles"*
---
### 13. Embed Hypermedia Controls at Runtime (Recipe 3.5)
`#api` `#architecture`

**Principle:** Put current interaction metadata in each representation so service details can change while clients keep running.

**Do:**
- Include target URL, method, encoding, fields, defaults, constraints, and action identity.
- Let the current caller context determine which controls appear.
- Change service locations by changing returned controls, not client code.
- Adapt multistep workflows by changing controls in responses.
- Support multiple hypermedia formats through content negotiation.
- Pay the one-time cost of implementing a parser for each supported format.

**Don't:**
- Make the client memorize action details from prose.
- Assume only one hypermedia format can be supported.
- Return controls the current caller cannot execute.

**Code:**
```
<html>
 <head>
 <title>Create Person</title>
 <link rel="profile" href="http://api.example.org/profiles/person" />
 <style>
 input {display:block;}
 </style>
 </head>
 <body>
 <h1>Create Person</h1>
 <form name="doCreate" action="http://api.example.org/person/"
 method="post" enctype="application/x-www-form-urlencoded">
 <fieldset>
 <hidden name="identifier" value="q1w2e3r4" />
 <input name="givenName" placeholder="givenName" required/>
 <input name="familyName" placeholder="familyName" required/>
 <input name="telephone" placeholder="telephone" pattern="[0-9]{10}"/>
 <input type="submit" />
 <input type="reset" />
 <input type="button" value="Cancel" />
 </fieldset>
 </form>
 </body>
</html>
```

```
{ "collection" :
 {
 "version" : "1.0",
 "href" : "http://api.example.org/person/",
 "links": [
 {"rel": "self", "href": "http://api.xample.org/person/doCreate"},
 {"rel": "reset", "href":"http://api.example.org/person/doCreate?reset"},
 {"rel": "cancel", "href":"http://api.example.org./person"}
 ],
 "template" : {
 "data" : [
 {"name" : "identifer", "value": "q1w2e3r4"},
 {"name" : "givenName", "value" : "", "required":true},
 {"name" : "familyName", "value" : "", "required":true},
 {"name" : "telephone", "value" : "", "regex":"[0-9]{10}"}
 ]
 }
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.5 Expressing Actions at Runtime with Embedded Hypermedia"*
---
### 14. Use PUT-Create and Conditional Writes (Recipe 3.6)
`#api` `#architecture`

**Principle:** Use idempotent PUT plus entity-tag preconditions for both creation and replacement.

**Do:**
- Create with a client-supplied URL and `If-None-Match: *`.
- Return `201 Created` and a fresh `ETag` for a successful create.
- Replace with `If-Match` set to the representation's current ETag.
- Reject a stale update with a precondition failure.
- Bake correct header handling into `createResource` and `updateResource` helpers.
- Retry PUT when the response is lost.

**Don't:**
- Use POST when a lost response would make retry safety unknowable.
- Update without an entity-tag precondition.
- Generate sequential identifiers when the client can provide a unique ID.

**Code:**
```
**** REQUEST
PUT /person/q1w2e3 HTTP/2.0
Host: api.example.org
Content-Type: application/x-www-form-urlencoded
If-None-Match: *
givenName=Mace&familyName=Morris
**** RESPONSE
HTTP/2.0 201 CREATED
Content-Type: application/vnd.collection+json
ETag: "p0o9i8u7y6t5r4e3w2q1"
...
```

```
**** REQUEST
PUT /person/q1w2e3 HTTP/2.0
Host: api.example.org
Content-Type: application/x-www-form-urlencoded
If-Match: "p0o9i8u7y6t5r4e3w2q1"
givenName=Mace&familyName=Morris
**** RESPONSE
HTTP/2.0 200 OK
Content-Type: application/vnd.collection+json
ETag: "o9i8u7y6t5r4e3w2q1p0"
...
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.6 Designing Consistent Data Writes with Idempotent Actions"*
---
### 15. Transfer State Between Services (Recipe 3.7)
`#api` `#architecture`

**Principle:** Make each service independently composable by transferring state through forms or shared resources.

**Do:**
- Prefer pass-by-value through an existing form for small state.
- Add import/export actions for large or complex state collections.
- Use pass-by-reference through a URL only when both parties share format and vocabulary expectations.
- Keep state transfer stateless and single-step where possible.
- Redirect to authentication rather than requiring a bespoke preliminary session.
- Advertise expected media type and profile for uploaded state.

**Don't:**
- Assume callers are captive to one service workflow.
- Share internal models or databases as the transfer contract.
- Add orchestration steps that the receiving action does not need.

**Code:**
```
<form action="http://api.example.org/shopping/cart"
 method="post" name="cartCreate">
 <input name="cartId" value="q1w2e3r4t5y6u7i8" />
 <input name="cartName" value="Mike's Cart" />
</form>
```

```
<form action="http://api.example.org/users/q1w2e3r4"
 method="post" enctype="multipart/form-data">
 <input type="file" name="userData" accept="application/vnd.collection+json"/>
</form>
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.7 Enabling Interoperability with Inter-Service State Transfers"*
---
### 16. Design Network and Operation Repeatability (Recipe 3.8)
`#api` `#architecture`

**Principle:** Make both the HTTP method and the requested state transition idempotent.

**Do:**
- Use GET, PUT, and DELETE for operations that may need automatic repetition.
- Express replacement state rather than increments.
- Include identifiers, current values, and target values when validators are useful.
- Skip already-applied records safely during a replay.
- Use an idempotency key only when POST cannot be avoided.
- Design repeatability before the first production failure.

**Don't:**
- Assume PUT alone makes a percentage increment repeatable.
- Retry a partial batch whose body says only `updatePercent=.05`.
- Depend on a human to resolve every lost response.

**Code:**
```
**** REQUEST ****
PUT /catalog/priceUpdate
Host: api.example.org
Content-Type:application/x-www-form-urlencoded
Accept: application/vnd.siren+json
....
updatePercent=.05
```

```
**** REQUEST ****
PUT /catalog/priceUpdate
Host: api.example.org
Content-Type:text/csv
Accept: application/vnd.siren+json
....
productId, currentPrice,newPrice
q1w2e3, 100,105
t5y6u7, 200,210
i8o9p0, 250,265
i8y6r4, 50,55
...
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.8 Designing for Repeatable Actions"*
---
### 17. Design Reversible Actions (Recipe 3.9)
`#api` `#architecture`

**Principle:** Preserve enough prior state to reverse writes and expose explicit undo when ordinary replacement cannot restore state.

**Do:**
- Re-PUT previous values with the current ETag for simple rollback.
- Store the prior representation before modification.
- Add an `undoDelete`-style action when HTTP has no inverse method.
- Retain deleted resources for a defined restoration window.
- Return `201 Created` when an undo recreates a resource.
- Give each dependent service its own rollback capability.

**Don't:**
- Roll back over another consumer's intervening update.
- Assume DELETE can be reversed without retained history.
- Hide irreversible side effects inside an apparently reversible action.

**Code:**
```
**** REQUEST ****
DELETE /users/q1w2e3r4
Host: api.example.org
Accept: application/html
If-Match "w/y6t5r4e3w2q1"
**** RESPONSE ****
204 No Content
....
```

```
**** REQUEST ****
PUT /users/rollback?id=q1w2e3r4
Host: api.example.org
Accept: application/html
If-Match "w/y6t5r4e3w2q1"
**** RESPONSE ****
201 Created
Location: /users/q1w2e3r4
....
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.9 Designing for Reversible Actions"*
---
### 18. Extend Messages with NVPs and Parallel Properties (Recipe 3.10)
`#api` `#architecture`

**Principle:** Follow “Don't Change It, Add It” by designing expansion points before extensions are needed.

**Do:**
- Include a name-value-pair collection in the initial model.
- Allow NVP values to be scalar, array, object, or null.
- Add new semantic properties beside old ones.
- Keep the old property populated while consumers migrate.
- Add a stable root wrapper that can host multiple representation versions.
- Accept old and new input forms and translate between them.
- Prefer structured media types that already separate structure from properties.

**Don't:**
- Replace a scalar with an array under the same name.
- Rename or remove an existing property.
- Reorder positional formats casually.
- Assume strict consumer schemas will accept additions.

**Code:**
```
{
 "name": "Merk Muffly",
 "region", "southwest",
 "age": 21,
 "nvp" : [...]
}
```

```
{
 "name": "Merk Muffly",
 "region", "southwest",
 "age": 21,
 "nvp" : [
 {"hatsize" : "3"},
 {"phoneNumbers": ["123-456-7890","980-657-3421"]},
 {"address": {"street":"...","city":"...","state":"...","zip":"..."}}
 ]
}
```

```
{
 "givenName": "Merk",
 "familyName": "Muffly",
 "name": "Merk Muffly",
 "region", "southwest",
 "age": 21,
 "nvp" : [
 {"hatsize" : "3"},
 {"phoneNumbers": ["123-456-7890","980-657-3421"]},
 {"address": {"street":"...","city":"...","state":"...","zip":"..."}}
 ]
}
```

```
{"message" : {
 "personv2": {...},
 "metadata": [...],
 "links": [...],
 "person" : {
 "givenName": "Merk",
 "familyName": "Muffly",
 "name": "Merk Muffly",
 "region", "southwest",
 "age": 21,
 "nvp" : [
 {"hatsize" : "3"},
 {"phoneNumbers": ["123-456-7890","980-657-3421"]},
 {"address": {"street":"...","city":"...","state":"...","zip":"..."}}
 ]
 }
}}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.10 Designing for Extensible Messages"*
---
### 19. Apply the Three Modification Rules (Recipe 3.11)
`#api` `#architecture`

**Principle:** Take nothing away, redefine nothing, and make every addition optional.

**Do:**
- Treat every published URL, method, input, output, and behavior as a promise.
- Add optional fields with documented defaults.
- Add a new action when new inputs must be required.
- Run old and new interfaces concurrently when a breaking fork is unavoidable.
- Run the complete old test suite against the modified interface.
- Assume Hyrum's Law: every observable behavior may have a dependent consumer.
- Preserve old profile semantics when adding vocabulary.

**Don't:**
- Change a query parameter's meaning.
- add a required field to an existing action.
- retire the old fork before consumers control their migration.
- assume documentation alone prevents breakage.

**Code:**
```
<!-- existing search form -->
<form action="..." method="GET" name="findUsers">
 <input name="givenName" value="" required="true" />
 <input name="familyName", value="" required="true" />
 <input type="submit" />
</form>
<!-- updated search form -->
<form action="..." method="GET" name="findUsers">
 <input name="givenName" value="" required="true" />
 <input name="familyName" value="" required="true" />
 <input name="regions" value="all" required="false" />
 <input type="submit" />
</form>
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "3.11 Designing for Modifiable Interfaces"*
---
### 20. Limit Hardcoded URLs (Recipe 4.1)
`#api` `#architecture`

**Principle:** Keep URLs out of client logic and reduce the required starting knowledge to one stable URL.

**Do:**
- Give every remembered URL a semantic variable name.
- Move URL values into replaceable configuration.
- Use RFC 6570 libraries for URI templates.
- Discover all nonentry URLs from response controls.
- Ask nonhypermedia providers for downloadable URL metadata.

**Don't:**
- Scatter literal endpoint strings through application code.
- Treat a configuration file as equivalent to runtime hypermedia.
- Depend on undocumented URL shape.

**Code:**
```
/* find-rel.js */
var startingURL = "http://service.example.org/";
var thisURL = "";
var link = {};
// using named URL variables
const http = new XMLHttpRequest();
// Send a request
http.open("GET", serviceURLs.list);
http.send();
// handle responses
http.onload = function() {
 switch (http.responseURL) {
 case startingURL:
 link = findREL("list");
 if(link.href) {
 thisURL = link.href;
 ...
 }
 ...
 break;
 ...
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.1 Limiting the Use of Hardcoded URLs"*
---
### 21. Keep Clients HTTP-Aware (Recipe 4.2)
`#api` `#architecture`

**Principle:** Preserve direct protocol access even when an SDK offers higher-level helpers.

**Do:**
- Build a thin, reusable HTTP layer for all methods, headers, bodies, and statuses.
- Make network calls and their multiplicity visible to developers.
- Mix provider SDK calls with direct HTTP when needed.
- Let client usage teach service teams which workflows deserve first-class support.
- Keep semantic helpers from hiding expensive sequential or parallel requests.

**Don't:**
- Let an SDK prevent valid protocol operations.
- hide how many HTTP requests one helper makes.
- use a mandatory SDK as an ineffective security control.

**Code:**
```
function getDocument(url) {
 var args = {};
 args.url = url;
 args.callbackFunction = ajaxComplete;
 args.context = "processLinks";
 args.headers = {'accept':'application/vnd.collection+json'}
 ajax.httpGet(args}
 // later ...
function ajaxComplete(response,headers,context,status,msg)
{
 switch(status) {...} // handle status
 switch(context) {...} // dispatch to context
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.2 Coding Clients to Be HTTP Aware"*
---
### 22. Build Message-Centric Clients (Recipe 4.3)
`#api` `#architecture`

**Principle:** Bind client behavior to the response media type rather than hardcoding domain operations.

**Do:**
- Parse requests, responses, controls, and data through media-type modules.
- Render newly returned actions without adding domain-specific client code.
- Separate request processing from domain vocabulary.
- Reuse one client across services that emit the same structured format.
- Prefer HTML, HAL, SIREN, or Collection+JSON over unstructured payloads.

**Don't:**
- Create one client function for every current service operation.
- make a new server action require a client release.
- claim message-centric resilience when the provider emits schema-free plain JSON.

**Code:**
```
/* to-do-messages.js */
var thisPage = function() {
 function init() {}
 function makeRequest(href, context, body) {}
 function processResponse(ajax, context) {}
 function displayResponse() {}
 function renderControls() {}
 function handleClicks() {}
};
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.3 Coding Resilient Clients with Message-Centric Implementations"*
---
### 23. Code Clients to Vocabulary Profiles (Recipe 4.4)
`#api` `#architecture`

**Principle:** Make profile terms the shared domain contract between a generic client and any compliant service.

**Do:**
- Select RDF, OWL, DCAP, ALPS, or another agreed profile format.
- Know action and property identifiers, not implementation endpoints.
- Store the relied-upon profile with client source for reference.
- Derive a local profile from service documentation when the provider publishes none.
- Pair profile awareness with hypermedia responses.

**Don't:**
- Bind a client to the provider's implementation definition when a semantic profile suffices.
- assume identical property spelling implies shared meaning.
- treat profile terms as media-type structural elements.

**Code:**
```
# data to work with
STACK PUSH {"id":"zaxscdvf","body":"testing"}
# vocabulary and format supported
CONFIG SET {"profile":"http://api.examples.org/profiles/todo-alps.json"}
CONFIG SET {"format":"application/vnd.mash+json"}
# write to service
REQUEST WITH-URL http://api.example.org/todo/list WITH-PROFILE WITH-FORMAT
REQUEST WITH-FORM doAdd WITH-STACK
REQUEST WITH-LINK goList
REQUEST WITH-FORM doRemove WITH-STACK
EXIT
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.4 Coding Effective Clients to Understand Vocabulary Profiles"*
---
### 24. Negotiate Profiles at Runtime (Recipe 4.5)
`#api` `#architecture`

**Principle:** Use profile identifiers to confirm semantic compatibility before processing a representation.

**Do:**
- Send the desired profile in `Accept-Profile`.
- Return the applied profile in `Content-Profile`.
- Treat profile links as a collection even when only one is present.
- Return `406 Not Acceptable` with links to supported profiles when appropriate.
- Keep compatible revisions under one profile identity where possible.
- assign a new identity to a breaking profile revision.

**Don't:**
- Version profiles at needless patch-level granularity.
- continue processing a profile mismatch without an explicit policy.
- assume profile negotiation is universally deployed; it remains uncommon.

**Code:**
```
*** REQUEST
GET /todo/list HTTP/1.1
Host: api.example.org
Accept-Profile: <http://profiles.example.org/to-do>
*** RESPONSE
HTTP/2.0 200 OK
Content-Profile: http://profiles/example.org/to-do
...
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.5 Negotiating for Profile Support at Runtime"*
---
### 25. Manage Representation Formats at Runtime (Recipe 4.6)
`#api` `#architecture`

**Principle:** Negotiate formats with HTTP and route each returned representation to a dedicated translator.

**Do:**
- Send `Accept` on every request.
- Validate `Content-Type` before reading the body.
- Stop or safely dump unsupported formats.
- Implement a Message Translator between external formats and internal models.
- Keep one parser per structured media type.
- Translate toward a generic internal or rendering model when possible.

**Don't:**
- Parse a body before confirming its type.
- make the external representation your internal domain model.
- expect resilient generic translation from undocumented plain JSON or XML.

**Code:**
```
function handleResponse(ajax,url) {
 var ctype
 if(ajax.readyState===4) {
 try {
 ctype = ajax.getResponseHeader("content-type").toLowerCase();
 switch(ctype) {
 case "application/vnd.collection+json":
 cj.parse(JSON.parse(ajax.responseText));
 break;
 case "application/vnd.siren+json":
 siren.parse(JSON.parse(ajax.responseText));
 break;
 case "application/vnd.hal+json":
 hal.parse(JSON.parse(ajax.responseText));
 break;
 default:
 dump(ajax.responseText);
 break;
 }
 }
 catch(ex) {
 alert(ex);
 }
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.6 Managing Representation Formats at Runtime"*
---
### 26. Use Schemas as Advisory Metadata (Recipe 4.7)
`#api` `#architecture`

**Principle:** Use schema identifiers to classify incoming messages, but reserve strict schema validation for outgoing bodies.

**Do:**
- Read schema identifiers from headers, media-type parameters, or bodies.
- Use identifiers to select client handlers.
- Keep JSON Schema `additionalProperties` permissive for extensibility.
- Treat unknown properties as inert until explicitly consumed.
- prefer media-type and profile awareness over object-schema awareness.

**Don't:**
- Strictly validate every incoming response against XML or JSON Schema.
- reject useful input because harmless elements were added or reordered.
- confuse a schema identifier with proof that values are safe.

**Code:**
```
*** REQUEST
GET /todo/list HTTP/1.1
Host: api.example.org
Accept-Schema: <urn:example:schema:e-commerce-payment>
*** RESPONSE
HTTP/1.1 200 OK
Schema: <urn:example:schema:e-commerce-payment
...
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.7 Using Schema Documents as a Source of Message Metadata"*
---
### 27. Identify Every Important Response Element (Recipe 4.8)
`#api` `#architecture`

**Principle:** Give every actionable form, link, item, and data block a stable machine-findable identifier.

**Do:**
- Use `id` for document-wide unique identity.
- Use `name` for application-wide semantic identity.
- Use multivalue `rel` for system-wide relationships.
- Use multivalue `tag` or class for solution-specific grouping.
- Decouple internal IDs from public URLs.
- Let clients locate controls without positional assumptions.

**Don't:**
- Make clients depend on array order or visual placement.
- equate a storage key with the permanent resource URL.
- publish anonymous controls that machines cannot select.

**Code:**
```
http://api.example.org/customers/123
http://api.example.org/users?customer=123
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.8 Every Important Element Within a Response Needs an Identifier"*
---
### 28. Rely on the Response's Hypermedia Signature (Recipe 4.9)
`#api` `#architecture`

**Principle:** Program clients to understand the link and control factors of each supported media type.

**Do:**
- Account for embedded, outbound, templated, nonidempotent, and idempotent links.
- Account for controls describing reads, updates, methods, and relations.
- Choose formats with enough H-Factors for expected evolution.
- Read action URLs, methods, encodings, and fields from the control.
- Combine media-type understanding with semantic-profile understanding.

**Don't:**
- Assume all hypermedia formats provide forms.
- describe plain JSON as hypermedia without an added control format.
- hardcode details already present in a returned control.

**Code:**
```
#
# SIREN Edit Session
# read a record, save it, modify it, write it back to the server
#
# ** make initial request
REQUEST WITH-URL http://rwcbook10.herokuapp.com
# ** retreive the first record in the list
REQUEST WITH-PATH $.entities[0].href
# ** push the item properties onto the stack
STACK PUSH WITH-PATH $.properties
# ** modify the tags property value on the stack
STACK SET {"tags":"fishing,\.\skiing,\.\hiking"}
# ** use the supplied edit form and updated stack to send update
REQUEST WITH-FORM taskFormEdit WITH-STACK
# ** confirm the change
SIREN PATH $.entities[0]
# ** exit session
EXIT
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.9 Relying on Hypermedia Controls in the Response"*
---
### 29. Simulate Controls for Nonhypermedia Services (Recipe 4.10)
`#api` `#architecture`

**Principle:** Translate human API documentation into machine-readable local action metadata when the provider emits no links or forms.

**Do:**
- Store action metadata in a separate module or configuration file.
- Include URL, method, target, arguments, defaults, and validation.
- Create separate control sets for distinct security roles.
- Render local controls through the same code used for returned hypermedia.
- update metadata without rewriting the full client.
- Share the translation across consumers.

**Don't:**
- Pretend static local metadata has runtime freshness.
- forget that server changes can invalidate the local map.
- scatter reconstructed actions through domain code.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.10 Supporting Links and Forms for Nonhypermedia Services"*
---
### 30. Honor Rich Input Descriptions (Recipe 4.11)
`#api` `#architecture`

**Principle:** Validate inputs from constraints delivered with the form so rule changes do not require client releases.

**Do:**
- Support core constraints such as readOnly, regex, required, and templated.
- Add min, max, length, placeholder, step, type, and layout hints when useful.
- Support enumerated options and selected values.
- At minimum, implement regular-expression validation for M2M clients.
- Convert prose-only validation rules into machine-readable metadata.

**Don't:**
- Hardcode constraints that the server already sends at runtime.
- require M2M clients to interpret user-interface rendering hints.
- accept values before applying supplied constraints.

**Code:**
```
{
 "_templates" : {
 "default" : {
 ...
 "properties" : [
 {
 "name" : "shipping",
 "type" : "radio",
 "prompt" : "Select Shipping Method",
 "options" : {
 "selectedValues" : ["FedEx"],
 "inline" : [
 {"prompt" : "Federal Express", "value" : "FedEx"},
 {"prompt" : "United Parcel Service", "value" : "UPS"},
 {"prompt" : "DHL Express", "value" : "DHL"}
 ]
 }
 }
 ]
 }
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.11 Validating Data Properties at Runtime"*
---
### 31. Validate Outgoing Messages with Schemas (Recipe 4.12)
`#api` `#architecture`

**Principle:** Make the sender responsible for producing a well-formed and valid request body.

**Do:**
- Check parseable structure first.
- Check field names, types, ranges, and required values second.
- Use JSON Schema for JSON and XSD for XML.
- Convert simple form-urlencoded bodies to JSON only when names are flat.
- Link required schemas from responses and forms.
- Write local validation when provider schemas are absent or unreliable.

**Don't:**
- Send a body and rely on the server to discover avoidable errors.
- force XML and JSON schemas through unreliable cross-format conversion.
- treat dotted form names as flat name/value pairs without checking semantics.

**Code:**
```
/*
 * load the schema file from external source
 * pass in the JSON message to send
 * process and return results/errors
 */
function jsonMessageCheck(schema, message) {
 var schemaCheck = ajv.compile(schema);
 var status = schemaCheck(message);
 return {status:status,errors:schemaCheck.errors};
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.12 Using Document Schemas to Validate Outgoing Messages"*
---
### 32. Validate Incoming Messages with Queries (Recipe 4.13)
`#api` `#architecture`

**Principle:** Inspect protocol, structure, and selected values without demanding exact schema identity.

**Do:**
- Check expected status and critical headers.
- Query for required controls and properties.
- Validate values only after their structural elements exist.
- Use XPath for mature XML querying.
- Use JSONPath cautiously and track specification/tool behavior.
- Generate repetitive validation code where possible.

**Don't:**
- Use strict whole-document schema matching for incoming responses.
- omit protocol-level checks.
- process a value before confirming its type and bounds.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.13 Using Document Queries to Validate Incoming Messages"*
---
### 33. Filter and Semantically Validate Incoming Data (Recipe 4.14)
`#api` `#architecture`

**Principle:** Treat every response as unsafe until an allow-list filter produces a safe internal representation.

**Do:**
- Allow-list fields the client actually understands.
- Apply syntactic type checks and min/max bounds.
- Apply cross-field semantic checks such as start date before stop date.
- Operate only on the filtered copy.
- Update the original full document when acting as a pass-through processor.
- Ignore unknown fields rather than executing or interpreting them.

**Don't:**
- Use deny lists as the main safety boundary.
- scrub fields owned by downstream processors.
- run scripts or operations sourced from unknown properties.

**Code:**
```
// make request, pull body, and scrub
var reponse = httpRequest(url, options);
var message = filterResponse(response.body, filters.taxRules);
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.14 Validating Incoming Data"*
---
### 34. Keep Application State on the Client (Recipe 4.15)
`#api` `#architecture`

**Principle:** Let the client maintain the authoritative transient history of its multiservice interaction.

**Do:**
- Store request URL, method, headers, query, and body.
- Store response URL, status, content type, headers, and body.
- Retain redirects and final response URLs distinctly.
- Use a reusable request/response stack.
- Extract explicit state variables from interaction history.
- Persist state remotely only when the client platform cannot store it locally.

**Don't:**
- Ask one server to know the complete state of a multiservice client.
- store only bodies and discard protocol metadata.
- make a remote state service an unacknowledged availability dependency.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.15 Maintaining Your Own State"*
---
### 35. Give Autonomous Clients Explicit Goals (Recipe 4.16)
`#api` `#architecture`

**Principle:** Define percepts, actions, goals, environment, and escape conditions for client-driven automation.

**Do:**
- Use a Defined Exit Goal for processes that halt at an end state.
- Use a Defined State Goal for continuously maintained ranges.
- Make monitored properties and thresholds configurable.
- Discover available actions from hypermedia controls.
- Verify the current state before acting.
- Set client-controlled loop limits and alert paths.

**Don't:**
- Run a goal loop without an escape condition.
- assume the service knows the client's private objective.
- rely on another service to decide whether the client must stop.

**Code:**
```
// set control values
var roomURL = "http://api.example.org/rooms/13";
var min = 18;
var max = 22;
var wait = (15*60*1000);
// set up periodic checks
setInterval(checkTemp(roomURL,min,max),wait));
// do the check
function checkTemp(roomURL, minTemp, maxTemp) {
 var rtn, temp;
 rtn = "";
 response = httpRequest(roomURL);
 printLine(req)
 if(response.temp<minTemp) {
 rtn = response.form("heat");
 }
 if(response.temp>maxTemp) {
 rtn = response.form("cool");
 }
 if(rtn!=="") {
 response = httpRequest(rtn);
 printLine();
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "4.16 Having a Goal in Mind"*
---
### 36. Publish at Least One Stable URL (Recipe 5.1)
`#api` `#architecture`

**Principle:** Promise one durable entry URL and let every other location remain discoverable and movable.

**Do:**
- Document the stable URL as a long-term promise.
- Return it with `rel="home"` in every possible response.
- Include it in both Link headers and hypermedia bodies when practical.
- Keep the old URL alive with `301 Moved Permanently` after relocation.
- Register a well-known URI only when the governance cost is justified.

**Don't:**
- Promise many stable endpoints without accepting their lifetime cost.
- require clients to revisit home before every valid request.
- break the entry point when moving the underlying service.

**Code:**
```
**** REQUEST
GET / HTTP/1.1
Host: api.example.org
**** RESPONSE
HTTP/1.1 200 OK
Content-Type: application/vnd.collection+json
ETag: "p0o9i8u7y6t5r4e3w2q1"
Link: <http://api.example.org/home>; rel="home"
...
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.1 Publishing at Least One Stable URL"*
---
### 37. Prevent Internal Model Leaks (Recipe 5.2)
`#api` `#architecture`

**Principle:** Design the API as an independent interface rather than a serialization of internal data, objects, or processes.

**Do:**
- Model external properties around consumer work.
- Denormalize the interface when that simplifies consumption.
- Keep data, object, resource, and message models distinct.
- expose domain actions rather than CRUD-shaped internals.
- Allow storage and service models to change behind a stable interface.

**Don't:**
- Generate a public contract directly from ORM or database schema.
- mirror every internal collection as an HTTP resource.
- expose mass-assignment surfaces accidentally.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.2 Preventing Internal Model Leaks"*
---
### 38. Convert Internal Models to External Messages (Recipe 5.3)
`#api` `#architecture`

**Principle:** Treat representation mapping as explicit design work and support multiple negotiated renderings of one semantic state.

**Do:**
- Parse client format preferences before rendering.
- Map internal data into each media type's defined structure.
- Document conversion rules internally.
- Keep internal renames invisible externally.
- Support one rich hypermedia format, one simple format, and HTML when useful.
- Pick Collection+JSON when property sets vary frequently.

**Don't:**
- blindly serialize internal objects.
- publish mapping internals to consumers.
- assume every internal property must appear in every representation.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.3 Converting Internal Models to External Messages"*
---
### 39. Express Internal Functions as External Actions (Recipe 5.4)
`#api` `#architecture`

**Principle:** Design actions around external intent and translate them to one or many internal operations.

**Do:**
- Use published external parameter names.
- Hide dependent calls behind one coherent action when appropriate.
- Translate external enumerations to internal booleans.
- Build declarative mapping functions for internal/external names.
- Collapse fragile internal sequences behind one external form.
- Keep action semantics stable while implementation functions change.

**Don't:**
- expose every internal function one-for-one.
- publish boolean controls that cannot grow beyond two states.
- leak the order of dependent internal operations.

**Code:**
```
function updateAction(identifier, givenName, familyName, email) {
 var user = data.read(identifier);
 if(user) {
 user.id = identifier;
 user.fname = givenName;
 user.lname = familyName;
 user.email = email;
 user = data.write(user);
 }
 return user;
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.4 Expressing Internal Functions as External Actions"*
---
### 40. Advertise Client Response Preferences (Recipe 5.5)
`#api` `#architecture`

**Principle:** Publish current protocol and representation options through a cacheable metadata resource.

**Do:**
- List supported methods, response types, request types, charsets, encodings, languages, and profiles.
- Support OPTIONS and a `rel="meta"` resource.
- Return metadata even when only one value is supported.
- Link the metadata resource from home.
- cache the standalone metadata resource aggressively.
- repeat critical options in headers and body.

**Don't:**
- depend solely on noncacheable OPTIONS at high request volume.
- omit a capability because it has only one possible value.
- force clients to infer current preferences from prose.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.5 Advertising Support for Client Response Preferences"*
---
### 41. Support Proactive and Reactive Content Negotiation (Recipe 5.6)
`#api` `#architecture`

**Principle:** Use proactive negotiation by default and reactive negotiation only when the extra round trip and selection protocol are justified.

**Do:**
- Read client media preferences from `Accept`.
- Return the selected type in `Content-Type`.
- Honor quality values as advice, not absolute commands.
- Return `406 Not Acceptable` when no viable representation exists.
- Advertise supported formats in metadata.
- Use `300 Multiple Choices` with alternate links for reactive negotiation.

**Don't:**
- use RCN for M2M without agreeing on response-selection details.
- assume the server must return the client's top preference.
- create format-specific URL trees unless negotiation cannot serve the use case.

**Code:**
```
**** REQUEST ****
GET /list HTTP/1.1
Accept: application/vnd.hal+json;q=0.8, application/json;q=0.4
...
**** RESPONSE ****
200 OK HTTP/1.1
Content-Type: application/json
....
```

```
**** REQUEST ****
GET /search HTTP/1.1
**** RESPONSE ****
HTTP/1.1 300 Multiple Choices
Link: <http://api.example.org/html/search>;rel="alternate html"
Link: <http://api.example.org/api/search>;rel="alternate api"
Location: http://api.example.org/html/search
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.6 Supporting HTTP Content Negotiation"*
---
### 42. Publish Complete Machine Vocabularies (Recipe 5.7)
`#api` `#architecture`

**Principle:** Document every semantic identifier a message may contain, including data and action names.

**Do:**
- Separate domain values from media-type structural names.
- Explain each identifier and where it appears in each format.
- Include property, relation, form, class, name, and tag semantics.
- Map one profile across all supported representations.
- Use `rel="profile"` to add semantics without changing representation meaning.
- keep the vocabulary complete as optional features grow.

**Don't:**
- call a data dictionary a complete service profile.
- omit action names and link relations.
- intertwine domain terms with XML element or JSON key structure when avoidable.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.7 Publishing Complete Vocabularies for Machine Clients"*
---
### 43. Share Vocabularies in Standard Formats (Recipe 5.8)
`#api` `#architecture`

**Principle:** Serialize shared meaning in a standard profile format and advertise its identifier independently of message format.

**Do:**
- Use RDF formats when data relationships dominate.
- Use ALPS when action and state relationships dominate.
- Use schemas in addition when object validation is needed.
- Link profile URLs from every applicable response.
- map profile elements to media-type elements.
- Include profiles in service documentation and metadata.

**Don't:**
- treat RDF, schema, ALPS, and OpenAPI as interchangeable.
- require dereferencing a profile just to compare its identifier.
- omit choreography from an interaction-oriented vocabulary.

**Code:**
```
**** REQUEST ****
GET /shopping/ HTTP/1.1
Host: api.example.org
Accept: application/vnd.collection+json
**** RESPONSE ****
HTTP/1.1 200 OK
Content-Type: application/vnd.collection+json
Link: <http://docs.alps.io/shopping-v2.json>; rel="profile"
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.8 Supporting Shared Vocabularies in Standard Formats"*
---
### 44. Publish Service Definition Documents (Recipe 5.9)
`#api` `#architecture`

**Principle:** Publish implementation-level interface definitions separately from semantic profiles.

**Do:**
- Choose a definition format matching HTTP CRUD, events, RPC, data query, messaging, or hypermedia style.
- Return `rel="service-desc"` in headers and bodies.
- Include SDD links in service metadata and OPTIONS.
- Publish multiple definitions when one service supports multiple styles.
- Use the Link `type` parameter to identify expected document format.
- Keep the document easy to find near the service root.

**Don't:**
- ask semantic profiles to carry concrete endpoint definitions.
- hide the SDD only in a developer portal.
- assume one interface style implies one universal definition format.

**Code:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.hal+json
Link: <http://api.example.org/service-desc>; rel=service-desc
...
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.9 Publishing Service Definition Documents"*
---
### 45. Publish API Metadata (Recipe 5.10)
`#api` `#architecture`

**Principle:** Make operational, documentary, security, ownership, and tooling metadata discoverable in an APIs.json resource.

**Do:**
- Publish `/apis.json` with `application/apis+json` when using the format.
- Link it with `rel="service-meta"`.
- Include human URL, base URL, documentation, definitions, contacts, tools, specifications, and maintainers.
- Use extensible property types for local needs.
- Link metadata from home and normal responses.
- Keep metadata separate from the API definition itself.

**Don't:**
- treat APIs.json as an OpenAPI replacement.
- let contact, security, policy, or status links drift out of date.
- require manual discovery of the metadata location.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.10 Publishing API Metadata"*
---
### 46. Expose Cacheable Health Resources (Recipe 5.11)
`#api` `#architecture`

**Principle:** Report interface health in `application/health+json` and protect the endpoint with caching.

**Do:**
- Publish a `/health`-style resource.
- Report pass, fail, or warn plus public version and release identity.
- Report downstream checks only at an appropriate authorization level.
- Return `Cache-Control` and `ETag`.
- Advertise with `rel="health-check"` in OPTIONS and service metadata.
- Customize detail by caller context.
- Keep health reporting focused on the interface.

**Don't:**
- turn health output into a public debugger.
- implement callback subscriptions that scale with every consumer.
- let health polling become a denial-of-service vector.

**Code:**
```
HTTP/1.1 200 OK
Content-Type: application/health+json
Cache-Control: max-age=3600
ETag: "w\i8u7y6t5r4e3w2"
...
{
 "status": "pass",
 "version": "1",
 "releaseId": "1.2.2",
 "notes": [""],
 "output": "",
 "serviceId": "f03e522f-1f44-4062-9b55-9587f91c9c41",
 "description": "health of authz service",
 "checks": {
 "cassandra:responseTime": [
 {
 "componentId": "dfd6cf2b-1b6e-4412-a0b8-f6f7797a60d2",
 "componentType": "datastore",
 "observedValue": 250,
 "observedUnit": "ms",
 "status": "pass",
 "affectedEndpoints" : [
 "/users/{userId}",
 "/customers/{customerId}/status",
 "/shopping/{anything}"
 ],
 "time": "2018-01-17T03:36:48Z",
 "output": ""
 }
 ],
 ...
 }
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.11 Supporting Service Health Monitoring"*
---
### 47. Standardize Errors with RFC 7807 (Recipe 5.12)
`#api` `#architecture`

**Principle:** Treat errors as recognized alternate representations and use Problem Details when a bare status is insufficient.

**Do:**
- Return `application/problem+json` or `application/problem+xml`.
- Include `type`, `title`, numeric `status`, occurrence-specific `detail`, and optional `instance`.
- Point `type` to documentation for the problem semantics.
- Document every extension property at the type URI.
- Keep reusable type/title/status stable across occurrences.
- Add `Retry-After` when recovery is time-based.
- Use a media type's built-in error object when it already provides one.

**Don't:**
- wrap every obvious 4xx or 5xx in a problem document.
- expose stack traces, storage details, or debugging internals.
- invent many narrowly reusable problem types.

**Code:**
```
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json
Content-Language: en
{
 "type": "https://example.com/probs/out-of-credit",
 "title": "You do not have enough credit.",
 "detail": "Your current balance is 30, but that costs 50.",
 "instance": "/account/12345/msgs/abc",
 "status": 403,
 "balance": 30,
 "accounts": ["/account/12345", "/account/67890"]
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.12 Standardizing Error Reporting"*
---
### 48. Self-Register with a Runtime Service Registry (Recipe 5.13)
`#api` `#architecture`

**Principle:** Make service discovery a runtime find-and-bind process based on current instances and capabilities.

**Do:**
- Register every instance or cluster at startup.
- Supply service URL, name, profiles, media types, definitions, and searchable tags.
- Send periodic liveness and optional usage reports.
- Unregister on controlled shutdown.
- Let the registry expire entries that miss the ping window.
- Register distinct locations and versions as distinct entries.
- Use registries to resolve dependent services dynamically.

**Don't:**
- expose registry lifecycle actions as the public business API.
- assume graceful shutdown always happens.
- register metadata too sparse for capability search.

**Code:**
```
var srsResponse = null;
var srsRegister({Url:"...","name":"...", .....});
// register this service w/ defaults
discovery.register(srsRegister, function(data, response) {
 srsResponse = JSON.parse(data);
 initiateKeepAlive(srsResponse.href, srsResponse.milliseconds);
 http.createServer(uuidGenerator).listen(port);
 console.info('uuid-generator running on port '+port+'.');
});
```

```
// set up proper discovery shutdown
process.on('SIGTERM', function () {
 discovery.unregister(null, function(response) {
 try {
 uuidGenerator.close(function() {
 console.log('gracefully shutting down');
 process.exit(0);
 });
 } catch(e){}
 });
 setTimeout(function() {
 console.error('forcefully shutting down');
 process.exit(1);
 }, 10000);
});
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.13 Improving Service Discoverability with a Runtime Service Registry"*
---
### 49. Use Client-Supplied Identifiers (Recipe 5.14)
`#api` `#architecture`

**Principle:** Let clients create globally unique IDs before service calls to remove sequencing and enable parallel work.

**Do:**
- Generate UUIDs or suitable random/time-based identifiers client-side.
- Validate identifier syntax and uniqueness server-side.
- Return `409 Conflict` for an unacceptable collision.
- Include the ID in the PUT target URL.
- Provide identifier-generation libraries to consumers.
- Use friendly display IDs separately when human readability matters.
- Precompute related IDs to parallelize independent writes.

**Don't:**
- assume every random-number generator is sufficiently collision-resistant.
- make downstream work wait for server-generated IDs unnecessarily.
- expose predictable sequences when they add no value.

**Code:**
```
var cId = makeId();
var aId = makeId();
var sId = makeId();
Promise.all([
 writeCustomer(cId),
 writeAccount(cId,aId),
 writeSalesRecord(cId,aId,sId)
])
.then(() => console.log('All done!'))
.catch(function(err) {
 rollbackAll(cId,aId,sId);
 console.log('Write failed!');
});
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.14 Increasing Throughput with Client-Supplied Identifiers"*
---
### 50. Improve Reliability with Idempotent Create (Recipe 5.15)
`#api` `#architecture`

**Principle:** Eliminate the lost-response ambiguity by requiring client-addressed conditional PUT for creation.

**Do:**
- Require a complete client-supplied resource URL.
- Send `If-None-Match: *` for creation.
- Send `If-Match` with the current ETag for updates.
- return `201 Created` and `Location` when creation succeeds.
- reject an occupied create target with conflict information.
- Return a new ETag after replacement.
- Repeat a lost PUT confidently.

**Don't:**
- repeat an ambiguous POST transfer automatically.
- accept an unconditioned state-changing request.
- call a POST convention protocol-level idempotence.

**Code:**
```
**** REQUEST ****
GET /persons/q1w2e3r4
Accept: text/plain
**** RESPONSE ****
200 OK
Content-Type: application/vnd.collection+json
ETag: "w/p0o9i8u7y6yt5r4"
{"collection": {
 "items": [
 {"href" : "/persons/q1w2e3r4", "data" : [ {"name" : "Mark Morkleson"} ]}
 ],
 "template" : { "data" : [ {"name" : "Mork Markleson"} ] }
}}
**** REQUEST ****
PUT /persons/q1w2e3r4
If-Match: "w/p0o9i8u7y6yt5r4"
Content-Type: application/x-www-form-urlencoded
Accept: application/vnd.collection+json
name=Mork%20Markleson
**** RESPONSE ****
200 OK
Content-Type: application/vnd.collection+json
ETag: "w/i8u7y6t5r4e3"
{"collection": {
 "items": [
 {"href" : "/persons/q1w2e3r4", "data" : [ {"name" : "Mork Markleson"} ]}
 ]
}}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.15 Improving Reliability with Idempotent Create"*
---
### 51. Implement the Dependency Fallback Chain (Recipe 5.16)
`#api` `#architecture`

**Principle:** Assume every dependency fails and progress through retry, static fallback, dynamic fallback, queued replay, then explicit failure.

**Do:**
- Distinguish read and write mitigation requirements.
- Retry only idempotent requests after bounded waits.
- Try a configured alternate service when state transfer permits.
- Query a runtime registry for a capability-compatible replacement.
- Queue work and return `202 Accepted` when delayed completion is part of the contract.
- Give up with a useful 5xx response and recovery timing.
- Apply mitigation to 408, 500, 502, 503, and 504 selectively.
- Keep mitigation logic local to avoid a new fatal dependency.

**Don't:**
- retry POST or PATCH automatically.
- hammer a dependency fast enough to resemble a denial-of-service attack.
- hide a possible 202 response from interface documentation.
- implement retries, fallback, or queuing as another required remote service.

**Code:**
```
var reqParams = {} // request params
reqParams.host = "https:/api.example.com"
reqParams.url = "/users/q1w2e3";
reqParams.body = "mork=mamund&name=Mike Morkelsen";
reqParams.method = "PUT";
reqParams.waitMS = 300;
reqParams.retryAttempts = 3;
reqParams.successFunction = requestSucceeded;
reqParams.failFunction = requestFailed;
reqParams.queuingFunction = queueRequest;
reqParams.alternateHost = "https://alternate-api.example.com";
httpLib.request(reqParams);
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.16 Providing Runtime Fallbacks for Dependent Services"*
---
### 52. Wrap Noncompliant Services with Semantic Proxies (Recipe 5.17)
`#api` `#architecture`

**Principle:** Put a compliant interface around irreplaceable legacy or third-party functionality, but treat the proxy as a costly new service.

**Do:**
- Use an enterprise-level proxy for an algorithmically related service family.
- Use a custom one-off proxy for one narrow integration.
- Use a semantic profile proxy for format or vocabulary normalization.
- Design the desired external API before coding translation.
- Publish the proxy's profile and service definition.
- Implement all external actions through the underlying service.
- Reserve proxies for traffic that tolerates added latency.
- Plan to maintain translation knowledge for its full lifetime.

**Don't:**
- assume semantic translation is easier than protocol translation.
- use a proxy in a low-latency, high-volume hot path without evidence.
- expose the underlying noncompliant contract through the wrapper.
- build an enterprise proxy without long-term resources.

**Code:**
```
// HTTP upload external action
function httpUpload(file) {
 var uploader = new httpService();
 var file = uploader.read();
 return file;
}
// FTP client service
function ftpUpload(file) {
 var client = new ftpService();
 var results = client.put(file);
 return results;
}
// proxy function for file uploads
function proxyUpload(file) {
 var results = null;;
 var file = httpUpload(file);
 if(file) {
 results = ftpUpload(file)
 }
 return results;
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "5.17 Using Semantic Proxies to Access Noncompliant Services"*
---
### 53. Hide Data Storage Internals (Recipe 6.1)
`#api` `#architecture`

**Principle:** Expose business capabilities and consumer vocabulary, never storage connections, schemas, or native query syntax.

**Do:**
- Model `updateCustomer` and `findUnpaidInvoices`, not database commands.
- Use named links and forms for common queries.
- Keep storage and query technology replaceable behind the interface.
- Make required query parameters optional with defaults when possible.

**Don't:**
- Expose SQL credentials, statements, tables, GraphQL internals, or storage relationships.
- turn an application API into an accidental database engine.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.1 Hiding Your Data Storage Internals"*
---
### 54. Make Every Data Change Idempotent (Recipe 6.2)
`#api` `#architecture`

**Principle:** Require conditional PUT and entity tags for every create, update, and delete path.

**Do:**
- Create with PUT plus `If-None-Match: *`.
- Update and delete with `If-Match` plus the latest ETag.
- Return ETags for every representation and every successful change.
- Refetch after a lost-update precondition failure before recomputing the change.
- Treat a representation's ETag as format-specific.

**Don't:**
- accept an unconditioned state-changing request.
- use POST or PATCH when reliable automatic repetition is required.
- overwrite a concurrent update after receiving stale-state evidence.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.2 Making All Changes Idempotent"*
---
### 55. Hide Data Relationships Behind Flat Actions (Recipe 6.3)
`#api` `#architecture`

**Principle:** Accept a flat external property set and split it into internal related writes behind the interface.

**Do:**
- Collect parent and child properties in one request when M2M payload size allows.
- Add follow-up controls such as “add another address.”
- Use WIP for long human-centric related-data collection.
- Log the complete submitted message for rollback.
- Keep entity-group hints optional and nonbinding.

**Don't:**
- expose foreign keys, joins, or storage collection boundaries as the contract.
- let clients depend on temporary grouping hints.

**Code:**
```
var message = http.request.body.toJSON();
var person = personFilter(message);
var adddress = addressFilter(message);
address.person_id = person.id;
Promise.all([writePerson(person), writeAddress(address)]).then(...);
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.3 Hiding Data Relationships for External Actions"*
---
### 56. Use Contains-and-AND HTTP Queries (Recipe 6.4)
`#api` `#architecture`

**Principle:** Implement the simplest useful IRQL with name/value pairs, contains semantics, and `&` conjunction.

**Do:**
- Interpret `name=value` as “field contains value” when that fits the domain.
- Interpret multiple pairs as AND conditions.
- Ignore empty form fields safely.
- Use GET forms, Collection+JSON queries, or URI templates to publish queries.
- Document case sensitivity and repeated names.

**Don't:**
- smuggle raw SQL or another storage query into `?query=`.
- invent operators before the simple model proves insufficient.
- expose query strings that leak storage or invite injection.

**Code:**
```
<form method="GET" action="http://api.example.org/persons/" rel="search">
 <input name="ID" value="e3" />
 <input name="NAME" value="" />
 <input name="CITY" value="Mo" />
 <input type="submit" />
</form>
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.4 Leveraging HTTP URLs to Support 'Contains' and 'AND' Queries"*
---
### 57. Return Query Metadata (Recipe 6.5)
`#api` `#architecture`

**Principle:** Return enough metadata for consumers to assess result quality, cost, truncation, and replay options.

**Do:**
- Consider `q-status`, `q-sent`, `q-returned`, `q-count`, `q-seconds`, and `q-datetime`.
- Add `q-score`, `q-suggest`, and `q-location` when useful.
- Put a few values in headers or body; link a dedicated resource for many.
- Mark truncation and cancellation explicitly.
- Balance consumer utility against information leakage.

**Don't:**
- expose `q-executed`, `q-source`, debugging, or internal performance data casually.
- return a result collection with no indication of limits or quality.

**Code:**
```
{"collection": {
 "title": "Person",
 "metadata" : [
 {"name": "q-sent", "value": "?id=q1"},
 {"name": "q-datetime", "value": "2024-12-12:00:12:0012TZ"},
 {"name": "q-status", "value": "result set too large, query canceled"},
 {"name": "q-seconds", "value": "120"},
 {"name": "q-count", "value": "10000+"},
 {"name": "q-suggest",
 "value": "reduce return set with additional query parameters"},
 ]
 ...
}}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.5 Returning Metadata for Query Responses"*
---
### 58. Distinguish 200, 404, 400, and 5xx for Queries (Recipe 6.6)
`#api` `#architecture`

**Principle:** Base status on request and resource semantics, not on whether rows happened to match.

**Do:**
- Return `200 OK` plus an empty collection for a valid collection query.
- Return `404 Not Found` for a requested single resource that does not exist.
- Return `400 Bad Request` for invalid query fields or syntax.
- Return an appropriate 5xx when the service cannot fulfill a valid request.
- Normalize a downstream 404-empty-collection response to your own 200 contract.

**Don't:**
- call “zero matches” a client error.
- leak downstream storage behavior through status codes.

**Code:**
```
**** REQUEST ****
GET /persons/?status=pending HTTP/1.1
Host: api.example.org
Accept: application/vnd.collection+json
...
**** RESPONSE ***
HTTP/1.1 200 OK
Content-Type: application/vnd.collection+json
...
{"collection": {
 "title": "Persons",
 "metadata": [
 "name": "q-status", "value": "success",
 "name": "q-sent", "value": "?status=pending",
 "name": "q-count", "value": "0"
 ],
 "items": []
}}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.6 Returning HTTP 200 Versus HTTP 400 for Data-Centric Queries"*
---
### 59. Carry Query Languages as Media Types (Recipe 6.7)
`#api` `#architecture`

**Principle:** Encapsulate established query languages in request media types so the interface can negotiate and translate them independently of storage.

**Do:**
- Use `application/sql` for SQL query bodies.
- Use documented personal types for Solr, OData, or GraphQL until registered types exist.
- Create a query resource with conditional PUT.
- Keep query and result resources separate.
- Translate the stable interface query to the current backend engine.
- Add new query languages without removing old ones.

**Don't:**
- invent a proprietary query language without resources to maintain it.
- bind the public HTTP method to the backend engine's method.
- equate query language with storage technology.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.7 Using Media Types for Data Queries"*
---
### 60. Preserve Unknown Fields (Recipe 6.8)
`#api` `#architecture`

**Principle:** Ignore fields you do not understand, but preserve and return the complete record when updating or forwarding it.

**Do:**
- Apply the Must Ignore rule to added properties.
- Modify only fields within the service's responsibility.
- Return the complete original record with local changes applied.
- Forward the source ETag in `If-Match`.
- Keep working when upstream adds unrelated fields.

**Don't:**
- strip unknown fields before writing a record back.
- process unknown fields merely because they were accepted.
- use partial replacement that can violate cross-field integrity.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.8 Ignoring Unknown Data Fields"*
---
### 61. Use Cache-Control, ETag, and Vary (Recipe 6.9)
`#api` `#architecture`

**Principle:** Mark every response with freshness and validation metadata, then require consumers to honor it.

**Do:**
- Set public/private scope and a volatility-appropriate `max-age`.
- Add `must-revalidate` and ETag for conditional requests.
- Permit `stale-if-error` or `max-stale` for suitable read paths.
- Use `immutable` for truly long-lived content.
- Use `no-cache` sparingly when the latest representation is required for editing.
- Set `Vary` for authorization, language, type, or other representation selectors.

**Don't:**
- replay one caller's cached representation to an incompatible context.
- give shopping-cart data the lifetime of a static country list.
- use cache busting for every read.

**Code:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.siren+json
Content-Length: NN
ETag: "w/p0o9i8u7y6t5"
Date: Tue, 15 Apr 2022 11:12:13 GMT
Cache-Control: public, max-age=300, must-revalidate, stale-if-error
...
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.9 Improving Performance with Caching Directives"*
---
### 62. Evolve Data with a Two-Tier Model (Recipe 6.10)
`#api` `#architecture`

**Principle:** Combine explicit typed fields with an implicit NVP collection to support forward and backward model evolution.

**Do:**
- Keep stable, common fields explicit.
- Put newly introduced fields in `nvp` first.
- Allow NVP values to hold number, string, boolean, object, array, or null.
- Use one access function that searches both tiers.
- Promote an implicit field to explicit without changing caller access.
- retain implicit values when rolling back a release.
- Validate unknown names and values before storage.

**Don't:**
- expose the storage model directly as the API representation.
- depend on every consumer schema allowing extra explicit properties.
- discard newly collected data during model rollback.

**Code:**
```
{
 "givenName": "John",
 "familyName": "Doe",
 "age": 23,
 "nvp" : [
 {"name" : "middleName", "value" : "Seymore"}
 ]
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.10 Modifying Data Models in Production"*
---
### 63. Extend Remote Stores by Association (Recipe 6.11)
`#api` `#architecture`

**Principle:** Store local extension properties separately and connect them to remote resources with a URL association.

**Do:**
- Use the remote resource URL as an associative key.
- Keep local property names distinct from remote names.
- Fall back to an appropriate cached remote representation when unavailable.
- Treat 404 as possibly temporary and 410 as permanent.
- retain or clean broken local associations according to history needs.

**Don't:**
- enforce cross-store invariants you cannot control atomically.
- copy remote values locally as if they remain authoritative.
- delete local history immediately after a transient remote failure.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.11 Extending Remote Data Stores"*
---
### 64. Limit Large Responses (Recipe 6.12)
`#api` `#architecture`

**Principle:** Enforce a documented default maximum on every query and report when results are limited.

**Do:**
- Push `$top`, `first`, `TOP`, `LIMIT`, or `rows` into the backend query.
- Insert a default when the client omits a limit.
- clamp negative or excessive client limits.
- Truncate in the interface only when the backend cannot limit.
- Return `q-status=truncated`, returned count, and estimated total.
- Keep query limits separate from page size.

**Don't:**
- issue an unbounded backend query.
- assume truncating after fetching protects backend latency or memory.
- hide a modified query limit from the caller.

**Code:**
```
function executeQuery(dataStoreAddress, dataQuery) {
 var ix=0;
 var maxLimit=100;
 var responseCollection = [];
 var dataCollection = httpRequest(dataStoreAddress, dataQuery);
 for (let item of dataCollection) {
 if(ix>maxLimit) {
 break;
 } else {
 responseCollection.push(item);
 }
 ix++;
 });
 return responseCollection;
}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.12 Limiting Large-Scale Responses"*
---
### 65. Preserve Integrity Through Pass-Through Proxies (Recipe 6.13)
`#api` `#architecture`

**Principle:** Let a proxy expose a subset while retaining the complete downstream response and all concurrency metadata.

**Do:**
- Store the full source response, including ETag and headers.
- Translate source fields into proxy vocabulary.
- Merge upstream edits into the retained complete record.
- Forward the source ETag when writing downstream.
- Return the relevant failure without revealing hidden source internals.
- report `502 Bad Gateway` when the source violates the proxy's promised shape.

**Don't:**
- tell callers whether the service is a source or pass-through implementation.
- lose the mapping between upstream and downstream IDs and URLs.
- overwrite a downstream record with only the exposed subset.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "6.13 Using Pass-Through Proxies for Data Exchange"*
---
### 66. Require a Composable Workflow Interface (Recipe 7.1)
`#api` `#architecture`

**Principle:** Give every task Execute, Repeat, Revert, and Cancel semantics, and give every job Continue, Restart, and Cancel semantics.

**Do:**
- Make every action a fully described form.
- Treat Repeat as idempotent and Revert as safe even before Execute.
- Cancel a failed job by reverting all completed tasks.
- Share `correlation-id` for the job and `request-id` for each task.
- Support maxTTL for tasks and jobs.
- expose no-op forms when a required semantic has no local work.

**Don't:**
- enlist a write service that cannot repeat or revert safely.
- make a task know the complete job.
- use a shared database as the workflow contract.

**Code:**
```
*** Checkout Job
***
READ sharedState WITH urlState
EXECUTE shoppingCartService->checkOutForm WITH sharedSTATE
IF-NOT-OK EXIT
EXECUTE salesTaxService->applyTaxesForm WITH sharedSTATE
IF-NOT-OK EXECUTE shoppingCartService->revertCheckoutForm WITH sharedSTATE
STORE sharedState WITH urlState
EXIT
***
*** End Job
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.1 Designing Workflow-Compliant Services" / "Hypermedia workflow"*
---
### 67. Share Workflow State as a Resource (Recipe 7.2)
`#api` `#architecture`

**Principle:** Put job properties in one independently addressable HTTP document that tasks can read and conditionally update.

**Do:**
- Use the job ID in the shared-state URL.
- Pass the URL in headers or response links.
- Prime the document before starting the job.
- Use replacement values such as current and updated price.
- PUT the state after each completed unit of work.
- archive state after completion.
- Map state properties into service forms rather than sharing data models.

**Don't:**
- confuse shared state with the progress resource.
- reduce shared state to an undocumented serialized blob.
- encode nonidempotent instructions such as percentage increments.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.2 Supporting Shared State for Workflows"*
---
### 68. Use Code for Small Stable Workflows (Recipe 7.3)
`#api` `#architecture`

**Principle:** Hide a simple, rarely changing workflow behind a stable API and implement its service calls in local code.

**Do:**
- Run independent calls in parallel.
- expose delayed execution with 202 and progress controls.
- Keep the external interface stable as enlisted services change.
- Split sequential phases into separate workflow elements.

**Don't:**
- use source code for a large family of frequently customized workflows.
- omit rollback handling for partial success.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.3 Describing Workflow as Code"*
---
### 69. Use a DSL for Repeated Workflow Authoring (Recipe 7.4)
`#api` `#architecture`

**Principle:** Adopt a constrained workflow DSL when source-code implementations no longer scale across many flows.

**Do:**
- Put URLs and other variables in configuration.
- Make HTTP, form selection, shared-state mapping, and errors first-class DSL operations.
- Use constrained syntax to reduce unsafe possibilities.
- use shell tools only when their additional power is worth the defect risk.

**Don't:**
- force every workflow author to rebuild HTTP plumbing.
- mistake unrestricted shell power for safer workflow design.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.4 Describing Workflow as DSL"*
---
### 70. Prefer Declarative Workflow Documents (Recipe 7.5)
`#api` `#architecture`

**Principle:** Describe tasks, job metadata, shared state, progress, time limits, and controls as resources, not imperative programs.

**Do:**
- Include job and task IDs, statuses, timestamps, maxTTL, and action URLs.
- Keep editor and execution engine independently evolvable.
- submit documents as HTTP resources or queue messages.
- Let task services own branching and local decisions.

**Don't:**
- put `if/then/else`, variables, or step-by-step execution in the document.
- use document workflow for noncompliant services without an adapter strategy.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.5 Describing Workflow as Documents"*
---
### 71. Standardize RESTful Job Control (Recipe 7.6)
`#api` `#architecture`

**Principle:** Use a common job-control vocabulary to author, run, monitor, continue, restart, cancel, and archive workflow documents.

**Do:**
- Require every job's tasks to be parallelizable.
- Split fixed sequences into separate jobs.
- Support task start, rerun, rollback, and cancel URLs.
- Support job continue, restart, success, failure, and cancel URLs.
- Manage jobs with list, filter, read, create, update, and remove.
- monitor task and job maxTTL.

**Don't:**
- build a general JCL before composable services exist.
- roll your own when one platform's workflow tooling fully meets the requirement.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.6 Supporting RESTful Job Control Language"*
---
### 72. Expose a Progress Resource (Recipe 7.7)
`#api` `#architecture`

**Principle:** Give every job a separate, cacheable progress resource containing minimal job and task execution metadata.

**Do:**
- Track IDs, URLs, descriptions, statuses, timestamps, and maxTTL.
- Include a refresh link and caching guidance.
- Record task messages without exposing private data.
- archive progress after completion.
- authorize detailed views carefully.

**Don't:**
- turn progress into a trace log or debugger.
- expose request bodies, internal code, or secrets casually.
- mix workflow-management actions into a read-only progress view.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.7 Exposing a Progress Resource for Your Workflows"*
---
### 73. Return All Related Actions Indirectly (Recipe 7.8)
`#api` `#architecture`

**Principle:** Keep common controls inline and put the complete current transition set behind a `related` resource.

**Do:**
- Include `rel="related"` where action sets are large.
- Build the related set from service, resource, client, and identity context.
- cache or use `text/uri-list` when suitable.
- Teach clients to search inline first, then related.

**Don't:**
- inflate every response with every possible form.
- hide every useful action behind an extra request.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.8 Returning All Related Actions"*
---
### 74. Return Most Recently Used Links (Recipe 7.9)
`#api` `#architecture`

**Principle:** Add a short, context-filtered MRU link list to reduce navigation cost without returning all actions.

**Do:**
- Track a FIFO of roughly three to five URLs.
- Filter MRUs for current validity and authorization.
- return simple links, not full forms.
- provide a standalone MRU resource when needed.
- allow preference controls for enabling or sizing MRUs.

**Don't:**
- store headers or infer intent in the MRU record.
- put a long MRU collection in response headers.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.9 Returning Most Recently Used Resources"*
---
### 75. Model Stateful Work in Progress (Recipe 7.10)
`#api` `#architecture`

**Principle:** Collect large, long-lived, multi-party input into a persistent WIP document before final submission.

**Do:**
- Support list, filter, create, read, update, cancel, share, and submit actions.
- accept any useful partial combination during update.
- Use submit as the final completeness and validation boundary.
- assign and filter WIPs with metadata such as owner, due date, and status.
- archive completed and abandoned WIPs.

**Don't:**
- create intricate cross-field dependencies during incremental collection.
- confuse WIP with short-lived partial form submit.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.10 Supporting Stateful Work in Progress"*
---
### 76. Navigate Lists with Standard Relations (Recipe 7.11)
`#api` `#architecture`

**Principle:** Publish list, first, previous, next, last, select, exit, and home controls according to the current page state.

**Do:**
- Omit previous on the first page and next on the last.
- Use opaque navigation URLs.
- provide select links from summary items to details.
- Make page size configurable with a safe default, often around 50.
- compute later pages lazily when list generation is costly.
- Use exit for cleanup or confirmation when abandoning costly state.

**Don't:**
- promise arbitrary page-number jumps when the list is dynamic or expensive.
- return full resources when summaries and select links suffice.
- confuse page size with the overall query limit.

**Code:**
```
{"collection" : {
 "title" : "Customer List",
 "links" : [
 {"rel" : "self list collection", "href" : "/customers/list"},
 {"rel" : "home", "href" : "/customers/"},
 {"rel" : "first", "href" : "/customers/list/q1w2"},
 {"rel" : "next", "href" : "/customers/list/t5y6"},
 {"rel" : "exit", "href" : "/customers/p0o9"}
 ],
 "items" : [
 ...
 ]
}}
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.11 Enabling Standard List Navigation"*
---
### 77. Support Partial Form Submit (Recipe 7.12)
`#api` `#architecture`

**Principle:** Separate “save these inputs” from “process this completed form” so machines can validate and recover one field at a time.

**Do:**
- Offer partialSubmit, resetSubmit, refreshSubmit, cancelSubmit, and finalSubmit.
- Validate and store each partial submission.
- return the updated form with accepted values filled in.
- run dependent and final validation at finalSubmit.
- allow already submitted values to be corrected.

**Don't:**
- require all fields before accepting any progress.
- make dependent validation so complex that an automated client cannot recover.

**Code:**
```
GET /users/filter?type=customer&submit=partialSubmit
GET /users/filter/?salesRep=Mork&submit=partialSubmit
GET /users/filter/?submit=finalSubmit
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.12 Supporting Partial Form Submit"*
---
### 78. Enable Client-Driven Workflow with State-Watch (Recipe 7.13)
`#api` `#architecture`

**Principle:** Let each client select a small set of watchable values and receive those values in subsequent representations.

**Do:**
- Publish a watchable-element list.
- Create a client-specific selected-watch resource.
- let the client supply the selected resource's unique ID.
- Return watch-list and watch-selected links with responses.
- support clear, create, update, list, and selected actions.
- Use the selected resource rather than long repeated query strings.

**Don't:**
- assume the service knows the client's private goal.
- share one selected-watch resource across clients.
- use an unsafe body query when an addressable watch resource is practical.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.13 Using State-Watch to Enable Client-Driven Workflow"*
---
### 79. Store and Replay Queries as Resources (Recipe 7.14)
`#api` `#architecture`

**Principle:** Put a complex query in a resource body, then execute or replay it through a cacheable GET URL.

**Do:**
- Create queries with client-addressed conditional PUT.
- separate execution URLs from management URLs clearly.
- store query text, cache metadata, description, owner, tags, and timestamps.
- support list, filter, update, remove, and optional share.
- return query metadata with results.
- return 410 after an intentionally temporary query resource expires.

**Don't:**
- put huge queries in URLs.
- rely on POST when replay caching is valuable.
- let share semantics obscure who may edit the source query.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.14 Optimizing Queries with Stored Replays"*
---
### 80. Return 202 for Incomplete Work (Recipe 7.15)
`#api` `#architecture`

**Principle:** Acknowledge long work immediately with a delayed-response resource the client can refresh, complete, fail, or cancel.

**Do:**
- Return `202 Accepted` before or after work begins.
- Include identifier, accepted/completed/failed URLs, description, status, refresh, percentage, and timestamps.
- Provide self, completed, failed, cancel, and home controls as applicable.
- document every operation that may return 202.
- keep completed delayed-response documents for an audit period.
- use maxTTL and cancellation for bounded work.

**Don't:**
- surprise a client with an undocumented 202 path.
- put rapidly changing progress fields in headers.
- claim cancel support when state changes cannot be reversed.

**Code:**
```
**** REQUEST
PUT /services/compute-results HTTP/1.1
Content-Type: application/vnd.collection+json
...
{"collection": {...}}
**** RESPONSE
202 Accepted HTTP/1.1
Content-Type: application/vnd.collection+json
Link: <http://api.example.org/services/compute-results/q1w2e3>;rel=self;
 refresh=60000
Link: <http://api.example.org/services/cancel-form/q1w2e3>;rel=cancel
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.15 Synchronous Reply for Incomplete Work with 202 Accepted"*
---
### 81. Retry with Bounded Exponential Backoff (Recipe 7.16)
`#api` `#architecture`

**Principle:** Retry only retryable idempotent failures, prefer exponential backoff, and stop after a small configured bound.

**Do:**
- Classify connection failures and selected 5xx responses as retry candidates.
- avoid retrying unchanged 4xx requests.
- Prefer waits of 2, 4, then 16 seconds and no more than three retries.
- Consider incremental, regular, immediate, or randomized strategies only when context warrants.
- Add randomization when synchronized callers could overload recovery.
- record attempts as warnings and the terminal failure as an error.
- cap task and job duration to contain compounded delays.

**Don't:**
- retry POST, PATCH, or operation-level increments automatically.
- expose internal retry configuration publicly.
- retry aggressively enough to trigger abuse defenses.

**Code:**
```
<!-- For EBO methods -->
<retries>
 <method>EBO<method>
 <starting-value-seconds>2</starting-value-seconds>
 <max-retries>3</max-retries>
</retries>
```

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.16 Short-Term Fixes with Automatic Retries"*
---
### 82. Support Local Undo or Delayed Rollback (Recipe 7.17)
`#api` `#architecture`

**Principle:** Expose direct undo when previous state is safely restorable; otherwise delay the write so cancellation prevents commitment.

**Do:**
- Log an undoable action under a context ID before execution.
- authorize undo with the same rights as its underlying inverse.
- set a short validity window for direct rollback.
- queue risky multi-service writes for a bounded cancellation window.
- return 202 when the delay should be explicit.

**Don't:**
- undo an old operation after dependent state may have changed.
- add fixed delays to latency-sensitive workflows without calculating compounding cost.
- claim local undo reverses an entire multiservice job.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.17 Supporting Local Undo or Rollback"*
---
### 83. Call for Human Help (Recipe 7.18)
`#api` `#architecture`

**Principle:** Escalate unrecoverable workflow failures with enough bounded context for a person to continue, restart, or cancel safely.

**Do:**
- Include or link the workflow description, progress, shared state, and error report.
- Put a responsible contact in the job document.
- send email, SMS, voice, or incident-platform alerts as appropriate.
- Record each escalation as an incident for recurring-problem analysis.
- protect private and proprietary data in incident material.

**Don't:**
- leave an unrecoverable workflow silently paused.
- publish traces, credentials, or personal data in the alert.
- build a new incident platform when an existing one can accept the report.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.18 Calling for Help"*
---
### 84. Scale Workflows with Queues and Clusters (Recipe 7.19)
`#api` `#architecture`

**Principle:** Add durable queues for admission and machine clusters for processing without changing the public interface.

**Do:**
- Acknowledge queued jobs with 202.
- persist self-describing workflow documents before processing.
- add processors when queued work approaches maxTTL.
- cluster workers behind one interface address.
- keep shared state independently addressable.
- require tasks to run safely in parallel.

**Don't:**
- expose queue or cluster topology as public API semantics.
- rely on machine-local folders when clustered workers require a shared queue.
- let queued work exceed TTL without cancellation or escalation.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.19 Scaling Workflow with Queues and Clusters"*
---
### 85. Proxy Only Safe Workflow Tasks (Recipe 7.20)
`#api` `#architecture`

**Principle:** Use a workflow proxy only when replacement is impossible, and prefer read-only or compute-only target services.

**Do:**
- Add shared-state read/write and correlation/request identifiers in the proxy.
- Map Execute to the target service.
- implement Repeat idempotently.
- remove proxy-produced shared state during Revert.
- use the proxy as a migration bridge when you own the target.
- replace the target with a compliant service when feasible.

**Don't:**
- proxy an unknown state-changing service whose side effects cannot be reversed.
- assume deleting one created resource reverses hidden dependent work.
- ignore the extra availability and latency failure point.

*Ref: Restful Web API Patterns and Practices Cookbook.md — "7.20 Using Workflow Proxies to Enlist Noncompliant Services"*
---
## Anti-Patterns & Common Mistakes

- **Four layers collapsed into one schema:** Protocol, representation, vocabulary, and actions cannot evolve independently. → *Fix:* define and publish each layer separately.
- **Plain JSON called a durable type:** Adding fields changes the object structure clients bind to. → *Fix:* use a structured media type and profile.
- **Private magic strings:** Consumers need undocumented tribal knowledge. → *Fix:* publish a complete vocabulary with authoritative definitions.
- **ALPS used as OpenAPI:** Problem semantics become tied to one deployment. → *Fix:* keep implementation details in an SDD.
- **URLs baked into clients:** Relocation becomes a client release. → *Fix:* memorize one home URL and follow controls.
- **POST used for critical writes:** A lost response makes repetition ambiguous. → *Fix:* conditional PUT-Create.
- **Increment bodies:** A retried partial batch compounds changes. → *Fix:* send current and replacement values.
- **No undo history:** DELETE and complex updates cannot be reversed. → *Fix:* retain prior state and publish rollback actions.
- **Breaking rename disguised as cleanup:** Existing consumers lose a promised property. → *Fix:* add the new property in parallel.
- **Required field added in place:** Old clients cannot submit the old form. → *Fix:* optional default or a new action.
- **Strict incoming schema validation:** Benign additions produce false negatives. → *Fix:* query for required structure and values.
- **Unknown fields stripped:** Round-trip updates corrupt records. → *Fix:* ignore locally but preserve globally.
- **Health endpoint without caching:** Monitoring becomes self-inflicted load. → *Fix:* return Cache-Control and ETag.
- **Problem Details as a debugger:** Internal data escapes the interface boundary. → *Fix:* report only actionable interface semantics.
- **Fallback service as dependency:** Recovery fails with the same network. → *Fix:* keep mitigation local.
- **Raw database query in URL:** Security, length, coupling, and encoding fail together. → *Fix:* named forms or query media types.
- **Empty collection returned as 404:** A valid query is mislabeled as failure. → *Fix:* 200 plus empty items and query metadata.
- **Unbounded query:** Growth eventually consumes service resources. → *Fix:* enforce a default maximum in every backend query.
- **Query limit confused with page size:** Collection scope and navigation behavior become inconsistent. → *Fix:* govern them separately.
- **Progress resource used as trace log:** Secrets and internals become public. → *Fix:* expose minimal status metadata only.
- **Retries on nonidempotent work:** Recovery duplicates side effects. → *Fix:* idempotent method plus idempotent operation.
- **Workflow proxy around unknown writes:** Revert is unprovable. → *Fix:* proxy read-only work or replace the service.

## Decision Heuristics / Checklists

### Interface Design Checklist
- [ ] Is HTTP behavior separate from representation format?
- [ ] Is representation structure separate from domain vocabulary?
- [ ] Are actions discoverable as links or forms?
- [ ] Is at least one registered structured media type supported?
- [ ] Is HTML useful as a testable baseline representation?
- [ ] Is every magic string in a published vocabulary?
- [ ] Does an ALPS profile cover ontology, taxonomy, and choreography?
- [ ] Does the API promise one stable home URL?
- [ ] Are internal models translated rather than serialized?
- [ ] Can additions remain optional and ignorable?

### Write Safety Checklist
- [ ] Does create use client-supplied ID, PUT, and `If-None-Match: *`?
- [ ] Does update use PUT and the current `If-Match` ETag?
- [ ] Does delete require `If-Match`?
- [ ] Is the body a replacement operation rather than an increment?
- [ ] Can the exact request be repeated after a lost response?
- [ ] Is prior state retained long enough for rollback?
- [ ] Is every successful representation returned with a new ETag?
- [ ] Does a stale precondition trigger refetch and recomputation?

### Client Resilience Checklist
- [ ] Does the client know only the entry URL?
- [ ] Does it send Accept and validate Content-Type?
- [ ] Does it parse by media type before reading domain values?
- [ ] Does it understand the expected profile?
- [ ] Does it locate controls by ID, name, rel, or tag?
- [ ] Does it strictly validate outgoing messages?
- [ ] Does it query-check required incoming elements without whole-schema rejection?
- [ ] Does it allow-list and semantically validate consumed values?
- [ ] Does it retain complete request/response history and its own transient state?
- [ ] Does every autonomous goal have a client-controlled escape?

### Service Operations Checklist
- [ ] Are preferences available through a cacheable meta resource?
- [ ] Are profile, service-desc, service-meta, and health links advertised?
- [ ] Is content negotiation proactive by default?
- [ ] Are health responses `application/health+json`, cacheable, and authorization-aware?
- [ ] Are detailed errors represented with RFC 7807 only when useful?
- [ ] Does every service instance register, ping, and unregister?
- [ ] Is dependency recovery ordered retry → static fallback → dynamic fallback → queue → give up?
- [ ] Are retry, fallback, and queue mechanisms local?
- [ ] Are proxies excluded from latency-sensitive paths unless measured?

### Data and Query Checklist
- [ ] Does the API hide storage technology and relationships?
- [ ] Do simple HTTP queries use contains and AND semantics?
- [ ] Does every query return relevant metadata?
- [ ] Does an empty valid collection query return 200?
- [ ] Are complex query languages carried as media types?
- [ ] Are unknown fields preserved on round trips?
- [ ] Does every response include caching metadata?
- [ ] Is `Vary` correct for negotiated or authorized representations?
- [ ] Does the store support explicit fields plus extensible NVPs?
- [ ] Is every query bounded before reaching storage?
- [ ] Are query limits and page sizes independent?

### Workflow Checklist
- [ ] Does every task support Execute, Repeat, Revert, and Cancel semantics?
- [ ] Does every job support Continue, Restart, and Cancel?
- [ ] Are job and task IDs propagated consistently?
- [ ] Is state an HTTP resource rather than a shared model?
- [ ] Is progress a separate minimal resource?
- [ ] Are task and job maxTTL values enforced?
- [ ] Are sequential phases split into separate jobs?
- [ ] Is long work represented by 202 plus refresh/status controls?
- [ ] Are retries idempotent, bounded, and backed off?
- [ ] Can unrecoverable failures call for human help?
- [ ] Are queues and clusters hidden behind the interface?
- [ ] Are workflow proxies limited to safely repeatable and reversible work?

## Key Takeaways

1. Separate protocol, format, vocabulary, and actions.
2. Bind clients to HTTP, registered media types, and semantic profiles—not endpoint trees.
3. Publish links and forms as the runtime engine of application state.
4. Make every write conditionally idempotent with PUT and entity tags.
5. Make operations repeatable, reversible, extensible, and nonbreaking by design.
6. Take nothing away, redefine nothing, and make additions optional.
7. Publish vocabulary, ALPS, service definitions, API metadata, health, and errors as distinct artifacts.
8. Hide internal service, storage, query, and relationship models.
9. Return query metadata, correct 200/4xx/5xx semantics, caching directives, and bounded results.
10. Preserve unknown fields while consuming only allow-listed values.
11. Coordinate workflows through documents, shared-state resources, progress resources, and composable actions.
12. Model long work with 202, bounded retries, rollback, escalation, queues, and clusters.
13. Introduce proxies only as carefully bounded translation or migration tools.
14. Make the smallest change that teaches the most, then repeat.
15. Design for people you have never met, uses you have not imagined, and timescales measured in decades.

## Cross-References
- Related: [[../Mastering_Api_Architecture.md]]
- Topic index: [[../INDEX.md]]
