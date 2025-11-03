# Dashboard comercial · Premium Nutrition (Zona FIT)

## 1. Contexto corporativo
- La razón social es **Premium Nutrition Group SAS**, pero la marca frente al cliente es **Zona FIT**, posicionada como la tienda online de suplementos deportivos más grande de Colombia.
- Propuesta de valor basada en (1) garantía de productos originales de marcas líderes, (2) catálogo curado que cubre metas de volumen, definición y bienestar, y (3) experiencia digital accesible con opciones de financiación.
- Audiencia principal: hombres y mujeres jóvenes-adultos (20-35 años), nativos digitales, orientados a resultados y sensibles a promociones, que dominan la jerga fitness y buscan asesoría experta.
- El sistema de clasificación vigente (ver `PROMPT_CLASIFICACION_MEJORADO.md`) agrupa el portafolio en Proteínas, Aminoácidos, Rendimiento y Energía, Control de Peso, Salud y Bienestar, Combos y Packs, y Accesorios.

## 2. Indicadores de ventas (Shopify bulk 2024)
- **Ingresos totales:** COP 20.4 mil millones con 62,434 órdenes registradas.
- **Ticket promedio:** COP 327,440; mediana COP 297,650.
- **Descuentos:** COP 5.3 mil millones; 92.8 % de las órdenes aplican algún descuento (descuento medio sobre subtotal ≈ 23.9 %).
- **Envíos:** 9,308 órdenes (14.9 %) generaron cobro de flete por COP 82.2 millones.
- **Mix de compra:** 3.79 ítems por orden y 5.03 unidades promedio (alto nivel de venta cruzada).

## 3. Productos líderes por ingresos
Ingresos expresados en miles de millones de COP (`COP B`):

| Producto | Marca | COP B | Unidades |
| --- | --- | ---: | ---: |
| Gold Standard 100% Whey Optimum Nutrition | Optimum Nutrition | 4.45 | 17,781 |
| Creatine Powder Micronized Optimum Nutrition | Optimum Nutrition | 2.79 | 21,364 |
| ISO 100 Dymatize Nutrition | Dymatize Nutrition | 1.76 | 4,982 |
| BiPro Classic Megaplex | Megaplex | 1.09 | 7,775 |
| Platinum 100% Creatine Muscletech | Zona FIT (lic.) | 0.82 | 5,567 |
| Gold Standard 100% Isolate Optimum Nutrition | Optimum Nutrition | 0.76 | 2,306 |
| Whey Pure Smart Nutrition | Smart Nutrition | 0.71 | 4,316 |
| Serious Mass Optimum Nutrition | Optimum Nutrition | 0.70 | 2,835 |
| Creatine Iron Smart Nutrition | Smart Nutrition | 0.56 | 5,623 |
| Creatine Monohydrate Healthy Sports | Healthy Sports | 0.55 | 7,103 |

**Claves:** Optimum Nutrition domina el ranking; la creatina (diferentes marcas) aparece en 4 de los 10 primeros SKU.

## 4. Pareto de productos
- El catálogo identificado incluye **2,068** productos (variantes).
- **Solo 27 productos (1.3 %) concentran 80.6 % del ingreso total.**
- El 20 % superior del catálogo (414 productos) acumula 99.7 % del ingreso, lo que indica una larga cola de bajo impacto.
- Top Pareto (primeros 5 SKU) están en proteínas de suero e isolatadas y creatinas de Optimum Nutrition, más BiPro Megaplex.

**Implicaciones para el agente:** concentrar esfuerzos comerciales y contenido en el núcleo reducido de SKU “estrella”, reforzar disponibilidad y bundles de estos productos y diseñar rutas de upselling desde los SKU de larga cola hacia los top performers.

## 5. Desempeño por categorías (reglas de clasificación propias)
- **Proteínas de suero:** 28.9 % de los ingresos (30,146 unidades). Base de alimentación de resultados musculares.
- **Creatina (Rendimiento y Energía):** 24.6 % y 50,181 unidades; es el segundo motor de ingresos y el de mayor volumen.
- **Proteínas aisladas/hidrolizadas:** 11.3 % del ingreso, ticket alto para consumidores premium.
- **Salud y bienestar – Otros suplementos:** 11.1 % (principalmente vitaminas, colágeno, probióticos).
- **Mass gainers:** 7.4 %; ideal para campañas de volumen/hiper-calóricas.
- **CLA (control de peso):** 5.4 % con 13,753 unidades; oportunidad de cross-sell con quemadores (1.98 % de ingresos).

Estas cifras respaldan priorizar comunicaciones en tres frentes: proteínas (diferenciar whey vs isolate vs mass gainers), creatinas y wellness (vitaminas/CLA) como líneas de soporte.

## 6. Correlaciones relevantes
- **Total vs subtotal:** correlación ≈ 1.0, confirmando integridad del dataset.
- **Total vs descuentos (0.86):** las órdenes de mayor ticket también concentran descuentos altos; el agente debe utilizar promociones como palanca de ticket promedio.
- **Total vs número de ítems (0.67) y unidades (0.65):** órdenes más grandes provienen de canastas amplias → priorizar bundles temáticos y scripts de venta cruzada.
- **Shipping vs total (-0.23) y vs ítems (-0.37):** los cobros de envío se asocian a órdenes más pequeñas; ofrecer umbrales de envío gratis puede impulsar volumen.
- **Impuesto:** sin variación (0), por lo que no aporta señal en correlaciones.

## 7. Recomendaciones para el agente estratégico
1. **Foco en héroes del portafolio:** automatizar respuestas destacando Gold Standard Whey, Creatine Micronized y ISO 100; asegurar scripts sobre autenticidad y beneficios diferenciales.
2. **Rutas de asesoría personalizadas:** usar las categorías del prompt de clasificación para guiar conversaciones (ej. identificar si el cliente busca masa, definición o bienestar y sugerir la categoría adecuada).
3. **Bundles y descuentos inteligentes:** dado el peso de los descuentos, sugerir combos (proteína + creatina, proteína + CLA) y aprovechar la alta elasticidad al precio.
4. **Capacitación en cross-sell:** promover complementos (vitaminas, omega 3) en cada venta de proteína/creatina para elevar unidades por orden.
5. **Promesas de valor clave:** reforzar en cada interacción los pilares de Zona FIT (producto original, amplitud de marcas, conveniencia digital) y segmentar mensajes según el nivel de experiencia del cliente.

---
**Archivos generados:** `metrics.json`, `orders_enriched.csv`, `products_aggregated.csv` y `category_breakdown.csv` contienen los datos de soporte para dashboards adicionales o entrenamiento del agente.
