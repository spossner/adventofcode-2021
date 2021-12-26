def process_input(filename):
    """Acquire input data"""
    with open(filename) as file:
        input = file.read().splitlines()

    rules = []

    for line in input:
        on_off, cubes = line.split()
        on = on_off == 'on'
        xrange, yrange, zrange = cubes.split(',')
        _v, xrange = xrange.split('=')
        _v, yrange = yrange.split('=')
        _v, zrange = zrange.split('=')
        low_x, high_x = xrange.split('..')
        low_y, high_y = yrange.split('..')
        low_z, high_z = zrange.split('..')
        rule = (on, ((int(low_x), int(high_x)), (int(low_y), int(high_y)), (int(low_z), int(high_z))))
        rules.append(rule)

    return rules


def apply_rule(rule, core):
    """Apply a rule to the core"""
    on_rule, cuboid_rule = rule
    (r_low_x, r_high_x), (r_low_y, r_high_y), (r_low_z, r_high_z) = cuboid_rule

    # if r_low_x < -50 or r_low_y < -50 or r_low_z < -50 or r_high_x > 50 or r_high_y > 50 or r_high_z > 50:
    #     print(f"ignoring {cuboid_rule}")
    #     return

    intersections = True
    while intersections:
        for c in reversed(range(len(core))):
            cuboid = core[c]
            (low_x, high_x), (low_y, high_y), (low_z, high_z) = cuboid

            # If rule cuboid encloses a core cuboid, remove the core cuboid
            if r_low_x <= low_x and r_high_x >= high_x and r_low_y <= low_y and r_high_y >= high_y and r_low_z <= low_z and r_high_z >= high_z:
                del core[c]
                break

            # Test if rule cuboid has any intersection at all with the core cuboid
            if r_low_x <= high_x and r_high_x >= low_x and r_low_y <= high_y and r_high_y >= low_y and r_low_z <= high_z and r_high_z >= low_z:
                pass
            else:
                continue

            # If rule cuboid intersects, split the core cuboid into two cuboids along the
            # intersection line
            if r_low_x in range(low_x + 1, high_x + 1):
                core[c] = (low_x, r_low_x - 1), (low_y, high_y), (low_z, high_z)
                core.append(((r_low_x, high_x), (low_y, high_y), (low_z, high_z)))
                break
            if r_high_x in range(low_x, high_x):
                core[c] = (r_high_x + 1, high_x), (low_y, high_y), (low_z, high_z)
                core.append(((low_x, r_high_x), (low_y, high_y), (low_z, high_z)))
                break

            if r_low_y in range(low_y + 1, high_y + 1):
                core[c] = (low_x, high_x), (low_y, r_low_y - 1), (low_z, high_z)
                core.append(((low_x, high_x), (r_low_y, high_y), (low_z, high_z)))
                break
            if r_high_y in range(low_y, high_y):
                core[c] = (low_x, high_x), (r_high_y + 1, high_y), (low_z, high_z)
                core.append(((low_x, high_x), (low_y, r_high_y), (low_z, high_z)))
                break

            if r_low_z in range(low_z + 1, high_z + 1):
                core[c] = (low_x, high_x), (low_y, high_y), (low_z, r_low_z - 1)
                core.append(((low_x, high_x), (low_y, high_y), (r_low_z, high_z)))
                break
            if r_high_z in range(low_z, high_z):
                core[c] = (low_x, high_x), (low_y, high_y), (r_high_z + 1, high_z)
                core.append(((low_x, high_x), (low_y, high_y), (low_z, r_high_z)))
                break
        else:
            intersections = False

    # Now new cuboid is distinct. If it is ON, add it to the core list
    if on_rule: core.append(cuboid_rule)
    return


def cuboid_size(cuboid):
    """Return the size of a cuboid"""
    (low_x, high_x), (low_y, high_y), (low_z, high_z) = cuboid
    size = (high_x - low_x + 1) * (high_y - low_y + 1) * (high_z - low_z + 1)
    return size


# -----------------------------------------------------------------------------------------

filename = 'input.txt'
# filename = 'sample3.txt'

#rules = process_input('22-dev.txt')
#rules = process_input('22-dev2.txt')
rules = process_input('22.txt')

# Core is a list of cubes that are On. There are no intersections
core = []

# Apply the rules
for rule in rules:
    apply_rule(rule, core)

# Calculate total size
total_on = 0
for cuboid in core:
    total_on += cuboid_size(cuboid)

print(total_on, 'cubes are on')
