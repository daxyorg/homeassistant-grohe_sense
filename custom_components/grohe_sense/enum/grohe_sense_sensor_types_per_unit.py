from custom_components.grohe_sense.enum.grohe_types import GroheTypes

SENSOR_TYPES_PER_UNIT = {
    GroheTypes.GROHE_SENSE: ['temperature', 'humidity'],
    GroheTypes.GROHE_SENSE_GUARD: ['flowrate', 'pressure', 'temperature_guard']
}
