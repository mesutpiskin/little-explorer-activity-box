"""Single source of truth for the activity-box geometry and electronics."""

BOX = {
    "width": 200,
    "height": 160,
    "depth": 52,
    "corner_radius": 14,
    "wall": 2.6,
    "front": 3.2,
    "back": 2.8,
    "clearance": 0.25,
}

LABEL = {
    "width": 204,
    "height": 164,
    "bleed": 2,
    "dpi": 300,
}

ELECTRICAL = {
    "supply_max": 6.4,
    "resistor": 220,
    "fuse_amp": 1.0,
    "potentiometer": 1000,
    "led_forward_voltages": {
        "red": 2.0,
        "yellow": 2.1,
        "orange": 2.1,
        "white_switch": 3.0,
        "white_dimmer": 3.0,
    },
}

LED_HOLE_DIAMETER = 8.2
BUTTON_HOLE_DIAMETER = 24.2
ROCKER_SIZE = (21.2, 15.2)
DIAL_OPENING_DIAMETER = 34.0
MASTER_SWITCH_SIZE = (13.2, 6.0)

PANEL_FEATURES = [
    {"id": "red_led", "kind": "circle", "x": 40, "y": 28, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "red_button", "kind": "circle", "x": 40, "y": 57, "radius": BUTTON_HOLE_DIAMETER / 2},
    {"id": "yellow_led", "kind": "circle", "x": 100, "y": 28, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "yellow_button", "kind": "circle", "x": 100, "y": 57, "radius": BUTTON_HOLE_DIAMETER / 2},
    {"id": "orange_led", "kind": "circle", "x": 160, "y": 28, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "orange_button", "kind": "circle", "x": 160, "y": 57, "radius": BUTTON_HOLE_DIAMETER / 2},
    {"id": "switch_led", "kind": "circle", "x": 40, "y": 101, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "rocker", "kind": "rect", "x": 40, "y": 129, "width": ROCKER_SIZE[0], "height": ROCKER_SIZE[1], "radius": max(ROCKER_SIZE) / 2},
    {"id": "dimmer_led", "kind": "circle", "x": 100, "y": 101, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "dial", "kind": "circle", "x": 100, "y": 128, "radius": DIAL_OPENING_DIAMETER / 2},
    {"id": "buzzer", "kind": "pattern", "x": 160, "y": 100, "radius": 8},
    {"id": "buzzer_button", "kind": "circle", "x": 160, "y": 130, "radius": BUTTON_HOLE_DIAMETER / 2},
]

BATTERY_BAY = {"width": 112, "height": 26, "depth": 18, "x": 44, "y": 64}
