"""
setup_stripe.py — Run once to create Stripe products and prices.
Usage: python scripts/setup_stripe.py

Set STRIPE_SECRET_KEY env var before running.
Outputs price IDs to paste into settings_prod.py.
"""
import os
import sys

def main():
    try:
        import stripe
    except ImportError:
        print("Run: pip install stripe")
        sys.exit(1)

    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        print("Set STRIPE_SECRET_KEY env var first")
        sys.exit(1)

    products = [
        {
            "name": "RFP Matrix — Starter",
            "description": "3 RFPs/month, AI response generation, DOCX export",
            "prices": [{"amount": 9900, "interval": "month", "nickname": "starter"}],
        },
        {
            "name": "RFP Matrix — Growth",
            "description": "25 RFPs/month, compliance scanning, Salesforce integration",
            "prices": [{"amount": 29900, "interval": "month", "nickname": "growth"}],
        },
        {
            "name": "RFP Matrix — Enterprise",
            "description": "Unlimited RFPs, custom AI models, dedicated support",
            "prices": [{"amount": 99900, "interval": "month", "nickname": "enterprise"}],
        },
        {
            "name": "Fleet Optimizer — Small Fleet",
            "description": "Up to 25 vehicles, predictive maintenance, work orders",
            "prices": [{"amount": 14900, "interval": "month", "nickname": "starter"}],
        },
        {
            "name": "Fleet Optimizer — Mid Fleet",
            "description": "Up to 100 vehicles, telematics integration, inventory",
            "prices": [{"amount": 79900, "interval": "month", "nickname": "growth"}],
        },
        {
            "name": "Fleet Optimizer — Enterprise",
            "description": "Unlimited vehicles, Samsara/Geotab integration, API",
            "prices": [{"amount": 249900, "interval": "month", "nickname": "enterprise"}],
        },
        {
            "name": "Construction Liaison — Contractor",
            "description": "5 projects, drawing revision detection, trade notifications",
            "prices": [{"amount": 19900, "interval": "month", "nickname": "starter"}],
        },
        {
            "name": "Construction Liaison — Regional Builder",
            "description": "25 projects, AI trade impact analysis, procurement automation",
            "prices": [{"amount": 79900, "interval": "month", "nickname": "growth"}],
        },
        {
            "name": "Construction Liaison — Enterprise GC",
            "description": "Unlimited projects, Procore/Autodesk integration, custom workflows",
            "prices": [{"amount": 249900, "interval": "month", "nickname": "enterprise"}],
        },
    ]

    print("\n=== Creating Stripe Products & Prices ===\n")
    price_map = {}

    for product_data in products:
        product = stripe.Product.create(
            name=product_data["name"],
            description=product_data["description"],
        )
        print(f"✓ Product: {product.name} ({product.id})")

        for price_data in product_data["prices"]:
            price = stripe.Price.create(
                product=product.id,
                unit_amount=price_data["amount"],
                currency="usd",
                recurring={"interval": price_data["interval"]},
                nickname=price_data["nickname"],
            )
            key = f"{product_data['name']} [{price_data['nickname']}]"
            price_map[key] = price.id
            print(f"  ├── Price: ${price_data['amount']/100:.0f}/mo → {price.id}")

    print("\n=== Price IDs (paste into settings_prod.py) ===\n")
    print("STRIPE_PRICE_IDS = {")
    for name, price_id in price_map.items():
        print(f'    "{name}": "{price_id}",')
    print("}")
    print()


if __name__ == "__main__":
    main()
