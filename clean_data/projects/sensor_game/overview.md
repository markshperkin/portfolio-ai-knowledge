# Sensor Game Application — Overview

## What It Is

An **Android game** that uses the device's **orientation sensors** as the primary control mechanism. Players tilt their phone to move a small circle onto a target larger circle. Built in **Java** as part of Android development coursework at USC.

GitHub: https://github.com/markshperkin/Sensor-Game-Application

## What It Does

The objective is simple: **place a small circle on a larger circle by tilting the device.**

That's it as a game. But what's interesting is the implementation — the device's pitch and roll sensors translate physical tilt into in-game motion. Tilt left, the small circle moves left. Tilt forward, the circle moves up. The phone becomes a controller.

## Key Features

- **Sensor-based gameplay** — leverages device orientation sensors for real-time input
- **Tilt controls** — players manipulate device pitch and roll to move game elements
- **Simple objective** — place small circle on target

## Why This Is Interesting

Sensor input is one of mobile's unique strengths over desktop or web. A game that uses tilt feels native to mobile in a way a touch-based game doesn't.

This project taught me:
- Reading from device sensors via `SensorManager`
- Coordinate translation (sensor frame → game frame)
- Real-time game loops on Android
- Handling sensor lifecycle (subscribe in `onResume`, unsubscribe in `onPause`)

These are foundational skills for AR apps, fitness apps, navigation apps, gaming, and anything else that uses physical device motion.

## Tech Stack

- **Language**: Java (100%)
- **Platform**: Android
- **Build system**: Gradle (with cross-platform wrapper scripts)
- **Sensors**: Android `SensorManager` + `Sensor.TYPE_ORIENTATION` (or accelerometer + magnetometer fused)

## My Specific Contribution

The project builds on a **Robert Bailey starter application** that provided basic sensor orientation display. I extended it by:

- Adding a complete game loop (small circle, target circle, win condition)
- Implementing the tilt-to-position mapping
- Handling game state (active, won, restart)
- Drawing the game elements on a canvas

Working from a starter is realistic — most real engineering involves building on existing code, not greenfield. The skill is figuring out the seams where new features fit and not breaking what's already there.

## My Role

Sole author of my extensions. The starter app provided sensor reading; the game itself is my work.

## Keywords

sensor game, Android, Java, orientation sensors, tilt control, accelerometer, magnetometer, SensorManager, motion-based gameplay, mobile game, custom game loop, USC coursework, Robert Bailey starter, sensor lifecycle, real-time input, custom View drawing
