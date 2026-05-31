import os
from PIL import Image

def optimizar_foto(ruta_entrada, carpeta_salida, nombre_archivo_salida):
    """
    Optimiza una foto de perfil:
    1. Recorta al centro (Smart Crop).
    2. Redimensiona.
    3. Guarda en formato WebP de alta calidad.
    """
    try:
        # 1. Abrir imagen
        img = Image.open(ruta_entrada)
        
        # Obtener dimensiones originales
        ancho, alto = img.size
        print(f"📏 Dimensiones originales: {ancho}x{alto}")
        
        # 2. Lógica de Recorte Central (Square Crop)
        # Calculamos el lado menor para hacer un cuadrado perfecto centrado
        lado = min(ancho, alto)
        izquierda = (ancho - lado) // 2
        arriba = (alto - lado) // 2
        derecha = (ancho + lado) // 2
        abajo = (alto + lado) // 2
        
        # Recortamos
        img_cortada = img.crop((izquierda, arriba, derecha, abajo))
        
        # 3. Redimensionar y Guardar Versiones
        
        # Versión HERO (Principal) - 800x800px
        tamanos = {
            "johanna-profile": 800,  # Para la sección Hero
            "johanna-thumb": 150     # Para el menú/header
        }
        
        os.makedirs(carpeta_salida, exist_ok=True)
        
        for nombre, size in tamanos.items():
            # Resize de alta calidad (LANCZOS es el mejor para fotos)
            img_final = img_cortada.resize((size, size), Image.LANCZOS)
            
            # Ruta de salida
            ruta_final = os.path.join(carpeta_salida, f"{nombre}.webp")
            
            # Guardar con calidad 90 (invisible al ojo humano, reduce peso drásticamente)
            img_final.save(ruta_final, format="WEBP", quality=90, optimize=True)
            
            peso_bytes = os.path.getsize(ruta_final)
            peso_kb = peso_bytes / 1024
            print(f"✅ Creado: {nombre}.webp | Tamaño: {size}x{size}px | Peso: {peso_kb:.2f} KB")

    except FileNotFoundError:
        print("❌ Error: No se encontró 'original.jpg'. Asegúrate de que el nombre sea correcto.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

# --- Ejecución ---
if __name__ == "__main__":
    print(" Iniciando optimización de fotos para Web...")
    optimizar_foto("original.jpg", "output", "perfil")
    print("🎉 ¡Listo! Revisa la carpeta 'output'.")