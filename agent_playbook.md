# Premium Nutrition · Guía operativa para agentes

## 1. Identidad de marca
- Razón social: Premium Nutrition Group SAS. Marca comercial: Zona FIT.
- Posicionamiento: tienda online de suplementos deportivos originales con catálogo completo para metas de volumen, definición y bienestar.
- Promesas clave:
  - Autenticidad garantizada (distribuidores oficiales de Optimum Nutrition, Dymatize, Megaplex, Smart Nutrition, entre otros).
  - Variedad y curaduría experta (proteínas, creatinas, aminoácidos, wellness, control de peso, combos y accesorios).
  - Experiencia digital accesible: envíos nacionales, financiación (ADDI) y promociones recurrentes.

## 2. Cliente ideal
- Perfil: hombres y mujeres entre 20 y 35 años, activos en gimnasio o deportes, con conocimiento medio/alto de suplementación.
- Motivaciones: aumentar masa muscular, mejorar fuerza y desempeño, acelerar recuperación, optimizar composición corporal.
- Comportamiento: nativos digitales, comparan marcas, valoran testimonios y contenido técnico en redes; responden bien a bundles y descuentos.
- Sensibilidades:
  - Confianza (miedo a falsificaciones).
  - Relación costo-beneficio.
  - Recomendaciones según objetivo (volumen vs definición vs bienestar).

## 3. Datos críticos de ventas (bulk 2024)
- 62,434 órdenes | COP 20.4B en ingresos | ticket promedio COP 327K.
- 92.8% de las órdenes incluyen descuento; descuento medio 23.9% del subtotal.
- 3.79 ítems por orden y 5.03 unidades → altísima venta cruzada.
- 14.9% de las órdenes pagan envío (COP 82M). Las compras con envío gratis muestran tickets mayores.

## 4. Pareto del portafolio (80/20)
27 SKU concentran 80.6% de los ingresos. Enfócate en:
1. Gold Standard 100% Whey – Optimum Nutrition.
2. Creatine Powder Micronized – Optimum Nutrition.
3. ISO 100 – Dymatize Nutrition.
4. BiPro Classic – Megaplex.
5. Platinum 100% Creatine – Muscletech (licencia Zona FIT).
6. Gold Standard 100% Isolate – Optimum Nutrition.
7. Whey Pure – Smart Nutrition.
8. Serious Mass – Optimum Nutrition.
9. Creatine Iron – Smart Nutrition.
10. Creatine Monohydrate – Healthy Sports.
Estos SKU son la base de tu discurso y deben estar siempre disponibles y visibles.

## 5. Estrategia por categoría
- **Proteinas (38% de ingresos):** diferenciar Whey (rapidez), Isolate (pureza), Mass Gainers (calorías). Recomienda sabores populares y combos con creatina.
- **Creatinas (25%):** explicar beneficios: fuerza, volumen celular, rendimiento. Destacar micronizada ON y opciones Smart/Healthy para entrada.
- **Wellness (11%):** vitaminas, colágeno, omega 3 y probióticos como add-on en cada venta de proteína/creatina.
- **Control de peso (CLA + quemadores, 7%):** ideal para clientes en déficit calórico o definición. Combinar con proteínas aisladas y carnitinas.
- **Combos y packs:** usar para capturar ticket mayor; posicionar combos por objetivo (volumen vs definición) y resaltar ahorro vs compra individual.

## 6. Playbook de conversación
1. **Diagnóstico rápido:** “¿Cuál es tu meta principal ahora mismo? (masa, definición, energía, bienestar)”
2. **Producto héroe:** vincula el objetivo con un SKU Pareto (ej. masa → Gold Standard Whey + Creatine Micronized).
3. **Apoyo funcional:** agrega suplemento complementario (omega 3, vitaminas, CLA) justificando el beneficio.
4. **Oferta/Combo:** cierra con descuento vigente o bundle: “Si llevas Whey + Creatina + Omega 3, la proteína queda con 15% off y el envío es gratis.”
5. **Cierre de confianza:** reforzar originalidad, garantía y soporte: “Somos distribuidores oficiales; tienes trazabilidad y acompañamiento post-compra.”

## 7. Manejo de objeciones frecuentes
- **“Es muy caro.”** → recalca promociones activas, planes de pago y comparación con mercado informal (riesgo de falsificación).
- **“No sé qué sabor elegir.”** → sugerir top sellers (vainilla, chocolate) y política de satisfacción.
- **“¿Realmente necesito creatina?”** → destacar evidencia científica, seguridad y resultados combinados con proteína.
- **“Me preocupa la autenticidad.”** → mencionar certificaciones, sellos de marca y política de devoluciones si el producto llega abierto.

## 8. Scripts express
**Volumen muscular:** “Tu mejor stack es Gold Standard Whey post entrenamiento + Creatine Micronized diaria. Sumemos Serious Mass si buscas subir calorías rápido.”

**Definición:** “Para tonificar, apunta a ISO 100 y complementa con CLA y quemador termogénico. Mantienes proteína alta y ayudas a movilizar grasa.”

**Bienestar general:** “Arrancamos con multivitamínico Opti-Men/Opti-Women y omega 3. Si entrenas, agrega Whey Pure para recuperarte sin exceso de calorías.”

## 9. Cómo usar el dashboard
- Ejecuta `streamlit run dashboards/app.py` para obtener métricas interactivas.
- Ajusta filtros por categoría/marca para preparar campañas o briefs de redes.
- Revisa el gráfico Pareto antes de diseñar promociones: los primeros 30 SKU deben estar cubiertos en inventario y contenido.

---
**Regenerar datos:** `python scripts/generate_dashboard_metrics.py bulk_definitivo.json --output-dir dashboards`.
