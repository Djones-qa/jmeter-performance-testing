# JMeter Performance Testing

![CI](https://github.com/Djones-qa/jmeter-performance-testing/actions/workflows/jmeter-tests.yml/badge.svg)

Enterprise performance testing framework using Apache JMeter 5.6.3. Covers smoke, load, stress, spike, and endurance testing scenarios against REST APIs with automated results analysis using Python and Pandas.

## Why JMeter
JMeter is the most widely used enterprise performance testing tool — required by banks, healthcare, and government contracts. Complements modern tools like K6 with GUI-based test plan creation and enterprise reporting.

## Tech Stack
- Apache JMeter 5.6.3
- Java 17
- Python — results analysis and metrics calculation
- Pandas — JTL results parsing
- Pytest — test validation
- GitHub Actions CI — runs JMeter and Python tests

## Test Plans

### Smoke Test
- 1 virtual user
- 1 iteration
- Validates baseline functionality
- GET, POST requests to httpbin.org
- Response code assertions

### Load Test
- 50 concurrent virtual users
- 30 second ramp up
- 5 iterations per user
- Normal expected traffic simulation

## Metrics Calculated
- Total requests and error rate
- Average, min, max response time
- P90 and P95 response time percentiles
- Throughput in requests per second
- SLA validation — response under 2000ms
- Error rate threshold — under 5%

## Project Structure
`
jmeter-performance-testing/
├── test-plans/
│   ├── smoke-test.jmx     # 1 user baseline test
│   └── load-test.jmx      # 50 concurrent users
├── scripts/
│   └── results_analyzer.py # JTL results parser and metrics
├── tests/
│   ├── test_test_plans.py      # Test plan structure validation
│   └── test_results_analysis.py # Metrics calculation tests
├── results/               # JMeter output files
├── conftest.py
├── pytest.ini
├── requirements.txt
└── .github/workflows/
    └── jmeter-tests.yml
`

## Run Tests
`ash
# Run Python tests
pip install -r requirements.txt
python -m pytest tests/ -v

# Run JMeter smoke test
jmeter -n -t test-plans/smoke-test.jmx -l results/smoke.jtl

# Run JMeter load test
jmeter -n -t test-plans/load-test.jmx -l results/load.jtl
`

## Author
Darrius Jones - github.com/Djones-qa