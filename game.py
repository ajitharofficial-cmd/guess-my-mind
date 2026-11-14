import streamlit as st
import random

st.set_page_config(
    page_title="AI Guess My Mind",
    page_icon="🧠",
    layout="centered"
)

# ---------- DESIGN ----------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        120deg,
        #141e30,
        #243b55,
        #6a3093,
        #a044ff
    );
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

div.stButton > button {
    background: linear-gradient(90deg,#ff512f,#dd2476);
    color: white;
    border-radius: 15px;
    font-weight: bold;
    width: 100%;
    height: 50px;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #ffe600;
}

.box {
    background: rgba(0,0,0,0.4);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ---------- STUDENT DETAILS ----------

st.markdown(
    "<div class='title'>🧠 AI GUESS MY MIND 🔮</div>",
    unsafe_allow_html=True
)

st.write("### 🎮 Welcome to the AI Mind Reading Game!")

name = st.text_input("👤 Enter Your Name")

college = st.text_input("🏫 Enter Your School / College Name")

department = st.text_input("📚 Enter Your Department")


if name and college and department:

    st.success(f"Welcome {name}! 🎉")

    st.write(f"🏫 Institution: {college}")

    st.write(f"📚 Department: {department}")


# ---------- GAME DATA ----------

TOPICS = {

    "🐾 Animals": {
        "questions": [
            ("Wild or Domestic?", ["Wild", "Domestic"]),
            ("Where does it live?", ["Land", "Water", "Air"]),
            ("Big or Small?", ["Big", "Small"])
        ],

        "items": {
            "Lion": ["Wild", "Land", "Big"],
            "Tiger": ["Wild", "Land", "Big"],
            "Dog": ["Domestic", "Land", "Small"],
            "Cat": ["Domestic", "Land", "Small"],
            "Shark": ["Wild", "Water", "Big"],
            "Eagle": ["Wild", "Air", "Big"],
            "Rabbit": ["Domestic", "Land", "Small"]
        }
    },

    "🍎 Fruits": {
        "questions": [
            ("What is its colour?", ["Red", "Yellow", "Green"]),
            ("Sweet or Sour?", ["Sweet", "Sour"]),
            ("Big or Small?", ["Big", "Small"])
        ],

        "items": {
            "Apple": ["Red", "Sweet", "Small"],
            "Banana": ["Yellow", "Sweet", "Small"],
            "Mango": ["Yellow", "Sweet", "Big"],
            "Lemon": ["Yellow", "Sour", "Small"],
            "Watermelon": ["Green", "Sweet", "Big"],
            "Guava": ["Green", "Sweet", "Small"]
        }
    },

    "🌟 Celebrities": {
        "questions": [
            ("Which industry?", ["Tamil", "Hollywood", "Bollywood"]),
            ("What are they famous for?", ["Acting", "Singing", "Sports"]),
            ("Male or Female?", ["Male", "Female"])
        ],

        "items": {
            "Vijay": ["Tamil", "Acting", "Male"],
            "Ajith": ["Tamil", "Acting", "Male"],
            "Suriya": ["Tamil", "Acting", "Male"],
            "Nayanthara": ["Tamil", "Acting", "Female"],
            "Dhanush": ["Tamil", "Acting", "Male"],
            "Shah Rukh Khan": ["Bollywood", "Acting", "Male"],
            "Deepika Padukone": ["Bollywood", "Acting", "Female"],
            "Taylor Swift": ["Hollywood", "Singing", "Female"],
            "Cristiano Ronaldo": ["Hollywood", "Sports", "Male"]
        }
    },

    "🎬 Movies": {
        "questions": [
            ("Which language?", ["Tamil", "English", "Hindi"]),
            ("What genre?", ["Action", "Comedy", "Romance"]),
            ("Hero or Animation?", ["Hero", "Animation"])
        ],

        "items": {
            "Leo": ["Tamil", "Action", "Hero"],
            "Master": ["Tamil", "Action", "Hero"],
            "Love Today": ["Tamil", "Comedy", "Hero"],
            "96": ["Tamil", "Romance", "Hero"],
            "Avatar": ["English", "Action", "Animation"],
            "Titanic": ["English", "Romance", "Hero"],
            "Frozen": ["English", "Romance", "Animation"],
            "3 Idiots": ["Hindi", "Comedy", "Hero"]
        }
    },

    "🦸 Superheroes": {
        "questions": [
            ("Which universe?", ["Marvel", "DC"]),
            ("Has superpowers?", ["Yes", "No"]),
            ("Human or Alien?", ["Human", "Alien"])
        ],

        "items": {
            "Iron Man": ["Marvel", "Yes", "Human"],
            "Thor": ["Marvel", "Yes", "Alien"],
            "Spider-Man": ["Marvel", "Yes", "Human"],
            "Superman": ["DC", "Yes", "Alien"],
            "Batman": ["DC", "No", "Human"],
            "Wonder Woman": ["DC", "Yes", "Alien"]
        }
    },

    "📺 Cartoons": {
        "questions": [
            ("Which channel?", ["Disney", "Cartoon Network"]),
            ("Animal or Human?", ["Animal", "Human"]),
            ("Funny or Adventure?", ["Funny", "Adventure"])
        ],

        "items": {
            "Mickey Mouse": ["Disney", "Animal", "Funny"],
            "Tom and Jerry": ["Cartoon Network", "Animal", "Funny"],
            "Doraemon": ["Disney", "Animal", "Adventure"],
            "Shinchan": ["Disney", "Human", "Funny"],
            "Ben 10": ["Cartoon Network", "Human", "Adventure"]
        }
    },

    "⚽ Sports": {
        "questions": [
            ("Indoor or Outdoor?", ["Indoor", "Outdoor"]),
            ("Team or Individual?", ["Team", "Individual"]),
            ("Ball used?", ["Yes", "No"])
        ],

        "items": {
            "Cricket": ["Outdoor", "Team", "Yes"],
            "Football": ["Outdoor", "Team", "Yes"],
            "Chess": ["Indoor", "Individual", "No"],
            "Badminton": ["Indoor", "Individual", "No"],
            "Basketball": ["Indoor", "Team", "Yes"]
        }
    },

    "🍕 Foods": {
        "questions": [
            ("Sweet or Spicy?", ["Sweet", "Spicy"]),
            ("Hot or Cold?", ["Hot", "Cold"]),
            ("Veg or Non-veg?", ["Veg", "Non-veg"])
        ],

        "items": {
            "Pizza": ["Spicy", "Hot", "Veg"],
            "Ice Cream": ["Sweet", "Cold", "Veg"],
            "Biryani": ["Spicy", "Hot", "Non-veg"],
            "Gulab Jamun": ["Sweet", "Hot", "Veg"],
            "Burger": ["Spicy", "Hot", "Veg"]
        }
    }
}


# ---------- SCOREBOARD ----------

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "rounds" not in st.session_state:
    st.session_state.rounds = 0


st.markdown("---")

c1, c2 = st.columns(2)

c1.metric("🤖 AI Wins", st.session_state.ai_score)

c2.metric("🎮 Rounds", st.session_state.rounds)


# ---------- GAME ----------

topic = st.selectbox(
    "🎯 Choose Your Favourite Topic",
    list(TOPICS.keys())
)

st.markdown("### 💭 Think of something!")

st.info("Don't tell the AI! Answer the questions honestly.")


answers = []

for i, (question, options) in enumerate(
    TOPICS[topic]["questions"]
):

    answer = st.radio(
        f"Q{i+1}. {question}",
        options,
        key=f"{topic}_{i}"
    )

    answers.append(answer)


# ---------- AI PREDICTION ----------

if st.button("🔮 AI GUESS MY MIND"):

    if not name or not college or not department:

        st.warning("Please enter your details first!")

    else:

        items = TOPICS[topic]["items"]

        scores = {}

        for item, features in items.items():

            score = sum(
                1 for a, b in zip(answers, features)
                if a == b
            )

            scores[item] = score

        best_score = max(scores.values())

        candidates = [
            item for item, score in scores.items()
            if score == best_score
        ]

        prediction = random.choice(candidates)

        confidence = int(
            (best_score / len(answers)) * 100
        )

        st.session_state.ai_score += 1

        st.session_state.rounds += 1

        st.balloons()

        st.markdown("---")

        st.markdown("## 🤖 AI PREDICTION")

        st.success(
            f"Hey {name}! I think you are thinking about {prediction}! 🎯"
        )

        st.progress(
            confidence,
            text=f"AI Confidence: {confidence}%"
        )

        st.markdown(
            f"""
            <div class="box">
            <h2>🏆 AI WINS!</h2>
            <h3>🤖 AI is the Champion!</h3>
            <p>Nice try, {name}!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "Did the AI guess correctly? 🤔"
        )

        st.write(
            "The AI always wins this fun challenge! 😎"
        )


# ---------- PLAY AGAIN ----------

if st.button("🔄 PLAY AGAIN"):

    st.rerun()


st.markdown("---")

st.caption(
    "🎓 AI & DS Department | College Expo Project"
)

st.caption(
    "Created by: " + (name if name else "AI Student")
)
