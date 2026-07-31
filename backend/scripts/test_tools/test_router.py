

from app import create_app

from app.bootstrap.service_registry import (
    ServiceRegistry,
)

###############################################################################
# Flask
###############################################################################

app = create_app()

###############################################################################
# Run
###############################################################################

with app.app_context():

    registry = ServiceRegistry()

    router = registry.router_agent

    questions = [

        "Show all shipments.",

        "Who owns tasks for SHP0001?",

        "Explain customs clearance SOP.",

        "Why was SHP0001 delayed?",

    ]

    for question in questions:

        print()
        print("=" * 100)
        print(question)
        print("=" * 100)
    
        execution = router.run(question)
    
        print()
    
        print("=" * 80)
        print("FINAL ANSWER")
        print("=" * 80)
    
        print(execution.answer)
    
        print()
    
        print("=" * 80)
        print("TOOLS")
        print("=" * 80)
    
        for result in execution.tool_results:
    
            print()
    
            print(result.tool_name.upper())
    
            print("-" * 40)
    
            print("Success :", result.success)
    
            print("Answer  :", result.answer)
    
            print("Metadata:", result.metadata)
    
            if result.error:
    
                print("Error   :", result.error)