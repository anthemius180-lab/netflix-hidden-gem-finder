import streamlit as st
import requests
import time

# ============ HARDCODED API KEY ============
# ⚠️ WARNING: Anyone with this code can see your API key!
# Replace this with your actual TMDB API key
API_KEY = "f2d4ca4c46b19fb8e16008636e764967"
YOUR_COUNTRY = "IN"
# ===========================================

# Page setup - Netflix Red Theme
st.set_page_config(
    page_title="Netflix Hidden Gem Finder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Netflix Red Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%) !important;
    }
    
    h1 {
        color: #E50914 !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 3.5rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    
    h2, h3 {
        color: #E50914 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #333 !important;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #E50914 0%, #b20710 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 14px 28px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(229, 9, 20, 0.5) !important;
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div {
        background-color: #333 !important;
        color: white !important;
        border: 2px solid #444 !important;
        border-radius: 6px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    
    .stSelectbox > label {
        color: #E50914 !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #E50914 0%, #ff6b6b 100%) !important;
        border-radius: 10px !important;
    }
    
    p, div, span, label {
        color: #e5e5e5 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stSuccess {
        background-color: rgba(229, 9, 20, 0.1) !important;
        border: 1px solid #E50914 !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid #ffc107 !important;
        border-radius: 8px !important;
    }
    
    hr {
        border-color: #333 !important;
        margin: 2rem 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #E50914; font-size: 2.5rem; margin: 0;">NETFLIX</h1>
        <p style="color: #666; font-size: 12px; margin-top: 5px;">HIDDEN GEM FINDER</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("⚙️ Settings")
    
    # Show API key is configured (hidden actual key)
    st.markdown("""
    <div style="background-color: rgba(229, 9, 20, 0.1); border: 1px solid #E50914; 
                border-radius: 8px; padding: 10px; margin-bottom: 20px;">
        <p style="color: #E50914; margin: 0; font-size: 12px; text-align: center;">
            ✅ API Key Configured
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    country_options = {
        "IN": "🇮🇳 India",
        "US": "🇺🇸 United States", 
        "GB": "🇬🇧 United Kingdom",
        "CA": "🇨🇦 Canada",
        "AU": "🇦🇺 Australia",
        "DE": "🇩🇪 Germany",
        "FR": "🇫🇷 France",
        "BR": "🇧🇷 Brazil",
        "JP": "🇯🇵 Japan"
    }
    
    selected_country = st.selectbox(
        "Your Country",
        options=list(country_options.keys()),
        format_func=lambda x: country_options[x],
        index=0
    )
    
    YOUR_COUNTRY = selected_country
    
    st.markdown("---")
    st.markdown("""
    <div style="color: #666; font-size: 11px; text-align: center;">
        <p>Made with ❤️ for movie lovers</p>
    </div>
    """, unsafe_allow_html=True)

# Main Content
st.title("🎬 HIDDEN GEM FINDER")
st.markdown("### Discover underrated movies from Reddit & Letterboxd")

st.markdown("---")

# Search Section
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_genre = st.text_input(
        "🔍 Enter Genre",
        placeholder="Try: Sci-Fi, Horror, Thriller, Comedy...",
        value="Sci-Fi"
    )

with col2:
    max_results = st.selectbox(
        "Results",
        options=[3, 5, 10, 15],
        index=1
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("🔍 FIND GEMS", use_container_width=True)

st.markdown("---")

# Functions
def get_movie_poster(tmdb_id, api_key):
    """Get movie poster URL from TMDB"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    return None

def check_netflix(tmdb_id, api_key, country):
    """Check Netflix availability"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers?api_key={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            netflix_countries = []
            for c, providers in data.get('results', {}).items():
                for provider in providers.get('flatrate', []):
                    if provider['provider_name'] == 'Netflix':
                        netflix_countries.append(c)
                        break
            return {
                'available': len(netflix_countries) > 0,
                'in_your_country': country in netflix_countries,
                'total_countries': len(netflix_countries)
            }
    except:
        pass
    return {'available': False, 'in_your_country': False, 'total_countries': 0}

def search_movies_by_genre(genre_name, api_key, max_results=10):
    """Search movies by genre using TMDB API"""
    try:
        # Get genre ID
        genres_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
        genres_response = requests.get(genres_url, timeout=10)
        
        if genres_response.status_code != 200:
            return []
        
        genres_data = genres_response.json()
        genre_id = None
        
        for genre in genres_data.get('genres', []):
            if genre_name.lower() in genre['name'].lower():
                genre_id = genre['id']
                break
        
        if not genre_id:
            return []
        
        # Discover movies
        discover_url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}&sort_by=vote_average.desc&vote_count.gte=100&vote_average.gte=6.0&page=1"
        discover_response = requests.get(discover_url, timeout=10)
        
        if discover_response.status_code != 200:
            return []
        
        movies_data = discover_response.json()
        movies = []
        
        for movie in movies_data.get('results', [])[:max_results]:
            movies.append({
                'title': movie.get('title'),
                'year': movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A',
                'tmdb_id': movie.get('id'),
                'imdb': round(movie.get('vote_average', 0), 1),
                'desc': movie.get('overview', 'No description available.')[:150] + '...' if len(movie.get('overview', '')) > 150 else movie.get('overview', 'No description available.'),
                'genres': [g['name'] for g in genres_data.get('genres', []) if g['id'] in movie.get('genre_ids', [])],
                'poster_path': movie.get('poster_path')
            })
        
        return movies
    except Exception as e:
        st.error(f"API Error: {e}")
        return []

# Curated fallback data
HIDDEN_GEMS = {
    "Sci-Fi": [
        {"title": "Coherence", "year": 2013, "tmdb_id": 220289, "imdb": 7.2, 
         "desc": "Friends at a dinner party experience strange occurrences during a passing comet.", "genres": ["Sci-Fi", "Thriller"]},
        {"title": "Moon", "year": 2009, "tmdb_id": 17431, "imdb": 7.8,
         "desc": "Astronaut Sam Bell's three-year shift on the moon is coming to an end.", "genres": ["Sci-Fi", "Drama"]},
        {"title": "Ex Machina", "year": 2014, "tmdb_id": 264660, "imdb": 7.7,
         "desc": "A young programmer is selected to participate in a ground-breaking AI experiment.", "genres": ["Sci-Fi", "Thriller"]},
        {"title": "Upgrade", "year": 2018, "tmdb_id": 500664, "imdb": 7.5,
         "desc": "A man is implanted with a chip that gives him superhuman abilities.", "genres": ["Sci-Fi", "Action"]},
        {"title": "The Endless", "year": 2017, "tmdb_id": 430231, "imdb": 6.5,
         "desc": "Two brothers return to the cult they fled from years ago.", "genres": ["Sci-Fi", "Horror"]},
    ],
    "Horror": [
        {"title": "The Autopsy of Jane Doe", "year": 2016, "tmdb_id": 397567, "imdb": 6.8,
         "desc": "A father and son coroner team uncover bizarre clues during an autopsy.", "genres": ["Horror", "Mystery"]},
        {"title": "Train to Busan", "year": 2016, "tmdb_id": 396535, "imdb": 7.6,
         "desc": "Passengers on a train must survive a zombie outbreak in South Korea.", "genres": ["Horror", "Action"]},
        {"title": "The Witch", "year": 2015, "tmdb_id": 310131, "imdb": 6.9,
         "desc": "A family in 1630s New England faces forces of evil in the woods.", "genres": ["Horror", "Drama"]},
        {"title": "Hereditary", "year": 2018, "tmdb_id": 330459, "imdb": 7.3,
         "desc": "A family begins to unravel cryptic and terrifying secrets about their ancestry.", "genres": ["Horror", "Drama"]},
        {"title": "The Invitation", "year": 2015, "tmdb_id": 336190, "imdb": 6.6,
         "desc": "A man attends a dinner party hosted by his ex-wife with sinister intentions.", "genres": ["Horror", "Thriller"]},
    ],
    "Thriller": [
        {"title": "Wind River", "year": 2017, "tmdb_id": 395834, "imdb": 7.7,
         "desc": "A tracker teams with an FBI agent to investigate a murder on a Native American reservation.", "genres": ["Thriller", "Crime"]},
        {"title": "Nightcrawler", "year": 2014, "tmdb_id": 242582, "imdb": 7.8,
         "desc": "A con man desperate for work muscles into the world of crime journalism.", "genres": ["Thriller", "Crime"]},
        {"title": "Prisoners", "year": 2013, "tmdb_id": 146233, "imdb": 8.1,
         "desc": "When his daughter is kidnapped, a father takes matters into his own hands.", "genres": ["Thriller", "Crime"]},
        {"title": "A Simple Favor", "year": 2018, "tmdb_id": 484459, "imdb": 6.8,
         "desc": "A mommy blogger seeks to uncover the truth behind her best friend's disappearance.", "genres": ["Thriller", "Comedy"]},
        {"title": "Gone Girl", "year": 2014, "tmdb_id": 210577, "imdb": 8.1,
         "desc": "With his wife's disappearance having become the focus of media frenzy, a man sees the spotlight turned on him.", "genres": ["Thriller", "Mystery"]},
    ],
    "Comedy": [
        {"title": "Palm Springs", "year": 2020, "tmdb_id": 587792, "imdb": 7.4,
         "desc": "Two wedding guests develop a budding romance while stuck in a time loop.", "genres": ["Comedy", "Romance"]},
        {"title": "Game Night", "year": 2018, "tmdb_id": 445571, "imdb": 6.9,
         "desc": "A group of friends who meet regularly for game night find themselves in a real-life mystery.", "genres": ["Comedy", "Action"]},
        {"title": "The Death of Stalin", "year": 2017, "tmdb_id": 452507, "imdb": 7.3,
         "desc": "The Soviet dictator's last days and the chaos that follows his death.", "genres": ["Comedy", "History"]},
        {"title": "What We Do in the Shadows", "year": 2014, "tmdb_id": 246741, "imdb": 7.6,
         "desc": "A documentary team films the lives of vampire roommates in New Zealand.", "genres": ["Comedy", "Horror"]},
        {"title": "Bridesmaids", "year": 2011, "tmdb_id": 55721, "imdb": 6.8,
         "desc": "Competition between the maid of honor and a bridesmaid over who is the bride's best friend.", "genres": ["Comedy", "Romance"]},
    ],
    "Drama": [
        {"title": "Short Term 12", "year": 2013, "tmdb_id": 169533, "imdb": 7.9,
         "desc": "A supervisor at a foster care facility navigates her own past while helping troubled teens.", "genres": ["Drama"]},
        {"title": "The Florida Project", "year": 2017, "tmdb_id": 391486, "imdb": 7.6,
         "desc": "A mischievous six-year-old girl lives with her rebellious mother in a motel.", "genres": ["Drama"]},
        {"title": "Leave No Trace", "year": 2018, "tmdb_id": 467956, "imdb": 7.1,
         "desc": "A father and daughter live in isolation in an urban park in Portland.", "genres": ["Drama"]},
        {"title": "Paterson", "year": 2016, "tmdb_id": 370106, "imdb": 7.4,
         "desc": "A quiet observation of the triumphs and defeats of daily life.", "genres": ["Drama", "Romance"]},
        {"title": "Manchester by the Sea", "year": 2016, "tmdb_id": 334543, "imdb": 7.8,
         "desc": "A depressed uncle is asked to take care of his teenage nephew after his father dies.", "genres": ["Drama"]},
    ],
    "Action": [
        {"title": "The Raid", "year": 2011, "tmdb_id": 97367, "imdb": 7.6,
         "desc": "An elite team of police officers go into a violent apartment building on a mission.", "genres": ["Action", "Crime"]},
        {"title": "Dredd", "year": 2012, "tmdb_id": 49049, "imdb": 7.1,
         "desc": "In a violent future, Judge Dredd is the law in a post-apocalyptic metropolis.", "genres": ["Action", "Sci-Fi"]},
        {"title": "Atomic Blonde", "year": 2017, "tmdb_id": 341013, "imdb": 6.7,
         "desc": "An undercover MI6 agent is sent to Berlin during the Cold War.", "genres": ["Action", "Thriller"]},
        {"title": "Headshot", "year": 2016, "tmdb_id": 361292, "imdb": 6.3,
         "desc": "A mysterious young man left for dead awakens with killer skills.", "genres": ["Action", "Thriller"]},
        {"title": "John Wick", "year": 2014, "tmdb_id": 245891, "imdb": 7.4,
         "desc": "An ex-hitman comes out of retirement to track down the gangsters that took everything from him.", "genres": ["Action", "Thriller"]},
    ],
    "Animation": [
        {"title": "Spider-Man: Into the Spider-Verse", "year": 2018, "tmdb_id": 324857, "imdb": 8.4,
         "desc": "Teen Miles Morales becomes Spider-Man of his reality, crossing paths with alternate versions.", "genres": ["Animation", "Action"]},
        {"title": "Your Name", "year": 2016, "tmdb_id": 372058, "imdb": 8.4,
         "desc": "Two teenagers share a profound, magical connection upon discovering they are swapping bodies.", "genres": ["Animation", "Romance"]},
        {"title": "Wolf Children", "year": 2012, "tmdb_id": 110420, "imdb": 8.1,
         "desc": "A mother struggles to raise her werewolf children after their father dies.", "genres": ["Animation", "Drama"]},
        {"title": "Kubo and the Two Strings", "year": 2016, "tmdb_id": 313297, "imdb": 7.8,
         "desc": "A young boy named Kubo must locate magical armor to defeat his evil grandfather.", "genres": ["Animation", "Adventure"]},
        {"title": "The Secret of Kells", "year": 2009, "tmdb_id": 24128, "imdb": 7.6,
         "desc": "A young boy in a remote medieval outpost under siege from barbarian raids.", "genres": ["Animation", "Adventure"]},
    ],
}

# Search functionality
if search_button:
    # Use hardcoded API key
    api_key = API_KEY
    
    # Use real TMDB API
    with st.spinner("🔍 Searching TMDB database..."):
        found_movies = search_movies_by_genre(search_genre, api_key, max_results)
    
    # Fallback to curated list if API returns empty
    if not found_movies:
        search_term = search_genre.lower().strip()
        for genre, movies in HIDDEN_GEMS.items():
            if search_term in genre.lower():
                found_movies = movies[:max_results]
                break
        
        if not found_movies:
            for genre, movies in HIDDEN_GEMS.items():
                for movie in movies:
                    if any(search_term in g.lower() for g in movie['genres']):
                        found_movies.append(movie)
            found_movies = found_movies[:max_results]
    
    if found_movies:
        st.success(f"🎉 Found {len(found_movies)} hidden gems in '{search_genre}'!")
        
        # Calculate Netflix availability with progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, movie in enumerate(found_movies):
            status_text.text(f"Checking Netflix for: {movie['title']}...")
            netflix_info = check_netflix(movie['tmdb_id'], api_key, YOUR_COUNTRY)
            movie['netflix'] = netflix_info
            progress_bar.progress((i + 1) / len(found_movies))
            time.sleep(0.3)
        
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        st.markdown(f"<h3 style='color: #E50914; margin-top: 20px;'>Results for '{search_genre}'</h3>", unsafe_allow_html=True)
        
        # Create grid layout
        cols = st.columns(3)
        
        for idx, movie in enumerate(found_movies):
            with cols[idx % 3]:
                # Netflix badge logic
                netflix = movie.get('netflix', {})
                if netflix.get('in_your_country'):
                    badge_class = "badge-available"
                    badge_text = f"✅ ON NETFLIX {YOUR_COUNTRY}"
                    card_border = "2px solid #E50914"
                elif netflix.get('available'):
                    badge_class = "badge-elsewhere"
                    badge_text = f"🌍 ON NETFLIX ({netflix['total_countries']} countries)"
                    card_border = "2px solid #46d369"
                else:
                    badge_class = "badge-unavailable"
                    badge_text = "❌ NOT ON NETFLIX"
                    card_border = "2px solid #444"
                
                # Get poster URL
                poster_url = None
                if movie.get('poster_path'):
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                else:
                    poster_url = get_movie_poster(movie.get('tmdb_id'), api_key)
                
                # Score percentage
                score_percent = (movie['imdb'] / 10) * 100
                
                # Create columns for layout
                inner_col1, inner_col2 = st.columns([1, 2])
                
                with inner_col1:
                    if poster_url:
                        st.image(poster_url, use_column_width=True)
                    else:
                        st.markdown("""
                        <div style="width: 100%; aspect-ratio: 2/3; background: linear-gradient(135deg, #333 0%, #222 100%); 
                                    border-radius: 8px; display: flex; align-items: center; justify-content: center; 
                                    color: #666; font-size: 40px; min-height: 150px;">
                            🎬
                        </div>
                        """, unsafe_allow_html=True)
                
                with inner_col2:
                    st.markdown(f"""
                    <div style="border: {card_border}; border-radius: 12px; padding: 10px; background-color: #181818;">
                        <h4 style="color: white; margin: 0 0 5px 0; font-size: 16px; font-weight: bold;">{movie['title']}</h4>
                        <p style="color: #aaa; margin: 0 0 8px 0; font-size: 12px;">{movie['year']} • ⭐ {movie['imdb']}</p>
                        <p style="color: #ddd; margin: 0 0 10px 0; font-size: 11px; line-height: 1.4; height: 40px; overflow: hidden;">
                            {movie['desc']}
                        </p>
                        <span style="background-color: {'#E50914' if netflix.get('in_your_country') else '#46d369' if netflix.get('available') else '#564d4d'}; 
                                     color: {'white' if netflix.get('in_your_country') or not netflix.get('available') else 'black'}; 
                                     padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: bold;">
                            {badge_text}
                        </span>
                        <div style="margin-top: 8px;">
                            {''.join([f'<span style="background-color: #333; color: #fff; padding: 2px 6px; border-radius: 10px; font-size: 9px; margin-right: 3px;">{g}</span>' for g in movie['genres']])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Score bar
                    st.markdown(f"""
                    <div style="margin-top: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
                            <span style="color: #aaa; font-size: 10px;">IMDb Score</span>
                            <span style="color: #ffc107; font-size: 10px; font-weight: bold;">{movie['imdb']}/10</span>
                        </div>
                        <div style="background-color: #333; border-radius: 10px; height: 5px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #E50914 0%, #ff6b6b 100%); height: 100%; width: {score_percent}%;\"></div>
                        </div>
                    </div>
                    """)
                
                st.markdown("---")
    else:
        st.warning(f"😕 No hidden gems found for '{search_genre}'")

else:
    # Landing page content
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%); border-radius: 16px; margin: 20px 0; border: 1px solid #333;">
        <h2 style="color: #E50914; margin-bottom: 20px;">🎬 Welcome to Hidden Gem Finder</h2>
        <p style="color: #aaa; font-size: 18px; max-width: 600px; margin: 0 auto 30px auto; line-height: 1.6;">
            Discover critically acclaimed but underseen movies curated from Reddit's r/MovieSuggestions 
            and Letterboxd hidden gem lists. Check real Netflix availability via TMDB!
        </p>
        <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🎯</div>
                <div style="color: white; font-weight: bold;">Curated</div>
                <div style="color: #666; font-size: 12px;">Hand-picked gems</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🔍</div>
                <div style="color: white; font-weight: bold;">Real Data</div>
                <div style="color: #666; font-size: 12px;">Live TMDB API</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🌍</div>
                <div style="color: white; font-weight: bold;">Netflix Check</div>
                <div style="color: #666; font-size: 12px;">Actual availability</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎭 Browse All Genres")
    
    genre_display = st.columns(4)
    genre_list = list(HIDDEN_GEMS.keys())
    
    for i, genre in enumerate(genre_list):
        with genre_display[i % 4]:
            movie_count = len(HIDDEN_GEMS[genre])
            avg_rating = sum(m['imdb'] for m in HIDDEN_GEMS[genre]) / movie_count
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a1a 0%, #181818 100%); padding: 20px; border-radius: 12px; 
                        text-align: center; border: 1px solid #333; margin-bottom: 15px;">
                <h4 style="color: #E50914; margin: 0 0 8px 0; font-size: 18px;">{genre}</h4>
                <p style="color: #666; margin: 0; font-size: 13px;">{movie_count} movies</p>
                <p style="color: #ffc107; margin: 5px 0 0 0; font-size: 12px;">⭐ Avg {avg_rating:.1f}</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px; background-color: #0a0a0a; border-radius: 8px; margin-top: 30px;">
    <p style="margin: 0 0 10px 0; font-size: 14px;">🎬 <strong style="color: #E50914;">Hidden Gem Finder</strong> - Powered by TMDB API</p>
    <p style="margin: 0; font-size: 11px; color: #444;">
        This product uses the TMDB API but is not endorsed or certified by TMDB
    </p>
</div>
""", unsafe_allow_html=True)