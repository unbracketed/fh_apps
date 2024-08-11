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

Use the `app.add_route` method for registering view functions with routes.  This will use the internal 
`RouteX` which adds the FastHTML handling for parameter mapping on the input and wrapping the output based on request type.

```python
app.add_route("/", events_views.homeview)
app.add_route("/calendar", events_views.calendar)
app.add_route("/events", events_views.compact_list)
app.add_route("/events/add-event", events_views.add_event_form)
```

