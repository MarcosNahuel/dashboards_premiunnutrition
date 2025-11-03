#!/usr/bin/env python3
"""Streamlit dashboard for Premium Nutrition (Zona FIT) commercial insights."""

from __future__ import annotations

import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent


@st.cache_data
def load_data():
    metrics = json.loads((DATA_DIR / "metrics.json").read_text(encoding="utf-8"))
    categories = pd.read_csv(DATA_DIR / "category_breakdown.csv")
    products = pd.read_csv(DATA_DIR / "products_aggregated.csv")
    orders = pd.read_csv(DATA_DIR / "orders_enriched.csv", parse_dates=["created_at"])
    orders["created_at"] = pd.to_datetime(orders["created_at"], errors="coerce")
    orders.dropna(subset=["created_at"], inplace=True)
    return metrics, categories, products, orders


def format_currency(value: float) -> str:
    return f"COP {value:,.0f}".replace(",", ".")


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def build_monthly_series(orders: pd.DataFrame) -> pd.DataFrame:
    series = (
        orders.assign(month=lambda df: df["created_at"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["total_price"]
        .sum()
        .sort_values("month")
    )
    series["total_price_mm"] = series["total_price"] / 1_000_000
    return series


def build_pareto(products: pd.DataFrame) -> pd.DataFrame:
    ranked = products.sort_values("total_revenue", ascending=False).copy()
    ranked["revenue_share"] = ranked["total_revenue"] / ranked["total_revenue"].sum()
    ranked["cum_share"] = ranked["revenue_share"].cumsum()
    ranked["rank"] = range(1, len(ranked) + 1)
    return ranked


metrics, categories_df, products_df, orders_df = load_data()
monthly_df = build_monthly_series(orders_df)
pareto_df = build_pareto(products_df)

st.set_page_config(page_title="Premium Nutrition · Dashboard", layout="wide")

st.title("Premium Nutrition · Dashboard comercial")
st.caption(
    "Vista ejecutiva para Zona FIT con indicadores de ventas, pareto de productos y recomendaciones para agentes."
)

with st.sidebar:
    st.header("Contexto de negocio")
    st.markdown(
        """
**Zona FIT** (Premium Nutrition Group SAS) es la tienda online de suplementos deportivos
enfocada en autenticidad, amplitud de catálogo y conveniencia digital para atletas
colombianos.

**Pilares clave**
- Productos 100% originales de marcas líderes.
- Cobertura integral de metas: volumen, definición y bienestar.
- Experiencia e-commerce con financiación y promociones frecuentes.
"""
    )
    st.header("Filtros")
    category_filter = st.multiselect(
        "Filtrar por categoría", sorted(products_df["category"].dropna().unique().tolist())
    )
    vendor_filter = st.multiselect(
        "Filtrar por marca",
        sorted(products_df["vendor"].dropna().unique().tolist()),
        default=[],
    )

filtered_products = products_df.copy()
if category_filter:
    filtered_products = filtered_products[filtered_products["category"].isin(category_filter)]
if vendor_filter:
    filtered_products = filtered_products[filtered_products["vendor"].isin(vendor_filter)]

summary = metrics["summary"]

st.header("1. Resumen ejecutivo")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ingresos totales", format_currency(summary["total_revenue"]))
col2.metric("Órdenes", f"{summary['orders_total']:,}")
col3.metric("Ticket promedio", format_currency(summary["average_order_value"]))
col4.metric("Órdenes con descuento", format_percent(summary["orders_with_discount"] / summary["orders_total"]))

col5, col6, col7, col8 = st.columns(4)
col5.metric("Descuentos aplicados", format_currency(summary["total_discounts"]))
col6.metric("Órdenes con envío", format_percent(summary["orders_with_shipping"] / summary["orders_total"]))
col7.metric("Ítems promedio por orden", f"{summary['average_line_items_per_order']:.2f}")
col8.metric("Unidades promedio por orden", f"{summary['average_quantity_per_order']:.2f}")

st.header("2. Dinámica de ingresos")
st.markdown("Evolución mensual de ventas (COP millones).")
st.line_chart(data=monthly_df, x="month", y="total_price_mm")

st.header("3. Productos destacados")
if filtered_products.empty:
    st.info("No hay productos que coincidan con los filtros seleccionados.")
else:
    top_products = filtered_products.sort_values("total_revenue", ascending=False).head(10).copy()
    top_products["total_revenue_bn"] = top_products["total_revenue"] / 1_000_000_000
    top_products_display = top_products[
        ["title", "vendor", "category", "subcategory", "total_revenue_bn", "total_quantity", "order_count"]
    ].rename(
        columns={
            "title": "Producto",
            "vendor": "Marca",
            "category": "Categoría",
            "subcategory": "Subcategoría",
            "total_revenue_bn": "Ingresos (COP B)",
            "total_quantity": "Unidades",
            "order_count": "Órdenes",
        }
    )
    st.dataframe(top_products_display, hide_index=True, use_container_width=True)

st.header("4. Pareto del portafolio")
st.markdown(
    "El 1.3% del catálogo (27 SKU) explica el 80% del ingreso. Utiliza la selección para inspeccionar el corte."
)
pareto_cut = st.slider("Visualizar top N productos", min_value=10, max_value=200, value=50, step=10)
pareto_chart_data = pareto_df.head(pareto_cut)
pareto_chart = (
    alt.Chart(pareto_chart_data)
    .mark_line(point=True)
    .encode(
        x=alt.X("rank:Q", title="Rango de producto"),
        y=alt.Y("cum_share:Q", title="Participación acumulada"),
        tooltip=["rank", "title", alt.Tooltip("cum_share:Q", format=".2f")],
    )
    .properties(height=300)
)
st.altair_chart(pareto_chart, use_container_width=True)

st.header("5. Desempeño por categoría")
category_chart = (
    alt.Chart(categories_df)
    .mark_bar()
    .encode(
        x=alt.X("total_revenue:Q", title="Ingresos (COP)"),
        y=alt.Y("subcategory:N", sort="-x", title="Subcategoría"),
        color=alt.Color("category:N", legend=alt.Legend(title="Categoría")),
        tooltip=[
            "category",
            "subcategory",
            alt.Tooltip("total_revenue:Q", format=","),
            "total_quantity",
        ],
    )
    .properties(height=450)
)
st.altair_chart(category_chart, use_container_width=True)

st.header("6. Correlaciones operativas")
corr_df = pd.DataFrame(metrics["correlations"])
corr_long = corr_df.reset_index(names="metric_a").melt(
    id_vars="metric_a", var_name="metric_b", value_name="correlation"
)
heatmap = (
    alt.Chart(corr_long)
    .mark_rect()
    .encode(
        x=alt.X("metric_b:N", title=""),
        y=alt.Y("metric_a:N", title=""),
        color=alt.Color(
            "correlation:Q",
            scale=alt.Scale(scheme="redblue", domain=(-1, 1)),
            title="Correlación",
        ),
        tooltip=[
            "metric_a",
            "metric_b",
            alt.Tooltip("correlation:Q", format=".2f"),
        ],
    )
    .properties(height=320)
)
st.altair_chart(heatmap, use_container_width=True)

st.header("7. Recomendaciones para agentes")
st.markdown(
    """
- **Liderazgo del portafolio:** Prioriza narrativas sobre Gold Standard Whey, creatinas y ISO 100; representan el núcleo de ingresos.
- **Cross-sell inteligente:** Combina proteínas con creatinas, CLA u omega 3 para aumentar unidades en cada orden.
- **Promociones como palanca:** 93% de las órdenes incluyen descuentos; refuerza cupones y combos para elevar ticket promedio.
- **Envío gratis estratégico:** Las órdenes sin envío tienden a tickets mayores; ofrece umbrales para motivar canastas más grandes.
- **Segmentación por objetivo:** Usa la clasificación (volumen, definición, bienestar) para adaptar scripts y contenido educativo.
"""
)

st.divider()
st.caption(
    "Fuente: Shopify bulk export (2024). Para regenerar métricas: "
    "`python scripts/generate_dashboard_metrics.py bulk_definitivo.json --output-dir dashboard`."
)
