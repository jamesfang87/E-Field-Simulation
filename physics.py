import math


def calculate_electric_field(x, y, charges):
    k = 8.988e9  # N·m²/C² (scaled down for visualization)
    total_ex = 0
    total_ey = 0

    for charge in charges:
        q = charge.charge
        dx = x - charge.x
        dy = y - charge.y
        r_sq = dx**2 + dy**2

        if r_sq == 0:
            continue  # avoid division by zero

        r = math.sqrt(r_sq)
        e_mag = k * abs(q) / r_sq
        direction = 1 if q > 0 else -1
        total_ex += direction * e_mag * dx / r
        total_ey += direction * e_mag * dy / r

    return total_ex, total_ey


def calculate_voltage(x, y, charges):
    k = 8.988e9  # Coulomb's constant
    total_voltage = 0
    for charge in charges:
        q = charge.charge
        r = math.dist([x, y], [charge.x, charge.y])
        if r > 0:  # Avoid division by zero
            total_voltage += k * q / r
    return total_voltage
