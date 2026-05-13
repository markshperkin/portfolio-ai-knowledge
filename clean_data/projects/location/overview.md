# Location App — Overview

## What It Is

A simple **Android application** that detects the user's current location and displays it on a map using the **Google Maps API**. Built in **Kotlin** as part of my Android development coursework at USC.

GitHub: https://github.com/markshperkin/location

## What It Does

Three core capabilities:

- **Location detection** — automatically identifies the user's current location using device GPS
- **Map visualization** — displays the detected location via Google Maps API integration
- **User interface** — simple navigation and interaction design

That's it. No frills, no extra features. Just a working location-aware Android app demonstrating the GPS + Maps integration that's foundational for so many Android apps.

## Why I Built It

This was a coursework project for an Android development class at USC. The point was to learn:
- How to request runtime permissions (location is a sensitive permission)
- How to use Android's location services to get GPS coordinates
- How to integrate Google Maps API into an Android app
- Standard Android UI patterns (Activities, Fragments, Maps Fragment)

These are foundational skills for any Android developer who deals with location-based features — ride-sharing apps, fitness trackers, maps apps, food delivery, etc. Half of consumer mobile apps need to know where the user is.

## Tech Stack

- **Language**: Kotlin (100%)
- **Platform**: Android
- **External API**: Google Maps API
- **Build**: Gradle (standard Android build system)

## Key Dependencies

- **Google Maps API key** — required, must be added to `manifest.kt`
- Standard Android location services (`FusedLocationProviderClient`)

## What I Learned

### Permissions Are Their Own Skill
Android's runtime permission system requires:
1. Declaring the permission in the manifest
2. Checking if the permission is already granted
3. Requesting it from the user if not
4. Handling the user's response asynchronously
5. Gracefully degrading if the user denies

This is more code than the actual feature. But it's how Android works, and any non-trivial app deals with this constantly.

### Async Location Updates
Location isn't a synchronous "get coordinates" call. It's a stream:
- Request location updates
- Receive callbacks when location changes
- Stop updates when no longer needed (battery!)

Getting this lifecycle right matters for both correctness and battery life.

### API Keys Need Care
The Google Maps API key has to live in the manifest but shouldn't be checked into source control if you're paying for usage. The standard pattern is to use a local properties file referenced from the manifest, with the actual key never hitting git.

## My Role

Sole author. Built the entire app from a starter template provided by my Android development course.

## Keywords

Android, Kotlin, Google Maps, location services, GPS, FusedLocationProviderClient, runtime permissions, mobile development, USC coursework, manifest configuration, Maps API, Android app, mobile UI, location-aware apps
