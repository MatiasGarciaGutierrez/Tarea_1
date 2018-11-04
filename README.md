# Tarea_1
El fin de este programa es detectar las apariciones de comerciales 
en cierto tiempo de la televisión abierta.

## Dependencias

Las dependencias son:

* NumPy
* scikit-learn
* OpenCV 3

## Formato

Esta implementación funciona con una estructura de carpetas descrita de la siguient forma:

* commercials: Carperta que contiene los videos de los comerciales
* television: Carpeta que contiene los videos de television
* descriptors: Carperta que contiene carpetas de descriptores de television y comerciales
    * commercials: descriptores de comerciales.
    * television: descriptores de television.  
* k_nearest: contiene los k más cercanos a cada video de televisión.

Para crear estas carpetas basta con utilizar el script `create_folder.py`.
 
## Uso

1. Crear las carpetas con `create_folder.py`.

```python 
python3 create_folder.py
```

2. Transferir los archivos de television a la carpeta "/television" y los archivos de 
comerciales a la carpeta "/commerciales"

3. Crear todos los descriptores de comerciales y televisión utilizando `create_descriptors.py`

```
python3 create_descriptors.py
```

4. Usar el script `Tarea_1.py`:

```python 
python3 Tarea_1.py --src television_video
```

Por ejemplo:

```
python3 Tarea_1.py --src mega-2014_04_25.mp4
```

## Resultados

| Television          | Correctas | Incorrectas | IoU  | Final |
|---------------------|-----------|-------------|------|-------|
| mega-2014_04_10.mp4 | 13/13     | 0/13        | 69.7 | 100.0 |
| mega-2014_04_11.mp4 | 24/28     | 0/28        | 68.9 | 85.7  |
| mega-2014_04_16.mp4 | 13/15     | 0/15        | 71.8 | 86.7  |
| mega-2014_04_17.mp4 | 9/11      | 0/11        | 74.0 | 81.8  |
| mega-2014_04_23.mp4 | 14/16     | 0/14        | 85.6 | 87.5  |
| mega-2014_04_25.mp4 | 17/20     | 1/20        | 67.4 | 80.0  |

## Contacto

Matías García - matias.garcia.gu@gmail.com.

## License & copyrigth

@Matías García, Universidad de Chile

