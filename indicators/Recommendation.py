def generate_recommendation(rsi, ema20, ema50, macd):
    score = 0
    reasons = []

    # RSI
    if 30 <= rsi <= 70:
        score += 1
        reasons.append("RSI is healthy.")
    elif rsi < 30:
        score += 2
        reasons.append("Stock is oversold.")
    else:
        reasons.append("Stock is overbought.")

    # EMA
    if ema20 > ema50:
        score += 1
        reasons.append("EMA20 is above EMA50 (Bullish Trend).")
    else:
        reasons.append("EMA20 is below EMA50 (Bearish Trend).")

    # MACD
    if macd["macd"] > macd["signal"]:
        score += 1
        reasons.append("MACD Bullish Crossover.")
    else:
        reasons.append("MACD Bearish Crossover.")

    # Final Recommendation
    if score >= 4:
        rating = "🟢 STRONG BUY"
    elif score == 3:
        rating = "🟢 BUY"
    elif score == 2:
        rating = "🟡 HOLD"
    else:
        rating = "🔴 SELL"

    confidence = round((score / 4) * 100)

    return {
        "rating": rating,
        "confidence": confidence,
        "reasons": reasons
    }