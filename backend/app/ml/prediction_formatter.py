class PredictionFormatter:

    @staticmethod
    def format(result: dict) -> str:
        print("=" * 50)
        print("PREDICTION FORMATTER")
        print(result)

        shipment_no = result["shipment_no"]

        prediction = result["prediction"]

        confidence = result["confidence"] * 100

        delay_probability = result["delay_probability"] * 100

        if prediction.lower() == "delayed":

            return (
                f"Shipment **{shipment_no}** is likely to be **delayed**.\n\n"
                # f"• Confidence: **{confidence:.2f}%**\n"
                f"• Delay Probability: **{delay_probability:.2f}%**\n\n"
                f"The shipment shows operational characteristics commonly associated with delayed deliveries."
            )

        return (
            f"Shipment **{shipment_no}** is likely to arrive **on time**.\n\n"
            # f"• Confidence: **{confidence:.2f}%**\n"
            f"• On-Time Probability: **{confidence:.2f}%**\n\n"
            f"The shipment currently shows a low risk of delay based on the available operational data."
        )