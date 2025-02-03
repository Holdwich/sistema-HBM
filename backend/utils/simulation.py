import math

def generate_baseline(time_ms: int) -> float:
    """Gera a medição baseline conforme a fórmula."""
    return (-0.06366 +
            0.12613 * (math.cos(math.pi * time_ms / 500)) +
            0.12258 * (math.cos(math.pi * time_ms / 250)) +
            0.01593 * (math.sin(math.pi * time_ms / 500)) +
            0.03147 * (math.sin(math.pi * time_ms / 250)))
