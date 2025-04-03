def get_message():
    """
    Servicio simple que retorna un mensaje con el párrafo y las proposiciones lógicas
    """
    parrafo = """Si tuvieran que justificarse ciertos hechos por su enorme tradición entonces, si 
estos hechos son inofensivos y respetan a todo ser viviente y al medio ambiente, no 
habría ningún problema. Pero si los hechos son bárbaros o no respetuosos con los 
seres vivientes o el medio ambiente, entonces habría que dejar de justificarlos o no 
podríamos considerarnos dignos de nuestro tiempo."""

    proposiciones = [
        "p: justificar hechos por su tradición.",
        "q: ser inofensivo.",
        "r: ser respetuoso con los seres vivos.",
        "s: ser respetuoso con el medio ambiente.",
        "t: tener problemas.",
        "¬q: ser bárbaro. (= no ser inofensivo)",
        "u: ser digno de nuestro tiempo."
    ]
    
    # Generar la expresión lógica - llamamos a la función calculos con los parámetros
    expresion = calculos(parrafo, proposiciones)
    
    return {
        "parrafo": parrafo,
        "proposiciones": proposiciones,
        "expresion_logica": expresion
    }

def calculos(parrafo, lista_proposiciones):
    # Split the paragraph into parts
    partes = parrafo.rsplit('.', parrafo.count('.'))
    
    # Clean the parts and count them
    partes = [parte.strip() for parte in partes if parte.strip()]
    cantidad_partes = len(partes)
    
    # Print the number of parts (for debugging)
    print(f"Número de partes encontradas: {cantidad_partes}")
    print(f"Partes del párrafo: {partes}")
    
    # Create lists for symbols and sentences
    valores = []
    oraciones = []
    
    # Extract symbols and sentences from propositions
    for prop in lista_proposiciones:
        if ":" in prop:
            simbolo, oracion = prop.split(":", 1)
            simbolo = simbolo.strip()
            oracion = oracion.strip().rstrip('.')
            
            # Clean any additional text in parentheses
            if "(" in oracion:
                oracion = oracion.split("(")[0].strip()
            
            valores.append(simbolo)
            oraciones.append(oracion)
    
    print(f"Símbolos extraídos: {valores}")
    print(f"Oraciones extraídas: {oraciones}")
    
    # Create a dictionary of propositions for easier lookup
    proposiciones = {}
    for i in range(len(valores)):
        proposiciones[valores[i]] = oraciones[i]
    
    print(f"Diccionario de proposiciones: {proposiciones}")
    
    # Analizar la estructura del párrafo
    primera_parte = None
    segunda_parte = None
    
    for i, parte in enumerate(partes):
        if parte.lower().strip().startswith("si"):
            primera_parte = parte
        elif parte.lower().strip().startswith("pero"):
            segunda_parte = parte
    
    print(f"Primera parte identificada: {primera_parte}")
    print(f"Segunda parte identificada: {segunda_parte}")
    
    resultado = ""
    
    # Analizar la primera parte
    if primera_parte:
        print("\n--- ANALIZANDO PRIMERA PARTE ---")
        # Encontrar el símbolo para la primera parte
        simbolo_p = None
        mejor_puntuacion = 0
        
        for simbolo, significado in proposiciones.items():
            palabras_significado = significado.lower().split()
            puntuacion = 0
            
            for palabra in palabras_significado:
                if len(palabra) > 3 and palabra in primera_parte.lower():
                    puntuacion += 1
                    print(f"Palabra '{palabra}' de símbolo '{simbolo}' encontrada en primera parte")
            
            print(f"Símbolo '{simbolo}' tiene puntuación: {puntuacion}")
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                simbolo_p = simbolo
        
        print(f"Símbolo principal para primera parte: {simbolo_p}")
        
        # Encontrar símbolos para condiciones
        simbolos_condicion = []
        for simbolo, significado in proposiciones.items():
            if simbolo != simbolo_p:  # No repetir el primer símbolo
                palabras_significado = significado.lower().split()
                for palabra in palabras_significado:
                    if len(palabra) > 3 and palabra in primera_parte.lower():
                        print(f"Condición: palabra '{palabra}' de símbolo '{simbolo}' encontrada en primera parte")
                        simbolos_condicion.append(simbolo)
                        break
        
        print(f"Símbolos de condición encontrados: {simbolos_condicion}")
        
        # Encontrar símbolo para "problema"
        simbolo_problema = None
        for simbolo, significado in proposiciones.items():
            if "t" == simbolo:  # Asumimos que t es el símbolo para problemas
                simbolo_problema = simbolo
                break
        
        print(f"Símbolo para problema: {simbolo_problema}")
        
        # Construir la primera parte de la expresión
        if simbolo_p and simbolos_condicion and simbolo_problema:
            condicion_expr = " ∧ ".join(simbolos_condicion)
            if len(simbolos_condicion) > 1:
                condicion_expr = f"( {condicion_expr} )"
            
            resultado = f"{simbolo_p} → [ {condicion_expr} → ¬{simbolo_problema} ]"
            print(f"Expresión primera parte: {resultado}")
    
    # Analizar la segunda parte
    if segunda_parte:
        print("\n--- ANALIZANDO SEGUNDA PARTE ---")
        # Encontrar símbolos para condiciones negadas
        simbolos_negados_condicion = []
        
        # Buscar símbolos que aparecen en la segunda parte
        antecedente_segunda = segunda_parte.lower().split("entonces")[0] if "entonces" in segunda_parte.lower() else segunda_parte.lower()
        print(f"Antecedente de segunda parte: {antecedente_segunda}")
        
        for simbolo, significado in proposiciones.items():
            palabras_significado = significado.lower().split()
            for palabra in palabras_significado:
                if len(palabra) > 3 and palabra in antecedente_segunda:
                    print(f"Palabra '{palabra}' de símbolo '{simbolo}' encontrada en antecedente de segunda parte")
                    # Si hay negación en el texto o el símbolo ya está negado
                    if "no" in antecedente_segunda or simbolo.startswith("¬"):
                        if simbolo.startswith("¬"):
                            simbolos_negados_condicion.append(simbolo)
                            print(f"Símbolo ya negado: {simbolo}")
                        else:
                            simbolos_negados_condicion.append(f"¬{simbolo}")
                            print(f"Negando símbolo: ¬{simbolo}")
                    else:
                        simbolos_negados_condicion.append(simbolo)
                        print(f"Símbolo sin negar: {simbolo}")
                    break
        
        print(f"Símbolos de condición negados: {simbolos_negados_condicion}")
        
        # Encontrar símbolos para consecuencia
        simbolos_consecuencia = []
        
        # Buscar símbolos que aparecen en la consecuencia
        consecuencia = segunda_parte.lower().split("entonces")[1] if "entonces" in segunda_parte.lower() else ""
        print(f"Consecuencia de segunda parte: {consecuencia}")
        
        for simbolo, significado in proposiciones.items():
            palabras_significado = significado.lower().split()
            for palabra in palabras_significado:
                if len(palabra) > 3 and consecuencia and palabra in consecuencia:
                    print(f"Palabra '{palabra}' de símbolo '{simbolo}' encontrada en consecuencia")
                    # Si hay negación en el texto, verificar dinámicamente
                    negacion_presente = False
                    for palabra_negativa in ["no", "ni", "sin"]:
                        if palabra_negativa in consecuencia:
                            negacion_presente = True
                            print(f"Palabra negativa '{palabra_negativa}' encontrada en consecuencia")
                            break
                    
                    if negacion_presente:
                        simbolos_consecuencia.append(f"¬{simbolo}")
                        print(f"Negando símbolo en consecuencia: ¬{simbolo}")
                    else:
                        simbolos_consecuencia.append(simbolo)
                        print(f"Símbolo en consecuencia sin negar: {simbolo}")
                    break
        
        print(f"Símbolos de consecuencia: {simbolos_consecuencia}")
        
        # Construir la segunda parte de la expresión
        if simbolos_negados_condicion and simbolos_consecuencia:
            condicion_expr = " ∨ ".join(simbolos_negados_condicion)
            if len(simbolos_negados_condicion) > 1:
                condicion_expr = f"({condicion_expr})"
            
            consecuencia_expr = " ∨ ".join(simbolos_consecuencia)
            if len(simbolos_consecuencia) > 1:
                consecuencia_expr = f"( {consecuencia_expr} )"
            
            segunda_expr = f"[ {condicion_expr} → {consecuencia_expr} ]"
            print(f"Expresión segunda parte: {segunda_expr}")
            
            # Unir con la primera parte
            if resultado:
                resultado = f"{resultado} ∧ {segunda_expr}"
            else:
                resultado = segunda_expr
    
    print(f"\nRESULTADO FINAL: {resultado}")
    return resultado