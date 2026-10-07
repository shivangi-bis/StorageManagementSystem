import json

from openai import OpenAI
from django.conf import settings

from products.models import Product
from orders.models import Order
from stock_history.models import StockMovement


client = OpenAI(api_key=settings.OPENAI_API_KEY)


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def get_product_count():
    return Product.objects.count()


def get_product_list():
    products = Product.objects.all()

    return [
        {
            "id": product.id,
            "name": product.name,
        }
        for product in products
    ]


def get_product_stock(product_name):
    products = Product.objects.filter(name__icontains=product_name)

    if not products.exists():
        return {
            "found": False,
            "message": f"No product found with name '{product_name}'."
        }

    result = []

    for product in products:

        try:
            inventory = product.inventory
            quantity = inventory.quantity
        except Exception:
            quantity = 0

        result.append({
            "id": product.id,
            "name": product.name,
            "stock": quantity,
        })

    return {
        "found": True,
        "products": result,
    }


def get_low_stock_products():
    LOW_STOCK_LIMIT = 5

    products = Product.objects.all()
    result = []

    for product in products:

        try:
            quantity = product.inventory.quantity
        except Exception:
            quantity = 0

        if quantity <= LOW_STOCK_LIMIT:
            result.append({
                "id": product.id,
                "name": product.name,
                "stock": quantity,
            })

    return result


def get_order_count():
    return Order.objects.count()


def get_recent_stock_movements():
    movements = (
        StockMovement.objects
        .select_related("product")
        .order_by("-created_at")[:10]
    )

    return [
        {
            "product": movement.product.name,
            "type": movement.movement_type,
            "quantity": movement.quantity,
            "reason": movement.reason,
            "created_at": movement.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
        for movement in movements
    ]


# =========================================================
# LLM INTENT DETECTION
# =========================================================

def detect_intent(question):

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
You are an intent classifier for a Storage Management System.

Understand the user's question.

Choose exactly ONE of these intents:

PRODUCT_COUNT
PRODUCT_LIST
PRODUCT_STOCK
LOW_STOCK
ORDER_COUNT
RECENT_STOCK_MOVEMENTS
UNKNOWN

If the intent is PRODUCT_STOCK, also identify the product name.

Return ONLY valid JSON.

For normal questions:
{{
    "intent": "PRODUCT_COUNT",
    "product_name": null
}}

For product stock questions:
{{
    "intent": "PRODUCT_STOCK",
    "product_name": "Dell Inspiron Laptop"
}}

Examples:

"How many products do I have?"
=> PRODUCT_COUNT

"Show me all products"
=> PRODUCT_LIST

"What is the stock of Dell Inspiron Laptop?"
=> PRODUCT_STOCK

"Which products are running low?"
=> LOW_STOCK

"Which products are almost out of stock?"
=> LOW_STOCK

"How many orders are there?"
=> ORDER_COUNT

"Show me the latest stock movements"
=> RECENT_STOCK_MOVEMENTS

User question:
{question}
"""
    )

    result = response.output_text.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        return {
            "intent": "UNKNOWN",
            "product_name": None
        }


# =========================================================
# LLM ANSWER GENERATION
# =========================================================

def generate_answer(question, intent_data, database_data):

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
You are a helpful assistant for a Storage Management System.

Answer the user's question using ONLY the database information
provided below.

Do NOT invent any information.

Keep the answer short, clear, and natural.

User question:
{question}

Detected intent:
{json.dumps(intent_data)}

Database information:
{json.dumps(database_data, default=str)}

Give only the final answer to the user.
"""
    )

    return response.output_text.strip()


# =========================================================
# MAIN CHATBOT FUNCTION
# =========================================================

def process_question(question):

    intent_data = detect_intent(question)

    intent = intent_data.get("intent")
    product_name = intent_data.get("product_name")

    database_data = None

    if intent == "PRODUCT_COUNT":

        database_data = {
            "product_count": get_product_count()
        }

    elif intent == "PRODUCT_LIST":

        database_data = {
            "products": get_product_list()
        }

    elif intent == "PRODUCT_STOCK":

        if not product_name:
            return {
                "intent": intent,
                "answer": "Please tell me the product name."
            }

        database_data = get_product_stock(product_name)

    elif intent == "LOW_STOCK":

        database_data = {
            "low_stock_products": get_low_stock_products()
        }

    elif intent == "ORDER_COUNT":

        database_data = {
            "order_count": get_order_count()
        }

    elif intent == "RECENT_STOCK_MOVEMENTS":

        database_data = {
            "recent_stock_movements": get_recent_stock_movements()
        }

    else:

        return {
            "intent": "UNKNOWN",
            "answer": "Sorry, I couldn't understand your question."
        }

    answer = generate_answer(
        question,
        intent_data,
        database_data
    )

    return {
        "intent": intent,
        "answer": answer,
        "data": database_data
    }


# =========================================================
# SIMPLE LLM TEST
# =========================================================

def test_llm():

    response = client.responses.create(
        model="gpt-4o-mini",
        input="Say hello in one short sentence."
    )

    return response.output_text