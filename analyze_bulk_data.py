#!/usr/bin/env python3
"""Descriptive analytics pipeline for Shopify bulk export (Premium Nutrition)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "export"
OUTPUT_DIR = BASE_DIR / "analysis_outputs"


ORDERS_FILENAME = "bulk_orders.csv"
LINE_ITEMS_FILENAME = "bulk_line_items.csv"


@dataclass
class KPIBundle:
    total_orders: int
    total_customers: int
    total_revenue: float
    subtotal_revenue: float
    total_discounts: float
    total_shipping: float
    total_tax: float
    average_order_value: float
    median_order_value: float
    orders_with_discount: int
    orders_with_shipping: int
    share_orders_discount: float
    share_orders_shipping: float
    avg_lines_per_order: float
    median_lines_per_order: float
    avg_units_per_order: float
    median_units_per_order: float
    avg_items_per_order: float
    median_items_per_order: float
    revenue_last_30_days: float
    revenue_last_90_days: float
    revenue_last_365_days: float


CLASSIFICATION_RULES = [
    ("Proteínas", "Proteína de Suero (Whey Protein)", ("whey", "suero", "100% whey")),
    ("Proteínas", "Proteína Aislada/Hidrolizada (Isolate/Hydrolyzed)", ("isolate", "iso 100", "aislada", "hydro")),
    ("Proteínas", "Proteínas Hipercalóricas (Mass Gainers)", ("mass", "gainer", "hipercal", "mega gainer", "serious mass")),
    ("Proteínas", "Proteína Vegana (Vegan Protein)", ("vegan", "vegana", "plant", "vegetal", "soya", "pea")),
    ("Proteínas", "Caseína (Casein)", ("casein", "caseína")),
    ("Proteínas", "Barras y Snacks de Proteína", ("barra", "bar ", "bar-", "snack", "bite")),
    ("Aminoácidos", "BCAA", ("bcaa", "branched chain")),
    ("Aminoácidos", "Glutamina", ("glutamine", "glutamina")),
    ("Aminoácidos", "L-Carnitina", ("carnitine", "carnitina", "acetyl")),
    ("Aminoácidos", "EAA / Mezclas", ("eaa", "amino ", "amino-", "essential amino")),
    ("Rendimiento y Energía", "Pre-Entrenos (Pre-Workouts)", ("pre-workout", "preworkout", "pre workout", "pump", "c4")),
    ("Rendimiento y Energía", "Creatina", ("creatine", "creatina", "micronized", "monohydrate")),
    ("Rendimiento y Energía", "Reguladores Hormonales", ("tribulus", "test ", "testo", "testosterone", "hormonal")),
    ("Control de Peso", "Quemadores de Grasa / Termogénicos", ("burn", "termog", "thermo", "lipo", "cut")),
    ("Control de Peso", "CLA", (" cla", "cla ", "linoleic")),
    ("Salud y Bienestar", "Vitaminas y Minerales", ("vitamin", "multi", "miner", "opti-men", "opti-women")),
    ("Salud y Bienestar", "Colágeno", ("collagen", "colageno", "colágeno")),
    ("Salud y Bienestar", "Omega 3", ("omega", "fish oil", "aceite de pescado")),
    ("Accesorios", "Shakers y Botellas", ("shaker", "bottle", "botella")),
    ("Accesorios", "Ropa y Otros", ("gorra", "camiseta", "apparel", "towel")),
]


def to_json_compatible(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (pd.Timedelta,)):
        return value.total_seconds()
    if isinstance(value, np.ndarray):
        return value.tolist()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def classify_product(title: str | None, product_type: str | None, variant_title: str | None) -> tuple[str, str]:
    parts: list[str] = []
    for value in (title, product_type, variant_title):
        if value is None:
            continue
        if isinstance(value, float) and np.isnan(value):
            continue
        parts.append(str(value))

    haystack = " ".join(parts).lower()
    if any(keyword in haystack for keyword in ("combo", "pack", "kit")):
        if any(keyword in haystack for keyword in ("mass", "gainer", "creatina")):
            return "Combos y Packs", "Combo de Volumen/Masa"
        if any(keyword in haystack for keyword in ("burn", "defin", "iso", "carnit", "cla")):
            return "Combos y Packs", "Combo de Definición"
        if any(keyword in haystack for keyword in ("x2", "x3", "2x", "3x", "duo", "trio")):
            return "Combos y Packs", "Pack de Ahorro"
        return "Combos y Packs", "Pack de Ahorro"

    for category, subcategory, keywords in CLASSIFICATION_RULES:
        if any(keyword in haystack for keyword in keywords):
            return category, subcategory

    return "Otros", product_type or "Sin categoría"


def to_float(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    orders_path = DATA_DIR / ORDERS_FILENAME
    items_path = DATA_DIR / LINE_ITEMS_FILENAME
    if not orders_path.exists() or not items_path.exists():
        raise FileNotFoundError(
            f"Required CSV files not found in {DATA_DIR}. Expected {ORDERS_FILENAME} and {LINE_ITEMS_FILENAME}."
        )

    orders = pd.read_csv(
        orders_path,
        parse_dates=["createdAt", "updatedAt"],
        keep_default_na=False,
        na_values=["", "null", None],
    )
    items = pd.read_csv(
        items_path,
        keep_default_na=False,
        na_values=["", "null", None],
    )
    return orders, items


def enrich_orders(orders: pd.DataFrame, items: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    orders = orders.copy()
    items = items.copy()

    orders["total_price"] = to_float(orders["totalPriceSet.shopMoney.amount"])
    orders["subtotal_amount"] = to_float(orders["subtotalPriceSet.shopMoney.amount"])
    orders["discount_amount"] = to_float(orders["totalDiscountsSet.shopMoney.amount"])
    orders["shipping_amount"] = to_float(orders["totalShippingPriceSet.shopMoney.amount"])
    orders["tax_amount"] = to_float(orders["totalTaxSet.shopMoney.amount"])

    orders["created_at_utc"] = pd.to_datetime(orders["createdAt"], utc=True)
    orders["created_at_bogota"] = orders["created_at_utc"].dt.tz_convert("America/Bogota")
    orders["created_date"] = orders["created_at_bogota"].dt.date
    orders["created_hour"] = orders["created_at_bogota"].dt.hour
    orders["created_weekday"] = orders["created_at_bogota"].dt.day_name()

    discounted_price = to_float(items["discountedUnitPriceSet.shopMoney.amount"])
    original_price = to_float(items["originalUnitPriceSet.shopMoney.amount"])
    items["quantity"] = to_float(items["quantity"])
    items["unit_price"] = np.where(discounted_price > 0, discounted_price, original_price)
    items["line_revenue"] = items["unit_price"] * items["quantity"]

    items["category"], items["subcategory"] = zip(
        *items.apply(
            lambda row: classify_product(
                row.get("variant.product.title"),
                row.get("variant.product.productType"),
                row.get("variant.title"),
            ),
            axis=1,
        )
    )

    summary = (
        items.groupby("__parentId")
        .agg(
            lines=("id", "count"),
            units=("quantity", "sum"),
            line_revenue=("line_revenue", "sum"),
        )
        .reset_index()
        .rename(columns={"__parentId": "id"})
    )

    orders = orders.merge(summary, on="id", how="left", validate="one_to_one")
    orders["lines"] = orders["lines"].fillna(0).astype(int)
    orders["units"] = orders["units"].fillna(0.0)
    orders["line_revenue"] = orders["line_revenue"].fillna(0.0)

    return orders, items


def compute_kpis(orders: pd.DataFrame) -> KPIBundle:
    total_orders = len(orders)
    total_customers = orders["customer.id"].nunique(dropna=True)

    total_revenue = orders["total_price"].sum()
    subtotal_revenue = orders["subtotal_amount"].sum()
    total_discounts = orders["discount_amount"].sum()
    total_shipping = orders["shipping_amount"].sum()
    total_tax = orders["tax_amount"].sum()

    average_order_value = orders["total_price"].mean()
    median_order_value = orders["total_price"].median()

    orders_with_discount = (orders["discount_amount"] > 0).sum()
    orders_with_shipping = (orders["shipping_amount"] > 0).sum()

    share_orders_discount = orders_with_discount / total_orders if total_orders else 0.0
    share_orders_shipping = orders_with_shipping / total_orders if total_orders else 0.0

    avg_lines_per_order = orders["lines"].mean()
    median_lines_per_order = orders["lines"].median()
    avg_units_per_order = orders["units"].mean()
    median_units_per_order = orders["units"].median()

    avg_items_per_order = avg_units_per_order
    median_items_per_order = median_units_per_order

    last_order_date = orders["created_at_bogota"].max()
    cutoff_30 = last_order_date - pd.Timedelta(days=30)
    cutoff_90 = last_order_date - pd.Timedelta(days=90)
    cutoff_365 = last_order_date - pd.Timedelta(days=365)

    revenue_last_30_days = orders.loc[orders["created_at_bogota"] >= cutoff_30, "total_price"].sum()
    revenue_last_90_days = orders.loc[orders["created_at_bogota"] >= cutoff_90, "total_price"].sum()
    revenue_last_365_days = orders.loc[orders["created_at_bogota"] >= cutoff_365, "total_price"].sum()

    return KPIBundle(
        total_orders=total_orders,
        total_customers=total_customers,
        total_revenue=total_revenue,
        subtotal_revenue=subtotal_revenue,
        total_discounts=total_discounts,
        total_shipping=total_shipping,
        total_tax=total_tax,
        average_order_value=average_order_value,
        median_order_value=median_order_value,
        orders_with_discount=orders_with_discount,
        orders_with_shipping=orders_with_shipping,
        share_orders_discount=share_orders_discount,
        share_orders_shipping=share_orders_shipping,
        avg_lines_per_order=avg_lines_per_order,
        median_lines_per_order=median_lines_per_order,
        avg_units_per_order=avg_units_per_order,
        median_units_per_order=median_units_per_order,
        avg_items_per_order=avg_items_per_order,
        median_items_per_order=median_items_per_order,
        revenue_last_30_days=revenue_last_30_days,
        revenue_last_90_days=revenue_last_90_days,
        revenue_last_365_days=revenue_last_365_days,
    )


def build_top_products(items: pd.DataFrame, limit: int = 25) -> pd.DataFrame:
    grouped = (
        items.groupby("variant.product.id")
        .agg(
            product_title=("variant.product.title", "first"),
            vendor=("variant.product.vendor", "first"),
            product_type=("variant.product.productType", "first"),
            category=("category", "first"),
            subcategory=("subcategory", "first"),
            units=("quantity", "sum"),
            revenue=("line_revenue", "sum"),
        )
        .sort_values("revenue", ascending=False)
    )
    grouped["revenue_share"] = grouped["revenue"] / grouped["revenue"].sum()
    return grouped.head(limit).reset_index().rename(columns={"variant.product.id": "product_id"})


def build_top_categories(items: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        items.groupby(["category", "subcategory"])
        .agg(units=("quantity", "sum"), revenue=("line_revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    grouped["revenue_share"] = grouped["revenue"] / grouped["revenue"].sum()
    return grouped


def build_time_series(orders: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    daily = (
        orders.groupby("created_date")
        .agg(
            revenue=("total_price", "sum"),
            orders_count=("id", "count"),
            units=("units", "sum"),
        )
        .reset_index()
        .rename(columns={"created_date": "date"})
        .sort_values("date")
    )

    hourly = (
        orders.groupby("created_hour")
        .agg(
            revenue=("total_price", "sum"),
            orders_count=("id", "count"),
        )
        .reset_index()
        .rename(columns={"created_hour": "hour"})
        .sort_values("hour")
    )

    return daily, hourly


def build_basket_shape(orders: pd.DataFrame) -> pd.DataFrame:
    bucket = pd.DataFrame(
        {
            "metric": [
                "lines_mean",
                "lines_median",
                "lines_p25",
                "lines_p75",
                "units_mean",
                "units_median",
                "units_p25",
                "units_p75",
                "orders_single_line",
                "orders_multi_line",
            ],
            "value": [
                orders["lines"].mean(),
                orders["lines"].median(),
                orders["lines"].quantile(0.25),
                orders["lines"].quantile(0.75),
                orders["units"].mean(),
                orders["units"].median(),
                orders["units"].quantile(0.25),
                orders["units"].quantile(0.75),
                (orders["lines"] == 1).mean(),
                (orders["lines"] >= 2).mean(),
            ],
        }
    )
    return bucket


def build_rfm(orders: pd.DataFrame) -> pd.DataFrame:
    orders_with_customer = orders.dropna(subset=["customer.id"]).copy()
    if orders_with_customer.empty:
        return pd.DataFrame()

    reference_date = orders_with_customer["created_at_bogota"].max().normalize() + pd.Timedelta(days=1)
    rfm = (
        orders_with_customer.groupby("customer.id")
        .agg(
            last_purchase=("created_at_bogota", "max"),
            frequency=("id", "count"),
            monetary=("total_price", "sum"),
        )
        .reset_index()
    )
    rfm["recency_days"] = (reference_date - rfm["last_purchase"]).dt.days

    bins = np.linspace(0, 1, 6)

    recency_pct = rfm["recency_days"].rank(method="first", pct=True)
    frequency_pct = rfm["frequency"].rank(method="first", pct=True)
    monetary_pct = rfm["monetary"].rank(method="first", pct=True)

    rfm["recency_score"] = pd.cut(recency_pct, bins=bins, labels=[5, 4, 3, 2, 1], include_lowest=True).astype(int)
    rfm["frequency_score"] = pd.cut(frequency_pct, bins=bins, labels=[1, 2, 3, 4, 5], include_lowest=True).astype(int)
    rfm["monetary_score"] = pd.cut(monetary_pct, bins=bins, labels=[1, 2, 3, 4, 5], include_lowest=True).astype(int)
    rfm["rfm_score"] = rfm["recency_score"] + rfm["frequency_score"] + rfm["monetary_score"]

    def segment(row: pd.Series) -> str:
        if row["recency_score"] >= 4 and row["frequency_score"] >= 4:
            return "Leal"
        if row["recency_score"] >= 4 and row["frequency_score"] <= 2:
            return "Nuevo/Potencial"
        if row["recency_score"] <= 2 and row["frequency_score"] >= 4:
            return "En Riesgo"
        if row["recency_score"] <= 2 and row["frequency_score"] <= 2:
            return "Churn"
        return "Activo"

    rfm["segment"] = rfm.apply(segment, axis=1)
    return rfm


def export_outputs(
    kpis: KPIBundle,
    top_products: pd.DataFrame,
    top_categories: pd.DataFrame,
    daily: pd.DataFrame,
    hourly: pd.DataFrame,
    basket_shape: pd.DataFrame,
    rfm: pd.DataFrame,
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    kpis_df = pd.DataFrame(
        {
            "metric": list(asdict(kpis).keys()),
            "value": list(asdict(kpis).values()),
        }
    )
    kpis_df.to_csv(OUTPUT_DIR / "kpis_overview.csv", index=False)
    top_products.to_csv(OUTPUT_DIR / "top_products.csv", index=False)
    top_categories.to_csv(OUTPUT_DIR / "top_categories.csv", index=False)
    daily.to_csv(OUTPUT_DIR / "sales_by_day.csv", index=False)
    hourly.to_csv(OUTPUT_DIR / "sales_by_hour.csv", index=False)
    basket_shape.to_csv(OUTPUT_DIR / "basket_shape.csv", index=False)
    if not rfm.empty:
        rfm.to_csv(OUTPUT_DIR / "rfm_segments.csv", index=False)

    summary_payload = {
        "kpis": asdict(kpis),
        "top_products": top_products.head(10).to_dict(orient="records"),
        "top_categories": top_categories.head(10).to_dict(orient="records"),
        "basket": basket_shape.to_dict(orient="records"),
        "rfm_overview": (
            rfm["segment"].value_counts(normalize=True).round(4).to_dict() if not rfm.empty else {}
        ),
    }
    (OUTPUT_DIR / "analysis_summary.json").write_text(
        json.dumps(summary_payload, indent=2, ensure_ascii=False, default=to_json_compatible),
        encoding="utf-8",
    )


def main() -> None:
    orders_raw, items_raw = load_data()
    orders, items = enrich_orders(orders_raw, items_raw)

    kpis = compute_kpis(orders)
    top_products = build_top_products(items)
    top_categories = build_top_categories(items)
    daily, hourly = build_time_series(orders)
    basket_shape = build_basket_shape(orders)
    rfm = build_rfm(orders)

    export_outputs(kpis, top_products, top_categories, daily, hourly, basket_shape, rfm)

    print("Analysis completed.")
    print(f"Outputs saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
