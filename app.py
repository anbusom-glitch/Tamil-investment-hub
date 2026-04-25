    # --- ⭐ RATINGS TAB (பிழையற்ற ரேட்டிங்) ---
    with tabs[2]:
        st.markdown(f"### {get_text('Quality Rating Score', 'தர மதிப்பீடு')}")
        
        # பாதுகாப்பான முறையில் டேட்டா எடுத்தல் (get method)
        score = 0
        pe = info.get('trailingPE', 0)
        roe = info.get('returnOnEquity', 0)
        debt = info.get('debtToEquity', 0)
        
        # 100-க்கு கணக்கிடும் லாஜிக்
        if pe > 0 and pe < 25: score += 35
        elif pe >= 25 and pe < 40: score += 15
        
        if roe > 0.18: score += 35
        elif roe > 0.12: score += 20
        
        if debt > 0 and debt < 100: score += 30
        elif debt == 0: score += 30 # கடன் இல்லாத நிறுவனம்
        
        # ஸ்கோர் நிறம் மற்றும் முடிவு
        color = "#39FF14" if score >= 70 else ("#ffd700" if score >= 40 else "#FF3131")
        verdict = get_text("STRONG BUY 🚀", "நிச்சயமாக வாங்கலாம் 🚀") if score >= 70 else \
                  (get_text("HOLD ⚖️", "தற்போது வைத்திருக்கலாம் ⚖️") if score >= 40 else \
                  get_text("AVOID ⚠️", "தவிர்ப்பது நல்லது ⚠️"))
        
        st.markdown(f"""
            <div class="rating-card">
                <p style="font-size: 18px; opacity: 0.8;">{get_text('Stock Quality Score', 'பங்கின் தரம்')}</p>
                <p class="score-text" style="color: {color};">{score} / 100</p>
                <p style="font-size: 22px; font-weight: bold; color: {color};">{verdict}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # கூடுதல் காரணிகள்
        st.write(f"📊 **P/E:** {pe if pe > 0 else 'N/A'} | **ROE:** {roe*100:.2f}% | **Debt/Equity:** {debt if debt > 0 else 'N/A'}")

    # --- 📅 CORPORATE ACTIONS TAB ---
    with tabs[3]:
        st.markdown(f"### {get_text('Corporate Actions', 'நிறுவன நிகழ்வுகள்')}")
        try:
            # டிவிடெண்ட் மற்றும் ஸ்பிளிட் விவரங்கள்
            acts = stock_obj.actions
            if not acts.empty:
                # சமீபத்திய 10 நிகழ்வுகள்
                st.dataframe(acts.tail(10).sort_index(ascending=False), use_container_width=True)
            else:
                st.info(get_text("No recent corporate actions found.", "சமீபத்திய நிகழ்வுகள் ஏதுமில்லை."))
        except Exception as e:
            st.error(get_text("Error loading actions.", "நிகழ்வுகளை லோடு செய்வதில் பிழை."))
