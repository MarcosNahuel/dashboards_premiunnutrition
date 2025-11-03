#!/usr/bin/env python3
"""Generate visuals (PNG) for the Premium Nutrition technical report."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "analysis_outputs"

plt.style.use("seaborn-v0_8-whitegrid")


def load_csv(name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name, **kwargs)


def plot_revenue_trend() -> None:
    df = load_csv("sales_by_day.csv", parse_dates=["date"]).sort_values("date")

    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.plot(df["date"], df["revenue"] / 1_000_000, color="#0b7285", linewidth=1.8)
    ax.set_title("Evolución diaria de ingresos (COP millones)", fontsize=15, color="#0b7285")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Ingresos (millones de COP)")
    ax.grid(alpha=0.25)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(BASE_DIR / "img_revenue_trend.png", dpi=220)
    plt.close(fig)


def plot_sales_by_hour() -> None:
    df = load_csv("sales_by_hour.csv")

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(df["hour"], df["revenue"] / 1_000_000, color="#ff7f0e", width=0.8)
    ax.set_xticks(range(0, 24, 1))
    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Ingresos (millones de COP)")
    ax.set_title("Ingresos promedio por hora del día", fontsize=15, color="#d9480f")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(BASE_DIR / "img_sales_by_hour.png", dpi=220)
    plt.close(fig)


def plot_top_products() -> None:
    df = load_csv("top_products.csv").head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(df["product_title"], df["revenue"] / 1_000_000_000, color="#1f77b4")
    ax.invert_yaxis()
    ax.set_xlabel("Ingresos (miles de millones de COP)")
    ax.set_title("Top 10 SKU por ingresos", fontsize=15, color="#1f3b4d")
    for bar, value in zip(bars, df["revenue"] / 1_000_000_000):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2, f"{value:.2f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(BASE_DIR / "img_top_products.png", dpi=220)
    plt.close(fig)


def plot_rfm_segments() -> None:
    df = load_csv("rfm_segments.csv")
    counts = df["segment"].map(
        {
            "Leal": "Leales",
            "Activo": "Activos",
            "En Riesgo": "En riesgo",
            "Churn": "Inactivos",
            "Nuevo/Potencial": "Nuevos",
        }
    ).value_counts().reset_index()
    counts.columns = ["segmento", "conteo"]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        counts["conteo"],
        labels=counts["segmento"],
        autopct=lambda pct: f"{pct:.1f}%",
        startangle=120,
        colors=["#0b7285", "#1f9d55", "#fcc419", "#845ef7", "#ff6b6b"],
        textprops={"fontsize": 11},
        wedgeprops={"linewidth": 0.8, "edgecolor": "white"},
    )
    ax.set_title("Distribución de clientes por segmento RFM", fontsize=15, color="#0b7285")
    fig.tight_layout()
    fig.savefig(BASE_DIR / "img_rfm_segments.png", dpi=220)
    plt.close(fig)


def main() -> None:
    plot_revenue_trend()
    plot_sales_by_hour()
    plot_top_products()
    plot_rfm_segments()
    print("Charts refreshed in", BASE_DIR)


if __name__ == "__main__":
    main()
