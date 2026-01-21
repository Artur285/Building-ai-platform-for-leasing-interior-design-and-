#!/usr/bin/env python
"""Test script for the AI Building Materials Leasing Platform."""
import requests
import json
import time

def test_api():
    """Test the API endpoints."""
    base_url = 'http://localhost:5000/api'
    
    print("Testing AI Building Materials Leasing Platform API...")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f'{base_url}/health', timeout=5)
        print(f'   Status: {response.status_code}')
        print(f'   Response: {response.json()}')
        print('   ✅ Health check passed')
    except Exception as e:
        print(f'   ❌ Health check failed: {e}')
        return False
    
    # Test materials endpoint
    print("\n2. Testing materials endpoint...")
    try:
        response = requests.get(f'{base_url}/materials', timeout=5)
        materials = response.json()
        print(f'   Total materials: {len(materials)}')
        if materials:
            print(f'   Sample material: {materials[0]["name"]}')
            print(f'   Category: {materials[0]["category"]}')
            print(f'   Price: ${materials[0]["price_per_day"]}/{materials[0]["unit"]}/day')
        print('   ✅ Materials endpoint passed')
    except Exception as e:
        print(f'   ❌ Materials endpoint failed: {e}')
        return False
    
    # Test recommendation endpoint
    print("\n3. Testing AI recommendation endpoint...")
    try:
        rec_data = {
            'project_description': 'Building a residential house with concrete foundation',
            'project_type': 'Residential Construction',
            'top_n': 3
        }
        response = requests.post(f'{base_url}/recommendations/project', 
                                json=rec_data, timeout=5)
        recs = response.json()
        print(f'   Recommendations found: {len(recs)}')
        if recs:
            print(f'   Top recommendation: {recs[0]["material"]["name"]}')
            print(f'   Relevance score: {recs[0]["relevance_score"]:.3f}')
            print(f'   Reason: {recs[0]["recommendation_reason"]}')
        print('   ✅ Recommendation endpoint passed')
    except Exception as e:
        print(f'   ❌ Recommendation endpoint failed: {e}')
        return False
    
    # Test pricing optimization
    print("\n4. Testing pricing optimization endpoint...")
    try:
        pricing_data = {
            'material_id': materials[0]['id'] if materials else 1,
            'lease_duration_days': 30,
            'quantity': 50
        }
        response = requests.post(f'{base_url}/pricing/optimize',
                                json=pricing_data, timeout=5)
        pricing = response.json()
        print(f'   Material: {pricing["material_name"]}')
        print(f'   Base price: ${pricing["base_price_per_day"]}/day')
        print(f'   Duration discount: {pricing["duration_discount_percent"]}%')
        print(f'   Quantity discount: {pricing["quantity_discount_percent"]}%')
        print(f'   Total discount: {pricing["total_discount_percent"]}%')
        print(f'   Total cost: ${pricing["total_cost"]}')
        if pricing['savings'] > 0:
            print(f'   Savings: ${pricing["savings"]}')
        print('   ✅ Pricing optimization passed')
    except Exception as e:
        print(f'   ❌ Pricing optimization failed: {e}')
        return False
    
    # Test complementary recommendations
    print("\n5. Testing complementary recommendations...")
    try:
        comp_data = {
            'material_ids': [materials[0]['id'], materials[1]['id']],
            'top_n': 3
        }
        response = requests.post(f'{base_url}/recommendations/complementary',
                                json=comp_data, timeout=5)
        comp_recs = response.json()
        print(f'   Complementary items found: {len(comp_recs)}')
        if comp_recs:
            print(f'   Top suggestion: {comp_recs[0]["material"]["name"]}')
        print('   ✅ Complementary recommendations passed')
    except Exception as e:
        print(f'   ❌ Complementary recommendations failed: {e}')
        return False
    
    # Test categories endpoint
    print("\n6. Testing categories endpoint...")
    try:
        response = requests.get(f'{base_url}/categories', timeout=5)
        categories = response.json()
        print(f'   Categories available: {len(categories)}')
        print(f'   Sample categories: {", ".join(categories[:5])}')
        print('   ✅ Categories endpoint passed')
    except Exception as e:
        print(f'   ❌ Categories endpoint failed: {e}')
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    # Give server time to start
    time.sleep(2)
    success = test_api()
    exit(0 if success else 1)
