import os
import gradio as gr
from modelo import CuantizadorKMeans, formatear_peso

def ejecutar_cuantizacion(ruta_imagen, k):
    if not ruta_imagen:
        return None, "", ""
    obj = CuantizadorKMeans(k=int(k))
    img_cuantizada, peso_orig, peso_proc = obj.procesar(ruta_imagen)
    return img_cuantizada, peso_orig, peso_proc

def actualizar_peso_original(ruta_imagen):
    if ruta_imagen is not None and os.path.exists(ruta_imagen):
        peso = os.path.getsize(ruta_imagen)
        return formatear_peso(peso)
    return ""

css = """
#main-title {
    text-align: center;
    font-size: 3em; 
    font-weight: bold;
    margin-bottom: 0.2em;
}
#subtitle {
    text-align: center;
    font-size: 1.5em; 
    color: #9ca3af; 
    margin-bottom: 1.5em;
}
.image-container {
    min-height: 400px;
}
"""

with gr.Blocks(title="K-Means Color Quantizer") as demo:
    
    gr.Markdown("<h1 id='main-title'>🎨 Optimizador de Paletas de Color con K-Means</h1>")
    gr.Markdown("<p id='subtitle'>Este proyecto utiliza <b>Machine Learning</b> para reducir la complejidad cromática de una imagen, logrando compresión de datos.</p>")

    # FILA 1: Exclusivamente para las imágenes (Garantiza misma altura)
    with gr.Row():
        entrada = gr.Image(label="Imagen Original", type="filepath", elem_classes="image-container")
        salida = gr.Image(label="Resultado (Descargable)", type="numpy", elem_classes="image-container")
            
    # FILA 2: Exclusivamente para los pesos (Garantiza alineación horizontal perfecta)
    with gr.Row():
        peso_orig_display = gr.Text(label="Peso Original", interactive=False)
        peso_proc_display = gr.Text(label="Peso Procesado (Estimado en PNG)", interactive=False)

    # FILA 3: Controles ocupando todo el ancho inferior
    with gr.Column(variant="panel"): 
        k_slider = gr.Slider(2, 32, value=8, step=1, label="Número de Colores (K)")
        btn = gr.Button("Procesar", variant="primary")
        
    # FILA 4: Ejemplos precargados para el usuario
    gr.Examples(
        examples=["img/ejemplo.jpg"], # <--- Agregamos la carpeta a la ruta
        inputs=entrada,
        label="Haz clic en la imagen para usarla de prueba:"
    )
    
    # Eventos
    entrada.change(fn=actualizar_peso_original, inputs=entrada, outputs=peso_orig_display)
    btn.click(
        fn=ejecutar_cuantizacion, 
        inputs=[entrada, k_slider], 
        outputs=[salida, peso_orig_display, peso_proc_display]
    )

if __name__ == "__main__":
    demo.launch(css=css)