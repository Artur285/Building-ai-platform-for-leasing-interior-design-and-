"""
Example usage of the AI Building Materials Leasing Platform API.

This script demonstrates how to interact with the platform programmatically.
Run the server first: python main.py
"""
import requests
import json

# Base URL for the API
BASE_URL = 'http://localhost:5000/api'


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_1_browse_materials():
    """Example 1: Browse available materials."""
    print_section("Example 1: Browse Materials")
    
    response = requests.get(f"{BASE_URL}/materials")
    materials = response.json()
    
    print(f"Total materials available: {len(materials)}\n")
    
    # Show first 3 materials
    for mat in materials[:3]:
        print(f"📦 {mat['name']}")
        print(f"   Category: {mat['category']}")
        print(f"   Price: ${mat['price_per_day']}/{mat['unit']}/day")
        print(f"   Available: {mat['quantity_available']} {mat['unit']}")
        print()


def example_2_get_recommendations():
    """Example 2: Get AI-powered recommendations for a project."""
    print_section("Example 2: AI Recommendations")
    
    project_data = {
        "project_description": "Building a 10-story residential apartment complex with "
                             "underground parking and modern amenities. Need materials "
                             "for concrete work, scaffolding, and safety equipment.",
        "project_type": "Residential Construction",
        "top_n": 5
    }
    
    print(f"Project: {project_data['project_description'][:80]}...\n")
    
    response = requests.post(
        f"{BASE_URL}/recommendations/project",
        json=project_data
    )
    recommendations = response.json()
    
    print("🤖 AI Recommendations:\n")
    for i, rec in enumerate(recommendations, 1):
        mat = rec['material']
        score = rec['relevance_score']
        print(f"{i}. {mat['name']} (Match: {score*100:.0f}%)")
        print(f"   {mat['category']} - ${mat['price_per_day']}/{mat['unit']}/day")
        print(f"   {rec['recommendation_reason']}")
        print()


def example_3_optimize_pricing():
    """Example 3: Calculate optimized pricing with discounts."""
    print_section("Example 3: Pricing Optimization")
    
    # Get materials first to find an ID
    response = requests.get(f"{BASE_URL}/materials")
    materials = response.json()
    
    # Use first material for example
    material = materials[0]
    
    pricing_data = {
        "material_id": material['id'],
        "lease_duration_days": 90,  # 3 months
        "quantity": 100
    }
    
    print(f"Material: {material['name']}")
    print(f"Quantity: {pricing_data['quantity']}")
    print(f"Duration: {pricing_data['lease_duration_days']} days\n")
    
    response = requests.post(
        f"{BASE_URL}/pricing/optimize",
        json=pricing_data
    )
    pricing = response.json()
    
    print("💰 Pricing Calculation:")
    print(f"   Base Price: ${pricing['base_price_per_day']}/day")
    print(f"   Duration Discount: {pricing['duration_discount_percent']}%")
    print(f"   Quantity Discount: {pricing['quantity_discount_percent']}%")
    print(f"   Total Discount: {pricing['total_discount_percent']}%")
    print(f"   Optimized Price: ${pricing['discounted_price_per_day']}/day")
    print(f"\n   TOTAL COST: ${pricing['total_cost']}")
    if pricing['savings'] > 0:
        print(f"   YOU SAVE: ${pricing['savings']} 🎉")


def example_4_create_user_and_lease():
    """Example 4: Create a user and a lease."""
    print_section("Example 4: Create User and Lease")
    
    # Create user
    user_data = {
        "username": "john_builder",
        "email": "john@construction.com",
        "company_name": "Builder's Paradise Inc.",
        "phone": "+1-555-9876"
    }
    
    print(f"Creating user: {user_data['username']}")
    
    try:
        response = requests.post(f"{BASE_URL}/users", json=user_data)
        user = response.json()
        user_id = user['id']
        print(f"✓ User created with ID: {user_id}\n")
    except:
        # User might already exist
        print("(User already exists, using existing user)\n")
        user_id = 1
    
    # Get materials for lease
    response = requests.get(f"{BASE_URL}/materials")
    materials = response.json()
    
    # Create a lease
    lease_data = {
        "user_id": user_id,
        "project_name": "Downtown Office Complex",
        "project_description": "5-story commercial office building with retail on ground floor",
        "start_date": "2024-02-01",
        "end_date": "2024-05-01",
        "delivery_address": "123 Main Street, Downtown",
        "items": [
            {"material_id": materials[0]['id'], "quantity": 100},
            {"material_id": materials[1]['id'], "quantity": 50}
        ]
    }
    
    print(f"Creating lease for project: {lease_data['project_name']}")
    
    response = requests.post(f"{BASE_URL}/leases", json=lease_data)
    
    if response.status_code == 201:
        lease = response.json()
        print(f"✓ Lease created with ID: {lease['id']}")
        print(f"   Total Cost: ${lease['total_cost']}")
        print(f"   Status: {lease['status']}")
        print(f"   Items: {len(lease['items'])} materials")
    else:
        print(f"Note: {response.json().get('error', 'Lease creation demo complete')}")


def example_5_complementary_recommendations():
    """Example 5: Get complementary material recommendations."""
    print_section("Example 5: Complementary Recommendations")
    
    # Get materials
    response = requests.get(f"{BASE_URL}/materials")
    materials = response.json()
    
    # Select some materials
    selected_ids = [mat['id'] for mat in materials[:2]]
    selected_names = [mat['name'] for mat in materials[:2]]
    
    print("Selected materials:")
    for name in selected_names:
        print(f"  • {name}")
    
    print("\n🤖 AI suggests complementary materials:\n")
    
    response = requests.post(
        f"{BASE_URL}/recommendations/complementary",
        json={"material_ids": selected_ids, "top_n": 5}
    )
    recommendations = response.json()
    
    for i, rec in enumerate(recommendations, 1):
        mat = rec['material']
        print(f"{i}. {mat['name']}")
        print(f"   {mat['category']} - ${mat['price_per_day']}/{mat['unit']}/day")
        print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("  AI Building Materials Leasing Platform - API Examples")
    print("=" * 60)
    print("\nMake sure the server is running on http://localhost:5000\n")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            return
    except:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python main.py")
        return
    
    print("✓ Server is running\n")
    
    # Run examples
    example_1_browse_materials()
    example_2_get_recommendations()
    example_3_optimize_pricing()
    example_5_complementary_recommendations()
    example_4_create_user_and_lease()
    
    print("\n" + "=" * 60)
    print("  All examples completed successfully!")
    print("=" * 60)
    print("\nVisit http://localhost:5000 for the web interface")
    print()


if __name__ == '__main__':
    main()
