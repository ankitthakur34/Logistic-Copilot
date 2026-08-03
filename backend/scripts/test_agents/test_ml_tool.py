from app import create_app

from app.tools.ml_tool import MLTool


def main():

    app = create_app()

    with app.app_context():

        tool = MLTool()

        shipment_no = "SHP0001"

        print("=" * 60)
        print("Testing ML Tool")
        print("=" * 60)

        result = tool.execute(shipment_no=shipment_no)

        print(result)

        print("=" * 60)


if __name__ == "__main__":
    main()