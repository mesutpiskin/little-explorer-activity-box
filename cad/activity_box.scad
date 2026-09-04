include <generated_dimensions.scad>

$fn = 48;
part = is_undef(part) ? "assembly" : part;
dial_grip_d = 32;
dial_flange_d = 46;
buzzer_port_depth = front_t + 1.4;
eps = 0.15;

module rounded_rect_2d(w, h, r) {
    hull() {
        for (x = [r, w - r], y = [r, h - r])
            translate([x, y]) circle(r = r);
    }
}

module rounded_box(w, h, d, r) {
    linear_extrude(height = d) rounded_rect_2d(w, h, r);
}

function front_xy(position) = [position[0], box_h - position[1]];

module circular_panel_hole(position, diameter) {
    xy = front_xy(position);
    translate([xy[0], xy[1], -eps])
        cylinder(h = front_t + 2 * eps, d = diameter);
}

module rectangular_panel_hole(position, size) {
    xy = front_xy(position);
    translate([xy[0] - size[0] / 2, xy[1] - size[1] / 2, -eps])
        cube([size[0], size[1], front_t + 2 * eps]);
}

module buzzer_holes_at(xy) {
    for (angle = [0 : 60 : 300])
        translate([xy[0] + 6.2 * cos(angle), xy[1] + 6.2 * sin(angle), -eps])
            cylinder(h = buzzer_port_depth + 2 * eps, d = 3);
    translate([xy[0], xy[1], -eps])
        cylinder(h = buzzer_port_depth + 2 * eps, d = 3);
}

module buzzer_holes() {
    buzzer_holes_at(front_xy(pos_buzzer));
}

module panel_cutouts() {
    for (position = [pos_red_led, pos_yellow_led, pos_green_led,
                     pos_switch_led, pos_dimmer_led])
        circular_panel_hole(position, led_hole_d);
    for (position = [pos_red_button, pos_yellow_button])
        circular_panel_hole(position, dc184_button_hole_d);
    for (position = [pos_green_button, pos_buzzer_button])
        circular_panel_hole(position, dc180_button_hole_d);
    circular_panel_hole(pos_rocker, room_switch_hole_d);
    circular_panel_hole(pos_dial, dial_opening_d);
    buzzer_holes();
}

module open_led_guard(position) {
    xy = front_xy(position);
    translate([xy[0], xy[1], front_t - eps])
        difference() {
            cylinder(h = 6, d = 16);
            translate([0, 0, -eps]) cylinder(h = 6 + 2 * eps, d = 12.4);
        }
}

module buzzer_cup_at(xy) {
    translate([xy[0], xy[1], front_t - eps])
        difference() {
            cylinder(h = 8, d = 17);
            translate([0, 0, 1]) cylinder(h = 7.2, d = 12.4);
        }
}

module buzzer_cup() {
    buzzer_cup_at(front_xy(pos_buzzer));
}

module pot_mount_bridge() {
    xy = front_xy(pos_dial);
    bridge_z = front_t + 13;
    union() {
        for (x = [xy[0] - 28, xy[0] + 24])
            translate([x, xy[1] - 6, front_t - eps])
                cube([4, 12, bridge_z - front_t + eps]);
        difference() {
            translate([xy[0] - 28, xy[1] - 6, bridge_z])
                cube([56, 12, 2.8]);
            translate([xy[0], xy[1], bridge_z - eps])
                cylinder(h = 2.8 + 2 * eps, d = pot_bushing_hole_d);
        }
    }
}

module wire_clip(x, y) {
    translate([x, y, front_t - eps])
        difference() {
            cube([12, 6, 5]);
            translate([2, -eps, 1.8]) cube([8, 6 + 2 * eps, 3.5]);
        }
}

module back_stop_ring() {
    translate([0, 0, box_d - back_t - 1.2])
        linear_extrude(height = 1.2)
            difference() {
                offset(delta = -wall) rounded_rect_2d(box_w, box_h, corner_r);
                offset(delta = -(wall + 1.4)) rounded_rect_2d(box_w, box_h, corner_r);
            }
}

module master_switch_cutout() {
    translate([box_w - wall - eps, box_h / 2 - master_switch_size[0] / 2,
               box_d / 2 - master_switch_size[1] / 2])
        cube([wall + 2 * eps, master_switch_size[0], master_switch_size[1]]);
}

module service_holes() {
    service_z = box_d - back_t - 6.5;
    translate([-eps, box_h / 2, service_z])
        rotate([0, 90, 0]) cylinder(h = wall + 2 * eps, d = 3);
    translate([box_w - wall - eps, box_h / 2, service_z])
        rotate([0, 90, 0]) cylinder(h = wall + 2 * eps, d = 3);
}

module body() {
    difference() {
        union() {
            difference() {
                rounded_box(box_w, box_h, box_d, corner_r);
                translate([wall, wall, front_t])
                    rounded_box(box_w - 2 * wall, box_h - 2 * wall,
                                box_d - front_t + eps, corner_r - wall);
            }
            for (position = [pos_red_led, pos_yellow_led, pos_green_led,
                             pos_switch_led, pos_dimmer_led])
                open_led_guard(position);
            buzzer_cup();
            pot_mount_bridge();
            wire_clip(63, 77);
            wire_clip(126, 77);
            back_stop_ring();
        }
        panel_cutouts();
        master_switch_cutout();
        service_holes();
    }
}

module back_plate() {
    plate_x = wall + fit_clearance;
    plate_y = wall + fit_clearance;
    translate([plate_x, plate_y, 0])
        linear_extrude(height = back_t)
            rounded_rect_2d(box_w - 2 * plate_x, box_h - 2 * plate_y,
                            corner_r - plate_x);
}

module tongue_ring() {
    inset = wall + fit_clearance + 0.7;
    translate([0, 0, back_t - eps])
        linear_extrude(height = 4.5)
            difference() {
                offset(delta = -inset) rounded_rect_2d(box_w, box_h, corner_r);
                offset(delta = -(inset + 1.2)) rounded_rect_2d(box_w, box_h, corner_r);
            }
}

module side_lock(left = true) {
    tab_x = left ? wall + fit_clearance
                 : box_w - wall - fit_clearance - 1.2;
    hook_x = left ? tab_x - 0.7 : tab_x + 1.2;
    translate([tab_x, box_h / 2 - 7, back_t - eps]) cube([1.2, 14, 8]);
    translate([hook_x, box_h / 2 - 7, back_t + 6.2]) cube([0.7, 14, 1.2]);
}

module passive_lock(top = true) {
    tab_y = top ? box_h - wall - fit_clearance - 1.2
                : wall + fit_clearance;
    hook_y = top ? tab_y + 1.2 : tab_y - 0.7;
    translate([box_w / 2 - 7, tab_y, back_t - eps]) cube([14, 1.2, 6]);
    translate([box_w / 2 - 7, hook_y, back_t + 4.5]) cube([14, 0.7, 1.1]);
}

module battery_rails() {
    bay_w = battery_bay_size[0] + 1;
    bay_h = battery_bay_size[1] + 1;
    x0 = battery_bay_pos[0];
    y0 = battery_bay_pos[1];
    rail_h = 5;
    for (x = [x0, x0 + bay_w - 2.2])
        translate([x, y0, back_t - eps]) cube([2.2, bay_h, rail_h]);
    for (y = [y0, y0 + bay_h - 2.2])
        translate([x0, y, back_t - eps]) cube([bay_w, 2.2, rail_h]);
}

module battery_center_divider() {
    bay_w = battery_bay_size[0] + 1;
    bay_h = battery_bay_size[1] + 1;
    x0 = battery_bay_pos[0];
    y0 = battery_bay_pos[1];
    translate([x0 + bay_w / 2 - 1.1, y0, back_t - eps])
        cube([2.2, bay_h, 5]);
}

module back() {
    union() {
        back_plate();
        tongue_ring();
        side_lock(true);
        side_lock(false);
        passive_lock(true);
        passive_lock(false);
        battery_rails();
        battery_center_divider();
    }
}

module dial() {
    difference() {
        union() {
            cylinder(h = 2.8, d = dial_flange_d);
            translate([0, 0, 2.7]) cylinder(h = 8, d = dial_grip_d);
            for (angle = [0 : 30 : 330])
                rotate([0, 0, angle]) translate([dial_grip_d / 2 - 1, 0, 3])
                    cube([1.2, 1.8, 7]);
        }
        translate([0, 0, -eps]) cylinder(h = 8, d = pot_shaft_d);
    }
}

module snap_fit_test() {
    // Receiving wall with a 3 mm service passage.
    difference() {
        cube([18, 24, 12]);
        translate([3, 3, 2]) cube([15.2, 18, 10.2]);
        translate([-eps, 12, 7]) rotate([0, 90, 0]) cylinder(h = 3.3, d = 3);
    }
    // Separate coupon tab, printed beside the receiving wall.
    translate([24, 4, 0]) {
        cube([12, 16, back_t]);
        translate([0.55, 1, back_t - eps]) cube([1.2, 14, 8]);
        translate([-0.2, 1, back_t + 6.2]) cube([0.75, 14, 1.2]);
    }
}

module component_fit_test() {
    test_w = fit_size[0];
    test_h = fit_size[1];
    test_r = fit_corner_radius;
    led_fit_diameters = fit_led_diameters;
    dc184_fit_diameters = fit_dc184_diameters;
    dc180_fit_diameters = fit_dc180_diameters;
    dc131a_fit_diameters = fit_dc131a_diameters;
    pot_bushing_fit_diameters = fit_pot_bushing_diameters;
    shaft_fit_diameters = fit_shaft_diameters;
    dc120_fit_sizes = fit_dc120_sizes;
    top_y = fit_top_y;
    bottom_y = fit_bottom_y;
    led_x = fit_led_x;
    dc184_x = fit_dc184_x;
    dc180_x = fit_dc180_x;
    dc131a_x = fit_dc131a_x;
    pot_bushing_x = fit_pot_bushing_x;
    shaft_x = fit_shaft_x;
    dc120_x = fit_dc120_x;
    dial_xy = fit_dial_xy;
    buzzer_xy = fit_buzzer_xy;

    difference() {
        union() {
            rounded_box(test_w, test_h, front_t, test_r);
            open_led_guard([led_x[1], box_h - top_y]);
            buzzer_cup_at(buzzer_xy);
            for (index = [0 : len(shaft_x) - 1])
                translate([shaft_x[index], bottom_y, front_t - eps])
                    cylinder(h = 8, d = 12);
        }
        for (index = [0 : len(led_x) - 1])
            translate([led_x[index], top_y, -eps])
                cylinder(h = front_t + 2 * eps, d = led_fit_diameters[index]);
        for (index = [0 : len(dc184_x) - 1])
            translate([dc184_x[index], top_y, -eps])
                cylinder(h = front_t + 2 * eps, d = dc184_fit_diameters[index]);
        for (index = [0 : len(dc180_x) - 1])
            translate([dc180_x[index], top_y, -eps])
                cylinder(h = front_t + 2 * eps, d = dc180_fit_diameters[index]);
        for (index = [0 : len(dc131a_x) - 1])
            translate([dc131a_x[index], top_y, -eps])
                cylinder(h = front_t + 2 * eps, d = dc131a_fit_diameters[index]);
        for (index = [0 : len(pot_bushing_x) - 1])
            translate([pot_bushing_x[index], bottom_y, -eps])
                cylinder(h = front_t + 2 * eps,
                         d = pot_bushing_fit_diameters[index]);
        for (index = [0 : len(shaft_x) - 1])
            translate([shaft_x[index], bottom_y, front_t + 1])
                cylinder(h = 7.2, d = shaft_fit_diameters[index]);
        for (index = [0 : len(dc120_x) - 1])
            translate([dc120_x[index] - dc120_fit_sizes[index][0] / 2,
                       bottom_y - dc120_fit_sizes[index][1] / 2, -eps])
                cube([dc120_fit_sizes[index][0], dc120_fit_sizes[index][1],
                      front_t + 2 * eps]);
        translate([dial_xy[0], dial_xy[1], -eps])
            cylinder(h = front_t + 2 * eps, d = dial_opening_d);
        buzzer_holes_at(buzzer_xy);
    }
}

if (part == "body") body();
else if (part == "back") back();
else if (part == "dial") dial();
else if (part == "snap_test") snap_fit_test();
else if (part == "component_test") component_fit_test();
else {
    color("wheat") body();
    color("lightgray") translate([0, box_h + 15, 0]) back();
    color("steelblue") translate([box_w + 30, 50, 0]) dial();
}
