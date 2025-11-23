"""
routes/chatbot_routes.py

AI Chatbot for helping users find restaurants.
Processes natural language queries and provides intelligent search results.
"""

from flask import Blueprint, request, jsonify, render_template
from models.restaurant import Restaurant
from models.review import Review
from sqlalchemy import or_, and_

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chatbot")
def chatbot_page():
    """Render the chatbot page."""
    return render_template("chatbot.html")

def get_food_mappings():
    """
    Map food items to search terms and cuisine types.
    Returns dict mapping food items to related search terms.
    """
    return {
        # Meat dishes
        "steak": ["steak", "beef", "grilled", "kabob", "kebab", "kabobs", "kebabs"],
        "chicken": ["chicken", "poultry", "tenders", "wings", "fried chicken", "hot chicken", 
                    "chicken over rice", "shawarma", "gyro", "tandoori"],
        "beef": ["beef", "steak", "kabob", "kebab", "gyro", "cheesesteak", "biryani"],
        "lamb": ["lamb", "kabob", "kebab", "gyro", "shawarma"],
        
        # Specific dishes
        "gyro": ["gyro", "gyros", "shawarma", "wrap", "platter"],
        "shawarma": ["shawarma", "gyro", "wrap", "platter", "chicken"],
        "falafel": ["falafel", "middle eastern", "vegetarian"],
        "kabob": ["kabob", "kebab", "kabobs", "kebabs", "grilled", "pakistani", "middle eastern"],
        "biryani": ["biryani", "rice", "pakistani", "indian"],
        "curry": ["curry", "curries", "indian", "pakistani", "sauce"],
        "tandoori": ["tandoori", "chicken", "indian", "pakistani"],
        "naan": ["naan", "bread", "pakistani", "indian"],
        "platter": ["platter", "platters", "combo", "meal"],
        "burger": ["burger", "burgers", "smash burger", "fusion"],
        "wings": ["wings", "chicken wings", "fried"],
        "tenders": ["tenders", "chicken tenders", "hot chicken"],
        "fried chicken": ["fried chicken", "chicken", "crispy"],
        "hot chicken": ["hot chicken", "spicy", "nashville", "chicken"],
        "cheesesteak": ["cheesesteak", "cheesesteaks", "philly", "sandwich"],
        
        # Cuisine indicators
        "spicy": ["spicy", "hot", "bold", "nashville"],
        "grilled": ["grilled", "kabob", "kebab", "bbq"],
        "fried": ["fried", "crispy", "fried chicken"],
        "comfort food": ["comfort food", "fried", "chicken", "late night"],
    }

def detect_craving_pattern(query_lower):
    """
    Detect if user is expressing a craving or desire.
    Returns the food item they're craving, or None.
    """
    craving_patterns = [
        "i'm craving", "im craving", "i am craving",
        "i want", "i'd like", "id like", "i would like",
        "i feel like", "i'm in the mood for", "im in the mood for",
        "i need", "i could go for", "i'm hungry for", "im hungry for",
        "craving", "want some", "feel like", "in the mood"
    ]
    
    for pattern in craving_patterns:
        if pattern in query_lower:
            # Extract what comes after the pattern
            idx = query_lower.find(pattern)
            after_pattern = query_lower[idx + len(pattern):].strip()
            # Remove common words
            words = after_pattern.split()
            if words:
                # Get the first meaningful word (food item)
                food_item = words[0].rstrip('.,!?')
                return food_item
    return None

def map_food_to_search_terms(food_item):
    """
    Map a food item to related search terms for database search.
    """
    food_mappings = get_food_mappings()
    food_lower = food_item.lower()
    
    # Direct match
    if food_lower in food_mappings:
        return food_mappings[food_lower]
    
    # Check if food item is in any mapping
    for food, terms in food_mappings.items():
        if food_lower in terms or any(term in food_lower for term in terms):
            return terms
    
    # Default: return the food item itself and common variations
    return [food_item, food_item + "s", food_item + "es"]

def parse_query(query):
    """
    Parse natural language query to extract search parameters.
    Returns a dict with search criteria.
    """
    query_lower = query.lower()
    criteria = {
        "keywords": [],
        "cuisine": None,
        "halal_status": None,
        "rating_min": None,
        "location": None,
        "intent": "search",  # search, recommend, question, craving
        "food_items": []  # Specific food items mentioned
    }
    
    # Detect craving patterns first
    craving_food = detect_craving_pattern(query_lower)
    if craving_food:
        criteria["intent"] = "craving"
        criteria["food_items"].append(craving_food)
        # Map food to search terms
        search_terms = map_food_to_search_terms(craving_food)
        criteria["keywords"].extend(search_terms)
    
    # Extract cuisine types
    cuisines = ["middle eastern", "pakistani", "indian", "lebanese", "ethiopian", 
                "american", "fusion", "fried chicken", "halal"]
    for cuisine in cuisines:
        if cuisine in query_lower:
            criteria["cuisine"] = cuisine
            break
    
    # Extract halal status
    if "certified halal" in query_lower or "certified" in query_lower:
        criteria["halal_status"] = "Certified Halal"
    elif "halal" in query_lower:
        criteria["halal_status"] = "Halal"
    elif "halal-friendly" in query_lower:
        criteria["halal_status"] = "Halal-Friendly"
    
    # Extract rating requirements
    if "high rating" in query_lower or "best rated" in query_lower or "top rated" in query_lower:
        criteria["rating_min"] = 4.0
    elif "good rating" in query_lower or "well rated" in query_lower:
        criteria["rating_min"] = 3.5
    elif "4 star" in query_lower or "4 stars" in query_lower:
        criteria["rating_min"] = 4.0
    elif "5 star" in query_lower or "5 stars" in query_lower:
        criteria["rating_min"] = 5.0
    
    # Extract location keywords
    locations = ["philadelphia", "philly", "west philly", "temple", "center city"]
    for loc in locations:
        if loc in query_lower:
            criteria["location"] = loc
            break
    
    # Determine intent (if not already set to craving)
    if criteria["intent"] != "craving":
        if any(word in query_lower for word in ["recommend", "suggest", "what should", "what can"]):
            criteria["intent"] = "recommend"
        elif any(word in query_lower for word in ["what", "how", "where", "when", "why"]):
            criteria["intent"] = "question"
    
    # Extract food items and keywords from the query
    # Enhanced stop words list
    stop_words = ["find", "search", "looking", "for", "want", "need", "show", "me", 
                  "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
                  "have", "has", "had", "do", "does", "did", "will", "would", "could",
                  "should", "may", "might", "can", "must", "shall", "i'm", "im", "i",
                  "am", "craving", "feel", "like", "some", "get", "give"]
    
    # Extract meaningful words
    words = query_lower.split()
    meaningful_words = [w.rstrip('.,!?') for w in words if w not in stop_words and len(w) > 2]
    
    # Add food-related words to keywords if not already added
    for word in meaningful_words:
        if word not in criteria["keywords"]:
            # Check if it's a food item
            food_mappings = get_food_mappings()
            if word in food_mappings or any(word in terms for terms in food_mappings.values()):
                criteria["food_items"].append(word)
                search_terms = map_food_to_search_terms(word)
                criteria["keywords"].extend(search_terms)
            else:
                criteria["keywords"].append(word)
    
    # Remove duplicates
    criteria["keywords"] = list(set(criteria["keywords"]))
    criteria["food_items"] = list(set(criteria["food_items"]))
    
    return criteria

def search_restaurants(criteria):
    """
    Search restaurants based on parsed criteria.
    Returns list of matching restaurants.
    """
    query = Restaurant.query
    
    # Filter by cuisine
    if criteria["cuisine"]:
        query = query.filter(
            or_(
                Restaurant.cuisine.ilike(f"%{criteria['cuisine']}%"),
                Restaurant.description.ilike(f"%{criteria['cuisine']}%")
            )
        )
    
    # Filter by halal status
    if criteria["halal_status"]:
        query = query.filter(Restaurant.halal_status == criteria["halal_status"])
    
    # Filter by keywords (name, description) - use OR logic for more flexible matching
    if criteria["keywords"]:
        keyword_filters = []
        for keyword in criteria["keywords"]:
            keyword_filters.append(
                or_(
                    Restaurant.name.ilike(f"%{keyword}%"),
                    Restaurant.description.ilike(f"%{keyword}%"),
                    Restaurant.cuisine.ilike(f"%{keyword}%")
                )
            )
        # Use OR between keywords (any match is good) for more flexible results
        if keyword_filters:
            query = query.filter(or_(*keyword_filters))
    
    restaurants = query.all()
    
    # Filter by rating if specified
    if criteria["rating_min"]:
        filtered = []
        for r in restaurants:
            reviews = Review.query.filter_by(restaurant_id=r.id).all()
            if reviews:
                avg_rating = sum([rev.rating for rev in reviews]) / len(reviews)
                if avg_rating >= criteria["rating_min"]:
                    filtered.append(r)
        restaurants = filtered
    
    return restaurants

def generate_response(restaurants, criteria, original_query):
    """
    Generate a natural language response based on search results.
    """
    if not restaurants:
        # More helpful error message based on intent
        if criteria["intent"] == "craving" and criteria["food_items"]:
            food = criteria["food_items"][0]
            return {
                "message": f"I couldn't find any restaurants specifically serving {food}. But I can help you find:\n\n"
                           "• Restaurants by cuisine type (e.g., 'Middle Eastern', 'Pakistani')\n"
                           "• Places by food type (e.g., 'chicken', 'kabob', 'shawarma')\n"
                           "• Highly rated halal restaurants\n\n"
                           "What else would you like to try?",
                "restaurants": [],
                "count": 0
            }
        return {
            "message": "I couldn't find any restaurants matching your search. Try asking for:\n\n"
                       "• A specific cuisine (e.g., 'Middle Eastern' or 'Pakistani')\n"
                       "• A food item (e.g., 'I'm craving chicken' or 'I want kabob')\n"
                       "• Halal status (e.g., 'certified halal places')\n"
                       "• Highly rated restaurants",
            "restaurants": [],
            "count": 0
        }
    
    # Format restaurant data
    restaurants_data = []
    for r in restaurants:
        reviews = Review.query.filter_by(restaurant_id=r.id).all()
        avg_rating = None
        if reviews:
            avg_rating = round(sum([rev.rating for rev in reviews]) / len(reviews), 1)
        
        restaurants_data.append({
            "id": r.id,
            "name": r.name,
            "cuisine": r.cuisine,
            "halal_status": r.halal_status,
            "description": r.description,
            "address": r.address,
            "image_url": r.image_url,
            "avg_rating": avg_rating,
            "review_count": len(reviews)
        })
    
    # Generate contextual message based on intent
    if criteria["intent"] == "craving" and criteria["food_items"]:
        food = criteria["food_items"][0]
        message = f"Great choice! I found {len(restaurants_data)} restaurant{'s' if len(restaurants_data) != 1 else ''} that serve {food} or similar dishes:\n\n"
    elif criteria["intent"] == "recommend":
        message = f"I found {len(restaurants_data)} restaurant{'s' if len(restaurants_data) != 1 else ''} that might interest you:\n\n"
    else:
        message = f"I found {len(restaurants_data)} restaurant{'s' if len(restaurants_data) != 1 else ''} matching your search:\n\n"
    
    # Add top recommendations
    if len(restaurants_data) <= 3:
        for r in restaurants_data:
            rating_text = f" ({r['avg_rating']}/5)" if r['avg_rating'] else ""
            message += f"• **{r['name']}** - {r['cuisine']}{rating_text}\n"
    else:
        # Show top 3 by rating or first 3
        sorted_restaurants = sorted(
            restaurants_data, 
            key=lambda x: x['avg_rating'] if x['avg_rating'] else 0, 
            reverse=True
        )[:3]
        for r in sorted_restaurants:
            rating_text = f" ({r['avg_rating']}/5)" if r['avg_rating'] else ""
            message += f"• **{r['name']}** - {r['cuisine']}{rating_text}\n"
        message += f"\n...and {len(restaurants_data) - 3} more. Click on any restaurant to see details!"
    
    return {
        "message": message,
        "restaurants": restaurants_data,
        "count": len(restaurants_data)
    }

@chatbot_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chatbot endpoint.
    Accepts user message and returns AI response with restaurant results.
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({
            "message": "Please ask me something! I can help you find halal restaurants.",
            "restaurants": [],
            "count": 0
        })
    
    # Handle greetings and help
    greetings = ["hi", "hello", "hey", "help", "what can you do"]
    if user_message.lower() in greetings:
        return jsonify({
            "message": "Hi! I'm your halal restaurant assistant. I can help you:\n\n"
                       "• Express cravings naturally (e.g., 'I'm craving steak' or 'I want chicken')\n"
                       "• Find restaurants by cuisine (e.g., 'Find Middle Eastern restaurants')\n"
                       "• Search by halal status (e.g., 'Show me certified halal places')\n"
                       "• Get recommendations (e.g., 'Recommend a good Pakistani restaurant')\n"
                       "• Find highly rated restaurants (e.g., 'Show me top rated halal restaurants')\n\n"
                       "What would you like to search for?",
            "restaurants": [],
            "count": 0
        })
    
    # Parse the query
    criteria = parse_query(user_message)
    
    # Search restaurants
    restaurants = search_restaurants(criteria)
    
    # Generate response
    response = generate_response(restaurants, criteria, user_message)
    
    return jsonify(response)
