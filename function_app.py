import logging
import azure.functions as func
from assistant import main_email_handler, main_summarizer

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 */2 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def check_emails(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function executed.")

    main_email_handler()


@app.timer_trigger(
    schedule="0 6,18 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def send_summary(myTimer: func.TimerRequest) -> None:
    main_summarizer()
