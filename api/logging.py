import json
import logging
import time
import uuid

from fastapi import FastAPI, Request

from api.metrics import REQUEST_COUNT, REQUEST_LATENCY


logger = logging.getLogger("house_price_api")
logging.basicConfig(level=logging.INFO)


def register_logging_middleware(app: FastAPI):

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            latency_ms = (time.perf_counter() - start_time) * 1000

            if request.url.path != "/metrics":
                REQUEST_COUNT.labels(
                    method=request.method,
                    path=request.url.path,
                    status_code=response.status_code,
                ).inc()

                REQUEST_LATENCY.labels(
                    method=request.method,
                    path=request.url.path,
                ).observe(latency_ms / 1000)

            log_data = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "latency_ms": round(latency_ms, 2),
            }

            logger.info(json.dumps(log_data))

            return response

        except Exception as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000

            if request.url.path != "/metrics":
                REQUEST_COUNT.labels(
                    method=request.method,
                    path=request.url.path,
                    status_code=500,
                ).inc()

                REQUEST_LATENCY.labels(
                    method=request.method,
                    path=request.url.path,
                ).observe(latency_ms / 1000)

            log_data = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": 500,
                "latency_ms": round(latency_ms, 2),
                "error": str(exc),
            }

            logger.exception(json.dumps(log_data))

            raise
