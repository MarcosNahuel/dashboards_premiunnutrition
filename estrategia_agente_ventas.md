# Guia de Estrategia Comercial para el Agente IA (Zona FIT · Colombia)

## 1. Contexto del negocio
- GMV observado (sep-2024 a nov-2025): **COP 20.44 B** en **62,434** ordenes de **36,429** clientes.
- Ticket promedio: **COP 327k** (mediana 298k); canasta media de **3.79** lineas y **5.03** unidades por orden.
- Descuentos: **COP 5.31 B** (23.9 % del subtotal); 92.8 % de las ordenes incluyen descuento.
- Envio cobrado en 14.9 % de las ordenes (promedio COP 8.8k); top ciudades por GMV: Bogota (COP 4.97 B), Medellin (1.70 B), Cali (0.75 B).
- Ultimos 90 dias concentran 25.1 % del GMV; picos semanales martes-jueves y horarios de 09h-17h.

## 2. Tendencias del mercado colombiano de suplementos
- Mercado nacional en crecimiento ~**6 % anual**, con ventas ~US$133 M en 2022 y proyeccion >US$160 M para 2027.
- Proteinas en polvo y creatina concentran ~50 % del volumen deportivo; importaciones de proteinas con +15 % anual.
- Segmentos en expansion: mass gainers, pre entrenos/aminoacidos, control de peso (CLA) y bienestar integral (vitaminas, colageno, omega).
- 45 % de los colombianos declaran consumo reciente de suplementos; mas de 2 millones asisten a gimnasios, priorizando hipertrofia, energia y definicion.
- 88 % de los adultos ya compran online; el consumidor valora autenticidad, precio por porcion y asesoria especializada.

## 3. Perfil y segmentacion accionable
- **Demografico principal:** 20-35 anos, nativos digitales, orientados a resultados, sensibles a promociones pero exigentes con la calidad.
- **Segmentacion RFM interna:**
  - **Leal (27.5 % clientes / 51.4 % GMV):** compras recurrentes, ticket alto; responder con exclusividad y lanzamientos anticipados.
  - **Activo (32.0 % / 23.6 %):** ciclo regular; priorizar upsell (isolate, wellness) y fidelizacion.
  - **En riesgo (5.9 % / 7.5 %):** grandes tickets pero menor frecuencia reciente; activar recordatorios de ciclo y asesorias.
  - **Churn (34.1 % / 17.1 %):** requieren win-back con mensajes de valor antes de incentivos.
- **Segmentos por objetivo** (extraidos del mercado): volumen/masa, definicion, energia/rendimiento, bienestar integral, control de peso.

## 4. Portafolio prioritario para el agente
- **SKU hero (63 % del GMV top-10):** Gold Standard 100 % Whey, Creatine Powder Micronized, ISO 100, BiPro Classic, Platinum 100 % Creatine. Garantizar narrativa de autenticidad, resultados y disponibilidad.
- **Ejes de categoria:**
  - Proteina de suero (29 % del revenue) y aisladas (11 %): diferenciar por velocidad de absorcion, lactosa, sabor.
  - Creatina (24.7 %): explicar beneficios (fuerza, recuperacion), seguridad y evidencia.
  - Mass gainers (7.2 %): recomendar a clientes de volumen/ektomorfos.
  - CLA y wellness (5.3 % + 11 % resto): posicionar como apoyo a definicion, salud femenina, energia diaria.
- **Bundles recomendados:**
  - Whey + Creatina + CLA (definicion tonificada).
  - Whey + Aminoacidos + Vitaminas (energia y recuperacion completa).
  - Mass gainer + Pre entreno + Creatina (ciclo de volumen).
  - Pack premium isolate + Omega + Multivitaminico (clientes leales de ticket alto).

## 5. Politica de descuentos y promociones
- Mantener descuentos como palanca pero modular intensidad:
  - **Leal/Activo:** priorizar beneficios no monetarios (puntos, acceso VIP, bundles exclusivos). Usar descuentos target <15 % para proteger margen.
  - **En riesgo/Churn:** aplicar descuentos escalonados (10/15/20 %) segun respuesta, siempre con fecha limite y asesoria.
- Comunicar **precio por porcion** y comparativas entre formatos (ej. 5 lb vs 2 lb) para justificar valor.
- Promover envio gratis desde COP 300k; reforzar durante conversaciones con canastas medianas (2-3 SKU) para empujar a 4+ SKU.

## 6. Playbook conversacional del agente
1. **Diagnostico rapido:** objetivo (masa, definicion, bienestar), nivel de entrenamiento, restricciones dietarias, presupuesto.
2. **Validacion de confianza:** resaltar autenticidad de Zona FIT, stock actualizado y experiencia digital segura.
3. **Propuesta base:** recomendar SKU hero alineado al objetivo + explicar beneficios concretos (ganancia muscular, recuperacion, energia).
4. **Cross-sell guiado:** sugerir complementos (creatina, aminoacidos, wellness) que suben unidades por orden, justificando sinergias.
5. **Gestor de objeciones:** usar datos (ahorro por porcion, 4.97 B en ventas Bogota, 93 % de ordenes con descuentos) para demostrar relevancia y respaldo.
6. **Cierre con incentivo:** ofrecer bundle, beneficio de fidelidad o envio gratis segun segmento; dejar CTA claro (checkout, agendar recordatorio).
7. **Seguimiento:** programar recordatorio segun ciclo (30/60/90 dias) y segmento RFM; incentivar testimonios o referidos.

## 7. Acciones tacticas calendarizadas
- Automatizar mensajes martes-jueves 09h-17h con ofertas segmentadas (email/SMS/push).
- Campanas geolocalizadas para Bogota y Medellin (pickup acelerado, eventos en gimnasios aliados).
- Revisar alertas de inventario para top 25 SKU (evitar quiebres que afectan >30 % GMV diario).
- Integrar scripts de contenido educativo (microdosificacion, comparativas de proteina/creatina) en conversaciones y RRSS.

## 8. Indicadores de control continuo
- GMV semanal y crecimiento 30/90 dias.
- % ordenes con ≥4 SKU y unidades promedio (meta ≥5.2).
- Descuento efectivo por segmento RFM y margen por bundle.
- Participacion de los SKU hero (objetivo ≥60 %).
- Retencion M1/M2 y conversion de campañas de win-back.
- AOV por franja horaria y tasa de respuesta de automatizaciones.

---
**Implementacion:** mantener actualizado el pipeline `python analyze_bulk_data.py` para refrescar datos internos y ajustar guiones del agente conforme varien los indicadores del negocio y el mercado colombiano.
