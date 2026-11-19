from prometheus_client import Counter, Histogram


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

PREDICTION_VALUE = Histogram(
    "house_price_prediction",
    "Distribution of predicted house prices",
    buckets=(
        50000,
        100000,
        150000,
        200000,
        300000,
        500000,
        750000,
        1000000,
    ),
)

LOT_AREA = Histogram(
    "house_input_lot_area",
    "Observed LotArea values",
    buckets=(
        2000,
        5000,
        7500,
        10000,
        15000,
        20000,
        30000,
        50000,
        100000,
    ),
)

OVERALL_QUAL = Histogram(
    "house_input_overall_qual",
    "Observed OverallQual values",
    buckets=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
)

GR_LIV_AREA = Histogram(
    "house_input_gr_liv_area",
    "Observed GrLivArea values",
    buckets=(
        500,
        750,
        1000,
        1500,
        2000,
        2500,
        3000,
        4000,
        5000,
    ),
)
