/**
 * OpenTelemetry tracing configuration
 */
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web'
import { registerInstrumentations } from '@opentelemetry/instrumentation'
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch'
import { XMLHttpRequestInstrumentation } from '@opentelemetry/instrumentation-xml-http-request'
import { DocumentLoadInstrumentation } from '@opentelemetry/instrumentation-document-load'
import { UserInteractionInstrumentation } from '@opentelemetry/instrumentation-user-interaction'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-web'
import { Resource } from '@opentelemetry/resources'
import {
  SEMRESATTRS_SERVICE_NAME,
  SEMRESATTRS_SERVICE_VERSION,
} from '@opentelemetry/semantic-conventions'

// Support both build-time and runtime configuration
const OTEL_ENDPOINT = (window as any).__ENV__?.VITE_OTEL_ENDPOINT || import.meta.env.VITE_OTEL_ENDPOINT
const APP_VERSION = (window as any).__ENV__?.VITE_APP_VERSION || import.meta.env.VITE_APP_VERSION || '1.0.0'

export function initTracing() {
  if (!OTEL_ENDPOINT) {
    console.log('[OTEL] Tracing disabled: VITE_OTEL_ENDPOINT not set')
    return
  }

  console.log('[OTEL] Initializing tracing, endpoint:', OTEL_ENDPOINT)

  try {
    const provider = new WebTracerProvider({
      resource: new Resource({
        [SEMRESATTRS_SERVICE_NAME]: 'book-club-frontend',
        [SEMRESATTRS_SERVICE_VERSION]: APP_VERSION,
      }),
    })

    const exporter = new OTLPTraceExporter({
      url: `${OTEL_ENDPOINT}/v1/traces`,
    })

    provider.addSpanProcessor(new BatchSpanProcessor(exporter))
    provider.register()

    registerInstrumentations({
      instrumentations: [
        new FetchInstrumentation({
          propagateTraceHeaderCorsUrls: [/.+/], // Propagate trace context to all origins
          clearTimingResources: true,
          applyCustomAttributesOnSpan: (span, request, result) => {
            // Add custom attributes to fetch spans
            if (request instanceof Request) {
              span.setAttribute('http.url', request.url)
              span.setAttribute('http.method', request.method)
            }
            if (result instanceof Response) {
              span.setAttribute('http.status_code', result.status)
            }
          },
        }),
        new XMLHttpRequestInstrumentation({
          propagateTraceHeaderCorsUrls: [/.+/],
          applyCustomAttributesOnSpan: (span, xhr) => {
            // Add custom attributes to XHR spans (axios uses XHR)
            span.setAttribute('http.url', xhr.responseURL || 'unknown')
            span.setAttribute('http.status_code', xhr.status)
          },
        }),
        new DocumentLoadInstrumentation(),
        new UserInteractionInstrumentation({
          eventNames: ['click', 'submit'],
        }),
      ],
    })

    console.log('[OTEL] Tracing initialized successfully')
  } catch (error) {
    console.error('[OTEL] Failed to initialize tracing:', error)
  }
}
