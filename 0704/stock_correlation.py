import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="台股相關係數分析", layout="wide")
st.title("台股相關係數分析")
st.markdown("輸入任意四個台股代號，計算日報酬率相關係數並以熱力圖呈現")

with st.sidebar:
    st.header("股票設定")
    ticker1 = st.text_input("股票 1", "2330.TW", help="2330.TW = 台積電")
    ticker2 = st.text_input("股票 2", "2317.TW", help="2317.TW = 鴻海")
    ticker3 = st.text_input("股票 3", "2303.TW", help="2303.TW = 聯電")
    ticker4 = st.text_input("股票 4", "2454.TW", help="2454.TW = 聯發科")

    st.header("日期範圍")
    start_date = st.date_input("開始日期", datetime(2020, 1, 1))
    end_date = st.date_input("結束日期", datetime.now())

    run = st.button("分析相關係數", type="primary")

if run:
    tickers = [t.strip() for t in [ticker1, ticker2, ticker3, ticker4] if t.strip()]

    if len(tickers) < 2:
        st.error("請輸入至少 2 個股票代號")
        st.stop()

    with st.spinner("正在下載股價資料..."):
        try:
            data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)
            if "Close" not in data:
                st.error("無法取得收盤價資料，請檢查股票代號是否正確")
                st.stop()

            close = data["Close"]
            if close.empty or close.isnull().all().all():
                st.error("下載的資料為空，請調整日期範圍或檢查股票代號")
                st.stop()

            returns = close.pct_change().dropna()

            corr = returns.corr()

            st.subheader("收盤價走勢")
            st.line_chart(close)

            st.subheader("日報酬率走勢")
            st.line_chart(returns)

            st.subheader("相關係數表")
            styled = corr.style.format("{:.4f}").background_gradient(
                cmap="RdYlBu", vmin=-1, vmax=1, axis=None
            )
            st.dataframe(styled, use_container_width=True)

            st.subheader("相關係數熱力圖")
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(corr.values, cmap="RdYlBu", vmin=-1, vmax=1)

            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=11)
            ax.set_yticklabels(corr.columns, fontsize=11)

            for i in range(len(corr.columns)):
                for j in range(len(corr.columns)):
                    val = corr.iloc[i, j]
                    color = "white" if abs(val) > 0.5 else "black"
                    ax.text(j, i, f"{val:.3f}", ha="center", va="center", color=color, fontsize=12)

            fig.colorbar(im, ax=ax, shrink=0.8)
            st.pyplot(fig)

            st.subheader("原始收盤價資料")
            with st.expander("點擊展開"):
                st.dataframe(close, use_container_width=True)

        except Exception as e:
            st.error(f"發生錯誤: {e}")
else:
    st.info("請在左側輸入股票代號後點擊「分析相關係數」")
