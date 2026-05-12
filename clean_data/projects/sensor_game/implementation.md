# Sensor Game — Implementation Notes

## Sensor Reading

Android's `SensorManager` is the entry point for sensor data. The pattern:

### Setup
```java
private SensorManager sensorManager;
private Sensor orientationSensor;
private SensorEventListener listener;

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
    orientationSensor = sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION);
    listener = new SensorEventListener() {
        @Override
        public void onSensorChanged(SensorEvent event) {
            float pitch = event.values[1];  // device tilt forward/back
            float roll = event.values[2];   // device tilt left/right
            updateBallPosition(pitch, roll);
        }
        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {}
    };
}
```

### Lifecycle
```java
@Override
protected void onResume() {
    super.onResume();
    sensorManager.registerListener(listener, orientationSensor, SensorManager.SENSOR_DELAY_GAME);
}

@Override
protected void onPause() {
    super.onPause();
    sensorManager.unregisterListener(listener);
}
```

### Why The Lifecycle Matters
Sensor listeners are tied to `Activity` lifecycle. Forget to unregister in `onPause`, and the sensor keeps draining battery even when the app is backgrounded. This is one of those Android conventions that's easy to forget but matters a lot for app quality.

## TYPE_ORIENTATION vs. Accelerometer + Magnetometer

`Sensor.TYPE_ORIENTATION` is technically deprecated. The modern approach is:
- Read raw accelerometer and magnetometer
- Use `SensorManager.getRotationMatrix()` to fuse them
- Use `SensorManager.getOrientation()` to get pitch/roll/azimuth

But for a coursework project, `TYPE_ORIENTATION` works and is simpler. Just be aware that production apps should use the fused approach.

## Mapping Sensor Values to Game Coordinates

The crux of the game is translating tilt to position:

```java
private void updateBallPosition(float pitch, float roll) {
    // Pitch ranges from -90 to +90 (degrees, forward/back tilt)
    // Roll ranges from -180 to +180 (left/right tilt)
    
    // Sensitivity factor: how much movement per degree of tilt
    float sensitivity = 5.0f;
    
    // Update ball position
    ballX += roll * sensitivity * deltaTime;
    ballY += pitch * sensitivity * deltaTime;
    
    // Clamp to game area
    ballX = clamp(ballX, 0, gameWidth);
    ballY = clamp(ballY, 0, gameHeight);
    
    invalidate();  // trigger redraw
}
```

Key choices:
- **Sensitivity** controls how fast the ball moves for a given tilt — too sensitive and the game is unplayable; too sluggish and it's frustrating
- **Direction signs** matter — does tilting forward move the ball up or down? Whatever feels intuitive
- **Clamping** keeps the ball inside the play area
- **Time-step (`deltaTime`)** ensures movement is consistent regardless of sensor update rate

## The Game Loop

A simple game loop runs the dynamics:

1. Receive sensor update
2. Update ball position based on tilt
3. Check win condition (does the ball overlap the target?)
4. Trigger view redraw

This isn't a fixed-rate loop — Android's sensor subsystem drives updates whenever new data arrives. For a slow game, this is fine.

## Win Condition

```java
private void checkWin() {
    float distance = Math.sqrt(
        Math.pow(ballX - targetX, 2) + 
        Math.pow(ballY - targetY, 2)
    );
    if (distance < (ballRadius + targetRadius)) {
        gameWon = true;
        showWinDialog();
    }
}
```

Standard 2D circle overlap check. Two circles overlap if the distance between their centers is less than the sum of their radii.

## Drawing the Game

A custom `View` renders the ball, target, and any UI elements:

```java
@Override
protected void onDraw(Canvas canvas) {
    super.onDraw(canvas);
    
    // Background
    canvas.drawColor(Color.WHITE);
    
    // Target circle (larger, drawn first so ball is on top)
    targetPaint.setColor(Color.RED);
    canvas.drawCircle(targetX, targetY, targetRadius, targetPaint);
    
    // Ball (smaller)
    ballPaint.setColor(Color.BLUE);
    canvas.drawCircle(ballX, ballY, ballRadius, ballPaint);
}
```

Same pattern as the MiniPaint project — custom View + onDraw + invalidate. Android's view system is consistent like that.

## Handling Different Devices

A subtle issue: not all devices report sensor values consistently. Some report orientation in different ranges, axes might be swapped depending on physical orientation, etc.

Real production apps handle:
- Portrait vs. landscape orientation differences
- Sensor coordinate frames (device frame vs. world frame)
- Calibration issues (some devices have noisy sensors)

For a coursework project, you can assume a "default" portrait orientation and ignore these.

## Lessons Learned

### Sensor Lifecycle Discipline
Always unregister listeners. Battery drain from leaked listeners is one of the most common Android mistakes.

### Sensitivity Tuning Is User Experience
Pure correctness ("the ball moves 1 pixel per degree of tilt") often produces a bad game. Tuning the sensitivity until it feels right is the difference between a fun game and a frustrating one.

### Game Loops Don't Have to Be Complex
For sensor-driven games, the sensor itself is the timing source. You don't need a separate game loop with `Handler.postDelayed` or `Choreographer`. The sensor drives everything.

### Mobile Sensors Are Surprisingly Powerful
The accelerometer and gyroscope in any modern smartphone are remarkably good. The main limitations are sensor noise and integration drift over long periods. For interactive use, they're great.

## Connection to Other Work

This project's lessons compounded into:
- My **wearable IMU thesis work** — same sensor types (accelerometer, gyroscope), same noise/drift challenges, but with much higher stakes
- The **HAR-STGCN paper** — where I tried to build a multi-sensor wearable suit and learned (the hard way) about sensor drift

Mobile sensor games taught me at small scale what wearable HAR taught me at full scale. Both are governed by the same physics; the wearable case just adds noise, drift, and the need for sensor fusion.

## What I'd Add If I Continued

- More levels (different target sizes, moving targets, obstacles)
- Multi-player via Bluetooth or local network
- Score tracking and persistence
- Sound effects and visual feedback on win
- Calibration step (so the game starts assuming the user's "neutral" tilt)

## Keywords

sensor game, SensorManager, Sensor.TYPE_ORIENTATION, accelerometer, magnetometer, sensor fusion, getRotationMatrix, getOrientation, pitch, roll, sensor lifecycle, registerListener, unregisterListener, custom View game, onDraw, game loop, tilt control, mobile sensors, sensitivity tuning
