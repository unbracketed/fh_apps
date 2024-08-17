# FastHTML tips, patterns and references

## View Special Parameters

There are a number of special parameter names, which will be passed useful information about the request:

`request`: the Starlette request (`starlette.requests.Request`); 

`auth`: the value of `scope['auth']`;

`htmx`: the HTMX headers, if any; (`HtmxHeaders`) 

`app`: the FastHTML app object.


You can also pass any string prefix of `request` or `session`.
Fasthtml injects stuff into your functions params based on param name and type. an untyped param called req or request will receive the starlette Request object, which fasthtml adds a hdrs attr to

## Using `@patch` for adding a Python `@property` to Dataclasses

```python
Event = events.dataclass()
@patch(as_prop=True)
def name(self: Event) -> str:
    return self.title if not self.artist else f"{self.title}: {self.artist}"
```

## Explicitly Adding Routes

Use the `app.get` and `app.post` methods for registering view functions with routes.  This will use the internal 
`RouteX` which adds the FastHTML handling for parameter mapping on the input and wrapping the output based on request type.

```python
app.get("/")(homeview)
app.get("/calendar")(calendar)
app.get("/events")(compact_list)
app.post("/events/add-event")(add_event_handler)
```

Use `uri` to map a named route to its path:

```python
uri("homeview")
uri("calendar")
uri("edit-event", event_id=event.id)
```

Named routes can be passed to components as `get`/`post` arguments to specify the `hx_get` / `hx_post` values:

```python
Button(get="homeview")
Button(post=uri("add_event_handler", event_id=event.id))
```
---

To render raw HTML / unescaped output, use `NotStr` or `Safe`

---

Specify the condition for indicating the selected option to the `value` parameter for `Option`:

```python
Select(
    *[Option(x[0], value=x[1]) for x in RARITIES],
    id="rarity",
),
```

---

## Live Reloading

To enable live reloading in FastHTML, you can use the `--reload` flag when running your application:
`uvicorn app:app --reload`

or 

`fast_app(live=True)`

---

## Named Route Mapping with HTMX verbs and targeting

1. The new verb/target parameters (`get`, `post`, `put`, `patch`) expect an encoded named route string, which you can get by calling uri(route_name, **kwargs)
2. `uri` creates an encoded named route string which FH uses to map to a url path; in practice one probably doesn't need to deal with these strings directly, but you can use `decode_uri` to split into route name and arguments
3. If you need to, you can use `request.url_for(route_name, **kwargs)` to get a formatted path for the route.  An example might be adding this to a `<form action=...>`