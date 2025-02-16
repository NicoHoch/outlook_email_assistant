import logging
import azure.functions as func
from assistant import main

app = func.FunctionApp()


@app.timer_trigger(
    schedule="*/10 * * * * *",  # This schedule will run every 10 seconds
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def check_emails(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function executed.")

    main()
