from app.rag.evaluation.metrics.default_metrics import (

    build_metrics,

)

metrics = build_metrics()

for metric in metrics:

    print(metric)