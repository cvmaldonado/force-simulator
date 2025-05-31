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
    masa = st.number_input("Masa del objeto (kg)", min_value=0.1, value=1.0, step=0.1)
    fuerza = st.number_input("Fuerza aplicada (N)", min_value=0.1, value=1.0, step=0.1)
    tiempo_simulacion = st.slider("Tiempo de simulación (s)", 1, 10, 5)

# Cálculos
aceleracion = fuerza / masa

# Mostrar resultados
st.subheader("Resultados")
col1, col2, col3 = st.columns(3)
col1.metric("Masa", f"{masa} kg")
col2.metric("Fuerza", f"{fuerza} N")
col3.metric("Aceleración", f"{aceleracion:.2f} m/s²")

# Gráfico de aceleración vs tiempo
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

# Animación del movimiento (versión simplificada para Streamlit)
st.subheader("Simulación del Movimiento")
st.write("Representación del objeto acelerando:")

# Crear una figura para la animación
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

# Guardar la animación como GIF
try:
    anim = FuncAnimation(fig_anim, animate, frames=tiempo_simulacion * 20,
                         init_func=init, blit=True, interval=50)

    # Crear un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmpfile:
        anim.save(tmpfile.name, writer='pillow', fps=20, dpi=100)
        tmpfile.seek(0)

        # Mostrar el GIF en Streamlit
        st.image(tmpfile.name, caption='Animación del movimiento')

except Exception as e:
    st.warning(f"No se pudo generar la animación: {e}")
    
# Explicación teórica
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

En esta simulación:
1. El objeto parte del reposo ($v_0 = 0$)
2. La aceleración es constante ($a = F/m$)
3. La velocidad aumenta linealmente con el tiempo ($v = a \\times t$)
4. La posición aumenta cuadráticamente con el tiempo ($x = \\frac{1}{2} a t^2$)
""")

# Notas finales
st.info("""
💡 **Consejo:** Prueba diferentes valores de masa y fuerza para observar cómo afectan 
a la aceleración del objeto. ¡Una mayor fuerza o menor masa resultará en mayor aceleración!
""")
    