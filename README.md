---
title: K-Means Color Quantizer
emoji: 🎨
colorFrom: blue
colorTo: indigo
sdk: gradio
python_version: "3.12"
app_file: main.py
pinned: false
license: mit
custom_package_manager: uv
---
# K-Means Color Quantizer 🎨

Este proyecto es una herramienta de **Ciencia de Datos** aplicada al procesamiento de imágenes. Utiliza el algoritmo de clustering **K-Means** para realizar una cuantización de colores, reduciendo la paleta de una imagen a un número específico de tonos representativos (K) sin perder la estructura visual principal.

🚀 **Probá la App aquí:** [Hugging Face Space - Live Demo](https://huggingface.co/spaces/SebaVida/K-Means-Color-Quantizer)

---

## 🚀 Características Técnicas
- **Clustering Perceptual:** A diferencia de las implementaciones básicas que usan RGB, este modelo transforma la imagen al espacio de color **CIE LAB**. Esto asegura que las distancias calculadas por el algoritmo correspondan a la percepción humana del color.
- **Optimización de Rendimiento:** Implementa `MiniBatchKMeans` de *scikit-learn* para procesar imágenes de alta resolución en segundos, optimizando el uso de memoria RAM.
- **Pre-procesamiento Inteligente:** Incluye una técnica de reescalado dinámico para mantener la eficiencia en el despliegue (Hugging Face Spaces).
- **Interfaz Moderna:** Desarrollado con **Gradio** para una experiencia de usuario fluida e interactiva.

## 🛠️ Tecnologías
- **Python** (Lógica principal)
- **Scikit-Learn** (Algoritmos de ML)
- **OpenCV** (Procesamiento de visión computacional)
- **NumPy** (Manipulación de matrices)
- **UV** (Gestor de paquetes y entorno)

## 📦 Instalación y Uso
Este proyecto utiliza `uv` para una gestión de dependencias ultra rápida.

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/color-quantizer-kmeans.git](https://github.com/tu-usuario/color-quantizer-kmeans.git)
   cd color-quantizer-kmeans

---

### 🤝 Charlemos
Si necesitás realizar esta operación de manera masiva o para otras cosas de ciencia de datos, contactame:
📩 [linkedin.com/in/sebastian-vidaurri-90a087185](https://linkedin.com/in/sebastian-vidaurri-90a087185) 🚀

---
*Sebastián Vidaurri - Lic. en Ciencia de Datos*