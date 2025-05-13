# Biomarcadores
0. Rellenar datos faltantes entre muestras

ts             ex  ey  sx  sy
14543536654    2   3   5    1
14543536658    6   2   1    6
14543536661    7   1   0    7

a

ts             ex  ey  sx  sy
14543536654    2   3   5    1
14543536655    2   3   5    1
14543536656    2   3   5    1
14543536657    2   3   5    1
14543536658    6   2   1    6
14543536659    6   2   1    6
14543536660    6   2   1    6
14543536661    7   1   0    7

1. **start_latency** (Latencia de arranque): Tiempo transcurrido (ms) desde que el estímulo cambia de posición y los
   ojos comienzan a moverse. Para esto hay que definir un umbral de velocidad que defina cuando se arranca.


## Tareas
1. Calcular vector de desplazamiento dado vectores de entrada x e y

```python
def distance(x: ndarray, y: ndarray) -> ndarray:
    x_prev = x[:-1]
    x_curr = x[1:]
    y_prev = y[:-1]
    y_curr = y[1:]
    return sqrt((x_prev - x_curr) ** 2 + (y_prev - y_curr) ** 2)
```

2. Calcular el perfil de velocidad instantánea de un vector utilizando el método differentiate:

```python
def differentiate(channel: ndarray) -> ndarray:
    """Super Lanczos 11  numerical differentiation method

    Args:
        channel (ndarray): Channel

    Returns:
        ndarray: Channel
    """
    window = array([300, -294, -532, -503, -296, 0, 296, 503, 532, 294, -300])
    result = convolve(channel, window, "same") / 5148.0
    result[:5] = 0
    result[-5:] = 0
    return result * 1000.0
```

3. Calcular ocurrencia de picos de velocidad utilizando la función:
[find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html)

4. Calcular los momentos donde se comienza a exceder el umbral de velocidad utilizando como entrada
el perfil absoluto de velocidad y los picos encontrados.

```python
def starts(velocity: ndarray, peaks: list[int]) -> list[int]:
    abs_velocity = abs(velocity)

    pass
```
