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
    "resistor": 330,
    "fuse_amp": 1.0,
    "potentiometer": 1000,
    "led_forward_voltages": {
        "red": 2.0,
        "yellow": 2.1,
        "green": 3.0,
        "blue_switch": 3.0,
        "white_dimmer": 3.0,
    },
}

LED_HOLE_DIAMETER = 10.2
DC184_BUTTON_HOLE_DIAMETER = 12.0
DC180_BUTTON_HOLE_DIAMETER = 16.0
ROOM_SWITCH_HOLE_DIAMETER = 20.2
DIAL_OPENING_DIAMETER = 34.0
POT_BUSHING_HOLE_DIAMETER = 7.0
POT_SHAFT_DIAMETER = 6.2
MASTER_SWITCH_SIZE = (19.0, 13.0)

PANEL_FEATURES = [
    {"id": "red_led", "kind": "circle", "x": 40, "y": 28, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "red_button", "kind": "circle", "x": 40, "y": 57, "radius": DC184_BUTTON_HOLE_DIAMETER / 2},
    {"id": "yellow_led", "kind": "circle", "x": 100, "y": 28, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "yellow_button", "kind": "circle", "x": 100, "y": 57, "radius": DC184_BUTTON_HOLE_DIAMETER / 2},
    {"id": "green_led", "kind": "circle", "x": 160, "y": 28, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "green_button", "kind": "circle", "x": 160, "y": 57, "radius": DC180_BUTTON_HOLE_DIAMETER / 2},
    {"id": "switch_led", "kind": "circle", "x": 40, "y": 101, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "rocker", "kind": "circle", "x": 40, "y": 129, "radius": ROOM_SWITCH_HOLE_DIAMETER / 2},
    {"id": "dimmer_led", "kind": "circle", "x": 100, "y": 101, "radius": LED_HOLE_DIAMETER / 2},
    {"id": "dial", "kind": "circle", "x": 100, "y": 128, "radius": DIAL_OPENING_DIAMETER / 2},
    {"id": "buzzer", "kind": "pattern", "x": 160, "y": 100, "radius": 8},
    {"id": "buzzer_button", "kind": "circle", "x": 160, "y": 130, "radius": DC180_BUTTON_HOLE_DIAMETER / 2},
]

BATTERY_BAY = {
    "holder_count": 2,
    "width": 62,
    "height": 68,
    "depth": 18,
    "x": 69,
    "y": 46,
}

FIT_TEST = {
    "size": (200, 76),
    "corner_radius": 5,
    "top_y": 58,
    "bottom_y": 20,
    "led_diameters": (10.0, 10.2),
    "dc184_diameters": (12.0, 12.2),
    "dc180_diameters": (16.0, 16.2),
    "dc131a_diameters": (20.0, 20.2),
    "pot_bushing_diameters": (7.0, 7.2),
    "shaft_diameters": (5.8, 6.0, 6.2),
    "dc120_sizes": ((19.0, 13.0), (19.4, 13.4)),
    "led_x": (10, 24),
    "dc184_x": (42, 59),
    "dc180_x": (81, 102),
    "dc131a_x": (130, 155),
    "pot_bushing_x": (10, 22),
    "shaft_x": (38, 54, 70),
    "dc120_x": (94, 120),
    "dial_xy": (153, 20),
    "buzzer_xy": (187, 58),
}
