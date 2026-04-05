import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pro Profit Manager", layout="centered")

st.title("💰 Advanced Step-wise Profit Manager")

# 🔹 Inputs
balance = st.number_input("Start Balance", value=100.0)
payout = st.number_input("Payout", value=1.96)
steps = st.number_input("Steps", value=4, step=1)

mode = st.selectbox("Select Mode", ["Balanced", "Safe", "Aggressive"])

# 🔹 Mode settings
if mode == "Safe":
    risk_factor = 7
elif mode == "Balanced":
    risk_factor = 5
else:
    risk_factor = 3  # aggressive

if st.button("Calculate"):

    if payout <= 1:
        st.error("Payout must be greater than 1")
    else:

        best_result = None
        best_diff = float("inf")

        # 🔥 Auto search best target profit
        target_profit = balance / (steps * risk_factor)

        while target_profit > 0:

            bets = []
            profits = []
            cumulative = 0

            for i in range(int(steps)):
                bet = (target_profit + cumulative) / (payout - 1)
                bet = round(bet)
                bets.append(bet)
                cumulative += bet
                profit = bet * payout - cumulative
                profits.append(round(profit, 2))

            total_risk = sum(bets)

            if total_risk <= balance:

                diff = max(profits) - min(profits)

                # 🔥 minimize profit difference
                if diff < best_diff:
                    best_diff = diff
                    best_result = (bets, profits, total_risk, target_profit)

            target_profit -= 0.1

        if best_result is None:
            st.error("❌ No valid setup found")
        else:
            bets, profits, total_risk, target_profit = best_result

            avg_profit = round(sum(profits) / len(profits), 2)
            leftover = balance - total_risk

            # 📊 Table
            df = pd.DataFrame({
                "Step": list(range(1, len(bets)+1)),
                "Bet": bets,
                "Profit": profits
            })

            st.subheader("📊 Step Details")
            st.dataframe(df)

            # 📈 Summary
            st.subheader("📈 Summary")
            st.write(f"**Total Risk:** {total_risk}")
            st.write(f"**Average Profit:** {avg_profit}")
            st.write(f"**Leftover Balance:** {leftover}")
            st.write(f"**Target Profit Used:** {round(target_profit,2)}")

            # 📉 Analysis
            st.subheader("📉 Profit Analysis")
            st.write(f"Max Profit: {max(profits)}")
            st.write(f"Min Profit: {min(profits)}")
            st.write(f"Difference: {round(best_diff,2)}")

            # 🚨 Risk Warning
            if total_risk > balance:
                st.error("⚠️ Risk exceeds balance!")
            elif leftover < balance * 0.1:
                st.warning("⚠️ Very high risk (low leftover)")
            else:
                st.success("✔ Well balanced setup")