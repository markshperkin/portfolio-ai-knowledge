# MiniPaint — Implementation Notes

## The Custom View

A drawing app revolves around a **custom `View` subclass** that:
- Listens for touch events
- Maintains a list of completed paths and the in-progress path
- Renders everything on each `onDraw()` call

```kotlin
class DrawingView(context: Context, attrs: AttributeSet?) : View(context, attrs) {
    private val paths = mutableListOf<Pair<Path, Paint>>()
    private var currentPath: Path? = null
    private var currentPaint: Paint = createDefaultPaint()
    
    // ... onTouchEvent and onDraw
}
```

That's the core. Everything else is filling in the details.

## Touch Event Handling

`onTouchEvent` is where drawing happens. The pattern:

```kotlin
override fun onTouchEvent(event: MotionEvent): Boolean {
    when (event.action) {
        MotionEvent.ACTION_DOWN -> {
            currentPath = Path()
            currentPath?.moveTo(event.x, event.y)
        }
        MotionEvent.ACTION_MOVE -> {
            currentPath?.lineTo(event.x, event.y)
            invalidate()  // trigger redraw
        }
        MotionEvent.ACTION_UP -> {
            currentPath?.let {
                paths.add(it to Paint(currentPaint))
            }
            currentPath = null
        }
    }
    return true
}
```

Key details:
- `ACTION_DOWN` starts a new path at the touch point
- `ACTION_MOVE` extends the path as the finger moves
- `ACTION_UP` finalizes the path and stores it
- `invalidate()` triggers a redraw so the user sees their stroke as they draw

## The Render Loop

```kotlin
override fun onDraw(canvas: Canvas) {
    super.onDraw(canvas)
    
    // Background
    canvas.drawColor(backgroundColor)
    
    // All completed paths
    for ((path, paint) in paths) {
        canvas.drawPath(path, paint)
    }
    
    // In-progress path (if user is currently drawing)
    currentPath?.let {
        canvas.drawPath(it, currentPaint)
    }
}
```

Every `invalidate()` call triggers `onDraw`, which re-renders everything. For a paint app this is fine — there aren't enough strokes to cause performance issues.

## Brush Customization

Color and size both modify the `currentPaint` object:

### Color Change
```kotlin
fun setBrushColor(color: Int) {
    currentPaint.color = color
}
```

### Size Change
```kotlin
fun setBrushSize(width: Float) {
    currentPaint.strokeWidth = width
}
```

The important detail: when a stroke is finalized, we **copy** the paint with `Paint(currentPaint)`. This snapshots the current settings so future changes don't affect already-drawn strokes.

Without that copy, all strokes would always render with the current brush settings — meaning if you change color mid-painting, all your previous strokes would change too.

## Undo Functionality

Implementation:

```kotlin
fun undo() {
    if (paths.isNotEmpty()) {
        paths.removeAt(paths.lastIndex)
        invalidate()
    }
}
```

That's it. Pop the last path, re-render. Because `onDraw` reconstructs everything from `paths`, the previous state is automatically what you see.

This is **functional programming in disguise** — application state is a sequence of operations, and rendering is a deterministic function of that state. Add or remove operations, re-render, done.

You could extend this with:
- **Redo** — keep a separate stack of undone operations
- **Clear all** — empty the paths list
- **Save state** — serialize the paths to disk

All of these become trivial because the state model is clean.

## Background Color

Two ways to handle:

1. **Set view background**: simplest. The `View` itself has a background color, drawn before `onDraw` runs.
2. **Draw background in `onDraw`**: more control. Lets you change without affecting the underlying View.

Either works. The README implies a configurable background, so the second approach is likely what's used.

## Common Gotchas

### Path Doesn't Render Without invalidate()
The first time I built a drawing app, paths drew correctly but only updated when something else triggered a redraw. Forgot `invalidate()`. Hours of confusion.

### Forgetting to Copy Paint
The first time I tried to support multi-color drawings, all strokes inherited the current color. Took a while to realize I was holding a reference, not a copy.

### Stylus vs. Finger
Different input devices report touch slightly differently. Pressure sensitivity, hover events, etc. For a basic paint app, you don't need to differentiate. For a serious drawing app, you do.

### Performance on Long Drawings
Storing every path forever is fine until you have thousands. Then `onDraw` gets slow. Production paint apps cache rendered bitmaps periodically and only redraw recent strokes on top.

## Lessons Learned

### State Model Determines Capability
Once I had the "list of paths" state model, undo was trivial. If I'd built it as a stateful bitmap that strokes wrote into, undo would have been hard or impossible.

### Custom Views Are Powerful
Android's view system is flexible. Custom `View` subclasses can do anything from drawings to charts to games. Learning to build them well opens up a lot of possibilities.

### Coordinate Spaces Matter
Touch coordinates are in view coordinates. If you have transforms (zoom, pan, rotate), you have to invert them. For a flat canvas this is trivial, but it scales up to be a real concern.

### `invalidate()` Is the Mental Model
"State changed → call `invalidate()` → render reflects new state" is the pattern that makes Android UI work. Internalize it once and lots of things make sense.

## What I'd Add If I Continued

- **Redo** — companion to undo
- **Multiple brush types** — pen, marker, spray paint, etc.
- **Layers** — overlay multiple drawing planes
- **Save and load** — persist drawings across sessions
- **Vector export** — output as SVG instead of bitmap
- **Pressure sensitivity** — for stylus users

## Connection to Other Projects

The custom-view + state-model + redraw pattern from MiniPaint shows up directly in:
- Sensor-Game-Application (custom view rendering game state)
- Anything I'd build with custom drawing or visualization

It's a pattern that compounds.

## Keywords

custom View, onTouchEvent, onDraw, Canvas drawing, Path, Paint, MotionEvent, ACTION_DOWN ACTION_MOVE ACTION_UP, invalidate, drawing state, undo implementation, brush color, stroke width, paint copy, render loop, application state model, Android graphics, custom drawing
