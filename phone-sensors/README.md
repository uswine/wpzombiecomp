# Sensor Deck — live phone sensor readout

A single-file web app (`index.html`) that lists every sensor a phone's browser can
reach and streams its current readings in real time: accelerometer, linear
acceleration, gyroscope, gravity vector, magnetometer, attitude, compass heading,
fused orientation quaternions, screen orientation, GNSS location, ambient light,
proximity, microphone level, camera stream settings, touch pressure and contact
size, network, Bluetooth, NFC, battery, display refresh rate and geometry, and
the device/CPU/memory/storage profile. Anything the browser cannot see is listed
explicitly under **Not reachable from a browser** so the coverage is honest.

No build step, no dependencies, no server code. Works on iPhone (Safari) and
Android (Chrome); the two browsers expose different subsets and the page says
which rows are unavailable and why.

## Opening it on the phone

Sensors only stream on a **secure (https) page opened directly in the browser**.
Three ways to get there:

1. **Host it on any https site.** Upload `index.html` as-is (for example to
   `https://zombiecomponents.com/sensors/index.html`) and open that URL in
   Safari or Chrome. This is the most reliable route: every API works exactly
   as the browser allows.
2. **Claude artifact link.** The same file is published as a private artifact
   at <https://claude.ai/code/artifact/5c8d570d-8dc7-42c7-85d9-437451e9f3bd>
   (visible only to the account that owns it). If any row shows *No data* or
   *Blocked* while viewed inside the Claude app, use the page's own
   "open it directly in your browser" link: some sensors are withheld from
   embedded frames.
3. **Local file (Android Chrome only).** Download `index.html` and open it from
   the Files app. Chrome treats local files as secure, so motion and location
   work; iOS Safari does not run local files this way.

Then **Add to Home Screen** (Safari share sheet, or Chrome's menu) to get an
icon that opens the deck full-screen. The page builds its own web-app manifest
at runtime so the shortcut points back at whatever URL you opened.

## Using it

- **Start sensors** — iOS requires a tap before motion and orientation events
  flow. Android starts them automatically on load.
- **Allow location / Allow microphone / Open camera / Listen for tags** — each
  permission-gated sensor has its own button in its row.
- **Pause** freezes the numbers and sparklines without stopping the sensors.
- **Keep screen on** holds a screen wake lock while you watch (where supported).
- **Copy snapshot** puts every reading, status, sample rate and API support flag
  on the clipboard as JSON — paste it into a chat when you want the full detail.
- **All / Live / Unavailable** filters the list.

Each row carries a status chip:

| Chip | Meaning |
|---|---|
| Live · N Hz | Data is streaming; N is the measured sample rate |
| Tap to allow | Supported, waiting for your permission tap |
| Waiting | Started, no reading yet (for example, waiting for a GNSS fix) |
| No data | The API exists but this device or context delivers nothing |
| Denied / Blocked | Permission refused, or the page is embedded without sensor rights |
| Not in this browser | The web API is not implemented here |
| Detected | Static capability, not a stream |

## What each phone browser exposes

| Sensor | iOS Safari | Android Chrome |
|---|---|---|
| Accelerometer, linear acceleration, gyroscope | Yes, after the permission tap | Yes |
| Attitude (alpha/beta/gamma) | Yes (relative frame) | Yes |
| Compass heading | Yes (`webkitCompassHeading`) | Yes (`deviceorientationabsolute`) |
| Gravity vector | Derived from the two acceleration vectors | Native `GravitySensor` |
| Fused orientation quaternions | No | Yes |
| Magnetometer (raw µT), ambient light | No | Only behind `chrome://flags/#enable-generic-sensor-extra-classes` |
| Location (GNSS) | Yes | Yes |
| Microphone level, camera stream | Yes | Yes |
| Touch pressure / contact size | Force on 3D-Touch era devices, size on all | Size and pressure where the digitizer reports them |
| Network Information | No (online/offline only) | Yes |
| Bluetooth availability, NFC | No | Yes |
| Battery | No | Yes |
| Vibration | No | Yes |
| Proximity | No | No (removed from the web platform) |

Barometer, thermometer, humidity, step counter, hall sensor, heart rate and depth
sensors have no web API at all. Reading those, or listing the phone's complete
hardware sensor inventory, needs a native app (Android `SensorManager`, iOS
`CoreMotion`).

## Files

| File | Contents |
|---|---|
| `index.html` | The whole app: markup, styles and script in one file |
| `README.md` | This guide |
