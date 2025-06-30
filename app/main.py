from fastapi import FastAPI, HTTPException, Request
import time, random
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.tracing import setup_tracer

tracer = setup_tracer()
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def root():
    return {"message": "Welcome to E-Shop"}

@app.get("/products/{product_id}")
async def get_product(product_id: int, request: Request):
    with tracer.start_as_current_span("get_product") as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.route", "/products/{product_id}")
        span.set_attribute("product.id", product_id)

        time.sleep(random.uniform(0.1, 0.3))

        if product_id > 100:
            span.set_attribute("http.status_code", 404)
            span.record_exception(HTTPException(status_code=404, detail="Product not found"))
            raise HTTPException(status_code=404, detail="Product not found")

        product_name = f"Product {product_id}"
        price = round(random.uniform(10, 100), 2)

        span.set_attribute("product.name", product_name)
        span.set_attribute("product.price", price)
        span.set_attribute("http.status_code", 200)

        return {"product_id": product_id, "name": product_name, "price": price}

@app.post("/checkout/")
async def checkout(request: Request):
    with tracer.start_as_current_span("checkout") as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.route", "/checkout/")

        with tracer.start_as_current_span("validate_cart") as validate_span:
            time.sleep(random.uniform(0.1, 0.2))
            validate_span.set_attribute("cart.valid", True)

        with tracer.start_as_current_span("process_payment") as payment_span:
            time.sleep(random.uniform(0.3, 0.5))
            payment_success = random.choice([True, True, True, False])
            payment_span.set_attribute("payment.success", payment_success)
            if not payment_success:
                payment_span.record_exception(Exception("Payment failed"))
                span.set_attribute("checkout.status", "failed")
                return {"status": "failed", "reason": "Payment failed"}

        order_id = random.randint(1000, 9999)
        span.set_attribute("order.id", order_id)
        span.set_attribute("checkout.status", "success")
        span.set_attribute("http.status_code", 200)

        time.sleep(0.1)
        return {"status": "success", "order_id": order_id}
