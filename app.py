import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tempfile
from matplotlib import rc
import base64
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Segunda Ley de Newton", page_icon="🚀")

# Título de la aplicación
st.title("🚀 Segunda Ley de Newton: Fuerza = Masa × Aceleración")

# Sidebar para los inputs
with st.sidebar:
    st.header("Parámetros de Entrada")
    opcion = st.radio("Modo de uso:", 
                     ["Ejemplo Práctico", "Simulación Personalizada"])
    
    if opcion == "Ejemplo Práctico":
        st.subheader("Problema Práctico")
        st.write("""
        **Situación:** Un trabajador empuja una caja en una superficie sin fricción.
        
        **Pregunta:** ¿Cuál será la aceleración de la caja y qué distancia recorrerá en 5 segundos?
        """)
        masa_ejemplo = st.number_input("Masa de la caja (kg)", min_value=0.1, value=10.0, step=0.5)
        fuerza_ejemplo = st.number_input("Fuerza aplicada por el trabajador (N)", min_value=0.1, value=50.0, step=1.0)
        tiempo_ejemplo = st.slider("Tiempo de observación (s)", 1, 10, 5)
    else:
        masa = st.number_input("Masa del objeto (kg)", min_value=0.1, value=1.0, step=0.1)
        fuerza = st.number_input("Fuerza aplicada (N)", min_value=0.1, value=1.0, step=0.1)
        tiempo_simulacion = st.slider("Tiempo de simulación (s)", 1, 10, 5)

# Contenido principal
if opcion == "Ejemplo Práctico":
    # Cálculos para el ejemplo práctico
    aceleracion_ejemplo = fuerza_ejemplo / masa_ejemplo
    distancia_ejemplo = 0.5 * aceleracion_ejemplo * tiempo_ejemplo**2
    
    st.subheader("Solución al Problema Práctico")
    
    st.markdown(f"""
    **Datos del problema:**
    - Masa de la caja: {masa_ejemplo} kg
    - Fuerza aplicada: {fuerza_ejemplo} N
    - Tiempo de observación: {tiempo_ejemplo} s
    
    **Paso 1:** Aplicar la Segunda Ley de Newton para calcular la aceleración
    
    $$
    a = \\frac{{F}}{{m}} = \\frac{{{fuerza_ejemplo}\\,N}}{{{masa_ejemplo}\\,kg}} = {aceleracion_ejemplo:.2f}\\,m/s²
    $$
    
    **Paso 2:** Calcular la distancia recorrida con aceleración constante
    
    $$
    d = \\frac{{1}}{{2}} a t^2 = \\frac{{1}}{{2}} \\times {aceleracion_ejemplo:.2f}\\,m/s² \\times ({tiempo_ejemplo}\\,s)^2 = {distancia_ejemplo:.2f}\\,m
    $$
    
    **Conclusión:** La caja acelerará a **{aceleracion_ejemplo:.2f} m/s²** y recorrerá **{distancia_ejemplo:.2f} metros** en {tiempo_ejemplo} segundos.
    """)
    
    # Gráfico para el ejemplo práctico
    st.subheader("Visualización del Movimiento")
    
    tiempo = np.linspace(0, tiempo_ejemplo, 100)
    velocidad = aceleracion_ejemplo * tiempo
    distancia = 0.5 * aceleracion_ejemplo * tiempo**2
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Gráfico de velocidad
    ax1.plot(tiempo, velocidad, 'r-', linewidth=2)
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Velocidad (m/s)')
    ax1.set_title('Velocidad de la caja en el tiempo')
    ax1.grid(True)
    
    # Gráfico de distancia
    ax2.plot(tiempo, distancia, 'g-', linewidth=2)
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Distancia (m)')
    ax2.set_title('Distancia recorrida por la caja')
    ax2.grid(True)
    
    st.pyplot(fig)
    
    # Animación del ejemplo práctico
    st.subheader("Simulación del Movimiento de la Caja")
    
    fig_anim, ax_anim = plt.subplots(figsize=(10, 3))
    max_dist = 0.5 * aceleracion_ejemplo * tiempo_ejemplo**2
    ax_anim.set_xlim(0, max_dist * 1.2)
    ax_anim.set_ylim(-0.5, 0.5)
    ax_anim.set_xlabel('Posición (m)')
    ax_anim.get_yaxis().set_visible(False)
    ax_anim.set_title('Movimiento de la Caja')
    
    caja = plt.Rectangle((0, -0.2), 0.4, 0.4, fc='brown')
    ax_anim.add_patch(caja)
    
    def init():
        caja.set_xy((0, -0.2))
        return caja,
    
    def animate(i):
        x = 0.5 * aceleracion_ejemplo * (i/20)**2
        caja.set_xy((x, -0.2))
        return caja,
    
    try:
        anim = FuncAnimation(fig_anim, animate, frames=tiempo_ejemplo * 20,
                             init_func=init, blit=True, interval=50)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmpfile:
            anim.save(tmpfile.name, writer='pillow', fps=20, dpi=100)
            tmpfile.seek(0)
            st.image(tmpfile.name, caption=f'Animación: Caja de {masa_ejemplo}kg empujada con {fuerza_ejemplo}N')
    
    except Exception as e:
        st.warning(f"No se pudo generar la animación: {e}")
    
else:
    # Código original para la simulación personalizada
    aceleracion = fuerza / masa
    
    st.subheader("Resultados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Masa", f"{masa} kg")
    col2.metric("Fuerza", f"{fuerza} N")
    col3.metric("Aceleración", f"{aceleracion:.2f} m/s²")
    
    st.subheader("Gráfico de Aceleración vs Tiempo")
    tiempo = np.linspace(0, tiempo_simulacion, 100)
    velocidad = aceleracion * tiempo
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(tiempo, velocidad, 'b-', linewidth=2)
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Velocidad (m/s)')
    ax.set_title('Velocidad del objeto en el tiempo')
    ax.grid(True)
    st.pyplot(fig)
    
    st.subheader("Simulación del Movimiento")
    st.write("Representación del objeto acelerando:")
    
    fig_anim, ax_anim = plt.subplots(figsize=(10, 3))
    ax_anim.set_xlim(0, tiempo_simulacion * aceleracion * 1.2)
    ax_anim.set_ylim(-0.5, 0.5)
    ax_anim.set_xlabel('Posición (m)')
    ax_anim.get_yaxis().set_visible(False)
    ax_anim.set_title('Movimiento del Objeto')
    
    objeto = plt.Rectangle((0, -0.2), 0.3, 0.4, fc='blue')
    ax_anim.add_patch(objeto)
    
    def init():
        objeto.set_xy((0, -0.2))
        return objeto,
    
    def animate(i):
        x = 0.5 * aceleracion * (i/20)**2
        objeto.set_xy((x, -0.2))
        return objeto,
    
    try:
        anim = FuncAnimation(fig_anim, animate, frames=tiempo_simulacion * 20,
                             init_func=init, blit=True, interval=50)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmpfile:
            anim.save(tmpfile.name, writer='pillow', fps=20, dpi=100)
            tmpfile.seek(0)
            st.image(tmpfile.name, caption='Animación del movimiento')
    
    except Exception as e:
        st.warning(f"No se pudo generar la animación: {e}")

# Explicación teórica (común para ambos modos)
st.subheader("Explicación Científica")
st.markdown("""
La **Segunda Ley de Newton** establece que:
            
$$
\\vec{F} = m \\times \\vec{a}
$$

Donde:
- $\\vec{F}$ es la fuerza neta aplicada (en Newtons, N)
- $m$ es la masa del objeto (en kilogramos, kg)
- $\\vec{a}$ es la aceleración resultante (en metros por segundo al cuadrado, m/s²)

**Relaciones importantes:**
1. Velocidad en función del tiempo (partiendo del reposo):
   $$
   v(t) = a \\times t
   $$
2. Posición en función del tiempo (partiendo del reposo y posición 0):
   $$
   x(t) = \\frac{1}{2} a t^2
   $$
""")

# Notas finales
st.info("""
💡 **Consejo:** En el modo "Ejemplo Práctico" puedes ver una aplicación real de la segunda ley. 
En el modo "Simulación Personalizada" puedes experimentar con diferentes valores.
""")