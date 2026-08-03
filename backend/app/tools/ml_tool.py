from app.tools.base_tool import BaseTool
from app.tools.tool_result import ToolResult

from app.ml.facade.ml_prediction_facade import (
    MLPredictionFacade,
)
from app.ml.prediction_formatter import PredictionFormatter


class MLTool(BaseTool):

    @property
    def name(self) -> str:
        return "ml"

    @property
    def description(self) -> str:
        return """
Predict whether a shipment will be delayed.

Use for:
- Will shipment SHP0001 be delayed?
- Predict shipment delay
- Delay probability
- Delay risk
- Shipment prediction
"""

    def execute(
    self,
    **kwargs,
) -> ToolResult:

        shipment_no = kwargs.get("shipment_no")

        result = MLPredictionFacade.predict(
        shipment_no
    )

        if result["success"]:

            answer = PredictionFormatter.format(result)



            return ToolResult(

            tool_name=self.name,

            success=True,

            answer=answer,

            metadata={

                "shipment_no": shipment_no,

                "confidence": result["confidence"],

                "delay_probability": result["delay_probability"],

                "on_time_probability": result["on_time_probability"],

                "risk_factors": result["risk_factors"],

            },

            data=result,

        )
        return ToolResult(

        tool_name=self.name,

        success=False,

        answer="",

        error=result.get("message", "Prediction failed."),

    )