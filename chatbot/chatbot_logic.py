
import json
import os
from openai import OpenAI

from products.models import Product
from orders.models import Order
from stock_history.models import StockMovement


# =========================================================
# OLLAMA LLM CLIENT
# =========================================================

client = OpenAI(
    base_url=os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434/v1"
    ),
    api_key="ollama"
)

OLLAMA_MODEL = "qwen2.5:1.5b"


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


def get_total_stock():
    total = 0

    for product in Product.objects.all():
        try:
            total += product.inventory.quantity
        except Exception:
            pass

    return total


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
            quantity = product.inventory.quantity
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
    result = []

    for product in Product.objects.all():
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
# INTENT DETECTION
# =========================================================

def detect_intent(question):
    question = " ".join(question.lower().strip().split())

    # Total number of products
    if any(phrase in question for phrase in [
        "how many products",
        "product count",
        "total products",
        "number of products",
        "count products",
    ]):
        return {"intent": "PRODUCT_COUNT", "product_name": None}

    # Total stock across all products
    if any(phrase in question for phrase in [
        "how many stock is left",
        "how much stock is left",
        "total stock",
        "overall stock",
        "total quantity",
        "how much inventory",
        "how many items are in stock",
        "available stock",
        "remaining stock",
        "how much stock is available",
        "how many units are in stock",
    ]):
        return {"intent": "TOTAL_STOCK", "product_name": None}

    # Low or out-of-stock products
    if any(phrase in question for phrase in [
        "low stock",
        "running low",
        "almost out of stock",
        "out of stock",
        "which products are low",
        "products running low",
        "stock is low",
    ]):
        return {"intent": "LOW_STOCK", "product_name": None}

    # Order count
    if any(phrase in question for phrase in [
        "how many orders",
        "order count",
        "total orders",
        "number of orders",
        "count orders",
    ]):
        return {"intent": "ORDER_COUNT", "product_name": None}

    # Product list
    if any(phrase in question for phrase in [
        "show me all products",
        "list products",
        "show all products",
        "product list",
        "all products",
        "list all products",
    ]):
        return {"intent": "PRODUCT_LIST", "product_name": None}

    # Recent stock history
    if any(phrase in question for phrase in [
        "recent stock movements",
        "latest stock movements",
        "stock history",
        "stock movement history",
        "recent stock history",
    ]):
        return {
            "intent": "RECENT_STOCK_MOVEMENTS",
            "product_name": None
        }

    # Ask the LLM to classify other questions
    try:
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
You classify questions for a Storage Management System.

Choose exactly one intent:
PRODUCT_COUNT
PRODUCT_LIST
PRODUCT_STOCK
TOTAL_STOCK
LOW_STOCK
ORDER_COUNT
RECENT_STOCK_MOVEMENTS
UNKNOWN

PRODUCT_STOCK means asking about the quantity of a
specific named product. Extract its product name.

TOTAL_STOCK means asking about total stock across all products.

Return ONLY valid JSON in this format:
{"intent": "PRODUCT_STOCK", "product_name": "Keyboard"}

If no product name is needed, use null.
If the question is unrelated or unclear, use UNKNOWN.
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        if result.startswith("```"):
            result = result.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(result)

        allowed_intents = {
            "PRODUCT_COUNT",
            "PRODUCT_LIST",
            "PRODUCT_STOCK",
            "TOTAL_STOCK",
            "LOW_STOCK",
            "ORDER_COUNT",
            "RECENT_STOCK_MOVEMENTS",
            "UNKNOWN",
        }

        if parsed.get("intent") not in allowed_intents:
            raise ValueError("Invalid intent")

        return {
            "intent": parsed["intent"],
            "product_name": parsed.get("product_name")
        }

    except Exception:
        return {"intent": "UNKNOWN", "product_name": None}


# =========================================================
# ANSWER GENERATION
# =========================================================

def generate_answer(question, intent_data, database_data):
    # Return clear database-based answers without relying on
    # the LLM to calculate or interpret inventory numbers.

    intent = intent_data.get("intent")

    if intent == "TOTAL_STOCK":
        return f"The total available stock is {database_data['total_stock']} units."

    if intent == "PRODUCT_COUNT":
        return f"You have {database_data['product_count']} products."

    if intent == "ORDER_COUNT":
        return f"You have {database_data['order_count']} orders."

    if intent == "PRODUCT_LIST":
        products = database_data.get("products", [])

        if not products:
            return "There are no products in your inventory."

        names = ", ".join(product["name"] for product in products)
        return f"Your products are: {names}."

    if intent == "PRODUCT_STOCK":
        if not database_data.get("found"):
            return database_data.get("message", "Product not found.")

        products = database_data.get("products", [])
        return "\n".join(
            f"{product['name']}: {product['stock']} units in stock."
            for product in products
        )

    if intent == "LOW_STOCK":
        products = database_data.get("low_stock_products", [])

        if not products:
            return "No low-stock products were found."

        return "Low-stock products:\n" + "\n".join(
            f"{product['name']}: {product['stock']} units"
            for product in products
        )

    if intent == "RECENT_STOCK_MOVEMENTS":
        movements = database_data.get("recent_stock_movements", [])

        if not movements:
            return "No recent stock movements were found."

        return "\n".join(
            f"{item['product']}: {item['type']} "
            f"{item['quantity']} units — {item['reason']}"
            for item in movements
        )

    return "Sorry, I couldn't find an answer to that question."


# =========================================================
# MAIN CHATBOT FUNCTION
# =========================================================

def process_question(question):
    intent_data = detect_intent(question)

    intent = intent_data.get("intent")
    product_name = intent_data.get("product_name")

    if intent == "PRODUCT_COUNT":
        database_data = {
            "product_count": get_product_count()
        }

    elif intent == "TOTAL_STOCK":
        database_data = {
            "total_stock": get_total_stock()
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
    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Say hello in one short sentence."
            }
        ]
    )

    return response.choices[0].message.content.strip()
