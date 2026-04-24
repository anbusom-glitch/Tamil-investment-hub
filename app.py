        # --- பிழை இல்லாத புதிய பகுதி ---
        if all_news:
            # .get() பயன்படுத்துவதால் 'providerPublishTime' இல்லையென்றாலும் error வராது
            all_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
            
            for news_item in all_news[:15]:
                # அனைத்து தகவல்களையும் .get() மூலம் பாதுகாப்பாகப் பெறுதல்
                title = news_item.get('title', 'No Title')
                link = news_item.get('link', '#')
                publisher = news_item.get('publisher', 'Unknown Source')
                raw_time = news_item.get('providerPublishTime', 0)
                
                # நேரத்தை மாற்றும் போது பிழை வராமல் தவிர்க்க
                try:
                    pub_time = datetime.fromtimestamp(raw_time).strftime('%Y-%m-%d %H:%M') if raw_time else "N/A"
                except:
                    pub_time = "N/A"

                st.markdown(f"""
                    <div class="news-feed-card">
                        <div class="stock-badge">{news_item.get('stock_ref', 'Stock')}</div><br>
                        <a href="{link}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold; font-size:14px;">
                            {title}
                        </a><br>
                        <span style="color:#666; font-size:10px;">{publisher} • {pub_time}</span>
                    </div>
                """, unsafe_allow_html=True)
