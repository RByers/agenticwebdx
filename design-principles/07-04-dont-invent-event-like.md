---
section: "7.4"
id: "dont-invent-event-like"
title: "Don’t invent your own event listener-like infrastructure"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#dont-invent-event-like"
agent_fit: "mixed"
slide_example: "clearly-harmful"
example_strength: 3
verdict: "Reusing EventTarget leverages strong agent priors and avoids hallucinated unsubscribe methods, but decoupling process start/stop from listener registration creates silent no-op traps and split cleanup lifecycles."
---

# §7.4 Don’t invent your own event listener-like infrastructure

GREP_SUMMARY: slide_example=clearly-harmful | strength=3/5 | agent_fit=mixed | §7.4 dont-invent-event-like — Don’t invent your own event listener-like infrastructure: Reusing EventTarget leverages strong agent priors and avoids hallucinated unsubscribe methods, but decoupling process start/stop from listener registration creates silent no-op traps and split cleanup lifecycles.

- **URL:** https://w3ctag.github.io/design-principles/#dont-invent-event-like
- **Chapter:** 7. Event Design
- **Agent-Fit:** mixed
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 3/5
- **Verdict:** Reusing EventTarget leverages strong agent priors and avoids hallucinated unsubscribe methods, but decoupling process start/stop from listener registration creates silent no-op traps and split cleanup lifecycles.

## Principle Summary

W3C TAG Design Principle §7.4 states that when an API allows authors to start and stop an underlying process that generates notifications, it should reuse the platform's standard `EventTarget` infrastructure (`addEventListener` / `removeEventListener`) for receiving those notifications rather than inventing a custom callback registration mechanism, while providing separate API methods to start and stop the underlying process.

The principle cites Web Bluetooth's `BluetoothRemoteGATTCharacteristic`, where `startNotifications()` and `stopNotifications()` control the device subscription while `'characteristicvaluechanged'` events are delivered via `EventTarget`. For human authors and browser engines, this separation allows multiple independent listeners to attach and detach without stopping the underlying hardware process for other consumers, and keeps asynchronous or fallible process startup separate from synchronous listener registration.

## Fit for Coding Agents

This principle cuts both ways for AI coding agents (`mixed`), because its two prescriptions pull in opposite directions for agent reliability. On the positive side, reusing `EventTarget` (`addEventListener` / `removeEventListener`) aligns with one of the strongest statistical priors in web training data, including composable lifecycle primitives like `{ once: true }` and `{ signal: abortController.signal }`. Whenever Web APIs invent bespoke listener-like infrastructure—such as `navigator.geolocation.watchPosition(cb)` returning a numeric ID for `clearWatch(id)`, legacy `MediaQueryList.addListener(cb)`, or custom `.subscribe()` / `.unsubscribe()` patterns—coding agents frequently hallucinate the teardown method name (e.g., calling `.unsubscribe()`, `.off()`, or `removeEventListener()` on non-`EventTarget` objects) or pass unsupported options objects.

On the negative side, the second requirement of §7.4—separating explicit `start()` / `stop()` controls for the underlying process from `addEventListener()`—splits a single logical intent ("listen to notifications from X") into two unlinked API calls. When an agent attaches `characteristic.addEventListener('characteristicvaluechanged', handler)` without calling `await characteristic.startNotifications()`, or calls `messagePort.addEventListener('message', handler)` without calling `messagePort.start()`, the platform fails silently: no exception or warning is emitted, and events simply never arrive. Silent non-delivery of events is particularly costly in an autonomous agent's test-and-fix feedback loop. Furthermore, decoupling process lifecycle from listener registration breaks single-point cleanup: passing `{ signal }` to `addEventListener` detaches the listener on abort, but leaks the active hardware or background process unless the agent separately remembers to call `stopNotifications()` or `close()`.

## Value as a Slide Example

As a standalone headline example for a TPAC slide, §7.4 is weak (2/5, `neither`) because its positive prescription ("reuse `EventTarget` instead of inventing bespoke callback registration") is a narrow special case of broader platform consistency principles.

However, the tension in its second prescription—requiring separate `start()` and `addEventListener()` calls—makes a good supporting example if a slide highlights silent no-op traps and split lifecycles in Web APIs (such as `MessagePort.addEventListener('message', fn)` silently doing nothing without `port.start()`, or Web Bluetooth's `BluetoothRemoteGATTCharacteristic` requiring both `startNotifications()` and `addEventListener('characteristicvaluechanged', fn)`).
