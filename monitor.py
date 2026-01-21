#!/usr/bin/env python3
"""
Performance monitoring and diagnostics utility.
"""
import time
import requests
import statistics
from datetime import datetime
import argparse


def test_endpoint(url, method='GET', data=None, iterations=10):
    """Test an endpoint and collect performance metrics."""
    response_times = []
    errors = 0
    
    print(f"\n🔍 Testing: {method} {url}")
    print(f"   Iterations: {iterations}")
    
    for i in range(iterations):
        try:
            start = time.time()
            
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=10)
            
            elapsed = (time.time() - start) * 1000  # Convert to ms
            response_times.append(elapsed)
            
            if response.status_code >= 400:
                errors += 1
                print(f"   [{i+1}] ❌ Status: {response.status_code} - {elapsed:.2f}ms")
            else:
                print(f"   [{i+1}] ✅ Status: {response.status_code} - {elapsed:.2f}ms")
        
        except Exception as e:
            errors += 1
            print(f"   [{i+1}] ❌ Error: {str(e)}")
    
    # Calculate statistics
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        median_time = statistics.median(response_times)
        
        print(f"\n📊 Performance Statistics:")
        print(f"   Average:  {avg_time:.2f}ms")
        print(f"   Median:   {median_time:.2f}ms")
        print(f"   Min:      {min_time:.2f}ms")
        print(f"   Max:      {max_time:.2f}ms")
        print(f"   Errors:   {errors}/{iterations}")
        print(f"   Success:  {((iterations-errors)/iterations)*100:.1f}%")
    
    return response_times


def load_test(base_url, duration=60, requests_per_second=10):
    """Perform a load test on the application."""
    print(f"\n🚀 Load Test Configuration:")
    print(f"   Base URL: {base_url}")
    print(f"   Duration: {duration}s")
    print(f"   Target RPS: {requests_per_second}")
    print(f"   Total Requests: {duration * requests_per_second}")
    
    input("\nPress Enter to start load test...")
    
    start_time = time.time()
    total_requests = 0
    successful_requests = 0
    failed_requests = 0
    response_times = []
    
    delay = 1.0 / requests_per_second
    
    print("\n⏱️  Load test running...")
    
    while time.time() - start_time < duration:
        try:
            req_start = time.time()
            response = requests.get(f"{base_url}/api/health", timeout=5)
            req_time = (time.time() - req_start) * 1000
            
            response_times.append(req_time)
            total_requests += 1
            
            if response.status_code == 200:
                successful_requests += 1
            else:
                failed_requests += 1
            
            # Progress indicator
            if total_requests % 50 == 0:
                elapsed = time.time() - start_time
                current_rps = total_requests / elapsed
                print(f"   Progress: {total_requests} requests, {current_rps:.1f} RPS")
            
            # Maintain target rate
            sleep_time = delay - (time.time() - req_start)
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        except Exception as e:
            failed_requests += 1
            total_requests += 1
    
    # Results
    elapsed = time.time() - start_time
    actual_rps = total_requests / elapsed
    
    print(f"\n✅ Load Test Complete!")
    print(f"\n📊 Results:")
    print(f"   Total Requests:      {total_requests}")
    print(f"   Successful:          {successful_requests}")
    print(f"   Failed:              {failed_requests}")
    print(f"   Duration:            {elapsed:.2f}s")
    print(f"   Actual RPS:          {actual_rps:.2f}")
    
    if response_times:
        print(f"\n⏱️  Response Times:")
        print(f"   Average:  {statistics.mean(response_times):.2f}ms")
        print(f"   Median:   {statistics.median(response_times):.2f}ms")
        print(f"   Min:      {min(response_times):.2f}ms")
        print(f"   Max:      {max(response_times):.2f}ms")
        print(f"   95th %ile: {statistics.quantiles(response_times, n=20)[18]:.2f}ms")


def health_check(base_url):
    """Perform comprehensive health check."""
    print(f"\n🏥 Health Check: {base_url}")
    print("=" * 60)
    
    endpoints = [
        ('Health', '/api/health', 'GET'),
        ('Liveness', '/api/health/live', 'GET'),
        ('Readiness', '/api/health/ready', 'GET'),
        ('Materials', '/api/materials', 'GET'),
        ('Categories', '/api/categories', 'GET'),
        ('Metrics', '/api/metrics', 'GET'),
    ]
    
    for name, endpoint, method in endpoints:
        try:
            start = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            elapsed = (time.time() - start) * 1000
            
            if response.status_code == 200:
                print(f"✅ {name:<15} - OK ({elapsed:.0f}ms)")
            else:
                print(f"❌ {name:<15} - Status {response.status_code}")
        
        except Exception as e:
            print(f"❌ {name:<15} - Error: {str(e)}")
    
    print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Performance monitoring utility for AI Leasing Platform'
    )
    
    parser.add_argument('--url', default='http://localhost:5000',
                       help='Base URL of the application')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Health check command
    subparsers.add_parser('health', help='Perform health check')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test specific endpoint')
    test_parser.add_argument('endpoint', help='Endpoint to test')
    test_parser.add_argument('-n', '--iterations', type=int, default=10,
                            help='Number of iterations')
    test_parser.add_argument('-m', '--method', default='GET',
                            choices=['GET', 'POST'], help='HTTP method')
    
    # Load test command
    load_parser = subparsers.add_parser('load', help='Perform load test')
    load_parser.add_argument('-d', '--duration', type=int, default=60,
                            help='Duration in seconds')
    load_parser.add_argument('-r', '--rps', type=int, default=10,
                            help='Requests per second')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'health':
        health_check(args.url)
    elif args.command == 'test':
        endpoint = args.endpoint if args.endpoint.startswith('/') else f'/{args.endpoint}'
        test_endpoint(f"{args.url}{endpoint}", args.method, iterations=args.iterations)
    elif args.command == 'load':
        load_test(args.url, args.duration, args.rps)


if __name__ == '__main__':
    main()
