from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'cyber_matrix_ultra_secret_key'

# Strict Mapping based on your required age conditions
SKILL_CATALOG = {
    "Below 15": [
        {"id": 1, "title": "Scratch Programming", "desc": "Logic building & core visual algorithm design.", "tag": "Logic Core", "cost": "Free"},
        {"id": 2, "title": "Basic English", "desc": "Global lingual protocols & clear communication.", "tag": "Linguistics", "cost": "Free"},
        {"id": 3, "title": "Communication", "desc": "Interpersonal networking & vocal presence.", "tag": "Soft Skills", "cost": "Free"}
    ],
    "15–18": [
        {"id": 4, "title": "Python Basics", "desc": "High-level automation & computational scripting.", "tag": "Software", "cost": "$29"},
        {"id": 5, "title": "Web Development", "desc": "Frontend web architecture (HTML/CSS/JS).", "tag": "Web Eng", "cost": "$39"},
        {"id": 6, "title": "Git & GitHub", "desc": "Version control & distributed code collaboration.", "tag": "DevOps Tools", "cost": "Free"}
    ],
    "19–22": [
        {"id": 7, "title": "Data Structures", "desc": "Advanced algorithmic speed & data structures.", "tag": "CS Core", "cost": "$49"},
        {"id": 8, "title": "Docker", "desc": "App isolation, image builds, and containerization.", "tag": "Containers", "cost": "$59"},
        {"id": 9, "title": "Cloud Computing", "desc": "Serverless architectures & infrastructure design.", "tag": "Cloud Eng", "cost": "$69"}
    ],
    "23–30": [
        {"id": 10, "title": "AWS Cloud", "desc": "Enterprise cloud deployment & fault tolerance.", "tag": "AWS Architect", "cost": "$89"},
        {"id": 11, "title": "DevOps", "desc": "CI/CD automation pipelines & Kubernetes orchestration.", "tag": "DevOps Specialist", "cost": "$99"},
        {"id": 12, "title": "AI & Machine Learning", "desc": "Predictive neural models & Deep Learning.", "tag": "AI Engineering", "cost": "$129"}
    ],
    "Above 30": [
        {"id": 13, "title": "Leadership", "desc": "Executive vision, team scaling, and strategy.", "tag": "Executive", "cost": "$149"},
        {"id": 14, "title": "Project Management", "desc": "Agile framework, risk mitigation, and execution.", "tag": "Agile Lead", "cost": "$119"},
        {"id": 15, "title": "AI for Professionals", "desc": "AI productivity integration & workplace automation.", "tag": "AI Strategy", "cost": "$139"}
    ]
}

def determine_age_tier(age):
    if age < 15:
        return "Below 15"
    elif 15 <= age <= 18:
        return "15–18"
    elif 19 <= age <= 22:
        return "19–22"
    elif 23 <= age <= 30:
        return "23–30"
    else:
        return "Above 30"

@app.before_request
def initialize_session():
    if 'cart' not in session:
        session['cart'] = []
    if 'installed' not in session:
        session['installed'] = []

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('recommendations'))
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name', '').strip()
    age_raw = request.form.get('age', '').strip()

    if not name or not age_raw:
        flash('⚠️ Diagnostic Failure: Name and age are mandatory.', 'danger')
        return redirect(url_for('home'))

    try:
        age = int(age_raw)
        if age <= 0 or age > 120:
            raise ValueError
    except ValueError:
        flash('⚠️ Invalid Age Protocol: Enter a valid number between 1 and 120.', 'danger')
        return redirect(url_for('home'))

    session['user'] = {
        'name': name,
        'age': age,
        'tier': determine_age_tier(age)
    }
    flash(f"⚡ Biometric scan complete. Welcome Operative {name}.", "success")
    return redirect(url_for('recommendations'))

@app.route('/recommendations')
def recommendations():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    
    available_courses = SKILL_CATALOG.get(user['tier'], [])
    return render_template('recommendations.html', user=user, courses=available_courses)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    course_id = request.form.get('course_id', type=int)
    
    # Locate skill in database
    target_skill = None
    for tier_skills in SKILL_CATALOG.values():
        for skill in tier_skills:
            if skill['id'] == course_id:
                target_skill = skill
                break
                
    if target_skill:
        cart = session.get('cart', [])
        installed = session.get('installed', [])
        
        if any(item['id'] == course_id for item in cart):
            flash(f"ℹ️ Module '{target_skill['title']}' is already staged in your Cart Bay.", "warning")
        elif any(item['id'] == course_id for item in installed):
            flash(f"ℹ️ Module '{target_skill['title']}' is already installed in your Neural Matrix.", "warning")
        else:
            cart.append(target_skill)
            session['cart'] = cart
            flash(f"✅ Staged '{target_skill['title']}' into Cart Bay.", "success")
            
    return redirect(url_for('recommendations'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart=cart_items)

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    course_id = request.form.get('course_id', type=int)
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['id'] != course_id]
    flash("🗑️ Skill module removed from cart.", "info")
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash("⚠️ Your Cart Bay is empty.", "danger")
        return redirect(url_for('cart'))
    
    installed = session.get('installed', [])
    installed.extend(cart)
    session['installed'] = installed
    session['cart'] = []  # Clear cart
    
    flash("🚀 System Upgrade Complete! Skills synced to Neural Profile.", "success")
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    
    installed_skills = session.get('installed', [])
    return render_template('profile.html', user=user, courses=installed_skills)

@app.route('/logout')
def logout():
    session.clear()
    flash("🔌 Session terminated. Diagnostic cleared.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)