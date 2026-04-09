import os
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from dataclasses import dataclass
from PIL import Image
import io

@dataclass
class ConfigCuantizacion:
    max_dimension: int = 800
    random_state: int = 42
    batch_size: int = 1024

def formatear_peso(peso_bytes: int) -> str:
    """Convierte bytes a un formato legible (KB o MB)."""
    if peso_bytes < 1024 * 1024:
        return f"{peso_bytes / 1024:.2f} KB"
    return f"{peso_bytes / (1024 * 1024):.2f} MB"

class CuantizadorKMeans:
    def __init__(self, k: int, config: ConfigCuantizacion = ConfigCuantizacion()):
        self.k = k
        self.config = config
        self.model = MiniBatchKMeans(
            n_clusters=self.k, 
            batch_size=self.config.batch_size, 
            random_state=self.config.random_state,
            n_init="auto"
        )

    def _optimizar_dimensiones(self, imagen: np.ndarray) -> np.ndarray:
        # Optimización de la imagen: reescalado preventivo para evitar 
        # agotar la memoria RAM (OOM) en entornos con recursos limitados.
        h, w = imagen.shape[:2]
        if max(h, w) > self.config.max_dimension:
            escala = self.config.max_dimension / max(h, w)
            nuevo_tamano = (int(w * escala), int(h * escala))
            return cv2.resize(imagen, nuevo_tamano, interpolation=cv2.INTER_AREA)
        return imagen

    def procesar(self, ruta_imagen: str) -> tuple[np.ndarray, str, str]:
        if not ruta_imagen or not os.path.exists(ruta_imagen):
            raise ValueError("Ruta de imagen no válida")

        # 1. Peso Original
        peso_orig_bytes = os.path.getsize(ruta_imagen)
        peso_orig_str = formatear_peso(peso_orig_bytes)

        # 2. Carga y preprocesamiento (Seguro para caracteres especiales o tildes)
        stream = np.fromfile(ruta_imagen, np.uint8)
        img_bgr = cv2.imdecode(stream, cv2.IMREAD_COLOR)
        
        if img_bgr is None:
            raise ValueError("No se pudo decodificar la imagen. El formato podría no ser compatible.")

        imagen = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img = self._optimizar_dimensiones(imagen)
        
        # 3. K-Means en espacio de color perceptualmente uniforme (LAB)
        img_lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        h, w, c = img_lab.shape
        pixeles = img_lab.reshape(-1, c)

        etiquetas = self.model.fit_predict(pixeles)
        centroides = self.model.cluster_centers_.astype(np.uint8)
        pixeles_cuantizados = centroides[etiquetas]
        img_reconstruida_lab = pixeles_cuantizados.reshape(h, w, c)
        
        # 4. Resultado para mostrar en la Interfaz (RGB)
        img_reconstruida_rgb = cv2.cvtColor(img_reconstruida_lab, cv2.COLOR_LAB2RGB)

        # 5. Simulación de Compresión con PIL (Mapa de paleta indexada de K colores)
        pil_img = Image.fromarray(img_reconstruida_rgb)
        pil_img_quantized = pil_img.quantize(colors=self.k)

        buffer = io.BytesIO()
        pil_img_quantized.save(buffer, format="PNG", optimize=True)
        peso_proc_bytes = buffer.tell()
        peso_proc_str = formatear_peso(peso_proc_bytes)

        return img_reconstruida_rgb, peso_orig_str, peso_proc_str