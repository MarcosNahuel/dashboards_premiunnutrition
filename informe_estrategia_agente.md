# Estrategia Comercial para el Agente IA · Premium Nutrition (Zona FIT)

## 1. Alcance del análisis
- **Fuente primaria:** `bulk_definitivo.json` de Shopify → transformado a `bulk_orders.csv` (62.434 órdenes) y `bulk_line_items.csv` (236.451 líneas).
- **Horizonte temporal:** 10-sep-2024 al 2-nov-2025 (fechas convertidas a América/Bogotá).
- **Cobertura de clientes:** 36.429 registros únicos con `customer_id`.
- **Artefactos generados:** `analysis_outputs/` (KPIs, top productos/categorías, series temporales, basket shape, RFM).
- **Limitaciones:** inconsistencias menores de codificación (acentos) y columnas mixtas (Shopify), sin impacto material en métricas; los impuestos se reportan en cero.

## 2. Indicadores clave del negocio
- **GMV** COP **20.44 B**; **órdenes** 62.434; **clientes** 36.429.
- **Ticket promedio (AOV)** COP **327k** (mediana 298k); **líneas promedio** 3.79; **unidades promedio** 5.03.
- **Descuentos** COP **5.31 B** ⇒ **23.9 %** del subtotal; **92.8 %** de órdenes con descuento.
- **Envío cobrado** en 14.9 % de órdenes; ticket con envío promedio COP 8.8k.
- **Concentración de catálogo:** 25 SKU top explican ~79 % del GMV; top 5 → 45 %.
- **Momento comercial:** 25.1 % del GMV se generó en los últimos 90 días; 6.8 % en los últimos 30 días.

## 3. Estructura de la canasta y comportamiento de compra
- Sólo **19.9 %** de las órdenes son monoproducto; **45.0 %** incluyen ≥4 líneas ⇒ amplio potencial de cross-sell.
- Descuento medio por orden: **−23.9 %** sobre el subtotal, con correlación alta entre tamaño de orden y descuento aplicado.
- **Mix de categorías (share de revenue):**
  - Proteínas de suero: **29.0 %**
  - Creatinas (Rendimiento y Energía): **24.7 %**
  - Proteínas isolate/hidrolizadas: **11.3 %**
  - Mass gainers: **7.2 %**
  - CLA (Control de peso): **5.3 %**
  - Resto del catálogo: 22.5 %
- **Top SKU (share GMV):**
  1. Gold Standard 100% Whey ON — 19.9 %
  2. Creatine Powder Micronized ON — 12.5 %
  3. ISO 100 Dymatize — 7.9 %
  4. BiPro Classic Megaplex — 4.9 %
  5. Platinum 100% Creatine Muscletech — 3.7 %
  (Top 10 acumulado ≈ 63 %)

## 4. Segmentación de clientes (RFM)
- **Leal (27.5 % de clientes / 51.4 % del GMV):** alta frecuencia y monetización; foco en exclusividad, prioridad de inventario y bundles premium.
- **Activo (32.0 % / 23.6 %):** ciclo regular; oportunidad de upsell (isolate, wellness) y programas de referidos.
- **En riesgo (5.9 % / 7.5 %):** tickets altos (COP ~710k); requiere campañas de retención con asesoría personalizada y recompra asistida.
- **Churn (34.1 % / 17.1 %):** reactivaciones escalonadas con oferta de valor y testimoniales, evitando descuentos agresivos de entrada.
- **Nuevo/potencial (0.5 % / 0.3 %):** secuencia de bienvenida con scripts del agente centrados en educar por objetivos.

## 5. Dinámica temporal y geográfica
- **Días pico:** Martes (COP 3.67 B) y Miércoles (COP 3.37 B), seguidos por Jueves (COP 3.32 B). Fin de semana cae ~40 % vs martes.
- **Horas pico:** 09 h–17 h concentran >60 % del revenue; máximos a las 11 h, 15 h, 17 h.
- **Top ciudades (normalizadas):** Bogotá 4.97 B, Medellín 1.70 B, Cali 0.75 B, Barranquilla 0.69 B, Bucaramanga 0.64 B. Resto con cola larga.

## 6. Insight profundos para el agente IA
1. **Dominio de proteínas y creatinas:** discursos y guiones deben priorizar autenticidad, beneficios diferenciados, comparativas (whey vs isolate) y stacks complementarios.
2. **Cross-sell estructurado:** con 80 % de órdenes multiproducto, diseñar “recetas” (proteína + creatina + wellness) y recomendar presentaciones grandes en clientes Leales.
3. **Gestión inteligente de descuentos:** migrar parte del incentivo a beneficios de fidelidad, puntos o contenido exclusivo; reservar descuentos altos para cohortes En Riesgo/Churn con seguimiento posterior.
4. **Estrategia de envío:** comunicar umbral de envío gratis (≥COP 300k) en interacciones para convertir canastas medianas y reducir fricción en órdenes pequeñas.
5. **Cadencia de comunicación:** activar automatizaciones martes‑jueves, 09‑17h, combinando email/SMS/notificaciones. En fines de semana, enfocarse en campañas de awareness o retos.
6. **Segmentación geográfica:** habilitar mensajes de disponibilidad, eventos o alianzas con gimnasios en Bogotá y Medellín; explorar fulfillment acelerado en estas plazas.
7. **Playbook RFM para el agente:**
   - *Leal:* acceso anticipado y comunidad VIP → reforzar exclusividad.
   - *Activo:* sugerir upgrades (isolate, stacks wellness) y programas referidos.
   - *En Riesgo:* recordatorios de ciclos (30/60/90 días), combos premium con asesoría.
   - *Churn:* historias de éxito + garantía de autenticidad antes de ofrecer incentivo.
8. **Planificación de inventario:** monitorear los top 25 SKU con alertas de stock; 1 día de fallas en Gold Standard o Creatine Micronized impacta ~32 % del GMV diario.

## 7. Plan de acción propuesto
| Horizonte | Iniciativas clave | Responsable sugerido |
|-----------|-------------------|----------------------|
| **0‑15 días** | Implementar dashboards con artefactos `analysis_outputs/`; entrenar al agente en guiones por segmento y objetivo; definir umbral de envío gratis y script asociado. | Data / CX |
| **15‑45 días** | Lanzar automatizaciones martes‑jueves (email/SMS) segmentadas RFM; configurar bundles inteligentes en Shopify; crear secciones de “Stacks recomendados” y “Top 5 héroes”. | CRM / E-commerce |
| **45‑90 días** | Medir uplift por segmento; afinar programa de fidelidad sin descuentos; explorar eventos presenciales Bogotá/Medellín; evaluar attach-rate para recomendaciones dinámicas. | Marketing / Ventas |

## 8. Indicadores para seguimiento continuo
- GMV semanal y tasa de crecimiento (últimos 30/90 días).
- % órdenes con ≥4 SKU y unidades promedio (meta ≥5.2).
- Descuento efectivo promedio por segmento RFM.
- Participación de los 10 SKU hero (debe mantenerse ≥60 %).
- Retención M1/M2 de cohortes recientes y conversión de campañas de win-back.
- AOV y revenue por franja horaria tras la implementación de automatizaciones.

## 9. Próximos desarrollos analíticos
- Generar vistas SQL (`v_orders_daily`, `v_top_products`, `v_basket_shape`) para explotación BI.
- Construir gráficos requeridos (series, estacionalidad, pareto, basket) en `analysis_outputs`.
- Profundizar en attach-rate y afinidad de SKU una vez estructurada la tabla `order_items`.
- Normalizar geocodificación y categorías para reporting operativo y modelos predictivos.

---
**Referencia rápida:** los CSV y JSON mencionados se encuentran en `dashboards_premiunnutrition/analysis_outputs/`. Ejecutar `python analyze_bulk_data.py` para regenerar métricas con un nuevo corte de datos.
