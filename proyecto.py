import re
import flet as ft

ofensas = ["tonto", "idiota", "mula", "puñetas", "puto"]

def analisis_lexico(entrada):
    return entrada.strip().split()

def analisis_sintactico(tokens):
    joined = " ".join(tokens)
    if re.match(r"^\d+\s*[\+\-\*/]\s*\d+$", joined):
        return "operacion"
    elif any(tok in ["->", "|"] for tok in tokens):
        return "gramatica"
    elif re.match(r"^\/.*\/$", joined):
        return "er"
    elif any(pal.lower() in ofensas for pal in tokens):
        return "ofensa"
    else:
        return "cadena"

def analisis_semantico(tipo):
    return tipo != "ofensa"

def generar_codigo_intermedio(tipo, tokens):
    if tipo == "operacion":
        return f"t1 = {' '.join(tokens)}"
    elif tipo in ["cadena", "er", "gramatica"]:
        return f"t1 = '{' '.join(tokens)}'"
    return None

def generar_codigo_objeto(tipo, tokens):
    if tipo == "operacion":
        try:
            return str(eval("".join(tokens)))
        except:
            return "Error de evaluación"
    else:
        return " ".join(tokens)

def main(page: ft.Page):
    page.title = "Compilador Educativo"
    page.vertical_alignment = ft.MainAxisAlignment.START

    entrada = ft.TextField(
        label="entrada",
        multiline=True,
        min_lines=10,
        max_lines=1000,
        expand=True,
        border_color=ft.colors.BLUE_GREY_500,
        text_size=20,
        label_style=ft.TextStyle(color=ft.colors.GREEN_500),
        text_style=ft.TextStyle(font_family="consolas")
    )

    salida = ft.Text(value="", selectable=True, size=14)
    
    def compilar(e):
        text = entrada.value
        tokens = analisis_lexico(text)
        tipo = analisis_sintactico(tokens)
        valido = analisis_semantico(tipo)

        output = []
        output.append("🧩 Fase 1 - Léxico:\n" + str(tokens))
        output.append("🔧 Fase 2 - Sintáctico:\n" + tipo)
        
        if not valido:
            output.append("🧠 Fase 3 - Semántico:\n❌ Entrada ofensiva detectada.")
            output.append("🚫 Compilación detenida.")
        else:
            output.append(f"🧠 Fase 3 - Semántico:\n✔️ Entrada válida.")
            
        intermedio = generar_codigo_intermedio(tipo, tokens)
        objeto = generar_codigo_objeto(tipo, tokens)
        output.append(f"🛠️ Fase 4 - Código Intermedio:\n {intermedio}" )
        output.append(f"🏗️ Fase 5 - Código Objeto:\n {objeto}")
        output.append(f"✅ Compilación finalizada.")

        salida.value = "\n\n".join(output)
        page.update()

    page.add(
        ft.Text("Mini Compilador en Flet", size=24, weight="bold"),
        entrada,
        ft.ElevatedButton("Compilar", on_click=compilar),
      
        salida
    )

ft.app(target=main)

