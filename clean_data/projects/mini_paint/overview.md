# MiniPaint — Overview

## What It Is

An **Android painting app** built in Kotlin. Users can paint on a canvas with customizable brush colors and sizes, change the canvas background, and undo their last drawing action. Built as an extension to a starter app from my Android development course at USC.

GitHub: https://github.com/markshperkin/MiniPaint

## What It Does

Core features:

- **Painting canvas** — users draw with finger or stylus on a custom canvas
- **Brush customization** — change the **color** and **size** of the brush for painting
- **Canvas background** — change the **background color** of the canvas
- **Undo capability** — undo the **last drawing action** for correction

It's intentionally minimal — a learning project demonstrating Android's `Canvas` and `Path` drawing APIs, not a competitor to Procreate.

## Why I Built It

This was a coursework project for an Android development class at USC. The point was to learn:
- Custom `View` implementation
- `Canvas` and `Path` drawing APIs
- Touch event handling (`onTouchEvent`)
- State management (drawing history, current brush settings)
- Basic Android UI for color/size pickers

These fundamentals matter for any Android app that does custom drawing — games, charts, visualizations, photo editors, signature capture, etc.

## Tech Stack

- **Language**: Kotlin (100%)
- **Platform**: Android
- **Build system**: Gradle (with wrapper scripts)
- **APIs**: Android `Canvas`, `Path`, `Paint`

## What I Built

The starter app (from Professor's course material, by Robert Bailey) provided basic canvas drawing. My extensions added:

### Brush Color Customization
A color picker UI letting the user select from preset colors or pick a custom color. The brush's `Paint` object updates accordingly.

### Brush Size Customization
A size slider/picker that adjusts the stroke width. The `Paint`'s `strokeWidth` property updates with the user's choice.

### Background Customization
The canvas itself can be filled with a chosen color, replacing the default white. This required clearing existing strokes (or layering them on top of the new background).

### Undo Functionality
The trickiest feature. To support undo, every drawing operation has to be recorded:
- Maintain a list of `Path` objects with their associated `Paint` settings
- On each touch sequence, append a new `(Path, Paint)` entry
- Undo pops the most recent entry from the list and re-renders the canvas

The re-rendering is the key insight. The canvas isn't a stateful bitmap — it's a sequence of operations. Re-running all but the last operation gives you the undo state.

## Why This Is a Useful Learning Project

Custom canvas drawing teaches:

### Coordinate Systems
Touch events come in screen coordinates, but the canvas might have its own. Understanding the math of mapping touch → canvas → drawn output is foundational graphics work.

### State vs. Rendering
A drawing app illustrates the difference between **application state** (the list of strokes) and **rendered state** (what's currently shown). The canvas can always be re-rendered from the application state. This pattern shows up everywhere in software.

### Performance
Drawing a complex Path on every `onDraw()` is fine for short sessions. For really long drawing histories, you'd need to cache rendered bitmaps periodically. This isn't an issue at coursework scale but is worth understanding.

## Attribution

The README explicitly credits **Professor's Starter App by Robert Bailey** as the foundation. My extensions added the painting features described above.

## My Role

Sole author of the extensions. Worked from the starter code provided in my Android course.

## Keywords

MiniPaint, Android, Kotlin, paint app, drawing app, custom canvas, Canvas API, Path, Paint, brush customization, color picker, brush size, undo, drawing history, custom View, onTouchEvent, USC Android coursework, Robert Bailey starter app
