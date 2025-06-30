import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

def setup_tracer(service_name: str = "ecommerce-shop"):
    agent_host = os.getenv("JAEGER_AGENT_HOST", "localhost")
    agent_port = int(os.getenv("JAEGER_AGENT_PORT", 6831))

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    jaeger_exporter = JaegerExporter(
        agent_host_name=agent_host,
        agent_port=agent_port,
    )
    span_processor = BatchSpanProcessor(jaeger_exporter)
    provider.add_span_processor(span_processor)

    tracer = trace.get_tracer(__name__)
    return tracer
