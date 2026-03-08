"""
Observability configuration for Pyroscope and Tempo
"""
import os
import sys


# Pyroscope continuous profiling
PYROSCOPE_ENABLED = os.getenv("PYROSCOPE_ENABLED", "false").lower() == "true"
PYROSCOPE_SERVER_ADDRESS = os.getenv("PYROSCOPE_SERVER_ADDRESS", "http://pyroscope.monitoring.svc.cluster.local:4040")
PYROSCOPE_APPLICATION_NAME = os.getenv("PYROSCOPE_APPLICATION_NAME", "book-club-backend")

print(f"[OBSERVABILITY] Pyroscope enabled: {PYROSCOPE_ENABLED}", file=sys.stderr)

if PYROSCOPE_ENABLED:
    try:
        import pyroscope

        pyroscope.configure(
            application_name=PYROSCOPE_APPLICATION_NAME,
            server_address=PYROSCOPE_SERVER_ADDRESS,
            tags={
                "environment": os.getenv("ENVIRONMENT", "production"),
                "version": os.getenv("APP_VERSION", "unknown"),
            },
        )
        print(f"[OBSERVABILITY] Pyroscope configured: {PYROSCOPE_SERVER_ADDRESS}", file=sys.stderr)
    except ImportError as e:
        print(f"[OBSERVABILITY] Pyroscope not available: {e}", file=sys.stderr)
    except Exception as e:
        print(f"[OBSERVABILITY] Pyroscope error: {e}", file=sys.stderr)


# tracing
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
OTEL_ENABLED = bool(OTEL_ENDPOINT)

print(f"[OBSERVABILITY] OpenTelemetry enabled: {OTEL_ENABLED}, endpoint: {OTEL_ENDPOINT}", file=sys.stderr)

if OTEL_ENABLED:
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.django import DjangoInstrumentor
        from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
        from opentelemetry.sdk.resources import Resource

        # resource with service information
        resource = Resource.create({
            "service.name": os.getenv("OTEL_SERVICE_NAME", "book-club-backend"),
            "service.version": os.getenv("APP_VERSION", "unknown"),
            "deployment.environment": os.getenv("ENVIRONMENT", "production"),
        })

        # tracer provider
        trace.set_tracer_provider(TracerProvider(resource=resource))

        # OTLP exporter
        otlp_exporter = OTLPSpanExporter(
            endpoint=OTEL_ENDPOINT,
            insecure=True,  # Use TLS in production
        )

        # span processor
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(otlp_exporter)
        )
        
        DjangoInstrumentor().instrument()
        PsycopgInstrumentor().instrument()

        print(f"[OBSERVABILITY] OpenTelemetry configured successfully", file=sys.stderr)

    except ImportError as e:
        print(f"[OBSERVABILITY] OpenTelemetry not available: {e}", file=sys.stderr)
    except Exception as e:
        print(f"[OBSERVABILITY] OpenTelemetry error: {e}", file=sys.stderr)
