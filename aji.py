import streamlit as st
import random
import time

st.set_page_config(page_title="AI Guess My Mind", page_icon="🧠", layout="centered")

# ---------- DESIGN + ANIMATIONS ----------

st.markdown("""
<style>
@keyframes bgmove {
    0%   {background-position: 0% 50%;}
    50%  {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
@keyframes rainbow {
    0%   {background-position: 0% 50%;}
    100% {background-position: 200% 50%;}
}
@keyframes pulse {
    0%,100% {transform: scale(1);}
    50%     {transform: scale(1.06);}
}
@keyframes floaty {
    0%   {transform: translateY(105vh) rotate(0deg); opacity: 0;}
    10%  {opacity: 0.8;}
    100% {transform: translateY(-15vh) rotate(360deg); opacity: 0;}
}
@keyframes pop {
    0%   {transform: scale(0.3); opacity: 0;}
    70%  {transform: scale(1.1); opacity: 1;}
    100% {transform: scale(1);}
}
@keyframes slidein {
    from {transform: translateX(-40px); opacity: 0;}
    to   {transform: translateX(0); opacity: 1;}
}
@keyframes shake {
    0%,100% {transform: translateX(0);}
    20% {transform: translateX(-8px);}
    40% {transform: translateX(8px);}
    60% {transform: translateX(-8px);}
    80% {transform: translateX(8px);}
}
@keyframes glow {
    0%,100% {box-shadow: 0 0 10px #ff512f, 0 0 20px #dd2476;}
    50%     {box-shadow: 0 0 25px #00f2fe, 0 0 45px #a044ff;}
}

.stApp {
    background: linear-gradient(120deg,#141e30,#243b55,#6a3093,#a044ff,#ff512f,#00c6ff);
    background-size: 400% 400%;
    animation: bgmove 18s ease infinite;
    color: white;
}
h1, h2, h3, p, label, span, div[data-testid="stMarkdownContainer"] {
    color: white !important;
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: 900;
    background: linear-gradient(90deg,#ffe600,#ff512f,#00f2fe,#7CFC00,#ffe600);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rainbow 3s linear infinite, pulse 2s ease-in-out infinite;
}
div.stButton > button {
    background: linear-gradient(90deg,#ff512f,#dd2476,#a044ff);
    background-size: 200% auto;
    color: white;
    border: none;
    border-radius: 15px;
    font-weight: bold;
    width: 100%;
    height: 52px;
    transition: all .3s ease;
    animation: glow 3s ease-in-out infinite;
}
div.stButton > button:hover {
    transform: scale(1.04) translateY(-2px);
    background-position: right center;
}
.qcard {
    background: rgba(0,0,0,0.45);
    padding: 18px 20px;
    border-radius: 18px;
    border-left: 8px solid var(--accent, #ffe600);
    margin: 10px 0;
    font-size: 22px;
    font-weight: bold;
    animation: slidein .5s ease;
}
.box {
    background: rgba(0,0,0,0.45);
    padding: 22px;
    border-radius: 20px;
    text-align: center;
    animation: pop .7s ease;
    margin-top: 12px;
}
.ai-win   {border: 3px solid #00f2fe; box-shadow: 0 0 30px #00f2fe;}
.user-win {border: 3px solid #ffe600; box-shadow: 0 0 30px #ffe600; animation: pop .7s ease, shake .6s ease .7s;}
.guess {
    font-size: 36px;
    font-weight: 900;
    color: #ffe600;
    animation: pulse 1.2s ease-in-out infinite;
}
.stat {
    background: rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 8px;
    text-align: center;
    font-weight: bold;
}
.float {
    position: fixed;
    bottom: -60px;
    font-size: 30px;
    z-index: 0;
    pointer-events: none;
    animation: floaty linear infinite;
}
</style>

<div class="float" style="left:5%;  animation-duration:11s;">🧠</div>
<div class="float" style="left:20%; animation-duration:15s; animation-delay:2s;">🔮</div>
<div class="float" style="left:38%; animation-duration:13s; animation-delay:5s;">⭐</div>
<div class="float" style="left:55%; animation-duration:17s; animation-delay:1s;">🎯</div>
<div class="float" style="left:72%; animation-duration:12s; animation-delay:4s;">✨</div>
<div class="float" style="left:88%; animation-duration:16s; animation-delay:3s;">🤖</div>
""", unsafe_allow_html=True)


# ---------- GAME DATA (10 questions per topic) ----------

YN = ["Yes", "No"]

TOPICS = {
    "🐾 Animals": {
        "color": "#7CFC00",
        "questions": [
            ("Wild or Domestic?", ["Wild", "Domestic"]),
            ("Where does it live?", ["Land", "Water", "Air"]),
            ("Big or Small?", ["Big", "Small"]),
            ("What does it eat?", ["Carnivore", "Herbivore", "Omnivore"]),
            ("Can it fly?", YN),
            ("Is it a mammal?", YN),
            ("Is it dangerous?", YN),
            ("Can it be kept as a pet?", YN),
            ("Does it live in groups?", YN),
            ("Is it fast?", YN),
        ],
        "items": {
            "Lion":     ["Wild", "Land", "Big", "Carnivore", "No", "Yes", "Yes", "No", "Yes", "Yes"],
            "Tiger":    ["Wild", "Land", "Big", "Carnivore", "No", "Yes", "Yes", "No", "No", "Yes"],
            "Dog":      ["Domestic", "Land", "Small", "Omnivore", "No", "Yes", "No", "Yes", "Yes", "Yes"],
            "Cat":      ["Domestic", "Land", "Small", "Carnivore", "No", "Yes", "No", "Yes", "No", "Yes"],
            "Shark":    ["Wild", "Water", "Big", "Carnivore", "No", "No", "Yes", "No", "No", "Yes"],
            "Eagle":    ["Wild", "Air", "Big", "Carnivore", "Yes", "No", "Yes", "No", "No", "Yes"],
            "Rabbit":   ["Domestic", "Land", "Small", "Herbivore", "No", "Yes", "No", "Yes", "Yes", "Yes"],
            "Elephant": ["Wild", "Land", "Big", "Herbivore", "No", "Yes", "No", "No", "Yes", "No"],
            "Parrot":   ["Domestic", "Air", "Small", "Herbivore", "Yes", "No", "No", "Yes", "Yes", "No"],
        },
    },

    "🍎 Fruits": {
        "color": "#ff4d6d",
        "questions": [
            ("What is its colour?", ["Red", "Yellow", "Green", "Orange"]),
            ("Sweet or Sour?", ["Sweet", "Sour"]),
            ("Big or Small?", ["Big", "Small"]),
            ("Does it have a thick peel?", YN),
            ("Does it grow on a tree?", YN),
            ("Is it very juicy?", YN),
            ("Is it available all year?", YN),
            ("Does it have one big seed/stone?", YN),
            ("Does it grow in tropical places?", YN),
            ("Is it popular as a juice?", YN),
        ],
        "items": {
            "Apple":      ["Red", "Sweet", "Small", "No", "Yes", "Yes", "Yes", "No", "No", "Yes"],
            "Banana":     ["Yellow", "Sweet", "Small", "Yes", "No", "No", "Yes", "No", "Yes", "No"],
            "Mango":      ["Yellow", "Sweet", "Big", "Yes", "Yes", "Yes", "No", "Yes", "Yes", "Yes"],
            "Lemon":      ["Yellow", "Sour", "Small", "Yes", "Yes", "Yes", "Yes", "No", "No", "Yes"],
            "Watermelon": ["Green", "Sweet", "Big", "Yes", "No", "Yes", "No", "No", "Yes", "Yes"],
            "Guava":      ["Green", "Sweet", "Small", "No", "Yes", "No", "No", "No", "Yes", "Yes"],
            "Orange":     ["Orange", "Sweet", "Small", "Yes", "Yes", "Yes", "No", "No", "No", "Yes"],
            "Strawberry": ["Red", "Sweet", "Small", "No", "No", "Yes", "No", "No", "No", "No"],
        },
    },

    "🌟 Celebrities": {
        "color": "#ffd700",
        "questions": [
            ("Which industry?", ["Tamil", "Bollywood", "International"]),
            ("What are they famous for?", ["Acting", "Singing", "Sports"]),
            ("Male or Female?", ["Male", "Female"]),
            ("Is their age above 40?", YN),
            ("Are they Indian?", YN),
            ("Are they famous worldwide?", YN),
            ("Known for dance / music?", YN),
            ("Started career before 2005?", YN),
            ("Has their own business / brand?", YN),
            ("Won major awards?", YN),
        ],
        "items": {
            "Vijay":             ["Tamil", "Acting", "Male", "Yes", "Yes", "No", "Yes", "Yes", "No", "Yes"],
            "Ajith":             ["Tamil", "Acting", "Male", "Yes", "Yes", "No", "No", "Yes", "Yes", "Yes"],
            "Suriya":            ["Tamil", "Acting", "Male", "Yes", "Yes", "No", "No", "Yes", "Yes", "Yes"],
            "Nayanthara":        ["Tamil", "Acting", "Female", "Yes", "Yes", "No", "No", "Yes", "Yes", "Yes"],
            "Dhanush":           ["Tamil", "Acting", "Male", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"],
            "Shah Rukh Khan":    ["Bollywood", "Acting", "Male", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"],
            "Deepika Padukone":  ["Bollywood", "Acting", "Female", "Yes", "Yes", "Yes", "No", "Yes", "Yes", "Yes"],
            "Taylor Swift":      ["International", "Singing", "Female", "No", "No", "Yes", "Yes", "No", "Yes", "Yes"],
            "Cristiano Ronaldo": ["International", "Sports", "Male", "Yes", "No", "Yes", "No", "Yes", "Yes", "Yes"],
        },
    },

    "🎬 Movies": {
        "color": "#ff9f1c",
        "questions": [
            ("Which language?", ["Tamil", "English", "Hindi"]),
            ("What genre?", ["Action", "Comedy", "Romance"]),
            ("Hero or Animation?", ["Hero", "Animation"]),
            ("Released after 2015?", YN),
            ("Has many songs?", YN),
            ("Has a sad ending?", YN),
            ("Has a sequel / franchise?", YN),
            ("Is it family friendly?", YN),
            ("Is it longer than 2.5 hours?", YN),
            ("Won big awards?", YN),
        ],
        "items": {
            "Leo":        ["Tamil", "Action", "Hero", "Yes", "No", "No", "No", "No", "Yes", "No"],
            "Master":     ["Tamil", "Action", "Hero", "Yes", "Yes", "No", "No", "No", "Yes", "No"],
            "Love Today": ["Tamil", "Comedy", "Hero", "Yes", "Yes", "No", "No", "Yes", "No", "No"],
            "96":         ["Tamil", "Romance", "Hero", "Yes", "Yes", "Yes", "No", "Yes", "No", "Yes"],
            "Avatar":     ["English", "Action", "Animation", "No", "No", "No", "Yes", "Yes", "Yes", "Yes"],
            "Titanic":    ["English", "Romance", "Hero", "No", "Yes", "Yes", "No", "Yes", "Yes", "Yes"],
            "Frozen":     ["English", "Romance", "Animation", "No", "Yes", "No", "Yes", "Yes", "No", "Yes"],
            "3 Idiots":   ["Hindi", "Comedy", "Hero", "No", "Yes", "No", "No", "Yes", "Yes", "Yes"],
        },
    },

    "🦸 Superheroes": {
        "color": "#4cc9f0",
        "questions": [
            ("Which universe?", ["Marvel", "DC"]),
            ("Has superpowers?", YN),
            ("Human or Alien?", ["Human", "Alien"]),
            ("Wears a mask?", YN),
            ("Wears a cape?", YN),
            ("Can fly?", YN),
            ("Part of a team?", YN),
            ("Is a billionaire?", YN),
            ("Uses gadgets / weapons?", YN),
            ("Has a dark, serious style?", YN),
        ],
        "items": {
            "Iron Man":     ["Marvel", "Yes", "Human", "No", "No", "Yes", "Yes", "Yes", "Yes", "No"],
            "Thor":         ["Marvel", "Yes", "Alien", "No", "Yes", "Yes", "Yes", "No", "Yes", "No"],
            "Spider-Man":   ["Marvel", "Yes", "Human", "Yes", "No", "No", "Yes", "No", "Yes", "No"],
            "Hulk":         ["Marvel", "Yes", "Human", "No", "No", "No", "Yes", "No", "No", "Yes"],
            "Superman":     ["DC", "Yes", "Alien", "No", "Yes", "Yes", "Yes", "No", "No", "No"],
            "Batman":       ["DC", "No", "Human", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes"],
            "Wonder Woman": ["DC", "Yes", "Alien", "No", "No", "Yes", "Yes", "No", "Yes", "No"],
            "Flash":        ["DC", "Yes", "Human", "Yes", "No", "No", "Yes", "No", "No", "No"],
        },
    },

    "📺 Cartoons": {
        "color": "#f72585",
        "questions": [
            ("Which channel?", ["Disney", "Cartoon Network"]),
            ("Animal or Human?", ["Animal", "Human"]),
            ("Funny or Adventure?", ["Funny", "Adventure"]),
            ("Is it a duo / group show?", YN),
            ("Uses gadgets or powers?", YN),
            ("Started before the year 2000?", YN),
            ("Is the hero a kid?", YN),
            ("Is the hero naughty?", YN),
            ("Has a gang of friends?", YN),
            ("Very popular in India?", YN),
        ],
        "items": {
            "Mickey Mouse":      ["Disney", "Animal", "Funny", "No", "No", "Yes", "No", "Yes", "Yes", "Yes"],
            "Tom and Jerry":     ["Cartoon Network", "Animal", "Funny", "Yes", "No", "Yes", "No", "Yes", "No", "Yes"],
            "Doraemon":          ["Disney", "Animal", "Adventure", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes"],
            "Shinchan":          ["Disney", "Human", "Funny", "No", "No", "Yes", "Yes", "Yes", "Yes", "Yes"],
            "Ben 10":            ["Cartoon Network", "Human", "Adventure", "No", "Yes", "No", "Yes", "No", "Yes", "Yes"],
            "Powerpuff Girls":   ["Cartoon Network", "Human", "Adventure", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes"],
        },
    },

    "⚽ Sports": {
        "color": "#06d6a0",
        "questions": [
            ("Indoor or Outdoor?", ["Indoor", "Outdoor"]),
            ("Team or Individual?", ["Team", "Individual"]),
            ("Is a ball used?", YN),
            ("Is it in the Olympics?", YN),
            ("Needs a bat / racket / stick?", YN),
            ("Lots of running?", YN),
            ("Physical contact?", YN),
            ("Popular in India?", YN),
            ("Has a net or goal?", YN),
            ("Mostly a brain game?", YN),
        ],
        "items": {
            "Cricket":    ["Outdoor", "Team", "Yes", "No", "Yes", "Yes", "No", "Yes", "No", "No"],
            "Football":   ["Outdoor", "Team", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "No"],
            "Chess":      ["Indoor", "Individual", "No", "No", "No", "No", "No", "Yes", "No", "Yes"],
            "Badminton":  ["Indoor", "Individual", "No", "Yes", "Yes", "Yes", "No", "Yes", "Yes", "No"],
            "Basketball": ["Indoor", "Team", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "No"],
            "Kabaddi":    ["Outdoor", "Team", "No", "No", "No", "Yes", "Yes", "Yes", "No", "No"],
            "Tennis":     ["Outdoor", "Individual", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes", "No"],
        },
    },

    "🍕 Foods": {
        "color": "#ff7b00",
        "questions": [
            ("Sweet or Spicy?", ["Sweet", "Spicy"]),
            ("Hot or Cold?", ["Hot", "Cold"]),
            ("Veg or Non-veg?", ["Veg", "Non-veg"]),
            ("Is it a snack?", YN),
            ("Eaten with hands?", YN),
            ("Is it fried?", YN),
            ("Has cheese?", YN),
            ("Is it Indian origin?", YN),
            ("Eaten for breakfast?", YN),
            ("Common at parties / festivals?", YN),
        ],
        "items": {
            "Pizza":       ["Spicy", "Hot", "Veg", "No", "Yes", "No", "Yes", "No", "No", "Yes"],
            "Ice Cream":   ["Sweet", "Cold", "Veg", "Yes", "No", "No", "No", "No", "No", "Yes"],
            "Biryani":     ["Spicy", "Hot", "Non-veg", "No", "No", "No", "No", "Yes", "No", "Yes"],
            "Gulab Jamun": ["Sweet", "Hot", "Veg", "Yes", "No", "Yes", "No", "Yes", "No", "Yes"],
            "Burger":      ["Spicy", "Hot", "Veg", "Yes", "Yes", "No", "Yes", "No", "No", "No"],
            "Dosa":        ["Spicy", "Hot", "Veg", "No", "Yes", "No", "No", "Yes", "Yes", "No"],
            "Samosa":      ["Spicy", "Hot", "Veg", "Yes", "Yes", "Yes", "No", "Yes", "No", "Yes"],
        },
    },
}

TOTAL_Q = 10

# ---------- SESSION STATE ----------

defaults = {
    "ai_score": 0,
    "user_score": 0,
    "rounds": 0,
    "stage": "start",      # start -> quiz -> guess -> result
    "qi": 0,
    "answers": [],
    "topic": None,
    "prediction": None,
    "confidence": 0,
    "runners": [],
    "winner": None,
    "thinking": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_round():
    st.session_state.stage = "start"
    st.session_state.qi = 0
    st.session_state.answers = []
    st.session_state.prediction = None
    st.session_state.winner = None
    st.session_state.thinking = False


def make_prediction():
    topic = st.session_state.topic
    answers = st.session_state.answers
    items = TOPICS[topic]["items"]
    scores = {
        item: sum(1 for a, b in zip(answers, feats) if a == b)
        for item, feats in items.items()
    }
    best = max(scores.values())
    candidates = [i for i, s in scores.items() if s == best]
    st.session_state.prediction = random.choice(candidates)
    st.session_state.confidence = int(best / TOTAL_Q * 100)
    ranked = sorted(scores, key=scores.get, reverse=True)
    st.session_state.runners = [
        r for r in ranked if r != st.session_state.prediction
    ][:2]


# ---------- HEADER ----------

st.markdown("<div class='title'>🧠 AI GUESS MY MIND 🔮</div>", unsafe_allow_html=True)
st.write("### 🎮 Can you beat the AI?")

name = st.text_input("👤 Enter Your Name")
college = st.text_input("🏫 Enter Your School / College Name")
department = st.text_input("📚 Enter Your Department")

if name and college and department:
    st.success(f"Welcome {name}! 🎉")
    st.write(f"🏫 Institution: {college}")
    st.write(f"📚 Department: {department}")

# ---------- SCOREBOARD ----------

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='stat'>🤖 AI Wins<br><span style='font-size:28px'>{st.session_state.ai_score}</span></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat'>🧑 {name or 'You'}<br><span style='font-size:28px'>{st.session_state.user_score}</span></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat'>🎮 Rounds<br><span style='font-size:28px'>{st.session_state.rounds}</span></div>", unsafe_allow_html=True)
st.markdown("")

stage = st.session_state.stage

# ---------- STAGE: START ----------

if stage == "start":
    topic = st.selectbox("🎯 Choose Your Favourite Topic", list(TOPICS.keys()))
    st.markdown("### 💭 Think of something!")
    st.info(f"Think of one thing from the topic. The AI will ask {TOTAL_Q} questions. Don't tell the AI!")

    if st.button("🚀 START GAME"):
        if not name or not college or not department:
            st.warning("Please enter your details first!")
        else:
            st.session_state.topic = topic
            st.session_state.answers = []
            st.session_state.qi = 0
            st.session_state.stage = "quiz"
            st.rerun()

# ---------- STAGE: QUIZ ----------

elif stage == "quiz":
    topic = st.session_state.topic
    qi = st.session_state.qi
    question, options = TOPICS[topic]["questions"][qi]
    accent = TOPICS[topic]["color"]

    st.markdown(f"#### {topic}")
    st.progress(qi / TOTAL_Q, text=f"Question {qi + 1} of {TOTAL_Q}")

    st.markdown(
        f"<div class='qcard' style='--accent:{accent}'>❓ Q{qi + 1}. {question}</div>",
        unsafe_allow_html=True,
    )

    choice = st.radio("Your answer", options, key=f"ans_{topic}_{qi}", horizontal=True)

    last = qi == TOTAL_Q - 1
    if st.button("🔮 REVEAL MY MIND" if last else "➡️ NEXT"):
        st.session_state.answers.append(choice)
        if last:
            make_prediction()
            st.session_state.thinking = True
            st.session_state.stage = "guess"
        else:
            st.session_state.qi += 1
        st.rerun()

# ---------- STAGE: GUESS ----------

elif stage == "guess":
    if st.session_state.thinking:
        holder = st.empty()
        bar = st.progress(0)
        msgs = [
            "🧠 Scanning your brain waves...",
            "📡 Connecting to the mind network...",
            "🔍 Analysing your 10 answers...",
            "✨ Almost there...",
        ]
        for pct in range(0, 101, 4):
            holder.markdown(
                f"<div class='box'><h3>{msgs[min(pct // 26, 3)]}</h3></div>",
                unsafe_allow_html=True,
            )
            bar.progress(pct)
            time.sleep(0.06)
        holder.empty()
        bar.empty()
        st.session_state.thinking = False
        st.balloons()

    pred = st.session_state.prediction
    conf = st.session_state.confidence

    st.markdown(
  f"""
        <div class="box">
            <h3>🤖 I think you are thinking about...</h3>
            <div class="guess">🎯 {pred} 🎯</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(conf, text=f"AI Confidence: {conf}%")
    if st.session_state.runners:
        st.caption("Other options I considered: " + ", ".join(st.session_state.runners))

    st.markdown("### 🤔 Did the AI guess correctly?")
    b1, b2 = st.columns(2)
    if b1.button("✅ Yes, AI got it!"):
        st.session_state.winner = "ai"
        st.session_state.ai_score += 1
        st.session_state.rounds += 1
        st.session_state.stage = "result"
        st.rerun()
    if b2.button("❌ No, I fooled AI!"):
        st.session_state.winner = "user"
        st.session_state.user_score += 1
        st.session_state.rounds += 1
        st.session_state.stage = "result"
        st.rerun()

# ---------- STAGE: RESULT ----------

elif stage == "result":
    pred = st.session_state.prediction

    if st.session_state.winner == "ai":
        st.balloons()
        st.markdown(
            f"""
            <div class="box ai-win">
                <h1>🏆 AI WINS! 🤖</h1>
                <h3>It guessed <span style='color:#ffe600'>{pred}</span> correctly!</h3>
                <p>Nice try, {name}! Want a rematch? 😎</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.snow()
        st.balloons()
        st.markdown(
            f"""
            <div class="box user-win">
                <h1>🎉 {name or 'YOU'} WIN! 🏆</h1>
                <h3>You fooled the AI! It guessed wrong with <span style='color:#ffe600'>{pred}</span> 😜</h3>
                <p>Mind of steel, {name}! 🔥</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    if st.session_state.user_score > st.session_state.ai_score:
        st.success(f"👑 {name or 'You'} are leading the match!")
    elif st.session_state.ai_score > st.session_state.user_score:
        st.error("🤖 AI is leading the match!")
    else:
        st.warning("🤝 It's a tie so far!")

    if st.button("🔄 PLAY AGAIN"):
        reset_round()
        st.rerun()

st.markdown("---")
st.caption("🎓 AI & DS Department | College Expo Project")
st.caption("Created by: " + (name if name else "AI Student"))
